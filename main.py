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

import json
import jsonschema

from data import DATABASE
from data import CONFIG_SCHEMA

import twitchio
from twitchio import http as twio_http
from twitchio.ext import pubsub
from twitchio.ext import commands

import base64
import pickle
import sqlite3

import logging
_time_stamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    filename=os.path.join('logs', '%s.log' % _time_stamp),
                    filemode='w',
                    encoding='utf-8',
                    level=logging.DEBUG)

_config = {}
try:
    _config = json.loads(open('config.json', 'r', encoding='utf-8').read())
except (json.JSONDecodeError, ValueError) as _e:
    print('[MAIN] Ошибка при загрузке файла конфигурации:', _e)
    sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

try:
    jsonschema.validate(_config, schema=CONFIG_SCHEMA)
except jsonschema.ValidationError as _e:
    print('[MAIN] Ошибка при загрузке файла конфигурации:', _e)
    sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

__title__ = 'genshin-twitch-wish'
__site__ = 'github.com/dzmuh97/genshin-twitch-wish'
__version__ = '2.0.2'

CONFIG = _config['CONFIG']
_messages = _config['MESSAGES']
USER_SPLASH_TEXT = _messages['user_splash_text']
CHATBOT_TEXT = _messages['chatbot_text']
NOTIFY_TEXT = _messages['notify_text']
POINTS_TEXT = _messages['chanel_points_text']

SOUND_CFG = CONFIG['sound']

USERTEXT_COLOR = (255, 255, 255, 0)
USERTEXT_OUTLINE = (0, 0, 0, 0)

pygame.init()
pygame.display.set_caption(CONFIG['window_name'])

programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

SOUND = {
    'fall': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['fall'])),
    '3': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['3'])),
    '4': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['4'])),
    '5': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['5']))
}

fps = pygame.time.Clock()
mdisplay = pygame.display.set_mode(size=(1280, 720), vsync=1)

wish_que = queue.Queue()
animations = []

if SOUND_CFG['enabled']:
    pygame.mixer.init()

@dataclass
class WishData:
    wish_count: int
    wish_4_grn: int
    wish_5_grn: int
    cwish_star: str
    cwish_stype: str
    cwish_wtype: str
    cwish_wmetatype: str
    cwish_wmetaelem: str
    cwish_cname: str
    cwish_wname: str

@dataclass
class Wish:
    username: str
    ucolor: str
    wish_data_c: int
    wish_data_l: list

class Gacha:
    wish_5_garant = 1
    wish_4_garant = 1
    wish_count = 0

    def __init__(self, wish_count=0, wish_4_garant=1, wish_5_garant=1):
        self.wish_stamp = 0
        self.wish_5_garant = wish_5_garant
        self.wish_4_garant = wish_4_garant
        self.wish_count = wish_count
        logging.debug('[GACHA] Создана гача с параметрами w%d w4%d w4%d', wish_count, wish_4_garant, wish_5_garant)

    def __roll(self) -> tuple:
        self.wish_count += 1
        _random_tap = lambda x: random.choice(range(10000)) <= int(x * 100)

        if (self.wish_5_garant > CONFIG['wish_fi_soft_a']) and (self.wish_5_garant < CONFIG['wish_fi_garant']):
            _soft_i = (self.wish_5_garant - CONFIG['wish_fi_soft_a']) / (CONFIG['wish_fi_garant'] - CONFIG['wish_fi_soft_a'])
            _soft_chance = CONFIG['wish_fi_chance'] + _soft_i * 100
            if _random_tap(_soft_chance):
                self.wish_5_garant = 1
                return '5', 'srnd'
        else:
            if _random_tap(CONFIG['wish_fi_chance']):
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

        if _random_tap(CONFIG['wish_fo_chance']):
            self.wish_4_garant = 1
            return '4', 'rnd'

        return '3', 'rnd'

    def generate_wish(self, count) -> list:
        self.wish_stamp = int(time.time())

        rolls = []
        for _ in range(count):
            star, star_type = self.__roll()
            logging.debug('[GACHA] Результат крутки: %s %s', star, star_type)
            if star == '3':
                wtype = 'weapon'
            else:
                wtype = random.choice(['weapon', 'char'])

            data = random.choice(DATABASE[star][wtype])
            logging.debug('[GACHA] Данные крутки: %s', data)
            gacha_obj = WishData(self.wish_count, self.wish_4_garant, self.wish_5_garant, star, star_type, **data)
            rolls.append(gacha_obj)

        return rolls

class UserDB:
    database = 'database.sqlite'
    database_old = 'database.sql'

    def __init__(self):
        self.conn = sqlite3.connect(self.database)
        logging.debug('[DB] Создано новое подключение к базе данных')
        if not self._check_table():
            logging.debug('[DB] Таблицы пользователей не существует, создаем..')
            self._create_table()
        self._restore_old()

    def _restore_old(self):
        if not os.path.exists(self.database_old):
            return

        logging.debug('[DB] Начата загрузка данных из старой базы данных (<=1.3)')

        print('[DB] Начинаем импорт старой базы данных..')
        with open(self.database_old, mode='rb') as f:
            data = pickle.loads(f.read())

        i_users = 0
        print('[DB] В старой базе найдено пользователей:', len(data))
        for user, gacha in data.items():
            user = user.lower()

            check = self.get(user)
            if check:
                self.update(user, gacha)
                continue

            self.push(user, gacha)
            i_users += 1

        print('[DB] Импортировано пользователей:', i_users)
        os.remove(self.database_old)
        print('[DB] Старая база данных удалена!',)

    def _check_table(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        ret = cur.fetchone()
        cur.close()

        if ret is None:
            return False

        return True

    def _create_table(self):
        cur = self.conn.cursor()
        payload = 'CREATE TABLE users (username TEXT PRIMARY KEY, wish_count INTEGER, wish_4_garant INTEGER, wish_5_garant INTEGER);'
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def get_all(self):
        logging.debug('[DB] Вызван метод get_all')
        cur = self.conn.cursor()
        payload = 'SELECT * FROM users;'
        cur.execute(payload)
        data = cur.fetchall()
        cur.close()

        return data

    def get(self, username):
        logging.debug('[DB] Вызван метод get с параметрами %s', username)
        cur = self.conn.cursor()
        payload = 'SELECT * FROM users WHERE username=?;'
        cur.execute(payload, (username,))
        data = cur.fetchone()
        cur.close()

        return data

    def push(self, username, gacha):
        logging.debug('[DB] Вызван метод push с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = 'INSERT INTO users VALUES(?, ?, ?, ?);'
        cur.execute(payload, (username, gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant))
        self.conn.commit()
        cur.close()

    def update(self, username, gacha):
        logging.debug('[DB] Вызван метод update с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = 'UPDATE users SET wish_count=?, wish_4_garant=?, wish_5_garant=? WHERE username=?;'
        cur.execute(payload, (gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, username))
        self.conn.commit()
        cur.close()

class Coordiantor:
    states_name = ['IDLE', 'INIT', 'DRAW_TEXT', 'DRAW_FALL', 'DRAW_WISH', 'CLEAR']

    def __init__(self, que, animl):
        self.states = cycle(self.states_name)
        self.state = next(self.states)

        self.animl = animl
        self.que = que

        self.t_load_done = True

        self.cur_wish = None
        self.n_cur_wish = None
        self.wish_objs = {}
        self.sound = []

        logging.debug('[PANEL] Создана новая панель управления')

    def _t_load_chunk(self, usiwshdata):
        self.t_load_done = False

        _t = time.time()
        logging.debug('[PANEL] Вызван метод _t_load_chunk с параметрами: %s', usiwshdata)

        anim_config = CONFIG['animations']
        w_splash_list = self.wish_objs['wish_splash_list']

        multi = True if self.cur_wish.wish_data_c > 1 else False
        uwstar = usiwshdata.cwish_star
        wtype = usiwshdata.cwish_wtype
        wback = usiwshdata.cwish_wmetaelem if usiwshdata.cwish_wmetatype == 'weapon' else None
        wmetatype = usiwshdata.cwish_wmetatype
        wmetaelem = usiwshdata.cwish_wmetaelem
        cname = usiwshdata.cwish_cname
        wname = usiwshdata.cwish_wname

        _wmeta_text = [WishText(_wname) for _wname in wname.split('\n')]
        _wmeta = merge_wish_meta((80, 450), WishMeta(wmetatype, wmetaelem), _wmeta_text, int(uwstar))
        wish_meta_type, wish_meta_name, wish_meta_star = _wmeta

        w_splash_list.append(
            {
            'back_static': {'obj': Background(anim_config['end_delay_milti' if multi else 'end_delay'][uwstar]), 'play': False},
            'back_anim_first': {'obj': BackAnimated('first', uwstar), 'play': False},
            'back_anim_second': {'obj': BackAnimated('second', uwstar), 'play': False},
            'wish_color': {'obj': WishSplash(wtype, cname), 'play': False},
            'wish_black': {'obj': objfill(WishSplash(wtype, cname), pygame.Color(0, 0, 0)), 'play': False},
            'wish_back': {'obj': WishBack(wback), 'play': False},
            'wish_meta_type': {'obj': wish_meta_type, 'play': False},
            'wish_meta_name': {'obj': wish_meta_name, 'play': False},
            'wish_meta_star': {'obj': wish_meta_star, 'play': False},
            'done': False
            }
        )

        logging.debug('[PANEL] Метод _t_load_chunk загрузил данные за %s с.', time.time() - _t)
        self.t_load_done = True

    def _remove_obj(self, obj_data):
        obj = obj_data['obj']

        if isinstance(obj, list):
            for objl in obj:
                if objl in self.animl:
                    self.animl.remove(objl)

        if obj in self.animl:
            self.animl.remove(obj)

    def _play_obj(self, obj_data):
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

        logging.debug('[PANEL] Состояние панели: IDLE')

        self.cur_wish = wish
        self.que.task_done()

        star_types = {
            'srnd': 'мягкий гарант',
            'garant': 'гарант',
            'rnd': 'рандом',
        }

        for uwishdata in wish.wish_data_l:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('[ГАЧА]', '[%s]' % current_time,
                  'Результат для', wish.username,
                  '#%d' % uwishdata.wish_count,
                  'w4#%d' % uwishdata.wish_4_grn,
                  'w5#%d' % uwishdata.wish_5_grn,
                  uwishdata.cwish_star, '* ->', uwishdata.cwish_wname.replace('\n', ' '),
                  '[%s]' % star_types[uwishdata.cwish_stype])

            if CONFIG['history_file'][uwishdata.cwish_star]:
                write_history(wish.username, uwishdata.wish_count, uwishdata.cwish_star, star_types[uwishdata.cwish_stype], uwishdata.cwish_wname)

        return True

    def state_INIT(self):
        logging.debug('[PANEL] Состояние панели: INIT')
        _t = time.time()

        wish_data = self.cur_wish
        wish_list = self.cur_wish.wish_data_l

        multi = True if self.cur_wish.wish_data_c > 1 else False

        if any(x.cwish_star == '5' for x in wish_list):
            wstar = '5'
        elif any(x.cwish_star == '4' for x in wish_list):
            wstar = '4'
        else:
            wstar = '3'

        utext = random.choice(USER_SPLASH_TEXT)
        logging.debug('[PANEL] Анимация падения имеет параметры: wstar=%s, multi=%s', wstar, multi)

        self.wish_objs.update(
            {
            'user_perm_text': {'obj': PermaText(wish_data.username), 'play': False},
            'user_nick': {'obj': UserText(wish_data.username, (640, 300), wish_data.ucolor),'play': False},
            'user_text': {'obj': UserText(utext, (640, 530)), 'play': False},
            'fall_anim': {'obj': FallAnimated(wstar, multi), 'play': False}
            }
        )

        w_splash_list = []
        self.wish_objs.update(
            {
            'wish_splash_list': w_splash_list
            }
        )

        logging.debug('[PANEL] Начальные данные для анимации загружены за %s с.', time.time() - _t)
        logging.debug('[PANEL] Инициализация анимации с данными: %s', self.wish_objs)

        anim_config = CONFIG['animations']
        uback_cfg = anim_config['user_background']
        uback_enabled = uback_cfg['enabled']
        if not uback_enabled:
            return True

        if uback_cfg['type'] == 'static':
            uback_obj = UserBackground(uback_cfg['path'])
        else:
            uback_obj = UserBackgroundAnim(uback_cfg['path'])

        self.wish_objs.update(
            {
            'user_background': {'obj': uback_obj, 'play': False}
            }
        )

        logging.debug('[PANEL] Загружен пользовательский фон: %s', self.wish_objs['user_background'])
        return True

    def state_DRAW_TEXT(self):
        userback_cfg = CONFIG['animations']['user_background']

        if userback_cfg['enabled']:
            self._play_obj(self.wish_objs['user_background'])

        textnickobj = self._play_obj(self.wish_objs['user_nick'])
        textuserobj = self._play_obj(self.wish_objs['user_text'])
        if textnickobj.is_play and textuserobj.is_play:
            return False

        pre_wish = self.cur_wish.wish_data_l.pop(0)
        self._t_load_chunk(pre_wish)

        return True

    def state_DRAW_FALL(self):
        userback_cfg = CONFIG['animations']['user_background']
        sound_cfg = CONFIG['sound']

        self._remove_obj(self.wish_objs['user_nick'])
        self._remove_obj(self.wish_objs['user_text'])

        if userback_cfg['enabled']:
            self._remove_obj(self.wish_objs['user_background'])

        self._play_obj(self.wish_objs['user_perm_text'])
        fallobj = self._play_obj(self.wish_objs['fall_anim'])

        if sound_cfg['enabled']:
            sound_fall = SOUND['fall']
            if not (sound_fall in self.sound):
                self.sound.append(sound_fall)
                sound_fall.play()

        if fallobj.is_play:
            return False

        return True

    def state_DRAW_WISH(self):
        sound_cfg = CONFIG['sound']

        if not (self.wish_objs.get('fall_anim', None) is None):
            self._remove_obj(self.wish_objs['fall_anim'])
            new_wish_obj = {'wish_splash_list': self.wish_objs['wish_splash_list'][:]}
            self.wish_objs.clear()
            self.wish_objs = new_wish_obj

        if not (self.n_cur_wish is None) and self.n_cur_wish['done']:
            self._remove_obj(self.n_cur_wish['back_static'])
            self._remove_obj(self.n_cur_wish['wish_back'])
            self._remove_obj(self.n_cur_wish['wish_color'])
            self._remove_obj(self.n_cur_wish['wish_meta_type'])
            self._remove_obj(self.n_cur_wish['wish_meta_name'])
            self._remove_obj(self.n_cur_wish['wish_meta_star'])

            if len(self.cur_wish.wish_data_l) > 0:
                new_cur_wish = self.cur_wish.wish_data_l.pop(0)
                self._t_load_chunk(new_cur_wish)

            self.n_cur_wish = None

        wish_splash_list = self.wish_objs['wish_splash_list']
        if len(wish_splash_list) > 0 and self.n_cur_wish is None:
            self.n_cur_wish = self.wish_objs['wish_splash_list'].pop(0)

        if not (self.n_cur_wish is None):
            back_tmpl = self._play_obj(self.n_cur_wish['back_static'])
            back_f = self._play_obj(self.n_cur_wish['back_anim_first'])
            self._play_obj(self.n_cur_wish['wish_black'])

            if sound_cfg['enabled']:
                sound_star = SOUND[back_f.star]
                if not (sound_star in self.sound):
                    self.sound.append(sound_star)
                    sound_star.play()

            if back_f.is_play:
                return False

            self._remove_obj(self.n_cur_wish['wish_black'])
            self._remove_obj(self.n_cur_wish['back_anim_first'])

            back_s = self._play_obj(self.n_cur_wish['back_anim_second'])
            self._play_obj(self.n_cur_wish['wish_back'])
            self._play_obj(self.n_cur_wish['wish_color'])
            if back_s.is_play:
                return False

            self._remove_obj(self.n_cur_wish['back_anim_second'])

            self._play_obj(self.n_cur_wish['wish_meta_type'])
            self._play_obj(self.n_cur_wish['wish_meta_name'])
            self._play_obj(self.n_cur_wish['wish_meta_star'])

            if back_tmpl.is_play:
                return False

            if sound_cfg['enabled']:
                sound_star = SOUND[back_f.star]
                self.sound.remove(sound_star)

            self.n_cur_wish['done'] = True
            return False

        return True

    def state_CLEAR(self):
        logging.debug('[PANEL] Состояние панели: CLEAR')
        self.animl.clear()
        self.wish_objs.clear()
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

class BackAnimated(AnimatedVideo):
    def __init__(self, num: str, star: str):
        super().__init__()
        self.star = star
        self.num = num
        self._load()

    def _load(self):
        path = os.path.join('background', 'dyn', self.star, self.num, 'effect.mp4')
        self.im_sub_load(path)

class FallAnimated(AnimatedVideo):
    def __init__(self, star: str, multi: False):
        super().__init__()
        self.multi = multi
        self.star = star
        self._load()

    def _load(self):
        if self.star in ['4', '5']:
            if self.multi:
                path = os.path.join('background', 'fall', self.star, 'multi.mp4')
            else:
                path = os.path.join('background', 'fall', self.star, 'effect.mp4')
        else:
            path = os.path.join('background', 'fall', self.star, 'effect.mp4')
        self.im_sub_load(path)

class Background(Static):
    def __init__(self, lifetime):
        super().__init__()
        self.lifetime = 60 + lifetime * CONFIG['animations']['fps']
        self.re_lifetime = self.lifetime
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
        self.lifetime = CONFIG['animations']['start_delay'] * CONFIG['animations']['fps']
        self.center = cords
        self.color = color
        self._render()
        self._load()

    def _render(self):
        textobj = None
        font = None

        font_config = CONFIG['animations']['font']
        for sfont in range(18, 240):
            font = pygame.font.Font(os.path.join('fonts', font_config['path']), sfont)
            textobj = font.render(self.text, True, USERTEXT_COLOR if self.color is None else self.color).convert_alpha()

            if 1280 - textobj.get_width() < 30:
                break

        self.font = font
        self.image = textobj
        self.out_image = surfill(textobj.copy(), USERTEXT_OUTLINE)

    def _load(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class WishSplash(Static):
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

        font_config = CONFIG['animations']['font']
        self.font = pygame.font.Font(os.path.join('fonts', font_config['path']), font_config['wish_name_size'])
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

        font_config = CONFIG['animations']['font']
        self.font = pygame.font.Font(os.path.join('fonts', font_config['path']), font_config['user_uid_size'])
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
        self.chatbot_cfg = CONFIG['chat_bot']
        self.eventbot_cfg = CONFIG['event_bot']
        self.savefile = 'database.sql'
        self.gacha_users = {}
        self.last_re = 0
        self.que = que

        self.user_db = UserDB()

        b_token, wcmd_pref, wchn = self.chatbot_cfg['bot_token'], self.chatbot_cfg['wish_command_prefix'], self.chatbot_cfg['work_channel']
        super().__init__(token='oauth:' + b_token,
                         prefix=wcmd_pref,
                         initial_channels=[wchn,])
        self.pubsub = pubsub.PubSubPool(self)
        self.sub_topics = []

        logging.debug('[TWITCH] Инициализация твич бота, параметры: %s, %s, %s', b_token, wcmd_pref + self.chatbot_cfg['wish_command'], wchn)
        self._load()

    def _load(self):
        print('[TWITCH] Загружаем данные пользователей..')
        for user in self.user_db.get_all():
            username, wc, w4c, w5c = user
            ugacha = Gacha(wc, w4c, w5c)
            self.gacha_users.update({username: ugacha})
        print('[TWITCH] Данные загружены. Всего пользователей в базе:', len(self.gacha_users))

        if self.chatbot_cfg['enabled']:
            chb_com = self.chatbot_cfg['wish_command']
            command = commands.Command(chb_com, self.wish)
            self.add_command(command)
            print('[TWITCH] Чат бот включен, команда:', chb_com)

        if self.eventbot_cfg['enabled']:
            eve_tk = self.eventbot_cfg['channel_token']
            eve_id = self.eventbot_cfg['work_channel_id']
            pubsub_tpic = pubsub.channel_points(eve_tk)[eve_id]
            self.sub_topics.append(pubsub_tpic)
            print('[TWITCH] Баллы канала включены, активировано наград:', len(self.eventbot_cfg['rewards']))

        if self.chatbot_cfg['enabled']:
            print('[TWITCH] Подключаемся к чату на канал %s..' % self.chatbot_cfg['work_channel'])
        if self.eventbot_cfg['enabled']:
            print('[TWITCH] Подключаемся к баллам канала %d..' % self.eventbot_cfg['work_channel_id'])

    async def event_ready(self):
        print('[TWITCH] Подключено. Данные чатбота:', self.nick, self.user_id)
        if self.eventbot_cfg['enabled']:
            await self.pubsub.subscribe_topics(self.sub_topics)
        if self.chatbot_cfg['self_wish']:
            print('[TWITCH] Молитвы бота включены каждые %d сек.' % self.chatbot_cfg['self_wish_every'])
            asyncio.Task(self.send_autowish(), loop=self.loop)

    async def event_pubsub_error(self, message):
        print('[TWITCH] Не удалось подключиться к баллам канала [ %d ] -> %s' % (self.eventbot_cfg['work_channel_id'], message))

    async def event_pubsub_nonce(self, _):
        print('[TWITCH] Успешно подключен к баллам канала [ %d ]' % self.eventbot_cfg['work_channel_id'])

    async def send_notify(self, mention, wtime):
        ntext_c = random.choice(NOTIFY_TEXT)
        ntext = ntext_c.format(username=mention,
                               command=self.chatbot_cfg['wish_command_prefix'] + self.chatbot_cfg['wish_command'])

        await asyncio.sleep(wtime)
        await self.connected_channels[0].send(ntext)

    async def send_autowish(self):
        auto_gacha = Gacha()
        while True:
            print('[TWITCH] Отправляю автосообщение..')
            await self.connected_channels[0].send(self.chatbot_cfg['wish_command_prefix'] + self.chatbot_cfg['wish_command'])
            await asyncio.sleep(1)

            wl = auto_gacha.generate_wish(self.chatbot_cfg['wish_count'])
            wo = Wish(self.nick, '#FFFFFF', self.chatbot_cfg['wish_count'], wl)
            self.que.put(wo)

            anwser_text_c = random.choice(CHATBOT_TEXT)
            anwser_text = anwser_text_c.format(username='@' + self.nick, wish_count=auto_gacha.wish_count)

            await self.connected_channels[0].send(anwser_text)
            await asyncio.sleep(self.chatbot_cfg['self_wish_every'])

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

    async def wish(self, ctx: commands.Context):
        user = ctx.author

        logging.debug('[TWITCH] Получен команда wish: %s, %s, %s', user.name, user.display_name, user.color)

        if user.name in self.gacha_users:
            ugacha = self.gacha_users[user.name]
        else:
            ugacha = Gacha()
            self.gacha_users[user.name] = ugacha
            self.user_db.push(user.name, ugacha)

        ctime = int(time.time())
        wtimeoust_cfg = self.chatbot_cfg['wish_timeout']
        if user.is_broadcaster:
            out_wait = wtimeoust_cfg['broadcaster']
        elif user.is_mod:
            out_wait = wtimeoust_cfg['mod']
        elif user.is_subscriber:
            out_wait = wtimeoust_cfg['subscriber']
        else:
            out_wait = wtimeoust_cfg['user']

        if ctime - ugacha.wish_stamp < out_wait:
            return
        if ctime - self.last_re < self.chatbot_cfg['wish_global_timeout']:
            return

        if self.chatbot_cfg['send_notify']:
            asyncio.Task(self.send_notify(user.mention, out_wait), loop=self.loop)

        if self.chatbot_cfg['enable_colors']:
            ucolor = user.color if user.color else self.eventbot_cfg['default_color']
        else:
            ucolor = self.eventbot_cfg['default_color']

        wl = ugacha.generate_wish(self.chatbot_cfg['wish_count'])
        wo = Wish(user.display_name, ucolor, self.chatbot_cfg['wish_count'], wl)
        self.que.put(wo)

        self.user_db.update(user.name, ugacha)

        self.last_re = int(time.time())
        answer_text_c = random.choice(CHATBOT_TEXT)
        answer_text = answer_text_c.format(username=user.mention,
                                           wish_count=ugacha.wish_count,
                                           wish_count_w4=ugacha.wish_4_garant - 1,
                                           wish_count_w5=ugacha.wish_5_garant - 1,
                                           wishes_in_cmd=self.chatbot_cfg['wish_count'])

        await ctx.send(answer_text)

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        user = event.user.name.lower()
        title = event.reward.title
        color = self.eventbot_cfg['default_color']

        logging.debug('[TWITCH] Получен ивент pubsub_channel_points: %s, %s, %s', user, title, color)

        rewards_map = {}
        for reward in self.eventbot_cfg['rewards']:
            rewards_map.update({reward['event_name']: reward['wish_count']})

        if not title in rewards_map:
            return

        if user in self.gacha_users:
            ugacha = self.gacha_users[user]
        else:
            ugacha = Gacha()
            self.gacha_users[user] = ugacha
            self.user_db.push(user, ugacha)

        wish_in_command = rewards_map[title]
        wl = ugacha.generate_wish(wish_in_command)
        wo = Wish(user, color, wish_in_command, wl)
        self.que.put(wo)

        self.user_db.update(user, ugacha)

        anwser_text_c = random.choice(POINTS_TEXT)
        anwser_text = anwser_text_c.format(username='@' + user,
                                           wish_count=ugacha.wish_count,
                                           wish_count_w4=ugacha.wish_4_garant - 1,
                                           wish_count_w5=ugacha.wish_5_garant - 1,
                                           reward_cost=event.reward.cost,
                                           wishes_in_cmd=wish_in_command)

        await self.connected_channels[0].send(anwser_text)

    @commands.command()
    async def gbot_status(self, ctx: commands.Context):
        user = ctx.author
        answer_text = '%s я работаю на %s v%s (%s) HungryPaimon ' % (user.mention, __title__, __version__, __site__)
        ugacha = None
        if user.name in self.gacha_users:
            ugacha = self.gacha_users[user.name]
        if not (ugacha is None):
            answer_text += 'твоя статистика: w#%d w4#%d w5#%d MrDestructoid ' % (ugacha.wish_count, ugacha.wish_4_garant, ugacha.wish_5_garant)
        await ctx.send(answer_text)

def merge_wish_meta(cords, meta_type, meta_name, stars):
    meta_type.rect.center = cords

    name_shift = 0
    for meta_text_n in meta_name:
        meta_text_n.rect.midleft = ((meta_type.rect.center[0] - 20) + meta_type.image.get_width() / 2, cords[1] + name_shift)
        name_shift += meta_text_n.image.get_height()
    meta_text_n = meta_name[-1]

    starl = []
    for i in range(stars):
        star = WishMeta('star', None)
        star.rect.topleft = (meta_text_n.rect.bottomleft[0] + 20 * i, meta_text_n.rect.bottomleft[1])
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
    twiohttp = twio_http.TwitchHTTP(bot)
    start_task = loop.create_task(twiohttp.validate(token=bot.chatbot_cfg['bot_token']))

    try:
        loop.run_until_complete(start_task)
    except (twitchio.errors.AuthenticationError, twitchio.errors.HTTPException) as twe:
        print('[TWITCH] Ошибка авторизации:', twe)
        threading.Event().wait()

    bot.run()

def thrbot(que):
    tbot = threading.Thread(target=bot_hande, args=(que, ))
    tbot.daemon = True
    return tbot

def write_history(nickname, wish_count, star, wtype, wish):
    history_cfg = CONFIG['history_file']
    if not history_cfg['enabled']:
        return

    fpath = history_cfg['path']
    if not os.path.exists(fpath):
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write('date,nickname,wish_count,star,type,wish\n')

    t = time.localtime()
    wdate = time.strftime("%d.%m.%Y-%H:%M:%S", t)
    with open(fpath, 'a', encoding='utf-8') as fp:
        fp.write('%s,%s,%s,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, wish.replace('\n', ' ')))

def make_user_wish(username, color, count) -> tuple:
    gacha = Gacha()
    wish_list = gacha.generate_wish(count)
    wish = Wish(username, color, count, wish_list)
    return gacha, wish

def send_stats():
    if not CONFIG['send_dev_stats']:
        return

    def _send_stats():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        t_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        stats_data = json.dumps({'date': t_stamp, 'version': __version__, 'channel': CONFIG['chat_bot']['work_channel'], 'channel_id': CONFIG['event_bot']['work_channel_id']})
        stats_data_b64 = base64.encodebytes(stats_data.encode(encoding='utf-8'))
        try:
            s.connect(("5.252.195.165", 8001))
            s.send(b'POST / HTTP/1.1\r\nHost: 127.0.0.1:9515\r\nContent-Length: %d\r\n\r\n%s' % (len(stats_data_b64), stats_data_b64))
            s.recv(4096)
        except:
            pass
        s.close()

    logging.debug('[STATS] Отправка статистики..')
    t = threading.Thread(target=_send_stats, args=())
    t.daemon = True
    t.start()

def main():
    global mdisplay, wish_que, animations

    # #
    # _star = '4'
    # _type = 'weapon'
    # _name = 'ceremonialgsw'
    #
    # _wd_r = list(filter(lambda x: x['cwish_cname'] == _name, DATABASE[_star][_type]))[0]
    # _wd = WishData(1, 1, 1, _star, 'rnd', **_wd_r)
    # _wish = Wish("__test_mode__", '#000000', 1, [_wd,])
    # wish_que.put(_wish)
    # #

    #
    # for _star in DATABASE:
    #     _wd_l = [DATABASE[_star][x] for x in DATABASE[_star] if x == 'char']
    #     for _wd_r in _wd_l:
    #         if not _wd_r:
    #             continue
    #         _wish = Wish("__test_mode__", '#000000', 2, [WishData(1, 1, 1, _star, 'rnd', **_wd_x) for _wd_x in _wd_r])
    #         wish_que.put(_wish)
    #

    chatbot_cfg = CONFIG['chat_bot']
    eventbot_cfg = CONFIG['event_bot']
    if CONFIG['test_mode']:
        nuser = '__test_mode__'
        chatbot_cfg['enabled'] = eventbot_cfg['enabled'] = False
        _, wl = make_user_wish(nuser, '#FFFFFF', 100)
        wish_que.put(wl)

    tbot_w = False
    tbot = None
    print('[MAIN] Запускаемся..')

    if chatbot_cfg['enabled'] or eventbot_cfg['enabled']:
        tbot = thrbot(wish_que)
        tbot.start()
        tbot_w = True
        print('[MAIN] Твич бот запущен')
        send_stats()
    else:
        print('[MAIN] Твич бот отключен')

    control = Coordiantor(wish_que, animations)

    anim_cfg = CONFIG['animations']
    print('[MAIN] FPS установлен в', anim_cfg['fps'])
    while True:
        fps.tick(anim_cfg['fps'])

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
        mdisplay.fill(anim_cfg['chroma_color'])
        draw_group(mdisplay, animations)
        update_group(animations, 1.0)

        pygame.display.update()

if __name__ == '__main__':
    main()