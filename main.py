import os
import sys

import gc
import cv2
import time
import queue
import base64
import random

from itertools import cycle
from dataclasses import dataclass

import asyncio
import aiohttp

import requests
import threading

import json
import jsonschema

from data import DATABASE
from data import CONFIG_SCHEMA, AUTH_SCHEMA, MESSAGES_SCHEMA
from data import HTML_HISTORY_TEMPLATE_HEADER, HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STATS, HTML_HISTORY_TEMPLATE_HEAD_TABLE_STATS_PRE
from data import HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STARS, HTML_HISTORY_TEMPLATE_HEAD_TABLE_END, HTML_HISTORY_TEMPLATE_MAIN_TABLE_ROW
from data import HTML_HISTORY_TEMPLATE_END

import network
from network import do_background_work, interactive_auth

import twitchio
from twitchio import http as twio_http
from twitchio.ext import pubsub
from twitchio.ext import commands

import pickle
import sqlite3

import logging

__title__ = 'genshin-twitch-wish'
__site__ = 'github.com/dzmuh97/genshin-twitch-wish'
__version__ = '2.1.0'

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Union, Tuple, List, Dict, Optional

DbUserTuple = Tuple[str, int, int, int]
BaseDrawClass = Union['StaticImage', 'AnimatedVideo']
DrawDataChunk = Union[BaseDrawClass, List[BaseDrawClass]]
DrawData = Dict[str, DrawDataChunk]

os.chdir(os.path.dirname(sys.argv[0]))
if not os.path.exists('logs'):
    os.makedirs('logs')

_time_stamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    filename=os.path.join('logs', '%s.log' % _time_stamp),
                    filemode='w',
                    encoding='utf-8',
                    level=logging.DEBUG)


def _err_logger(msg: str) -> None:
    message_strip = msg.strip()
    if (message_strip != '\n') and (len(message_strip) > 0):
        logging.error(message_strip)


def _config_check(json_file: str, schema: Dict) -> Dict:
    try:
        config = json.loads(open(json_file, 'r', encoding='utf-8').read())
    except (json.JSONDecodeError, ValueError) as json_error:
        print('[MAIN] Ошибка при загрузке файла конфигурации (%s) : %s' % (json_file, json_error))
        sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

    try:
        jsonschema.validate(config, schema=schema)
    except jsonschema.ValidationError as json_error:
        print('[MAIN] Ошибка при проверке файла конфигурации (%s) : %s' % (json_file, json_error))
        sys.exit(input('Нажмите любую кнопку чтобы выйти > '))

    return config


logging.write = _err_logger

_messages = _config_check('messages.json', MESSAGES_SCHEMA)
USER_SPLASH_TEXT = _messages['user_splash_text']
CHATBOT_TEXT = _messages['chatbot_text']
NOTIFY_TEXT = _messages['notify_text']
POINTS_TEXT = _messages['chanel_points_text']
STATS_MESSAGE = _messages['stats_message']

CONFIG = _config_check('config.json', CONFIG_SCHEMA)
_test_mode = CONFIG['test_mode']
if not _test_mode:
    interactive_auth()
    if not os.path.exists('auth.json'):
        sys.exit()
    _auth_config = _config_check('auth.json', AUTH_SCHEMA)
else:
    _auth_config = {'chat_bot': {}, 'event_bot': {}}

AUTH_CHAT_BOT = _auth_config['chat_bot']
AUTH_EVENT_BOT = _auth_config['event_bot']

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


@dataclass
class WishData:
    wish_count: int
    wish_4_garant: int
    wish_5_garant: int
    wish_star: str
    wish_star_type: str
    wish_type: str
    wish_meta_type: str
    wish_meta_element: str
    wish_obj_name: str
    wish_obj_text: str


@dataclass
class Wish:
    username: str
    user_color: str
    wish_data_count: int
    wish_data_list: List[WishData]


class Gacha:
    def __init__(self, wish_count: int = 0, wish_4_garant: int = 1, wish_5_garant: int = 1):
        self.wish_5_garant = wish_5_garant
        self.wish_4_garant = wish_4_garant
        self.wish_count = wish_count
        self.last_wish_time = 0
        self.wish_count = 0
        logging.debug('[GACHA] Создана гача с параметрами w%d w4%d w4%d', wish_count, wish_4_garant, wish_5_garant)

    @staticmethod
    def _random_tap(x: float) -> bool:
        return random.choice(range(10000)) <= int(x * 100)

    def __roll(self) -> Tuple[str, str]:
        self.wish_count += 1

        wish_garant_starts = CONFIG['wish_fi_soft_a']
        wish_5_garant = CONFIG['wish_fi_garant']
        wish_5_chance = CONFIG['wish_fi_chance']
        wish_4_garant = CONFIG['wish_fo_garant']
        wish_4_chance = CONFIG['wish_fo_chance']

        if (self.wish_5_garant > wish_garant_starts) and (self.wish_5_garant < wish_5_garant):
            _soft_i = (self.wish_5_garant - wish_garant_starts) / (wish_5_garant - wish_garant_starts)
            _soft_chance = wish_5_chance + _soft_i * 100
            if self._random_tap(_soft_chance):
                self.wish_5_garant = 1
                return '5', 'srnd'
        else:
            if self._random_tap(wish_5_chance):
                self.wish_5_garant = 1
                return '5', 'rnd'

        if self.wish_5_garant % wish_5_garant == 0:
            self.wish_5_garant = 1
            return '5', 'garant'
        else:
            self.wish_5_garant += 1

        if self.wish_4_garant % wish_4_garant == 0:
            self.wish_4_garant = 1
            return '4', 'garant'
        else:
            self.wish_4_garant += 1

        if self._random_tap(wish_4_chance):
            self.wish_4_garant = 1
            return '4', 'rnd'

        return '3', 'rnd'

    def generate_wish(self, count: int) -> List[WishData]:
        self.last_wish_time = int(time.time())

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


class Coordinator:
    def __init__(self, wish_que: queue.Queue, animl: List[BaseDrawClass]):
        self.states_list: List[str] = ['idle', 'init', 'draw_usertext', 'draw_fall', 'draw_wishes', 'clear']
        self.current_wish: Optional[Wish] = None
        self.current_wish_data: Optional[WishData] = None
        self.current_draw_objs: DrawData = {}
        self.current_draw_objs_played: Dict[str, bool] = {}
        self.used_sound: List[pygame.mixer.Sound] = []

        self.sound_cfg = CONFIG['sound']
        self.animation_cfg = CONFIG['animations']

        self.states = cycle(self.states_list)
        self.current_state = next(self.states)

        self.animations_list = animl
        self.wish_que = wish_que

        self.que_processing = True
        logging.debug('[PANEL] Создана новая панель управления анимации')

    def _load_chunk_check(self):
        if self.current_wish_data is None:
            self._iter_wdata()
            self._load_chunk()

    def _iter_wdata(self) -> bool:
        if len(self.current_wish.wish_data_list) > 0:
            self.current_wish_data = self.current_wish.wish_data_list.pop(0)
            return True
        return False

    def _load_chunk(self) -> None:
        if self.current_wish_data is None:
            logging.debug('[PANEL] BUG? Вызван метод _t_load_chunk, но cur_wish_data == None')
            return

        wish_data = self.current_wish_data

        _t = time.time()
        logging.debug('[PANEL] Вызван метод _t_load_chunk с параметрами: %s', wish_data)

        is_multi_star = True if self.current_wish.wish_data_count > 1 else False
        wish_stars = wish_data.wish_star
        wish_type = wish_data.wish_type
        wish_meta_type = wish_data.wish_meta_type
        wish_meta_element = wish_data.wish_meta_element
        wish_name = wish_data.wish_obj_name
        wish_text = wish_data.wish_obj_text

        wish_sign = WishMeta(wish_meta_type, wish_meta_element)
        _wish_meta_text = [WishText(_wname) for _wname in wish_text.split('\n')]
        _wish_meta = merge_wish_meta((80, 450), wish_sign, _wish_meta_text, int(wish_stars))
        wish_meta_type, wish_meta_name, wish_meta_star = _wish_meta

        wish_cords_normal = (640, 360)
        wish_cords_shadow = (645, 375)
        wish_color = WishSplash(wish_type, wish_name, wish_cords_normal)
        wish_black = fill_object(WishSplash(wish_type, wish_name, wish_cords_normal), pygame.Color(0, 0, 0))
        wish_black_shift = fill_object(WishSplash(wish_type, wish_name, wish_cords_shadow), pygame.Color(0, 0, 0))

        background_delay = self.animation_cfg['end_delay_milti' if is_multi_star else 'end_delay'][wish_stars]

        self.current_draw_objs.update(
            {
                'back_static': Background(background_delay),
                'back_anim_first': BackAnimated('first', wish_stars),
                'back_anim_second': BackAnimated('second', wish_stars),
                'wish_color': wish_color,
                'wish_black': wish_black,
                'wish_black_shift': wish_black_shift,
                'wish_back': WishBack(wish_data.wish_meta_element) if wish_data.wish_meta_type == 'weapon' else None,
                'wish_meta_type': wish_meta_type,
                'wish_meta_name': wish_meta_name,
                'wish_meta_star': wish_meta_star
            }
        )

        self.current_draw_objs_played.update(
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
        if not (obj_name in self.current_draw_objs):
            return

        del self.current_draw_objs[obj_name]

    def _hide_obj(self, obj_name: str) -> None:
        if not (obj_name in self.current_draw_objs):
            return

        obj = self.current_draw_objs[obj_name]
        if isinstance(obj, list):
            for objl in obj:
                if objl in self.animations_list:
                    self.animations_list.remove(objl)
        else:
            if obj in self.animations_list:
                self.animations_list.remove(obj)

    def _play_obj(self, obj_name: str) -> DrawDataChunk:
        obj = self.current_draw_objs[obj_name]
        objp = self.current_draw_objs_played

        if objp[obj_name]:
            return obj

        if isinstance(obj, list):
            for obji in obj:
                self.animations_list.append(obji)
                obji.play()
        else:
            self.animations_list.append(obj)
            obj.play()

        objp[obj_name] = True
        return obj

    def update(self) -> None:
        state_config = self.animation_cfg['draw_states']

        current_state_name = 'state_%s' % self.current_state
        state_func = getattr(self, current_state_name)

        state_activated = state_config.get(self.current_state, True)
        if state_activated:
            is_next = state_func()
        else:
            is_next = True

        if is_next:
            self.current_state = next(self.states)

    def state_idle(self) -> bool:
        if not self.que_processing:
            return False

        try:
            wish: Wish = self.wish_que.get(block=False)
        except queue.Empty:
            return False

        logging.debug('[PANEL] Состояние панели: IDLE')

        self.current_wish = wish
        self.wish_que.task_done()

        star_types = {
            'srnd': 'мягкий гарант',
            'garant': 'гарант',
            'rnd': 'рандом',
        }

        for wish_data in wish.wish_data_list:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('[ГАЧА]', '[%s]' % current_time,
                  'Результат для', wish.username,
                  '#%d' % wish_data.wish_count,
                  'w4#%d' % wish_data.wish_4_garant,
                  'w5#%d' % wish_data.wish_5_garant,
                  wish_data.wish_star, '* ->', wish_data.wish_obj_text.replace('\n', ' '),
                  '[%s]' % star_types[wish_data.wish_star_type])

            history_cfg = CONFIG['history_file']
            if history_cfg[wish_data.wish_star]:
                write_history(wish.username, wish_data.wish_count, wish_data.wish_star,
                              star_types[wish_data.wish_star_type], wish_data.wish_obj_text)

        return True

    def state_init(self) -> bool:
        logging.debug('[PANEL] Состояние панели: INIT')
        _t = time.time()

        wish_data = self.current_wish
        is_multi_star = True if self.current_wish.wish_data_count > 1 else False

        if any(x.wish_star == '5' for x in self.current_wish.wish_data_list):
            wish_stars = '5'
        elif any(x.wish_star == '4' for x in self.current_wish.wish_data_list):
            wish_stars = '4'
        else:
            wish_stars = '3'

        user_wishes_in_cmd = len(wish_data.wish_data_list)
        user_wish_count = wish_data.wish_data_list[-1].wish_count
        user_gems_in_cmd = user_wishes_in_cmd * 160

        user_text_raw = random.choice(USER_SPLASH_TEXT)
        user_text = user_text_raw.format(wishes_in_cmd=user_wishes_in_cmd,
                                         wish_count=user_wish_count,
                                         gems_in_cmd=user_gems_in_cmd)

        logging.debug('[PANEL] Анимация падения имеет параметры: wish_stars=%s, multi=%s', wish_stars, is_multi_star)

        self.current_draw_objs = \
            {
                'user_perm_text': FrontText(wish_data.username),
                'user_nick': UserText(wish_data.username, (640, 300), wish_data.user_color),
                'user_text': UserText(user_text, (640, 530)),
                'fall_anim': FallAnimated(wish_stars, is_multi_star)
            }

        self.current_draw_objs_played = \
            {
                'user_perm_text': False,
                'user_nick': False,
                'user_text': False,
                'fall_anim': False,
                'user_background': False
            }

        logging.debug('[PANEL] Начальные данные для анимации загружены за %s с.', time.time() - _t)
        logging.debug('[PANEL] Инициализация анимации с данными: %s', self.current_draw_objs)

        background_cfg = self.animation_cfg['user_background']
        background_enabled = background_cfg['enabled']
        if not background_enabled:
            return True

        if background_cfg['type'] == 'static':
            background_obj = UserBackground(background_cfg['path'])
        else:
            background_obj = UserBackgroundAnim(background_cfg['path'])

        self.current_draw_objs.update(
            {
                'user_background': background_obj
            }
        )

        logging.debug('[PANEL] Загружен пользовательский фон: %s', self.current_draw_objs['user_background'])
        return True

    def state_draw_usertext(self) -> bool:
        userback_cfg = self.animation_cfg['user_background']

        if userback_cfg['enabled']:
            self._play_obj('user_background')

        textnickobj = self._play_obj('user_nick')
        textuserobj = self._play_obj('user_text')
        if textnickobj.is_play and textuserobj.is_play:
            return False

        self._load_chunk_check()
        return True

    def state_draw_fall(self) -> bool:
        userback_cfg = self.animation_cfg['user_background']

        self._load_chunk_check()

        self._purge_obj('user_nick')
        self._purge_obj('user_text')
        if userback_cfg['enabled']:
            self._purge_obj('user_background')

        self._play_obj('user_perm_text')
        fallobj = self._play_obj('fall_anim')

        if self.sound_cfg['enabled']:
            sound_fall = SOUND['fall']
            if not (sound_fall in self.used_sound):
                self.used_sound.append(sound_fall)
                sound_fall.play()

        if fallobj.is_play:
            return False

        return True

    def state_draw_wishes(self) -> bool:
        self._purge_obj('fall_anim')

        self._load_chunk_check()
        self._play_obj('user_perm_text')

        back_tmpl = self._play_obj('back_static')
        if not back_tmpl.is_play:
            if self.sound_cfg['enabled']:
                sound_star = SOUND[self.current_wish_data.wish_star]
                self.used_sound.remove(sound_star)

            self._purge_obj('back_static')

            self._purge_obj('wish_meta_type')
            self._purge_obj('wish_meta_name')
            self._purge_obj('wish_meta_star')

            if self.current_wish_data.wish_meta_type == 'weapon':
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

        if self.sound_cfg['enabled']:
            sound_star = SOUND[self.current_wish_data.wish_star]
            if not (sound_star in self.used_sound):
                self.used_sound.append(sound_star)
                sound_star.play()

        if back_f.is_play:
            return False

        self._hide_obj('back_anim_first')
        self._hide_obj('wish_black')

        back_s = self._play_obj('back_anim_second')
        if self.current_wish_data.wish_meta_type == 'weapon':
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
        self.animations_list.clear()
        self.current_draw_objs.clear()
        self.used_sound.clear()
        self.current_wish = None
        self.current_wish_data = None
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
        animations_cfg = CONFIG['animations']
        self.lifetime = 60 + lifetime * animations_cfg['fps']
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
        animations_cfg = CONFIG['animations']
        self.lifetime = animations_cfg['start_delay'] * animations_cfg['fps']
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
        self.out_image = fill_surface(textobj.copy(), USERTEXT_OUTLINE)

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
        self.out_image = fill_surface(textobj.copy(), USERTEXT_OUTLINE)
        self.rect = self.image.get_rect()


class FrontText(StaticImage):
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
        self.out_image = fill_surface(textobj.copy(), USERTEXT_OUTLINE)
        self.rect = self.image.get_rect()
        self.rect.bottomright = (1270, 710)


class TwitchBot(commands.Bot):
    def __init__(self, wish_que: queue.Queue, coordinator: Coordinator):
        self.gacha_users: Dict[str, Gacha] = {}
        self.sub_topics: List[pubsub.Topic] = []
        self.user_db: Optional[UserDB] = None

        self.chatbot_cfg = CONFIG['chat_bot']
        self.eventbot_cfg = CONFIG['event_bot']

        self.wish_que = wish_que
        self.user_db = UserDB()
        self.coordinator = coordinator

        chat_bot_token = AUTH_CHAT_BOT['bot_token']
        work_channel = AUTH_CHAT_BOT['work_channel']

        command_prefix = self.chatbot_cfg['wish_command_prefix']

        super().__init__(token='oauth:' + chat_bot_token, prefix=command_prefix, initial_channels=[work_channel, ])

        self.chatbot_wish_command = self.chatbot_cfg['wish_command_prefix'] + self.chatbot_cfg['wish_command']
        self.pubsub = pubsub.PubSubPool(self)

        self.last_wish_time = 0
        self.wish_c_use = 0
        self.wish_c_primo = 0
        self.wish_r_use = 0
        self.wish_r_primo = 0
        self.wish_r_sum = 0

        logging.debug('[TWITCH] Инициализация твич бота, параметры: %s, %s, %s', chat_bot_token,
                      command_prefix + self.chatbot_cfg['wish_command'], work_channel)

    def run(self):
        self._load()
        super().run()

    def _load(self) -> None:
        print('[TWITCH] Загружаем данные пользователей..')
        for user_data in self.user_db.get_all():
            username, user_wish_count, user_wish_4garant, user_wish_5garant = user_data
            user_gacha = Gacha(user_wish_count, user_wish_4garant, user_wish_5garant)
            self.gacha_users.update({username: user_gacha})
        print('[TWITCH] Данные загружены. Всего пользователей в базе:', len(self.gacha_users))

        if self.chatbot_cfg['enabled']:
            chat_wish_command = self.chatbot_cfg['wish_command']
            command_function = commands.Command(chat_wish_command, self.wish)
            self.add_command(command_function)
            print('[TWITCH] Чат бот включен, команда:', chat_wish_command)

        if self.eventbot_cfg['enabled']:
            event_token = AUTH_EVENT_BOT['channel_token']
            event_channel = AUTH_EVENT_BOT['work_channel_id']
            pubsub_topic = pubsub.channel_points(event_token)[event_channel]
            self.sub_topics.append(pubsub_topic)
            print('[TWITCH] Баллы канала включены, активировано наград:', len(self.eventbot_cfg['rewards']))

        if self.chatbot_cfg['enabled']:
            print('[TWITCH] Подключаемся к чату на канал %s..' % AUTH_CHAT_BOT['work_channel'])
        if self.eventbot_cfg['enabled']:
            print('[TWITCH] Подключаемся к баллам канала %d..' % AUTH_EVENT_BOT['work_channel_id'])

    async def event_ready(self) -> None:
        print('[TWITCH] Подключено. Данные чатбота:', self.nick, self.user_id)
        if self.eventbot_cfg['enabled']:
            await self.pubsub.subscribe_topics(self.sub_topics)
        if self.chatbot_cfg['self_wish']:
            print('[TWITCH] Молитвы бота включены каждые %d сек.' % self.chatbot_cfg['self_wish_every'])
            asyncio.Task(self.send_autowish(), loop=self.loop)

    @staticmethod
    async def event_pubsub_error(message: dict) -> None:
        print('[TWITCH] Не удалось подключиться к баллам канала [ %d ] -> %s' % (AUTH_EVENT_BOT['work_channel_id'], message))

    @staticmethod
    async def event_pubsub_nonce(_) -> None:
        print('[TWITCH] Успешно подключен к баллам канала [ %d ]' % AUTH_EVENT_BOT['work_channel_id'])

    async def send_notify(self, mention: str, wtime: int) -> None:
        notify_text_raw = random.choice(NOTIFY_TEXT)
        try:
            notify_text = notify_text_raw.format(username=mention, command=self.chatbot_wish_command)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        await asyncio.sleep(wtime)
        await self.connected_channels[0].send(notify_text)

    async def send_autowish(self) -> None:
        auto_gacha = Gacha()
        while True:
            print('[TWITCH] Отправляю автосообщение..')
            await self.connected_channels[0].send(self.chatbot_wish_command)
            await asyncio.sleep(1)

            wish_count = self.chatbot_cfg['wish_count']
            wish_data_list = auto_gacha.generate_wish(wish_count)
            wish = Wish(self.nick, '#FFFFFF', wish_count, wish_data_list)
            self.wish_que.put(wish)

            anwser_text_raw = random.choice(CHATBOT_TEXT)
            anwser_text = anwser_text_raw.format(username='@' + self.nick, wish_count=auto_gacha.wish_count)

            await self.connected_channels[0].send(anwser_text)
            await asyncio.sleep(self.chatbot_cfg['self_wish_every'])

    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return

        await self.handle_commands(message)

    async def wish(self, ctx: commands.Context) -> None:
        user = ctx.author
        logging.debug('[TWITCH] Получена команда wish: %s, %s', user.name, user.color)

        if user.name in self.gacha_users:
            user_gacha = self.gacha_users[user.name]
        else:
            user_gacha = Gacha()
            self.gacha_users[user.name] = user_gacha
            self.user_db.push(user.name, user_gacha)

        current_time = int(time.time())
        wtimeoust_cfg = self.chatbot_cfg['wish_timeout']
        if user.is_broadcaster:
            user_timeout = wtimeoust_cfg['broadcaster']
        elif user.is_mod:
            user_timeout = wtimeoust_cfg['mod']
        elif user.is_subscriber:
            user_timeout = wtimeoust_cfg['subscriber']
        else:
            user_timeout = wtimeoust_cfg['user']

        if current_time - user_gacha.last_wish_time < user_timeout:
            return
        if current_time - self.last_wish_time < self.chatbot_cfg['wish_global_timeout']:
            return

        if self.chatbot_cfg['send_notify']:
            asyncio.Task(self.send_notify(user.mention, user_timeout), loop=self.loop)

        if self.chatbot_cfg['enable_colors']:
            ucolor = user.color if user.color else self.eventbot_cfg['default_color']
        else:
            ucolor = self.eventbot_cfg['default_color']

        wishes_in_command = self.chatbot_cfg['wish_count']
        wish_data_list = user_gacha.generate_wish(wishes_in_command)
        wish = Wish(user.name, ucolor, wishes_in_command, wish_data_list)

        try:
            self.last_wish_time = int(time.time())
            answer_text_raw = random.choice(CHATBOT_TEXT)
            answer_text = answer_text_raw.format(username=user.mention,
                                                 wish_count=user_gacha.wish_count,
                                                 wish_count_w4=user_gacha.wish_4_garant - 1,
                                                 wish_count_w5=user_gacha.wish_5_garant - 1,
                                                 wishes_in_cmd=wishes_in_command,
                                                 user_wish_delay=user_timeout,
                                                 global_wish_delay=self.chatbot_cfg['wish_global_timeout'],
                                                 que_num=self.wish_que.qsize() + 1)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        self.wish_que.put(wish)

        self.wish_c_use += 1
        self.wish_c_primo += wishes_in_command * 160

        self.user_db.update(user.name, user_gacha)
        await ctx.send(answer_text)

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage) -> None:
        user = event.user.name.lower()
        reward_title = event.reward.title
        user_color = self.eventbot_cfg['default_color']

        logging.debug('[TWITCH] Получен ивент pubsub_channel_points: %s, %s, %s', user, reward_title, user_color)

        rewards_map = {}
        for reward in self.eventbot_cfg['rewards']:
            rewards_map.update({reward['event_name']: reward['wish_count']})

        logging.debug('[TWITCH] pubsub_channel_points rewards_map: %s', rewards_map)

        if not (reward_title in rewards_map):
            return

        if user in self.gacha_users:
            user_gacha = self.gacha_users[user]
        else:
            user_gacha = Gacha()
            self.gacha_users[user] = user_gacha
            self.user_db.push(user, user_gacha)

        wishes_in_command = rewards_map[reward_title]
        wish_data_list = user_gacha.generate_wish(wishes_in_command)
        wish = Wish(user, user_color, wishes_in_command, wish_data_list)

        try:
            anwser_text_raw = random.choice(POINTS_TEXT)
            anwser_text = anwser_text_raw.format(username='@' + user,
                                                 wish_count=user_gacha.wish_count,
                                                 wish_count_w4=user_gacha.wish_4_garant - 1,
                                                 wish_count_w5=user_gacha.wish_5_garant - 1,
                                                 reward_cost=event.reward.cost,
                                                 wishes_in_cmd=wishes_in_command,
                                                 que_num=self.wish_que.qsize() + 1)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        self.wish_que.put(wish)

        self.wish_r_use += 1
        self.wish_r_sum += event.reward.cost
        self.wish_r_primo += wishes_in_command * 160

        self.user_db.update(user, user_gacha)
        await self.connected_channels[0].send(anwser_text)

    @commands.command()
    async def gbot_status(self, ctx: commands.Context) -> None:
        user = ctx.author

        if user.name in self.gacha_users:
            user_gacha = self.gacha_users[user.name]
            uwish_count = user_gacha.wish_count
            uwish_4_garant = user_gacha.wish_4_garant
            uwish_5_garant = user_gacha.wish_5_garant
        else:
            uwish_count = 0
            uwish_4_garant = 0
            uwish_5_garant = 0

        primogems = self.wish_r_primo + self.wish_c_primo
        try:
            answer_text = STATS_MESSAGE.format(user_mention=user.mention,
                                               proj_name=__title__,
                                               proj_ver=__version__,
                                               proj_url=__site__,
                                               wcommand=self.chatbot_wish_command,
                                               wcommand_c=self.wish_c_use,
                                               rcommand_c=self.wish_r_use,
                                               wish_points=self.wish_r_sum,
                                               wish_gems=primogems,
                                               u_w_c=uwish_count,
                                               u_w4_c=uwish_4_garant,
                                               u_w5_c=uwish_5_garant,
                                               user_primo=uwish_count * 160)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        await ctx.send(answer_text)

    @commands.command()
    async def gbot_sound(self, ctx: commands.Context) -> None:
        global _sound_work
        sound_cfg = CONFIG['sound']

        user = ctx.author
        if user.is_mod or user.is_broadcaster:
            if _sound_work:
                sound_cfg['enabled'] = not sound_cfg['enabled']
                pygame.mixer.stop()

            sound_text = 'включен' if sound_cfg['enabled'] else 'выключен'
            answer_text = '%s звук: %s' % (user.mention, sound_text)

            await ctx.send(answer_text)

    @commands.command()
    async def gbot_pause(self, ctx: commands.Context) -> None:
        user = ctx.author

        if user.is_mod or user.is_broadcaster:
            self.coordinator.que_processing = not self.coordinator.que_processing

            pause_text = 'включена' if self.coordinator.que_processing else 'выключена'
            answer_text = '%s обработка команд: %s' % (user.mention, pause_text)

            await ctx.send(answer_text)

    @commands.command()
    async def gbot_history(self, ctx: commands.Context) -> None:
        user = ctx.author
        code, html_history = render_html_history(user.name)

        errors_map = {
            1: '%s у стримера выключена запись истории молитв :(' % user.mention,
            2: '%s истории молитв еще нет, попробуй позже :(' % user.mention,
            3: '%s тебя еще нет в истории молитв, попробуй позже :(' % user.mention
        }

        if code < 0:
            error_response = errors_map[abs(code)]
            await ctx.send(error_response)
            return

        channel_id = AUTH_EVENT_BOT['work_channel_id']
        html_history_b64 = base64.urlsafe_b64encode(html_history.encode(encoding='utf-8')).decode(encoding='utf-8')
        json_data = {'user_id': user.id, 'channel_id': channel_id, 'html': html_history_b64}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(network.URL_HISTORY, json=json_data) as post_data:
                    response = await post_data.json()
            except aiohttp.ClientError as history_error:
                print('[TWITCH] Ошибка получения файла истории:', history_error)
                error_response = '%s не удалось загрузить историю, попробуй позже :(' % user.mention
                await ctx.send(error_response)
                return

        if not ('url' in response):
            error_response = '%s Не удалось создать ссылку, попробуйте позже :(' % user.mention
            await ctx.send(error_response)
            return

        history_url = response['url']
        response = '%s твоя история молитв: %s' % (user.mention, history_url)
        await ctx.send(response)


def merge_wish_meta(cords: Tuple[int, int],
                    wish_type: StaticImage,
                    wish_name: List[StaticImage],
                    wish_stars: int
                    ) -> Tuple[StaticImage, List[StaticImage], List[StaticImage]]:
    """
    Function to create wish information (type, name and number of stars), combines 3 objects at specified coordinates.
    """
    wish_type.rect.center = cords

    wish_name_offset = 0
    for wish_name_n in wish_name:
        wish_name_n.rect.midleft = (
            (wish_type.rect.center[0] - 20) + wish_type.image.get_width() / 2, cords[1] + wish_name_offset)
        wish_name_offset += wish_name_n.image.get_height()
    wish_name_last = wish_name[-1]

    wish_stars_list = list()
    for i in range(wish_stars):
        star = WishMeta('star', None)
        star.rect.topleft = (wish_name_last.rect.bottomleft[0] + 30 * i, wish_name_last.rect.bottomleft[1] + 5)
        wish_stars_list.append(star)

    return wish_type, wish_name, wish_stars_list


def fill_surface(surf: pygame.Surface, color: pygame.Color) -> pygame.Surface:
    w, h = surf.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surf.get_at((x, y))[3]
            surf.set_at((x, y), pygame.Color(r, g, b, a))
    return surf


def fill_object(obj: StaticImage, color: pygame.Color) -> StaticImage:
    obj.image = fill_surface(obj.image, color)
    return obj


def render_text_outline(display: pygame.Surface, anim: Union[WishText, UserText, FrontText], tx: int) -> None:
    """
    We draw the outlines of the text using a simple method: draw black text with tx offset in 8 directions relative to
    the center of the original text, then draw the original text on top of it.
    """
    offsets = [(ox, oy) for ox in range(-tx, 2 * tx, tx) for oy in range(-tx, 2 * tx, tx) if ox != 0 or oy != 0]
    for ox, oy in offsets:
        display.blit(anim.out_image, (anim.rect[0] + ox, anim.rect[1] + oy))


def draw_group(display: pygame.Surface, animation_group: List[BaseDrawClass]) -> None:
    draw_list = []
    front_text = []
    for animation in animation_group:
        if isinstance(animation, FrontText):
            front_text.append(animation)
        else:
            draw_list.append(animation)

    draw_list += front_text
    for animation in draw_list:
        if isinstance(animation, WishText) or isinstance(animation, UserText) or isinstance(animation, FrontText):
            render_text_outline(display, animation, 1)
        display.blit(animation.image, animation.rect)


def update_group(animation_group: List[BaseDrawClass], speed: float) -> None:
    for animation in animation_group:
        animation.update(speed)


def update_auth() -> None:
    with open('auth.json', 'r', encoding='utf-8') as authf:
        jdata = json.load(authf)

    jdata.update({'chat_bot': AUTH_CHAT_BOT})
    jdata.update({'event_bot': AUTH_EVENT_BOT})

    with open('auth.json', 'w', encoding='utf-8') as authf:
        json.dump(jdata, authf)


def refresh_bot_token(ref_token: str) -> bool:
    try:
        twitch_user_data_raw = requests.post(network.URL_TOKEN_REF, json={'ref_token': ref_token})
        twitch_user_data = twitch_user_data_raw.json()
    except requests.RequestException as gate_error:
        print('[AUTH] Не удалось обновить токен:', gate_error)
        return False

    token_error = twitch_user_data.get('error')
    if not (token_error is None):
        print('[AUTH] Не удалось обновить токен:', token_error)
        return False

    config_chat_bot_token_ref = AUTH_CHAT_BOT['bot_token_ref']
    if config_chat_bot_token_ref == ref_token:
        bot_token_new = twitch_user_data['access_token']
        bot_token_ref_new = twitch_user_data['refresh_token']
        AUTH_CHAT_BOT['bot_token'] = bot_token_new
        AUTH_CHAT_BOT['bot_token_ref'] = bot_token_ref_new

    config_event_bot_ref = AUTH_EVENT_BOT['channel_token_ref']
    if config_event_bot_ref == ref_token:
        channel_token_new = twitch_user_data['access_token']
        channel_token_ref_new = twitch_user_data['refresh_token']
        AUTH_EVENT_BOT['channel_token'] = channel_token_new
        AUTH_EVENT_BOT['channel_token_ref'] = channel_token_ref_new

    update_auth()
    return True


def bot_handle(wish_que: queue.Queue, control: Coordinator) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    time.sleep(3)   # Prevent overload Twitch API

    bot = TwitchBot(wish_que, control)
    twiohttp = twio_http.TwitchHTTP(bot)

    check_tokens = (AUTH_EVENT_BOT['channel_token'], AUTH_CHAT_BOT['bot_token'])
    check_tokens_ref = (AUTH_EVENT_BOT['channel_token_ref'], AUTH_CHAT_BOT['bot_token_ref'])

    print('[TWITCH] Проверяем данные ботов..')
    for token_t in zip(check_tokens, check_tokens_ref):
        current_token, current_token_ref = token_t

        try:
            twiohttp.nick = None  # force get data from twitch
            check_task = loop.create_task(twiohttp.validate(token=current_token))
            loop.run_until_complete(check_task)
        except (twitchio.errors.AuthenticationError, twitchio.errors.HTTPException) as twitch_error:
            print('[TWITCH] Ошибка авторизации:', twitch_error)
            if not refresh_bot_token(current_token_ref):
                threading.Event().wait()
            return

        event_bot_channel_id = AUTH_EVENT_BOT['work_channel_id']
        event_bot_token_ref = AUTH_EVENT_BOT['channel_token_ref']
        if (event_bot_channel_id == 0) and (current_token_ref == event_bot_token_ref):
            AUTH_EVENT_BOT['work_channel_id'] = twiohttp.user_id
            update_auth()

        time.sleep(3)

    bot.run()


def create_bot_thread(wish_que: queue.Queue, control: Coordinator) -> threading.Thread:
    bot_thread = threading.Thread(target=bot_handle, args=(wish_que, control))
    bot_thread.daemon = True
    return bot_thread


def render_html_history(filter_nick: str) -> Tuple[int, str]:
    history_cfg = CONFIG['history_file']
    history_enabled = history_cfg['enabled']
    if not history_enabled:
        return -1, ''

    history_path = history_cfg['path']
    if not os.path.exists(history_path):
        return -2, ''

    style_map = {
        '3': 'star3',
        '4': 'star4',
        '5': 'star5',
    }

    wishes_map = {
        '3': 1,
        '4': 1,
        '5': 1
    }

    total = 0
    total_5 = 0
    total_4 = 0
    total_3 = 0

    html_result = ''
    html_result += HTML_HISTORY_TEMPLATE_HEADER

    html_main_table = ''

    with open(history_path, 'r', encoding='utf-8') as fp:
        for line_num, history_line in enumerate(fp):
            if line_num == 0:  # skip header
                continue

            history_data = history_line.strip().split(',')
            wdate, nickname, _, star, wish_type, wish_name = history_data

            if filter_nick != nickname.lower():
                continue

            wish_style = style_map[star]

            if star == '3':
                total_3 += 1

            if star == '4':
                total_4 += 1

            if star == '5':
                total_5 += 1

            table_row = HTML_HISTORY_TEMPLATE_MAIN_TABLE_ROW.format(
                wish_date=wdate.replace('-', ' '),
                wish_user=nickname,
                wish_count='1' if star == '3' else wishes_map[star],
                wish_type=wish_type,
                wish_style_color=wish_style,
                wish_name=wish_name
            )
            html_main_table += table_row

            for wish_star in wishes_map:
                wishes_map[wish_star] += 1

            wishes_map[star] = 1
            total += 1

    if total == 0:
        return -3, ''

    total_gems = total * 160
    html_result += HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STATS.format(
        total_wish=total,
        total_gems=total_gems
    )
    html_result += HTML_HISTORY_TEMPLATE_HEAD_TABLE_STATS_PRE
    html_result += HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STARS.format(
        total_wish3=total_3,
        total_wish4=total_4,
        total_wish5=total_5
    )
    html_result += HTML_HISTORY_TEMPLATE_HEAD_TABLE_END
    html_result += html_main_table
    html_result += HTML_HISTORY_TEMPLATE_END

    return 0, html_result


def write_history(nickname: str, wish_count: int, star: str, wtype: str, wish: str) -> None:
    test_mode_enabled = CONFIG['test_mode']
    if test_mode_enabled:
        return

    history_cfg = CONFIG['history_file']
    history_enabled = history_cfg['enabled']
    if not history_enabled:
        return

    history_path = history_cfg['path']
    if not os.path.exists(history_path):
        with open(history_path, 'w', encoding='utf-8') as fp:
            fp.write('date,nickname,wish_count,star,type,wish\n')

    history_time = time.localtime()
    wdate = time.strftime("%d.%m.%Y-%H:%M:%S", history_time)
    with open(history_path, 'a', encoding='utf-8') as fp:
        fp.write('%s,%s,%d,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, wish.replace('\n', ' ')))


def make_user_wish(username: str, color: str, count: int) -> Tuple[Gacha, Wish]:
    gacha = Gacha()
    wish_data_list = gacha.generate_wish(count)
    wish = Wish(username, color, count, wish_data_list)
    return gacha, wish


def main():
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

    # code, text = render_html_history('local')
    # print(code)
    # with open('_test.html', 'w', encoding='utf-8') as f:
    #     f.write(text)
    # sys.exit()

    fps = pygame.time.Clock()
    main_display = pygame.display.set_mode(size=(1280, 720), vsync=1)

    wish_que = queue.Queue()
    animation_group = []

    chatbot_cfg = CONFIG['chat_bot']
    eventbot_cfg = CONFIG['event_bot']
    test_mode_enabled = CONFIG['test_mode']
    if test_mode_enabled:
        test_user = os.getlogin()
        chatbot_cfg['enabled'] = eventbot_cfg['enabled'] = False
        _, wish = make_user_wish(test_user, '#FFFFFF', 100)
        wish_que.put(wish)

    twitch_bot_start = False
    twitch_bot_thread = None
    print('[MAIN] Запускаемся..')

    coordinator = Coordinator(wish_que, animation_group)

    if chatbot_cfg['enabled'] or eventbot_cfg['enabled']:
        twitch_bot_thread = create_bot_thread(wish_que, coordinator)
        twitch_bot_thread.start()
        twitch_bot_start = True
        print('[MAIN] Твич бот запущен')
        if CONFIG['send_dev_stats']:
            chat_bot_work_channel = AUTH_CHAT_BOT['work_channel']
            event_bot_work_channel_id = AUTH_EVENT_BOT['work_channel_id']
            do_background_work(chat_bot_work_channel, event_bot_work_channel_id, __version__)
    else:
        print('[MAIN] Твич бот отключен')

    animation_cfg = CONFIG['animations']
    print('[MAIN] FPS установлен в', animation_cfg['fps'])
    while True:
        fps.tick(animation_cfg['fps'])

        if twitch_bot_start and (not twitch_bot_thread.is_alive()):
            twitch_bot_thread.join()
            print('[MAIN] Твич бот умер, перезапускаем..')
            twitch_bot_thread = create_bot_thread(wish_que, coordinator)
            twitch_bot_thread.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        coordinator.update()

        main_display.fill(animation_cfg['chroma_color'])
        draw_group(main_display, animation_group)
        update_group(animation_group, 1.0)

        pygame.display.update()


if __name__ == '__main__':
    sys.stderr = logging
    main()
