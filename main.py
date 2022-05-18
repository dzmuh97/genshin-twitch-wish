import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import random
import queue
import time
import gc
import cv2

from itertools import cycle
from dataclasses import dataclass

import threading
import asyncio
import pygame
import pickle

import json
import jsonschema

from data import DATABASE
from data import CONFIG_SCHEMA
from twitchio.ext import commands

_config = {}
try:
    _config = json.loads(open('config.json', 'r', encoding='utf-8').read())
except (json.JSONDecodeError, ValueError) as e:
    print('[MAIN] Ошибка при загрузке файла конфигурации:', e)
    sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

try:
    jsonschema.validate(_config, schema=CONFIG_SCHEMA)
except jsonschema.ValidationError as e:
    print('[MAIN] Ошибка при загрузке файла конфигурации:', e)
    sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

CONFIG = _config['CONFIG']
MESSAGES = _config['MESSAGES']
CHATBOT_MSG = _config['CHATBOT']
NOTIFY_MSG = _config['NOTIFY']

USERTEXT_COLOR = (255, 255, 255, 0)
USERTEXT_OUTLINE = (0, 0, 0, 0)

pygame.init()
pygame.display.set_caption(CONFIG['window_name'])

programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

SOUND = {
    'fall': pygame.mixer.Sound(os.path.join('sound', 'soundfall.mp3')),
    '3': pygame.mixer.Sound(os.path.join('sound', '3star.mp3')),
    '4': pygame.mixer.Sound(os.path.join('sound', '4star.mp3')),
    '5': pygame.mixer.Sound(os.path.join('sound', '5star.mp3'))
}

fps = pygame.time.Clock()
mdisplay = pygame.display.set_mode(size=(1280, 720), vsync=1)

wish_que = queue.Queue()
animations = []
users = {}

if CONFIG['play_sound']:
    pygame.mixer.init()

@dataclass
class GachaWish:
    cwish_star: str
    username: str
    ucolor: str
    cwish_wtype: str
    cwish_wmetatype: str
    cwish_wmetaelem: str
    cwish_cname: str
    cwish_wname: str

class Gacha:
    wish_5_garant = 1
    wish_4_garant = 1
    wish_count = 0

    def __init__(self, username, color):
        self.username = username
        self.ucolor = color
        self.wish_stamp = 0

    def __roll(self):
        self.wish_count += 1

        if (self.wish_5_garant > CONFIG['wish_fi_soft_a']) and (self.wish_5_garant < CONFIG['wish_fi_garant']):
            if random.choice(range(CONFIG['wish_fi_garant'] - self.wish_5_garant)) == 0:
                self.wish_5_garant = 1
                return '5', 'srnd'
        else:
            if random.choice(range(100)) < CONFIG['wish_fi_chance']:
                self.wish_5_garant = 1
                return '5', 'rnd'

        if self.wish_5_garant % CONFIG['wish_fi_garant'] == 0:
            self.wish_5_garant = 1
            return '5', 'garant'

        self.wish_5_garant += 1

        if self.wish_4_garant % CONFIG['wish_fo_garant'] == 0:
            self.wish_4_garant = 1
            return '4', 'garant'

        self.wish_4_garant += 1

        if random.choice(range(100)) < CONFIG['wish_fo_chance']:
            self.wish_4_garant = 1
            return '4', 'rnd'

        return '3', 'rnd'

    def generate_wish(self):
        star_types = {
            'srnd': 'мягкий гарант',
            'garant': 'гарант',
            'rnd': 'рандом',
        }

        star, star_type = self.__roll()
        if star == '3':
            wtype = 'weapon'
        else:
            wtype = random.choice(['weapon', 'char'])

        self.wish_stamp = int(time.time())
        data = random.choice(DATABASE[star][wtype])

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('[ГАЧА]', '[%s]' % current_time,
              'Результат для', self.username,
              '#%d' % self.wish_count,
              'w4#%d' % self.wish_4_garant,
              'w5#%d' % self.wish_5_garant,
              star, '* ->', data.get('cwish_wname'),
              '[%s]' % star_types[star_type])

        if CONFIG['history_file'][star]:
            write_history(self.username, self.wish_count, star, star_types[star_type], data.get('cwish_wname'))

        return GachaWish(star, self.username, self.ucolor, **data)

class Coordiantor:
    states_name = ['IDLE', 'INIT', 'DRAW', 'CLEAR']

    def __init__(self, que, animl):
        self.states = cycle(self.states_name)
        self.state = next(self.states)
        self.animl = animl
        self.cur_wish = None
        self.que = que
        self.objs = {}
        self.sound = []

    def _play_obj(self, objn):
        obj_data = self.objs[objn]
        obj = obj_data['obj']

        if isinstance(obj, list):
            if not obj_data['play']:
                obj_data['play'] = True
                for objl in obj:
                    self.animl.append(objl)
                    objl.play()
            return obj

        if not obj_data['play']:
            self.animl.append(obj)
            obj_data['play'] = True
            obj.play()

        return obj

    def update(self):
        state_func = getattr(self, 'state_%s' % self.state)

        isnext = state_func()
        if isnext:
            self.state = next(self.states)

    def state_IDLE(self):
        try:
            wish = self.que.get(block=False)
        except queue.Empty:
            return False

        self.cur_wish = wish
        self.que.task_done()
        return True

    def state_INIT(self):
        wstar = self.cur_wish.cwish_star
        wtype = self.cur_wish.cwish_wtype
        wback = self.cur_wish.cwish_wmetaelem if self.cur_wish.cwish_wmetatype == 'weapon' else None
        wmetatype = self.cur_wish.cwish_wmetatype
        wmetaelem = self.cur_wish.cwish_wmetaelem
        cname = self.cur_wish.cwish_cname
        wname = self.cur_wish.cwish_wname

        utext = random.choice(MESSAGES)
        wish_meta_type, wish_meta_name, wish_meta_star = merge_wish_meta((80, 450), WishMeta(wmetatype, wmetaelem), WishText(wname), int(wstar))
        self.objs.update(
            {
            'fall_anim': {'obj': FallAnimated(wstar), 'play': False},
            'user_perm_text': {'obj': PermaText(self.cur_wish.username), 'play': False},
            'back_anim_first': {'obj': BackAnimated('first', wstar), 'play': False},
            'back_anim_second': {'obj': BackAnimated('second', wstar), 'play': False},
            'back_static': {'obj': Background(CONFIG['end_delay'][wstar]), 'play': False},
            'user_nick': {'obj': UserText(self.cur_wish.username, (640, 300), self.cur_wish.ucolor),'play': False},
            'user_text': {'obj': UserText(utext, (640, 530)), 'play': False},
            'wish_color': {'obj': Wish(wtype, cname), 'play': False},
            'wish_black': {'obj': objfill(Wish(wtype, cname), pygame.Color(0, 0, 0)), 'play': False},
            'wish_back': {'obj': WishBack(wback), 'play': False},
            'wish_meta_type': {'obj': wish_meta_type, 'play': False},
            'wish_meta_name': {'obj': wish_meta_name, 'play': False},
            'wish_meta_star': {'obj': wish_meta_star, 'play': False},
            }
        )

        uback_p = CONFIG['user_background']['path']
        uback_t = CONFIG['user_background']['ftype']
        if not uback_p:
            return True

        self.objs.update(
            {
            'user_background': {'obj': UserBackground(uback_p) if uback_t == 'static' else UserBackgroundAnim(uback_p), 'play': False}
            }
        )

        return True

    def state_DRAW(self):
        userback = None
        if CONFIG['user_background']['path']:
            userback = self._play_obj('user_background')

        textnickobj = self._play_obj('user_nick')
        textuserobj = self._play_obj('user_text')
        if textnickobj.is_play and textuserobj.is_play:
            return False

        if CONFIG['user_background']['path']:
            userback.is_play = False

        if CONFIG['play_sound']:
            sound_fall = SOUND['fall']
            if not (sound_fall in self.sound):
                self.sound.append(sound_fall)
                sound_fall.play()

        userperma = self._play_obj('user_perm_text')
        fallobj = self._play_obj('fall_anim')
        if fallobj.is_play:
            return False

        back_tmpl = self._play_obj('back_static')

        if CONFIG['play_sound']:
            sound_star = SOUND[self.cur_wish.cwish_star]
            if not (sound_star in self.sound):
                self.sound.append(sound_star)
                sound_star.play()

        back_f = self._play_obj('back_anim_first')
        wish_black = self._play_obj('wish_black')
        if back_f.is_play:
            return False
        wish_black.is_play = False

        back_s = self._play_obj('back_anim_second')
        wish_back = self._play_obj('wish_back')
        wish_color = self._play_obj('wish_color')
        if back_s.is_play:
            return False

        wish_meta_type = self._play_obj('wish_meta_type')
        wish_meta_name = self._play_obj('wish_meta_name')
        wish_meta_star = self._play_obj('wish_meta_star')

        if back_tmpl.is_play:
            return False

        userperma.is_play = False
        wish_back.is_play = False
        wish_color.is_play = False
        wish_meta_type.is_play = False
        wish_meta_name.is_play = False
        for star in wish_meta_star:
            star.is_play = False

        return True

    def state_CLEAR(self):
        self.animl.clear()
        self.objs.clear()
        self.sound.clear()
        self.cur_wish = None
        gc.collect()
        return True

class Static(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lifetime = 0
        self.is_play = False
        self.image = None
        self.rect = None

    def play(self):
        self.is_play = True

    def hide(self):
        self.is_play = False

    def update(self, speed: float):
        if not self.is_play:
            return

        if self.lifetime < 0:
            return

        self.lifetime -= speed
        if self.lifetime <= 0:
            self.is_play = False

    def im_sub_load(self, path):
        if path is None:
            empty = pygame.Color(0,0,0,0)
            field = pygame.Surface((1, 1), flags=pygame.SRCALPHA)
            field.fill(empty)
            self.image = field
        else:
            self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()

class Animated(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_play = False
        self.frame = 0
        self.images = []
        self.image = None
        self.rect = None

    def play(self):
        self.is_play = True

    def update(self, speed: float):
        if not self.is_play:
            return

        self.frame += speed
        s = int(self.frame)
        if s >= len(self.images):
            self.image = self.images[0]
            self.is_play = False
            self.frame = 0
            return

        self.image = self.images[s]

    def im_sub_load(self, path):
        for imgp in sorted(os.listdir(path)):
            img = pygame.image.load(os.path.join(path, imgp))
            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

class AnimatedVideo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cycled = False
        self.video = None
        self.is_play = False
        self.image = None
        self.last_image = None
        self.rect = None

    def _set_frame(self, video_image):
        self.image = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")

    def play(self):
        self.is_play = True

    def update(self, speed: float):
        if not self.is_play:
            return

        success, video_image = self.video.read()
        if not success:
            if self.cycled:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                _, video_image = self.video.read()
            else:
                self.is_play = False
                return

        self._set_frame(video_image)

    def im_sub_load(self, path):
        self.video = cv2.VideoCapture(path)
        _, video_image = self.video.read()
        self._set_frame(video_image)
        self.rect = self.image.get_rect()

class BackAnimated(Animated):
    def __init__(self, num: str, star: str):
        super().__init__()
        self.star = star
        self.num = num
        self._load()

    def _load(self):
        path = os.path.join('background', 'dyn', self.star, self.num)
        self.im_sub_load(path)
        self.rect.topleft = (0, 0)

class FallAnimated(AnimatedVideo):
    def __init__(self, star: str):
        super().__init__()
        self.star = star
        self._load()

    def _load(self):
        path = os.path.join('background', 'fall', self.star, 'effect.mp4')
        self.im_sub_load(path)

class Background(Static):
    def __init__(self, lifetime):
        super().__init__()
        self.lifetime = 60 + lifetime * CONFIG['fps']
        self._load()

    def _load(self):
        path = os.path.join('background', 'static', 'Wish_template.jpg')
        self.im_sub_load(path)
        self.rect.topleft = (0, 0)

class UserBackground(Static):
    def __init__(self, fname):
        super().__init__()
        self.fname = fname
        self.lifetime = -1
        self._load()

    def _load(self):
        path = os.path.join('background', self.fname)
        self.im_sub_load(path)
        self.rect.topleft = (0, 0)

class UserBackgroundAnim(AnimatedVideo):
    def __init__(self, fname):
        super().__init__()
        self.cycled = True
        self.fname = fname
        self.lifetime = -1
        self._load()

    def _load(self):
        path = os.path.join('background', self.fname)
        self.im_sub_load(path)
        self.rect.topleft = (0, 0)

class UserText(Static):
    def __init__(self, text, cords, color=None):
        super().__init__()
        self.text = text
        self.lifetime = CONFIG['start_delay'] * CONFIG['fps']
        self.center = cords
        self.color = color
        self._render()
        self._load()

    def _render(self):
        textobj = None
        font = None

        for sfont in range(18, 240):
            font = pygame.font.Font(os.path.join('fonts', 'Genshin_Impact.ttf'), sfont)
            textobj = font.render(self.text, True, USERTEXT_COLOR if self.color is None else self.color).convert_alpha()

            if 1280 - textobj.get_width() < 30:
                break

        self.font = font
        self.image = textobj
        self.out_image = surfill(textobj.copy(), USERTEXT_OUTLINE)

    def _load(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Wish(Static):
    def __init__(self, wtype, wname):
        super().__init__()
        self.lifetime = -1
        self.wtype = wtype
        self.wname = wname
        self._load()

    def _load(self):
        path = os.path.join('images', self.wtype, '%s.png' % self.wname)
        self.im_sub_load(path)
        self.rect.center = (640, 360)

class WishBack(Static):
    def __init__(self, wtype):
        super().__init__()
        self.lifetime = -1
        self.wtype = wtype
        self._load()

    def _load(self):
        if self.wtype is None:
            self.im_sub_load(None)
        else:
            path = os.path.join('background', 'weapon', '%s.png' % self.wtype)
            self.im_sub_load(path)
            self.rect.center = (640, 360)

class WishMeta(Static):
    def __init__(self, wtype, wname):
        super().__init__()
        self.lifetime = -1
        self.wtype = wtype
        self.wname = wname
        self._load()

    def _load(self):
        if self.wtype == 'star':
            path = os.path.join('images', 'star.png')
        else:
            path = os.path.join('images', 'elements', '%s-%s.png' % (self.wtype, self.wname))
        self.im_sub_load(path)

class WishText(Static):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(os.path.join('fonts', 'Genshin_Impact.ttf'), 38)
        self.lifetime = -1
        self._load()

    def _load(self):
        textobj = self.font.render(self.text, True, USERTEXT_COLOR).convert_alpha()
        self.image = textobj
        self.out_image = surfill(textobj.copy(), USERTEXT_OUTLINE)
        self.rect = self.image.get_rect()

class PermaText(Static):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(os.path.join('fonts', 'Genshin_Impact.ttf'), 48)
        self.lifetime = -1
        self._load()

    def _load(self):
        textobj = self.font.render(self.text, True, USERTEXT_COLOR).convert_alpha()
        self.image = textobj
        self.out_image = surfill(textobj.copy(), USERTEXT_OUTLINE)
        self.rect = self.image.get_rect()
        self.rect.bottomright = (1270, 710)

class TwitchBot(commands.Bot):
    def __init__(self, que):
        super().__init__(token=CONFIG['bot_token'], prefix='!', initial_channels=[CONFIG['work_channel'],])
        self.savefile = 'database.sql'
        self.gacha_users = {}
        self.last_re = 0
        self.que = que
        self._load()

    def _load(self):
        print('[TWITCH] Загружаем данные пользователей..')
        if os.path.exists(self.savefile):
            with open(self.savefile, 'rb') as sf:
                self.gacha_users = pickle.load(sf)
        else:
            self.gacha_users = {}

        command = commands.Command(CONFIG['wish_command'], self.wish)
        self.add_command(command)

        print('[TWITCH] Данные загружены. Всего пользователей в базе:', len(self.gacha_users))
        print('[TWITCH] Подключаемся к чату на канал %s..' % CONFIG['work_channel'])

    async def event_ready(self):
        print('[TWITCH] Подключено. Данные бота:', self.nick, self.user_id)
        if CONFIG['self_wish']:
            print('[TWITCH] Молитвы бота включены каждые %d сек.' % CONFIG['self_wish_every'])
            asyncio.Task(self.send_autowish(), loop=asyncio.get_event_loop())

    async def send_notify(self, mention, wtime):
        ntext_c = random.choice(NOTIFY_MSG)
        ntext = ntext_c.format(username=mention, command='!' + CONFIG['wish_command'])

        await asyncio.sleep(wtime)
        await self.connected_channels[0].send(ntext)

    async def send_autowish(self):
        auto_gacha = Gacha(self.nick, '#FFFFFF')
        while True:
            print('[TWITCH] Отправляю автосообщение..')
            await self.connected_channels[0].send(CONFIG['wish_command'])
            await asyncio.sleep(1)

            wo = auto_gacha.generate_wish()
            self.que.put(wo)

            anwser_text_c = random.choice(CHATBOT_MSG)
            anwser_text = anwser_text_c.format(username='@' + self.nick, wish_count=auto_gacha.wish_count)

            await self.connected_channels[0].send(anwser_text)
            await asyncio.sleep(CONFIG['self_wish_every'])

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

    async def wish(self, ctx: commands.Context):
        user = ctx.author
        if user.display_name in self.gacha_users:
            ugacha = self.gacha_users[user.display_name]
        else:
            ugacha = Gacha(user.display_name, user.color if user.color else '#FFFFFF')
            self.gacha_users[user.display_name] = ugacha

        ctime = int(time.time())
        if user.is_broadcaster:
            out_wait = CONFIG['wish_timeout']['broadcaster']
        elif user.is_mod:
            out_wait = CONFIG['wish_timeout']['mod']
        elif user.is_subscriber:
            out_wait = CONFIG['wish_timeout']['subscriber']
        else:
            out_wait = CONFIG['wish_timeout']['user']

        if ctime - ugacha.wish_stamp < out_wait:
            return
        if ctime - self.last_re < CONFIG['wish_global_timeout']:
            return

        if CONFIG['send_notify']:
            asyncio.Task(self.send_notify(user.mention, out_wait), loop=asyncio.get_event_loop())

        wo = ugacha.generate_wish()
        self.que.put(wo)

        # TODO: replace with REAL sql(lite)
        with open(self.savefile, 'wb') as sf:
            pickle.dump(self.gacha_users, sf)

        self.last_re = int(time.time())
        anwser_text_c = random.choice(CHATBOT_MSG)
        anwser_text = anwser_text_c.format(username=user.mention, wish_count=ugacha.wish_count)
        await ctx.send(anwser_text)

def merge_wish_meta(cords, meta_type, meta_name, stars):
    meta_type.rect.center = cords
    meta_name.rect.midleft = ((meta_type.rect.center[0] - 20) + meta_type.image.get_width() / 2, cords[1])

    starl = []
    for i in range(stars):
        star = WishMeta('star', None)
        star.rect.center = ((meta_name.rect.bottomleft[0] + 10) + 20 * i, meta_name.rect.bottomleft[1] + 5)
        starl.append(star)
    return meta_type, meta_name, starl

def surfill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))
    return surface

def objfill(obj, color):
    obj.image = surfill(obj.image, color)
    return obj

def render_text_outline(display, anim, tx):
    offsets = [(ox, oy) for ox in range(-tx, 2 * tx, tx) for oy in range(-tx, 2 * tx, tx) if ox != 0 or oy != 0]
    for ox, oy in offsets:
        display.blit(anim.out_image, (anim.rect[0] + ox, anim.rect[1] + oy))

def draw_group(display, group):
    draw_list = []
    perm_test = []
    for anim in group:
        if not anim.is_play:
            continue
        if isinstance(anim, PermaText):
            perm_test.append(anim)
        else:
            draw_list.append(anim)

    draw_list += perm_test
    for anim in draw_list:
        if isinstance(anim, WishText) or isinstance(anim, UserText) or isinstance(anim, PermaText):
            render_text_outline(display, anim, 1)
        display.blit(anim.image, anim.rect)

def update_group(group, speed):
    for anim in group:
        anim.update(speed)

def bot_hande(que):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print('[TWITCH] Ждем 5 секунд перед запуском..')
    time.sleep(5)

    bot = TwitchBot(que)
    bot.run()

def thrbot(que):
    tbot = threading.Thread(target=bot_hande, args=(que, ))
    tbot.daemon = True
    return tbot

def write_history(nickname, wish_count, star, wtype, wish):
    fpath = CONFIG['history_file']['path']
    if not fpath:
        return

    if not os.path.exists(fpath):
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write('date,nickname,wish_count,star,type,wish\n')

    t = time.localtime()
    wdate = time.strftime("%d.%m.%Y-%H:%M:%S", t)
    with open(fpath, 'a', encoding='utf-8') as fp:
        fp.write('%s,%s,%s,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, wish))

def main():
    global mdisplay, wish_que, animations

    # wo_ = GachaWish('4', "__test_mode__", '#000000', cwish_wtype='char', cwish_wmetatype='element', cwish_wmetaelem='anemo', cwish_cname='heizo', cwish_wname='Сиканоин Хэйдзо')
    # wish_que.put(wo_)

    if CONFIG['test_mode']:
        nuser = '__test_mode__'
        CONFIG['bot_token'] = nuser
        G = Gacha(nuser, '#000000')
        for _ in range(100):
            wo = G.generate_wish()
            wish_que.put(wo)

    tbot_w = False
    tbot = None
    print('[MAIN] Запускаемся..')

    if CONFIG['bot_token'].startswith('oauth:'):
        tbot = thrbot(wish_que)
        tbot.start()
        tbot_w = True
        print('[MAIN] Твич бот запущен')
    else:
        print('[MAIN] Твич токен не найден, бот запущен не будет')

    control = Coordiantor(wish_que, animations)

    print('[MAIN] FPS установлен в', CONFIG['fps'])
    while True:
        fps.tick(CONFIG['fps'])

        if tbot_w and (not tbot.is_alive()):
            tbot.join()
            print('[MAIN] Твич бот умер по причине ^, перезапускаем..')
            tbot = thrbot(wish_que)
            tbot.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        control.update()
        mdisplay.fill(CONFIG['chroma_color'])
        draw_group(mdisplay, animations)
        update_group(animations, 1.0)

        pygame.display.update()

if __name__ == '__main__':
    main()