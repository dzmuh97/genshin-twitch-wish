import sys
import os

import random
import queue
import time
import gc
import cv2

from itertools import cycle
from dataclasses import dataclass

import threading
import asyncio

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

__title__ = 'genshin-twitch-wish'
__site__ = 'github.com/dzmuh97/genshin-twitch-wish'
__version__ = '2.0.3'

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Union, Tuple, List, Dict, Optional
DbUserTuple = Tuple[str, int, int, int]
BaseDrawClass = Union['StaticImage', 'AnimatedVideo']
DrawDataChunk = Union[BaseDrawClass, List[BaseDrawClass]]
DrawData = Dict[str, DrawDataChunk]

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

CONFIG = _config['CONFIG']
_messages = _config['MESSAGES']
USER_SPLASH_TEXT = _messages['user_splash_text']
CHATBOT_TEXT = _messages['chatbot_text']
NOTIFY_TEXT = _messages['notify_text']
POINTS_TEXT = _messages['chanel_points_text']
STATS_MESSAGE = _messages['stats_message']

SOUND_CFG = CONFIG['sound']

USERTEXT_COLOR = pygame.Color(255, 255, 255, 0)
USERTEXT_OUTLINE = pygame.Color(0, 0, 0, 0)

pygame.init()
pygame.display.set_caption(CONFIG['window_name'])

programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

try:
    pygame.mixer.init()
    _sound_work = True
except pygame.error:
    _sound_work = False

if SOUND_CFG['enabled'] and (not _sound_work):
    SOUND_CFG['enabled'] = False

if SOUND_CFG['enabled']:
    SOUND = {
        'fall': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['fall'])),
        '3': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['3'])),
        '4': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['4'])),
        '5': pygame.mixer.Sound(os.path.join('sound', SOUND_CFG['5']))
    }
else:
    SOUND = {}

fps = pygame.time.Clock()
mdisplay = pygame.display.set_mode(size=(1280, 720), vsync=1)

wish_que = queue.Queue()
animations = []


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
    wish_data_l: List[WishData]


class Gacha:
    wish_5_garant = 1
    wish_4_garant = 1
    wish_count = 0

    def __init__(self, wish_count: int = 0, wish_4_garant: int = 1, wish_5_garant: int = 1):
        self.wish_stamp = 0
        self.wish_5_garant = wish_5_garant
        self.wish_4_garant = wish_4_garant
        self.wish_count = wish_count
        logging.debug('[GACHA] Создана гача с параметрами w%d w4%d w4%d', wish_count, wish_4_garant, wish_5_garant)

    @staticmethod
    def _random_tap(x: float) -> bool:
        return random.choice(range(10000)) <= int(x * 100)

    def __roll(self) -> Tuple[str, str]:
        self.wish_count += 1

        if (self.wish_5_garant > CONFIG['wish_fi_soft_a']) and (self.wish_5_garant < CONFIG['wish_fi_garant']):
            _soft_i = (self.wish_5_garant - CONFIG['wish_fi_soft_a']) / (
                    CONFIG['wish_fi_garant'] - CONFIG['wish_fi_soft_a'])
            _soft_chance = CONFIG['wish_fi_chance'] + _soft_i * 100
            if self._random_tap(_soft_chance):
                self.wish_5_garant = 1
                return '5', 'srnd'
        else:
            if self._random_tap(CONFIG['wish_fi_chance']):
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

        if self._random_tap(CONFIG['wish_fo_chance']):
            self.wish_4_garant = 1
            return '4', 'rnd'

        return '3', 'rnd'

    def generate_wish(self, count: int) -> List[WishData]:
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

    def _restore_old(self) -> None:
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
        print('[DB] Старая база данных удалена!', )

    def _check_table(self) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        ret = cur.fetchone()
        cur.close()

        if ret is None:
            return False

        return True

    def _create_table(self) -> None:
        cur = self.conn.cursor()
        payload = 'CREATE TABLE users (username TEXT PRIMARY KEY, wish_count INTEGER, wish_4_garant INTEGER, ' \
                  'wish_5_garant INTEGER); '
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def get_all(self) -> List[DbUserTuple]:
        logging.debug('[DB] Вызван метод get_all')
        cur = self.conn.cursor()
        payload = 'SELECT * FROM users;'
        cur.execute(payload)
        data = cur.fetchall()
        cur.close()

        return data

    def get(self, username) -> Optional[DbUserTuple]:
        logging.debug('[DB] Вызван метод get с параметрами %s', username)
        cur = self.conn.cursor()
        payload = 'SELECT * FROM users WHERE username=?;'
        cur.execute(payload, (username,))
        data = cur.fetchone()
        cur.close()

        return data

    def push(self, username: str, gacha: Gacha) -> None:
        logging.debug('[DB] Вызван метод push с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = 'INSERT INTO users VALUES(?, ?, ?, ?);'
        cur.execute(payload, (username, gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant))
        self.conn.commit()
        cur.close()

    def update(self, username: str, gacha: Gacha) -> None:
        logging.debug('[DB] Вызван метод update с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = 'UPDATE users SET wish_count=?, wish_4_garant=?, wish_5_garant=? WHERE username=?;'
        cur.execute(payload, (gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, username))
        self.conn.commit()
        cur.close()


class Coordiantor:
    states_name: List[str] = ['idle', 'init', 'draw_text', 'draw_fall', 'draw_wish', 'clear']
    cur_wish: Optional[Wish] = None
    cur_wish_data: Optional[WishData] = None
    cur_draw_objs: DrawData = {}
    cur_draw_objs_played: Dict[str, bool] = {}
    used_sound: List[pygame.mixer.Sound] = []

    def __init__(self, que: queue.Queue, animl: List[BaseDrawClass]):
        self.states = cycle(self.states_name)
        self.state = next(self.states)

        self.animl = animl
        self.que = que

        logging.debug('[PANEL] Создана новая панель управления')

    def _iter_wdata(self) -> bool:
        if len(self.cur_wish.wish_data_l) > 0:
            self.cur_wish_data = self.cur_wish.wish_data_l.pop(0)
            return True
        return False

    def _load_chunk(self) -> None:
        if self.cur_wish_data is None:
            logging.debug('[PANEL] BUG? Вызван метод _t_load_chunk, но cur_wish_data == None')
            return

        cwdata = self.cur_wish_data

        _t = time.time()
        logging.debug('[PANEL] Вызван метод _t_load_chunk с параметрами: %s', cwdata)

        anim_config = CONFIG['animations']

        multi = True if self.cur_wish.wish_data_c > 1 else False
        uwstar = cwdata.cwish_star
        wtype = cwdata.cwish_wtype
        wmetatype = cwdata.cwish_wmetatype
        wmetaelem = cwdata.cwish_wmetaelem
        cname = cwdata.cwish_cname
        wname = cwdata.cwish_wname

        _wmeta_text = [WishText(_wname) for _wname in wname.split('\n')]
        _wmeta = merge_wish_meta((80, 450), WishMeta(wmetatype, wmetaelem), _wmeta_text, int(uwstar))
        wish_meta_type, wish_meta_name, wish_meta_star = _wmeta

        wish_cords_normal = (640, 360)
        wish_cords_shadow = (645, 375)
        wish_color = WishSplash(wtype, cname, wish_cords_normal)
        wish_black = objfill(WishSplash(wtype, cname, wish_cords_normal), pygame.Color(0, 0, 0))
        wish_black_shift = objfill(WishSplash(wtype, cname, wish_cords_shadow), pygame.Color(0, 0, 0))

        self.cur_draw_objs.update(
            {
                'back_static': Background(anim_config['end_delay_milti' if multi else 'end_delay'][uwstar]),
                'back_anim_first': BackAnimated('first', uwstar),
                'back_anim_second': BackAnimated('second', uwstar),
                'wish_color': wish_color,
                'wish_black': wish_black,
                'wish_black_shift': wish_black_shift,
                'wish_back': WishBack(cwdata.cwish_wmetaelem) if cwdata.cwish_wmetatype == 'weapon' else None,
                'wish_meta_type': wish_meta_type,
                'wish_meta_name': wish_meta_name,
                'wish_meta_star': wish_meta_star
            }
        )

        self.cur_draw_objs_played.update(
            {
                'back_static': False,
                'back_anim_first': False,
                'back_anim_second': False,
                'wish_color': False,
                'wish_black': False,
                'wish_black_shift': False,
                'wish_back': False,
                'wish_meta_type': False,
                'wish_meta_name': False,
                'wish_meta_star': False
            }
        )

        logging.debug('[PANEL] Метод _t_load_chunk загрузил данные за %s с.', time.time() - _t)

    def _purge_obj(self, obj_name: str) -> None:
        self._hide_obj(obj_name)
        self._remove_obj(obj_name)

    def _remove_obj(self, obj_name: str) -> None:
        if not (obj_name in self.cur_draw_objs):
            return

        del self.cur_draw_objs[obj_name]

    def _hide_obj(self, obj_name: str) -> None:
        if not (obj_name in self.cur_draw_objs):
            return

        obj = self.cur_draw_objs[obj_name]
        if isinstance(obj, list):
            for objl in obj:
                if objl in self.animl:
                    self.animl.remove(objl)
        else:
            if obj in self.animl:
                self.animl.remove(obj)

    def _play_obj(self, obj_name: str) -> DrawDataChunk:
        obj = self.cur_draw_objs[obj_name]
        objp = self.cur_draw_objs_played

        if objp[obj_name]:
            return obj

        if isinstance(obj, list):
            for obji in obj:
                self.animl.append(obji)
                obji.play()
        else:
            self.animl.append(obj)
            obj.play()

        objp[obj_name] = True
        return obj

    def update(self) -> None:
        state_func = getattr(self, 'state_%s' % self.state)
        isnext = state_func()
        if isnext:
            self.state = next(self.states)

    def state_idle(self) -> bool:
        try:
            wish: Wish = self.que.get(block=False)
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
                write_history(wish.username, uwishdata.wish_count, uwishdata.cwish_star,
                              star_types[uwishdata.cwish_stype], uwishdata.cwish_wname)

        return True

    def state_init(self) -> bool:
        logging.debug('[PANEL] Состояние панели: INIT')
        _t = time.time()

        wish_data = self.cur_wish
        multi = True if self.cur_wish.wish_data_c > 1 else False

        if any(x.cwish_star == '5' for x in self.cur_wish.wish_data_l):
            wstar = '5'
        elif any(x.cwish_star == '4' for x in self.cur_wish.wish_data_l):
            wstar = '4'
        else:
            wstar = '3'

        utext = random.choice(USER_SPLASH_TEXT)
        logging.debug('[PANEL] Анимация падения имеет параметры: wstar=%s, multi=%s', wstar, multi)

        self.cur_draw_objs = \
            {
                'user_perm_text': PermaText(wish_data.username),
                'user_nick': UserText(wish_data.username, (640, 300), wish_data.ucolor),
                'user_text': UserText(utext, (640, 530)),
                'fall_anim': FallAnimated(wstar, multi)
            }

        self.cur_draw_objs_played = \
            {
                'user_perm_text': False,
                'user_nick': False,
                'user_text': False,
                'fall_anim': False
            }

        logging.debug('[PANEL] Начальные данные для анимации загружены за %s с.', time.time() - _t)
        logging.debug('[PANEL] Инициализация анимации с данными: %s', self.cur_draw_objs)

        anim_config = CONFIG['animations']
        uback_cfg = anim_config['user_background']
        uback_enabled = uback_cfg['enabled']
        if not uback_enabled:
            return True

        if uback_cfg['type'] == 'static':
            uback_obj = UserBackground(uback_cfg['path'])
        else:
            uback_obj = UserBackgroundAnim(uback_cfg['path'])

        self.cur_draw_objs.update(
            {
                'user_background': uback_obj
            }
        )

        logging.debug('[PANEL] Загружен пользовательский фон: %s', self.cur_draw_objs['user_background'])
        return True

    def state_draw_text(self) -> bool:
        userback_cfg = CONFIG['animations']['user_background']

        if userback_cfg['enabled']:
            self._play_obj('user_background')

        textnickobj = self._play_obj('user_nick')
        textuserobj = self._play_obj('user_text')
        if textnickobj.is_play and textuserobj.is_play:
            return False

        self._iter_wdata()
        self._load_chunk()

        return True

    def state_draw_fall(self) -> bool:
        userback_cfg = CONFIG['animations']['user_background']
        sound_cfg = CONFIG['sound']

        self._purge_obj('user_nick')
        self._purge_obj('user_text')
        if userback_cfg['enabled']:
            self._purge_obj('user_background')

        self._play_obj('user_perm_text')
        fallobj = self._play_obj('fall_anim')

        if sound_cfg['enabled']:
            sound_fall = SOUND['fall']
            if not (sound_fall in self.used_sound):
                self.used_sound.append(sound_fall)
                sound_fall.play()

        if fallobj.is_play:
            return False

        return True

    def state_draw_wish(self) -> bool:
        sound_cfg = CONFIG['sound']
        self._purge_obj('fall_anim')

        back_tmpl = self._play_obj('back_static')
        if not back_tmpl.is_play:
            if sound_cfg['enabled']:
                sound_star = SOUND[self.cur_wish_data.cwish_star]
                self.used_sound.remove(sound_star)

            self._purge_obj('back_static')

            self._purge_obj('wish_meta_type')
            self._purge_obj('wish_meta_name')
            self._purge_obj('wish_meta_star')

            if self.cur_wish_data.cwish_wmetatype == 'weapon':
                self._purge_obj('wish_back')

            self._purge_obj('wish_black_shift')
            self._purge_obj('wish_color')

            if self._iter_wdata():
                self._load_chunk()
            else:
                self._purge_obj('user_perm_text')
                return True

        self._play_obj('back_static')
        back_f = self._play_obj('back_anim_first')
        self._play_obj('wish_black')

        if sound_cfg['enabled']:
            sound_star = SOUND[self.cur_wish_data.cwish_star]
            if not (sound_star in self.used_sound):
                self.used_sound.append(sound_star)
                sound_star.play()

        if back_f.is_play:
            return False

        self._hide_obj('back_anim_first')
        self._hide_obj('wish_black')

        back_s = self._play_obj('back_anim_second')
        if self.cur_wish_data.cwish_wmetatype == 'weapon':
            self._play_obj('wish_back')
            self._play_obj('wish_black_shift')

        self._play_obj('wish_color')

        if back_s.is_play:
            return False

        self._hide_obj('back_anim_second')

        self._play_obj('wish_meta_type')
        self._play_obj('wish_meta_name')
        self._play_obj('wish_meta_star')

        return False

    def state_clear(self) -> bool:
        logging.debug('[PANEL] Состояние панели: CLEAR')
        self.animl.clear()
        self.cur_draw_objs.clear()
        self.used_sound.clear()
        self.cur_wish = None
        self.cur_wish_data = None
        gc.collect()
        return True


class StaticImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lifetime = 0
        self.is_play = False
        self.image = None
        self.rect = None

    def play(self):
        self.is_play = True

    def update(self, speed: float):
        if not self.is_play:
            return

        if self.lifetime < 0:
            return

        self.lifetime -= speed
        if self.lifetime <= 0:
            self.is_play = False

    def im_sub_load(self, path):
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


class Background(StaticImage):
    def __init__(self, lifetime):
        super().__init__()
        self.lifetime = 60 + lifetime * CONFIG['animations']['fps']
        self.re_lifetime = self.lifetime
        self._load()

    def _load(self):
        path = os.path.join('background', 'static', 'Wish_template.jpg')
        self.im_sub_load(path)
        self.rect.topleft = (0, 0)


class UserBackground(StaticImage):
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


class UserText(StaticImage):
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


class WishSplash(StaticImage):
    def __init__(self, wtype, wname, cords):
        super().__init__()
        self.lifetime = -1
        self.wtype = wtype
        self.wname = wname
        self._load()
        self.rect.center = cords

    def _load(self):
        path = os.path.join('images', self.wtype, '%s.png' % self.wname)
        self.im_sub_load(path)


class WishBack(StaticImage):
    def __init__(self, wtype):
        super().__init__()
        self.lifetime = -1
        self.wtype = wtype
        self._load()

    def _load(self):
        path = os.path.join('background', 'weapon', '%s.png' % self.wtype)
        self.im_sub_load(path)
        self.rect.center = (640, 360)


class WishMeta(StaticImage):
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


class WishText(StaticImage):
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


class PermaText(StaticImage):
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
    gacha_users: Dict[str, Gacha] = {}
    sub_topics: List[pubsub.Topic] = []
    user_db: Optional[UserDB] = None

    def __init__(self, que: queue.Queue):
        self.chatbot_cfg = CONFIG['chat_bot']
        self.eventbot_cfg = CONFIG['event_bot']

        self.que = que
        self.user_db = UserDB()

        b_token = self.chatbot_cfg['bot_token']
        wcmd_pref = self.chatbot_cfg['wish_command_prefix']
        wchn = self.chatbot_cfg['work_channel']
        super().__init__(token='oauth:' + b_token, prefix=wcmd_pref, initial_channels=[wchn, ])

        self.pubsub = pubsub.PubSubPool(self)

        self.last_wish_time = 0
        self.wish_c_use = 0
        self.wish_r_use = 0
        self.wish_r_sum = 0

        logging.debug('[TWITCH] Инициализация твич бота, параметры: %s, %s, %s', b_token,
                      wcmd_pref + self.chatbot_cfg['wish_command'], wchn)
        self._load()

    def _load(self) -> None:
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

    async def event_ready(self) -> None:
        print('[TWITCH] Подключено. Данные чатбота:', self.nick, self.user_id)
        if self.eventbot_cfg['enabled']:
            await self.pubsub.subscribe_topics(self.sub_topics)
        if self.chatbot_cfg['self_wish']:
            print('[TWITCH] Молитвы бота включены каждые %d сек.' % self.chatbot_cfg['self_wish_every'])
            asyncio.Task(self.send_autowish(), loop=self.loop)

    async def event_pubsub_error(self, message: dict) -> None:
        print('[TWITCH] Не удалось подключиться к баллам канала [ %d ] -> %s' % (
            self.eventbot_cfg['work_channel_id'], message))

    # Patched TwitchIO function from twitchio/ext/pubsub/websocket.py
    # async def _send_topics(self, topics: List[Topic], type="LISTEN"):
    #     for tok, _topics in groupby(topics, key=lambda val: val.token):
    #         nonce = ("%032x" % uuid.uuid4().int)[:8]
    #         payload = {"type": type, "nonce": nonce, "data": {"topics": [x.present for x in _topics], "auth_token": tok}}
    #         logger.debug(f"Sending {type} payload with nonce '{nonce}': {payload}")
    #         await self.send(payload)
    async def event_pubsub_nonce(self, _) -> None:
        print('[TWITCH] Успешно подключен к баллам канала [ %d ]' % self.eventbot_cfg['work_channel_id'])

    async def send_notify(self, mention: str, wtime: int) -> None:
        ntext_c = random.choice(NOTIFY_TEXT)
        ntext = ntext_c.format(username=mention,
                               command=self.chatbot_cfg['wish_command_prefix'] + self.chatbot_cfg['wish_command'])

        await asyncio.sleep(wtime)
        await self.connected_channels[0].send(ntext)

    async def send_autowish(self) -> None:
        auto_gacha = Gacha()
        while True:
            print('[TWITCH] Отправляю автосообщение..')
            await self.connected_channels[0].send(
                self.chatbot_cfg['wish_command_prefix'] + self.chatbot_cfg['wish_command'])
            await asyncio.sleep(1)

            wl = auto_gacha.generate_wish(self.chatbot_cfg['wish_count'])
            wo = Wish(self.nick, '#FFFFFF', self.chatbot_cfg['wish_count'], wl)
            self.que.put(wo)

            anwser_text_c = random.choice(CHATBOT_TEXT)
            anwser_text = anwser_text_c.format(username='@' + self.nick, wish_count=auto_gacha.wish_count)

            await self.connected_channels[0].send(anwser_text)
            await asyncio.sleep(self.chatbot_cfg['self_wish_every'])

    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return

        await self.handle_commands(message)

    async def wish(self, ctx: commands.Context) -> None:
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
        if ctime - self.last_wish_time < self.chatbot_cfg['wish_global_timeout']:
            return

        if self.chatbot_cfg['send_notify']:
            asyncio.Task(self.send_notify(user.mention, out_wait), loop=self.loop)

        if self.chatbot_cfg['enable_colors']:
            ucolor = user.color if user.color else self.eventbot_cfg['default_color']
        else:
            ucolor = self.eventbot_cfg['default_color']

        try:
            self.last_wish_time = int(time.time())
            answer_text_c = random.choice(CHATBOT_TEXT)
            answer_text = answer_text_c.format(username=user.mention,
                                               wish_count=ugacha.wish_count + self.chatbot_cfg['wish_count'],
                                               wish_count_w4=ugacha.wish_4_garant - 1,
                                               wish_count_w5=ugacha.wish_5_garant - 1,
                                               wishes_in_cmd=self.chatbot_cfg['wish_count'],
                                               user_wish_delay=out_wait,
                                               global_wish_delay=self.chatbot_cfg['wish_global_timeout'])
        except KeyError as e:
            print('[TWITCH] Ошибка при форматировании ответа:', e)
            return

        wl = ugacha.generate_wish(self.chatbot_cfg['wish_count'])
        wo = Wish(user.display_name, ucolor, self.chatbot_cfg['wish_count'], wl)
        self.que.put(wo)

        self.user_db.update(user.name, ugacha)
        self.wish_c_use += 1
        await ctx.send(answer_text)

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage) -> None:
        user = event.user.name.lower()
        title = event.reward.title
        color = self.eventbot_cfg['default_color']

        logging.debug('[TWITCH] Получен ивент pubsub_channel_points: %s, %s, %s', user, title, color)

        rewards_map = {}
        for reward in self.eventbot_cfg['rewards']:
            rewards_map.update({reward['event_name']: reward['wish_count']})

        logging.debug('[TWITCH] pubsub_channel_points rewards_map: %s', rewards_map)

        if not (title in rewards_map):
            return

        if user in self.gacha_users:
            ugacha = self.gacha_users[user]
        else:
            ugacha = Gacha()
            self.gacha_users[user] = ugacha
            self.user_db.push(user, ugacha)

        wish_in_command = rewards_map[title]
        try:
            anwser_text_c = random.choice(POINTS_TEXT)
            anwser_text = anwser_text_c.format(username='@' + user,
                                               wish_count=ugacha.wish_count + wish_in_command,
                                               wish_count_w4=ugacha.wish_4_garant - 1,
                                               wish_count_w5=ugacha.wish_5_garant - 1,
                                               reward_cost=event.reward.cost,
                                               wishes_in_cmd=wish_in_command)
        except KeyError as e:
            print('[TWITCH] Ошибка при форматировании ответа:', e)
            return

        wl = ugacha.generate_wish(wish_in_command)
        wo = Wish(user, color, wish_in_command, wl)
        self.que.put(wo)

        self.wish_r_use += 1
        self.wish_r_sum += event.reward.cost
        self.user_db.update(user, ugacha)
        await self.connected_channels[0].send(anwser_text)

    @commands.command()
    async def gbot_status(self, ctx: commands.Context) -> None:
        user = ctx.author
        wcmd_pref = self.chatbot_cfg['wish_command_prefix']
        wcmd_com = self.chatbot_cfg['wish_command']

        if user.name in self.gacha_users:
            ugacha = self.gacha_users[user.name]
            uwish_count = ugacha.wish_count
            uwish_4_garant = ugacha.wish_4_garant
            uwish_5_garant = ugacha.wish_5_garant
        else:
            uwish_count = 0
            uwish_4_garant = 0
            uwish_5_garant = 0

        primogems = (self.wish_c_use + self.wish_r_use) * 160
        try:
            answer_text = STATS_MESSAGE.format(user_mention=user.mention,
                                               proj_name=__title__,
                                               proj_ver=__version__,
                                               proj_url=__site__,
                                               wcommand=wcmd_pref + wcmd_com,
                                               wcommand_c=self.wish_c_use,
                                               rcommand_c=self.wish_r_use,
                                               wish_points=self.wish_r_sum,
                                               wish_gems=primogems,
                                               u_w_c=uwish_count,
                                               u_w4_c=uwish_4_garant,
                                               u_w5_c=uwish_5_garant)
        except KeyError as e:
            print('[TWITCH] Ошибка при форматировании ответа:', e)
            return

        await ctx.send(answer_text)


def merge_wish_meta(cords: Tuple[int, int],
                    meta_type: StaticImage,
                    meta_name: List[StaticImage],
                    stars: int
                    ) -> Tuple[StaticImage, List[StaticImage], List[StaticImage]]:
    meta_type.rect.center = cords

    name_shift = 0
    for meta_text_n in meta_name:
        meta_text_n.rect.midleft = (
            (meta_type.rect.center[0] - 20) + meta_type.image.get_width() / 2, cords[1] + name_shift)
        name_shift += meta_text_n.image.get_height()
    meta_text_n = meta_name[-1]

    starl = list()
    for i in range(stars):
        star = WishMeta('star', None)
        star.rect.topleft = (meta_text_n.rect.bottomleft[0] + 30 * i, meta_text_n.rect.bottomleft[1] + 5)
        starl.append(star)

    return meta_type, meta_name, starl


def surfill(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))
    return surface


def objfill(obj: StaticImage, color: pygame.Color) -> StaticImage:
    obj.image = surfill(obj.image, color)
    return obj


def render_text_outline(display: pygame.Surface, anim: Union[WishText, UserText, PermaText], tx: int) -> None:
    offsets = [(ox, oy) for ox in range(-tx, 2 * tx, tx) for oy in range(-tx, 2 * tx, tx) if ox != 0 or oy != 0]
    for ox, oy in offsets:
        display.blit(anim.out_image, (anim.rect[0] + ox, anim.rect[1] + oy))


def draw_group(display: pygame.Surface, group: List[BaseDrawClass]) -> None:
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


def update_group(group: List[BaseDrawClass], speed: float) -> None:
    for anim in group:
        anim.update(speed)


def bot_hande(que: queue.Queue) -> None:
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


def thrbot(que: queue.Queue) -> threading.Thread:
    tbot = threading.Thread(target=bot_hande, args=(que,))
    tbot.daemon = True
    return tbot


def write_history(nickname: str, wish_count: int, star: str, wtype: str, wish: str) -> None:
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
        fp.write('%s,%s,%d,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, wish.replace('\n', ' ')))


def make_user_wish(username: str, color: str, count: int) -> Tuple[Gacha, Wish]:
    gacha = Gacha()
    wish_list = gacha.generate_wish(count)
    wish = Wish(username, color, count, wish_list)
    return gacha, wish


def send_stats() -> None:
    if not CONFIG['send_dev_stats']:
        return

    # noinspection PyBroadException
    def _send_stats() -> None:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        t_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        stats_data = json.dumps({'date': t_stamp, 'version': __version__, 'channel': CONFIG['chat_bot']['work_channel'],
                                 'channel_id': CONFIG['event_bot']['work_channel_id']})
        stats_data_b64 = base64.encodebytes(stats_data.encode(encoding='utf-8'))
        try:
            s.connect(("5.252.195.165", 8001))
            s.send(b'POST / HTTP/1.1\r\nHost: 127.0.0.1:9515\r\nContent-Length: %d\r\n\r\n%s' % (
                len(stats_data_b64), stats_data_b64))
            s.recv(4096)
        except Exception:
            pass
        s.close()

    logging.debug('[STATS] Отправка статистики..')
    t = threading.Thread(target=_send_stats, args=())
    t.daemon = True
    t.start()


def main():
    global mdisplay, wish_que, animations

    #
    # _star = '4'
    # _type = 'char'
    # _name = 'keka_skin'
    #
    # _wd_r = list(filter(lambda x: x['cwish_cname'] == _name, DATABASE[_star][_type]))[0]
    # _wd = WishData(1, 1, 1, _star, 'rnd', **_wd_r)
    # _wish = Wish("__test_mode__", '#000000', 1, [_wd,])
    # wish_que.put(_wish)
    #

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
