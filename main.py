__ascii__ = r'''
   ___             _    _        _____        _ _      _     __      ___    _      ___ _           _      _           
  / __|___ _ _  __| |_ (_)_ _   |_   _|_ __ _(_) |_ __| |_   \ \    / (_)__| |_   / __(_)_ __ _  _| |__ _| |_ ___ _ _ 
 | (_ / -_) ' \(_-< ' \| | ' \    | | \ V  V / |  _/ _| ' \   \ \/\/ /| (_-< ' \  \__ \ | '  \ || | / _` |  _/ _ \ '_|
  \___\___|_||_/__/_||_|_|_||_|   |_|  \_/\_/|_|\__\__|_||_|   \_/\_/ |_/__/_||_| |___/_|_|_|_\_,_|_\__,_|\__\___/_|  
  
 https://github.com/dzmuh97/genshin-twitch-wish
'''

__title__ = 'genshin-twitch-wish'
__site__ = 'github.com/dzmuh97/genshin-twitch-wish'
__version__ = '2.3.0'

print(__ascii__)

import os
import sys

import gc
import cv2
import time
import queue
import base64
import random

from itertools import cycle, zip_longest
from functools import wraps

from dataclasses import dataclass

import asyncio
try:  # https://github.com/aio-libs/aiohttp/issues/4324
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise

        return wrapper

    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
except ImportError:
    _ProactorBasePipeTransport = None

import aiohttp

import threading

import json
import jsonschema

from data import DATABASE as _DATABASE
from data import CONFIG_SCHEMA, AUTH_SCHEMA, MESSAGES_SCHEMA, BANNER_SCHEMA
from data import (
    HTML_HISTORY_TEMPLATE_HEADER,
    HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STATS,
    HTML_HISTORY_TEMPLATE_HEAD_TABLE_STATS_PRE,
    HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STARS,
    HTML_HISTORY_TEMPLATE_HEAD_TABLE_END,
    HTML_HISTORY_TEMPLATE_MAIN_TABLE_ROW,
    HTML_HISTORY_TEMPLATE_END
)

import network
from network import do_background_work, interactive_auth

import twitchio
from twitchio.ext import pubsub
from twitchio.ext import commands

import pickle
import sqlite3

import logging

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Union, Tuple, List, Dict, Optional

DbUserTuple = Tuple[str, int, int, int, bool, bool]
BaseDrawClass = Union['StaticImage', 'AnimatedVideo']
DrawDataChunk = Union[BaseDrawClass, List[BaseDrawClass]]
DrawData = Dict[str, DrawDataChunk]

_script_path = os.path.realpath(sys.argv[0])
_script_dir = os.path.dirname(_script_path)

os.chdir(_script_dir)
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


def _load_database(config: Dict) -> Dict:
    base_name = config['banner_name']

    total = 0
    stats = {
        '5': {
            'char': 0,
            'weapon': 0,
            'garant': 0
        },
        '4': {
            'char': 0,
            'weapon': 0,
            'garant': 0
        },
        '3': {
            'weapon': 0
        }
    }
    data_template = {
        '3': {
            'weapon': []
        },
        '4': {
            'char': [], 'weapon': [], 'garant': []
        },
        '5': {
            'char': [], 'weapon': [], 'garant': []
        }
    }

    items_linear = [(item, star, wtype) for star in _DATABASE for wtype in _DATABASE[star] for item in _DATABASE[star][wtype]]
    print('[MAIN] Загружаю баннер "%s" ..' % base_name, end=' ')

    wishes = config['wishes']
    for ban_star in wishes:
        for ban_wtype in ['char', 'weapon', 'garant']:
            items = wishes[ban_star].get(ban_wtype, [])
            for ban_item in items:

                filtered_data = filter(lambda x: ban_item == _wish_name_normal(x[0]['wish_obj_text']), items_linear)
                try:
                    item_data = next(filtered_data)
                except StopIteration:
                    print('ошибка загрузки баннера: %s*%s:%s не найден' % (ban_star, ban_wtype, ban_item))
                    sys.exit(input())

                db_item, db_star, db_wtype = item_data

                if ban_wtype in ['char', 'weapon']:
                    if ban_star != db_star or ban_wtype != db_wtype:
                        _text_params = (ban_star, ban_wtype, ban_item, db_star, db_wtype, db_item['wish_obj_text'])
                        print('ошибка загрузки баннера: %s*%s:%s <> %s*%s:%s' % _text_params)
                        sys.exit(input())
                    total += 1

                data_template[ban_star][ban_wtype].append(db_item)
                stats[ban_star][ban_wtype] += 1

    if total == 0:
        print('ошибка загрузки баннера: ни одного предмета не загружено')
        sys.exit(input())

    stat_text = '(%d) | 5*: %d/%d[%d]; 4*: %d/%d[%d]; 3*: 0/%d' % (
        total,
        stats['5']['char'],
        stats['5']['weapon'],
        stats['5']['garant'],
        stats['4']['char'],
        stats['4']['weapon'],
        stats['4']['garant'],
        stats['3']['weapon']
    )
    print(stat_text)
    return data_template


def _wish_name_normal(name: str) -> str:
    return name.replace('\n', ' ')


def _wish_garant_type(gtype: str) -> str:
    star_types = {
        'srnd': 'мягкий гарант',
        'garant': 'рандом гарант',
        'event_garant': 'гарант',
        'rnd': 'рандом',
        '50/50': '50/50'
    }

    return star_types[gtype]


logging.write = _err_logger

_messages = _config_check('messages.json', MESSAGES_SCHEMA)
USER_SPLASH_TEXT = _messages['user_splash_text']
CHATBOT_TEXT = _messages['chatbot_text']
NOTIFY_TEXT = _messages['notify_text']
POINTS_TEXT = _messages['chanel_points_text']
STATS_MESSAGE = _messages['stats_message']
STATUS_MESSAGE = _messages['status_message']

CONFIG = _config_check('config.json', CONFIG_SCHEMA)
_test_mode = CONFIG['test_mode']
if not _test_mode:
    interactive_auth()
    if not os.path.exists('auth.json'):
        sys.exit()
    _auth_config = _config_check('auth.json', AUTH_SCHEMA)
else:
    _auth_config = {'chat_bot': {}, 'event_bot': {}}

BANNER_CONFIG = _config_check(os.path.join('banners', CONFIG['banner']) + '.json', BANNER_SCHEMA)
DATABASE = _load_database(BANNER_CONFIG)

AUTH_CHAT_BOT = _auth_config['chat_bot']
AUTH_EVENT_BOT = _auth_config['event_bot']

SOUND_CFG = CONFIG['sound']

USERTEXT_COLOR = pygame.Color(255, 255, 255, 0)
USERTEXT_OUTLINE = pygame.Color(0, 0, 0, 0)
WISH_BLACK_COLOR = pygame.Color(0, 0, 0)

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
    win_4_garant: int
    win_5_garant: int
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
    def __init__(self,
                 wish_count: int = 0,
                 wish_4_garant: int = 1,
                 wish_5_garant: int = 1,

                 win_5: bool = False,
                 win_4: bool = False
                 ):
        self.wish_5_garant = wish_5_garant
        self.wish_4_garant = wish_4_garant
        self.wish_count = wish_count
        self.last_wish_time = 0

        self.win_garant_table = {'5': win_5, '4': win_4}
        self._rollback = [0, 0, 0]

        logging.debug('[GACHA] Создана гача с параметрами w:%d g4:%d g5:%d w4:%d w5:%d', wish_count, wish_4_garant, wish_5_garant, win_4, win_5)

    @staticmethod
    def _random_tap(chance_percent: float) -> bool:
        return random.choice(range(10000)) <= int(chance_percent * 100)

    def __flip_garant(self, star: str, val: bool) -> None:
        self.win_garant_table[star] = val

    def __rollback(self) -> None:
        self.wish_count, self.wish_4_garant, self.wish_5_garant = self._rollback

    def __roll(self) -> Tuple[str, str]:
        self._rollback = [self.wish_count, self.wish_4_garant, self.wish_5_garant]
        self.wish_count += 1

        wish_garant_starts = BANNER_CONFIG['wish_fi_soft_a']
        wish_5_garant = BANNER_CONFIG['wish_fi_garant']
        wish_5_chance = BANNER_CONFIG['wish_fi_chance']
        wish_4_garant = BANNER_CONFIG['wish_fo_garant']
        wish_4_chance = BANNER_CONFIG['wish_fo_chance']

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
        roll_i = 0
        while roll_i < count:
            star, star_type = self.__roll()
            if star == '3':
                wtype = 'weapon'
            else:
                wtype = random.choice(['weapon', 'char'])

            if len(DATABASE[star][wtype]) == 0:
                self.__rollback()
                continue

            data = random.choice(DATABASE[star][wtype])
            garant_datas = DATABASE[star].get('garant', [])
            if (len(garant_datas) > 0) and (star in ['4', '5']):
                _win = self.win_garant_table[star]
                _tap = self._random_tap(50)
                if _win or _tap:
                    data = random.choice(garant_datas)
                    self.__flip_garant(star, False)
                    if _win:
                        star_type = 'event_garant'
                    else:
                        star_type = '50/50'
                else:
                    self.__flip_garant(star, True)

            logging.debug('[GACHA] Результат крутки: %s %s %s', star, star_type, data)

            win_4, win_5 = self.win_garant_table['4'], self.win_garant_table['5']
            gacha_obj = WishData(self.wish_count, self.wish_4_garant, self.wish_5_garant, win_4, win_5, star, star_type, **data)
            rolls.append(gacha_obj)
            roll_i += 1

        return rolls


class UserDB:
    database = 'database.sqlite'
    database_old = 'database.sql'
    old_to_new = ['win_4', 'win_5']

    def __init__(self):
        self.conn = sqlite3.connect(self.database)
        logging.debug('[DB] Создано новое подключение к базе данных')
        if not self._check_table():
            logging.debug('[DB] Таблицы пользователей не существует, создаем..')
            self._create_table()
        for new_column in self.old_to_new:
            if not self._check_column(new_column):
                logging.debug('[DB] Версия базы данных устарела, обновляем таблицу: %s', new_column)
                self._create_column(new_column)
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
            setattr(gacha, 'win_garant_table', {'5': 0, '4': 0})

            check = self.get(user)
            if check:
                self.update(user, gacha)
                continue

            self.push(user, gacha)
            i_users += 1

        print('[DB] Импортировано пользователей:', i_users)
        os.remove(self.database_old)
        print('[DB] Старая база данных удалена!', )

    def _create_column(self, column: str) -> None:
        cur = self.conn.cursor()
        payload = "ALTER TABLE users ADD COLUMN %s INTEGER DEFAULT 0;" % column
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def _check_column(self, column: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM pragma_table_info('users') WHERE name=?;", (column,))
        ret = cur.fetchone()
        cur.close()

        if ret is None:
            return False

        return True

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
        payload = "CREATE TABLE users (username TEXT PRIMARY KEY, wish_count INTEGER, wish_4_garant INTEGER, wish_5_garant INTEGER, win_4 INTEGER, win_5 INTEGER);"
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def get_all(self) -> List[DbUserTuple]:
        logging.debug('[DB] Вызван метод get_all')
        cur = self.conn.cursor()
        payload = "SELECT * FROM users;"
        cur.execute(payload)
        data = cur.fetchall()
        cur.close()

        return data

    def get(self, username) -> Optional[DbUserTuple]:
        logging.debug('[DB] Вызван метод get с параметрами %s', username)
        cur = self.conn.cursor()
        payload = "SELECT * FROM users WHERE username=?;"
        cur.execute(payload, (username,))
        data = cur.fetchone()
        cur.close()

        return data

    def push(self, username: str, gacha: Gacha) -> None:
        logging.debug('[DB] Вызван метод push с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?);"
        win_4, win_5 = gacha.win_garant_table['4'], gacha.win_garant_table['5']
        cur.execute(payload, (username, gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, win_4, win_5))
        self.conn.commit()
        cur.close()

    def update(self, username: str, gacha: Gacha) -> None:
        logging.debug('[DB] Вызван метод update с параметрами %s, %s', username, gacha)
        cur = self.conn.cursor()
        payload = "UPDATE users SET wish_count=?, wish_4_garant=?, wish_5_garant=?, win_4=?, win_5=? WHERE username=?;"
        win_4, win_5 = gacha.win_garant_table['4'], gacha.win_garant_table['5']
        cur.execute(payload, (gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, win_4, win_5, username))
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

        wish_meta_cords = (100, 450)
        wish_meta_cords_shift = (40, 450)

        wish_meta_kwargs = {
            'apply_trans': True,
            'trans_perc': 0,
            'trans_coef': 15,
            'apply_shift': True,
            'shift_cords': wish_meta_cords_shift,
            'shift_type': 'midleft',
            'shift_speed': -7,
            'shift_speed_coef': 0.3
        }

        wish_sign = WishMeta(wish_meta_type, wish_meta_element)
        _wish_meta_text = [_wname for _wname in wish_text.split('\n')]
        wish_meta = merge_wish_meta(wish_meta_cords, wish_meta_kwargs, wish_sign, _wish_meta_text, int(wish_stars))

        wish_args = (wish_type, wish_name)

        wish_shift_x_offset = 40
        wish_shadow_x_offset = 5
        wish_shadow_y_offset = 15

        _x, _y = 640, 360
        _x_s, _y_s = _x + wish_shadow_x_offset, _y + wish_shadow_y_offset

        wish_cords_normal = (_x, _y)
        wish_cords_normal_shift = (_x + wish_shift_x_offset, _y)

        wish_cords_shadow = (_x_s, _y_s)
        wish_cords_shadow_shift = (_x_s + wish_shift_x_offset, _y_s)

        wish_pack_shift_speed = 7
        wish_pack_shift_speed_coef = 0.7

        wish_black_kwargs = {
            'apply_res': True,
            'res_perc': 1000,
            'res_coef': 100,
            'res_speed': 3,
            'apply_black': True
        }

        wish_back_kwargs = {
            'apply_trans': True,
            'trans_perc': -30,
            'trans_coef': 10,
            'apply_shift': True,
            'shift_cords': wish_cords_normal_shift,
            'shift_speed': wish_pack_shift_speed,
            'shift_speed_coef': wish_pack_shift_speed_coef
        }

        wish_color_black_kwargs = {
            'apply_black': True,
            'apply_shift': True,
            'shift_cords': wish_cords_normal_shift,
            'shift_speed': wish_pack_shift_speed,
            'shift_speed_coef': wish_pack_shift_speed_coef
        }

        wish_color_kwargs = {
            'apply_trans': True,
            'trans_perc': 0,
            'trans_coef': 15,
            'apply_shift': True,
            'shift_cords': wish_cords_normal_shift,
            'shift_speed': wish_pack_shift_speed,
            'shift_speed_coef': wish_pack_shift_speed_coef
        }

        wish_shadow_kwargs = {
            'apply_black': True,
            'apply_trans': True,
            'trans_perc': 0,
            'trans_coef': 20,
            'apply_shift': True,
            'shift_cords': wish_cords_shadow_shift,
            'shift_speed': wish_pack_shift_speed,
            'shift_speed_coef': wish_pack_shift_speed_coef
        }

        if wish_data.wish_meta_type == 'weapon':
            wish_back = WishBack(wish_data.wish_meta_element, wish_cords_normal, **wish_back_kwargs)
        else:
            wish_back = None

        wish_black = WishSplash(*wish_args, wish_cords_normal, **wish_black_kwargs)
        wish_color_black = WishSplash(*wish_args, wish_cords_normal, **wish_color_black_kwargs)
        wish_color = WishSplash(*wish_args, wish_cords_normal, **wish_color_kwargs)
        wish_shadow = WishSplash(*wish_args, wish_cords_shadow, **wish_shadow_kwargs)

        background_delay = self.animation_cfg['end_delay_milti' if is_multi_star else 'end_delay'][wish_stars]

        self.current_draw_objs.update(
            {
                'back_static': Background(background_delay),
                'back_anim_first': BackAnimated('first', wish_stars),
                'back_anim_second': BackAnimated('second', wish_stars),
                'wish_color': wish_color,
                'wish_color_black': wish_color_black,
                'wish_black': wish_black,
                'wish_shadow': wish_shadow,
                'wish_back': wish_back,
                'wish_meta': wish_meta,
            }
        )

        self.current_draw_objs_played.update(
            {
                'back_static': False,
                'back_anim_first': False,
                'back_anim_second': False,
                'wish_color': False,
                'wish_color_black': False,
                'wish_black': False,
                'wish_shadow': False,
                'wish_back': False,
                'wish_meta': False,
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

        for wish_data in wish.wish_data_list:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('[ГАЧА]', '[%s]' % current_time,
                  'Результат для', wish.username,
                  '#%d' % wish_data.wish_count,
                  'g4#%d' % wish_data.wish_4_garant,
                  'g5#%d' % wish_data.wish_5_garant,
                  'w4#%d' % wish_data.win_4_garant,
                  'w5#%d' % wish_data.win_5_garant,
                  wish_data.wish_star, '* ->', _wish_name_normal(wish_data.wish_obj_text),
                  '[%s]' % _wish_garant_type(wish_data.wish_star_type))

            history_cfg = CONFIG['history_file']
            if history_cfg[wish_data.wish_star]:
                write_history(wish.username, wish_data.wish_count, wish_data.wish_star,
                              _wish_garant_type(wish_data.wish_star_type), wish_data.wish_obj_text)

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
            self._purge_obj('wish_meta')

            if self.current_wish_data.wish_meta_type == 'weapon':
                self._purge_obj('wish_back')

            self._purge_obj('wish_shadow')

            self._purge_obj('wish_color_black')
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
            self._play_obj('wish_shadow')

        self._play_obj('wish_color_black')
        self._play_obj('wish_color')

        self._play_obj('wish_meta')

        if back_s.is_play:
            return False

        self._hide_obj('back_anim_second')
        return False

    def state_clear(self) -> bool:
        logging.debug('[PANEL] Состояние панели: CLEAR')
        self.wish_que.task_done()
        self.animations_list.clear()
        self.current_draw_objs.clear()
        self.used_sound.clear()
        self.current_wish = None
        self.current_wish_data = None
        gc.collect()
        return True


class StaticImage(pygame.sprite.Sprite):
    def __init__(self,
                 apply_trans: bool = False,
                 trans_coef: int = 1,
                 trans_perc: int = 255,

                 apply_res: bool = False,
                 res_coef: int = 1,
                 res_perc: int = 0,
                 res_speed: float = 0,

                 apply_shift: bool = False,
                 shift_speed: float = 1.0,
                 shift_speed_coef: float = 0.0,
                 shift_cords: Tuple[int, int] = (0, 0),
                 shift_type: str = 'center',

                 apply_black: bool = False
                 ):
        super().__init__()
        self.lifetime = 0
        self.speed = 1

        self._apply_trans = apply_trans
        self._trans_coef = trans_coef
        self._trans_perc = trans_perc

        self._resized_buffer = []
        self._apply_res = apply_res
        self._res_speed = res_speed
        self._res_coef = res_coef
        self._res_perc = res_perc

        self._shift_ranges = []
        self._apply_shift = apply_shift
        self._shift_speed = shift_speed
        self._shift_speed_coef = shift_speed_coef
        self._shift_cords = shift_cords
        self._shift_type = shift_type
        self._shift_created = False

        self._apply_black = apply_black

        self.image = None
        self.image_copy = None

        self.is_play = False

        self.rect = None
        self.rect_copy = None

    def play(self):
        self.is_play = True

    @staticmethod
    def _var_range(start: int, stop: int, step: float, step_change: float):
        if step < 0:
            step_sign = -1
            while_sign = '<'
            if_sign = '>'
        else:
            step_sign = 1
            while_sign = '>'
            if_sign = '<'

        while eval(f'{stop} - {start} {while_sign} 0'):
            yield int(start)
            start += step
            step = step_sign * (abs(step) - step_change)
            if eval(f'{step} {if_sign} {step_sign}'):
                step = step_sign
        else:
            yield stop

    def update(self):
        if not self.is_play:
            return

        if (self._trans_perc < 255) and self._apply_trans:
            self._trans_perc += self.speed * self._trans_coef

            _local_trans_perc = self._trans_perc
            if _local_trans_perc < 0:
                _local_trans_perc = 0

            self.image.set_alpha(_local_trans_perc)

        if len(self._resized_buffer) > 0 and self._apply_res:
            self.image = self._resized_buffer.pop(0)
            self.rect = self.image.get_rect()
            self.rect.center = self.rect_copy.center

        if self._apply_shift:
            if not self._shift_created:
                rect_orig = getattr(self.rect, self._shift_type)
                rect_x, rect_y = rect_orig
                shift_x, shift_y = self._shift_cords

                x_range = list(self._var_range(rect_x, shift_x, self._shift_speed, self._shift_speed_coef))
                y_range = list(self._var_range(rect_y, shift_y, self._shift_speed, self._shift_speed_coef))

                last_value = x_range[-1] if len(x_range) < len(y_range) else y_range[-1]
                self._shift_ranges = list(zip_longest(x_range, y_range, fillvalue=last_value))
                self._shift_created = True

            if len(self._shift_ranges) > 0:
                shift_cords = self._shift_ranges.pop(0)
                setattr(self.rect, self._shift_type, shift_cords)

        if self.lifetime < 0:
            return

        self.lifetime -= self.speed
        if self.lifetime <= 0:
            self.is_play = False

    def im_sub_load_process(self):
        if self._apply_black:
            self.image = fill_surface(self.image, WISH_BLACK_COLOR)

        if self._apply_trans:
            self.image.set_alpha(self._trans_perc if self._trans_perc >= 0 else 0)

        if self._apply_res:
            self.image_copy = self.image.copy()
            self.rect_copy = self.rect.copy()

            res_perc_list = list(self._var_range(self._res_perc, 100, -self._res_coef, self._res_speed))

            for res_perc in res_perc_list:
                size = self.image_copy.get_size()
                size_coeff = res_perc / 100
                sizex, sizey = (int(size[0] * size_coeff), int(size[1] * size_coeff))

                resized_image = pygame.transform.smoothscale(self.image_copy, (sizex, sizey))
                self._resized_buffer.append(resized_image)

            if len(self._resized_buffer) > 0:
                self.image = self._resized_buffer.pop(0)

    def im_sub_load(self, path):
        self.image = pygame.image.load(path)
        self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.im_sub_load_process()


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

    def update(self):
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
        self.rect.topleft = (0, 0)

    def _load(self):
        path = os.path.join('background', 'static', 'background.jpg')
        self.im_sub_load(path)


class UserBackground(StaticImage):
    def __init__(self, fname):
        super().__init__()

        self.fname = fname
        self.lifetime = -1

        self._load()
        self.rect.topleft = (0, 0)

    def _load(self):
        path = os.path.join('background', self.fname)
        self.im_sub_load(path)


class UserBackgroundAnim(AnimatedVideo):
    def __init__(self, fname):
        super().__init__()

        self.cycled = True
        self.fname = fname
        self.lifetime = -1

        self._load()
        self.rect.topleft = (0, 0)

    def _load(self):
        path = os.path.join('background', self.fname)
        self.im_sub_load(path)


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
    def __init__(self, wtype, wname, cords, **kwargs):
        super().__init__(**kwargs)
        self.lifetime = -1

        self.wtype = wtype
        self.wname = wname

        self._load()

        if kwargs.get('apply_res', False):
            self.rect_copy.center = cords
        else:
            self.rect.center = cords

    def _load(self):
        path = os.path.join('images', self.wtype, '%s.png' % self.wname)
        self.im_sub_load(path)


class WishBack(StaticImage):
    def __init__(self, wtype, coords, **kwargs):
        super().__init__(**kwargs)

        self.lifetime = -1
        self.wtype = wtype

        self._load()

        self.rect.center = coords

    def _load(self):
        path = os.path.join('background', 'weapon', '%s.png' % self.wtype)
        self.im_sub_load(path)


class WishMeta(StaticImage):
    def __init__(self, wtype, wname, **kwargs):
        super().__init__(**kwargs)

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
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        font_config = CONFIG['animations']['font']
        self.font = pygame.font.Font(os.path.join('fonts', font_config['path']), font_config['wish_name_size'])

        self.text = text
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

        font_config = CONFIG['animations']['font']
        self.font = pygame.font.Font(os.path.join('fonts', font_config['path']), font_config['user_uid_size'])

        self.text = text
        self.lifetime = -1

        self._load()
        self.rect.bottomright = (1270, 710)

    def _load(self):
        textobj = self.font.render(self.text, True, USERTEXT_COLOR).convert_alpha()
        self.image = textobj
        self.out_image = fill_surface(textobj.copy(), USERTEXT_OUTLINE)
        self.rect = self.image.get_rect()


class TwitchBot(commands.Bot):
    def __init__(self, wish_que: queue.Queue, coordinator: Coordinator):
        self.gacha_users: Dict[str, Gacha] = {}
        self.sub_topics: List[pubsub.Topic] = []
        self.user_db: Optional[UserDB] = None

        self.chatbot_cfg = CONFIG['chat_bot']
        self.eventbot_cfg = CONFIG['event_bot']
        self.service_cfg = CONFIG['gbot_config']

        self.wish_que = wish_que
        self.user_db = UserDB()
        self.coordinator = coordinator

        self.cmd_timeout = {
            "gbot_status": 0,
            "gbot_stats": 0,
            "gbot_sound": 0,
            "gbot_pause": 0,
            "gbot_history": 0
        }

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

    async def start(self):
        self._load()
        await super().start()

    @staticmethod
    def _get_user_conf(conf: dict, user: twitchio.Chatter) -> Union[bool, int, str]:
        if user.is_broadcaster:
            user_cfg = conf['broadcaster']
        elif user.is_mod:
            user_cfg = conf['mod']
        elif user.is_vip:
            user_cfg = conf['vip']
        elif user.is_turbo:
            user_cfg = conf['turbo']
        elif user.is_subscriber:
            user_cfg = conf['subscriber']
        else:
            user_cfg = conf['user']
        return user_cfg

    def _load(self) -> None:
        print('[TWITCH] Загружаем данные пользователей..')
        for user_data in self.user_db.get_all():
            username, *gacha_params = user_data
            user_gacha = Gacha(*gacha_params)
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
        username = user.name

        logging.debug('[TWITCH] Получена команда wish: %s, %s', username, user.color)

        if username in self.gacha_users:
            user_gacha = self.gacha_users[username]
        else:
            user_gacha = Gacha()
            self.gacha_users[username] = user_gacha
            self.user_db.push(username, user_gacha)

        current_time = int(time.time())
        wtimeoust_cfg = self.chatbot_cfg['wish_timeout']
        user_timeout = self._get_user_conf(wtimeoust_cfg, user)

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
        wish = Wish(username, ucolor, wishes_in_command, wish_data_list)

        try:
            self.last_wish_time = current_time
            answer_text_raw = random.choice(CHATBOT_TEXT)
            answer_text = answer_text_raw.format(username=user.mention,
                                                 wish_count=user_gacha.wish_count,
                                                 wish_count_w4=user_gacha.wish_4_garant - 1,
                                                 wish_count_w5=user_gacha.wish_5_garant - 1,
                                                 wishes_in_cmd=wishes_in_command,
                                                 user_wish_delay=user_timeout,
                                                 global_wish_delay=self.chatbot_cfg['wish_global_timeout'],
                                                 que_num=self.wish_que.unfinished_tasks + 1)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        self.wish_que.put(wish)

        self.wish_c_use += 1
        self.wish_c_primo += wishes_in_command * 160

        self.user_db.update(username, user_gacha)
        await ctx.send(answer_text)

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage) -> None:
        username = event.user.name.lower()
        reward_title = event.reward.title
        user_color = self.eventbot_cfg['default_color']

        logging.debug('[TWITCH] Получен ивент pubsub_channel_points: %s, %s, %s', username, reward_title, user_color)

        rewards_map = {}
        for reward in self.eventbot_cfg['rewards']:
            rewards_map.update({reward['event_name']: reward['wish_count']})

        logging.debug('[TWITCH] pubsub_channel_points rewards_map: %s', rewards_map)

        if not (reward_title in rewards_map):
            return

        if username in self.gacha_users:
            user_gacha = self.gacha_users[username]
        else:
            user_gacha = Gacha()
            self.gacha_users[username] = user_gacha
            self.user_db.push(username, user_gacha)

        wishes_in_command = rewards_map[reward_title]
        wish_data_list = user_gacha.generate_wish(wishes_in_command)
        wish = Wish(username, user_color, wishes_in_command, wish_data_list)

        try:
            anwser_text_raw = random.choice(POINTS_TEXT)
            anwser_text = anwser_text_raw.format(username='@' + username,
                                                 wish_count=user_gacha.wish_count,
                                                 wish_count_w4=user_gacha.wish_4_garant - 1,
                                                 wish_count_w5=user_gacha.wish_5_garant - 1,
                                                 reward_cost=event.reward.cost,
                                                 wishes_in_cmd=wishes_in_command,
                                                 que_num=self.wish_que.unfinished_tasks + 1)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        self.wish_que.put(wish)

        self.wish_r_use += 1
        self.wish_r_sum += event.reward.cost
        self.wish_r_primo += wishes_in_command * 160

        self.user_db.update(username, user_gacha)
        await self.connected_channels[0].send(anwser_text)

    def _srv_bypass(self, fname: str, user: twitchio.Chatter) -> bool:
        func_config = self.service_cfg[fname]
        func_enabled = func_config['enabled']
        func_timeout = func_config['timeout']
        func_perms = func_config['permissions']

        if not func_enabled:
            return False

        if not self._get_user_conf(func_perms, user):
            return False

        current_time = int(time.time())
        if current_time - self.cmd_timeout[fname] < func_timeout:
            return False

        self.cmd_timeout[fname] = current_time
        return True

    @commands.command()
    async def gbot_stats(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_stats', user):
            return

        logging.debug('[TWITCH] Получена команда gbot_stats: %s', user)

        if user.name in self.gacha_users:
            user_gacha = self.gacha_users[user.name]
            uwish_count = user_gacha.wish_count
            uwish_4_garant = user_gacha.wish_4_garant
            uwish_5_garant = user_gacha.wish_5_garant
        else:
            uwish_count = 0
            uwish_4_garant = 0
            uwish_5_garant = 0

        try:
            answer_text = STATS_MESSAGE.format(user_mention=user.mention,
                                               user_wish_all=uwish_count,
                                               user_wish_epic=uwish_4_garant,
                                               user_wish_leg=uwish_5_garant,
                                               user_primo=uwish_count * 160)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        await ctx.send(answer_text)

    @commands.command()
    async def gbot_status(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_status', user):
            return

        logging.debug('[TWITCH] Получена команда gbot_status: %s', user)

        primogems = self.wish_r_primo + self.wish_c_primo
        try:
            answer_text = STATUS_MESSAGE.format(user_mention=user.mention,
                                                proj_name=__title__,
                                                proj_ver=__version__,
                                                proj_url=__site__,
                                                wcommand=self.chatbot_wish_command,
                                                wcommand_c=self.wish_c_use,
                                                rcommand_c=self.wish_r_use,
                                                wish_points=self.wish_r_sum,
                                                wish_gems=primogems,
                                                wish_queue_size=self.wish_que.unfinished_tasks)
        except KeyError as format_error:
            print('[TWITCH] Ошибка при форматировании ответа:', format_error)
            return

        await ctx.send(answer_text)

    @commands.command()
    async def gbot_sound(self, ctx: commands.Context) -> None:
        global _sound_work
        sound_cfg = CONFIG['sound']

        user = ctx.author
        if not self._srv_bypass('gbot_sound', user):
            return

        logging.debug('[TWITCH] Получена команда gbot_sound: %s', user)

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
        if not self._srv_bypass('gbot_pause', user):
            return

        logging.debug('[TWITCH] Получена команда gbot_pause: %s', user)

        if user.is_mod or user.is_broadcaster:
            self.coordinator.que_processing = not self.coordinator.que_processing

            pause_text = 'включена' if self.coordinator.que_processing else 'выключена'
            answer_text = '%s обработка команд: %s' % (user.mention, pause_text)

            await ctx.send(answer_text)

    @commands.command()
    async def gbot_history(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_history', user):
            return

        logging.debug('[TWITCH] Получена команда gbot_history: %s', user)

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
                    wish_kwargs: Dict,
                    wish_type: StaticImage,
                    wish_name: List[str],
                    wish_stars: int
                    ) -> StaticImage:
    """
    Function to create wish information (type, name and number of stars), combines 3 objects at specified coordinates.
    """
    wish_objs = []
    max_width, max_height = 0, 0

    wish_type.rect.topleft = (0, 0)
    wish_objs.append(wish_type)

    wish_name_offset = 0
    wish_name_last = None
    for wish_name_n in wish_name:
        wish_name_obj = WishText(wish_name_n)

        x_midleft = (wish_type.rect.center[0] - 20) + wish_type.image.get_width() / 2
        y_midleft = wish_type.rect.center[1] + wish_name_offset

        wish_name_obj.rect.midleft = (x_midleft, y_midleft)
        wish_name_offset += wish_name_obj.image.get_height()

        wish_objs.append(wish_name_obj)
        wish_name_last = wish_name_obj

        name_width = wish_name_last.rect.midright[0] + 5
        if name_width > max_width:
            max_width = name_width

    last_star = None
    for i in range(wish_stars):
        star = WishMeta('star', None)
        star.rect.topleft = (wish_name_last.rect.bottomleft[0] + 30 * i, wish_name_last.rect.bottomleft[1] + 5)
        wish_objs.append(star)
        last_star = star

    star_width = last_star.rect.bottomright[0]
    max_height = last_star.rect.bottomright[1]
    if star_width > max_width:
        max_width = star_width

    result_sur = StaticImage(**wish_kwargs)

    result_sur.image = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
    result_sur.image.convert_alpha()

    for wish_obj in wish_objs:
        if isinstance(wish_obj, WishText):
            render_text_outline(result_sur.image, wish_obj, 1)
        result_sur.image.blit(wish_obj.image, wish_obj.rect)

    result_sur.rect = result_sur.image.get_rect()
    result_sur.rect.midleft = cords

    result_sur.im_sub_load_process()
    result_sur.lifetime = -1

    return result_sur


def fill_surface(surf: pygame.Surface, color: pygame.Color) -> pygame.Surface:
    w, h = surf.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surf.get_at((x, y))[3]
            surf.set_at((x, y), pygame.Color(r, g, b, a))
    return surf


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


def update_group(animation_group: List[BaseDrawClass]) -> None:
    for animation in animation_group:
        animation.update()


def update_auth() -> None:
    with open('auth.json', 'r', encoding='utf-8') as authf:
        jdata = json.load(authf)

    jdata.update({'chat_bot': AUTH_CHAT_BOT})
    jdata.update({'event_bot': AUTH_EVENT_BOT})

    with open('auth.json', 'w', encoding='utf-8') as authf:
        json.dump(jdata, authf)


async def refresh_bot_token(ref_token: str) -> bool:
    print('[TWITCH] Пробуем обновить токен..')

    refresh_session = aiohttp.ClientSession()
    try:
        async with refresh_session.post(network.URL_TOKEN_REF, json={'ref_token': ref_token}) as twitch_user_data_raw:
            twitch_user_data = await twitch_user_data_raw.json()
    except aiohttp.ClientError as gate_error:
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

    print('[TWITCH] Токен успешно обновлен, бот будет перезапущен..')
    update_auth()
    return True


async def _tokens_check(bot: TwitchBot):
    print('[TWITCH] Проверяем данные ботов..')

    event_bot_channel_id = AUTH_EVENT_BOT['work_channel_id']
    event_bot_token_ref = AUTH_EVENT_BOT['channel_token_ref']
    event_bot_token = AUTH_EVENT_BOT['channel_token']

    chat_bot_token_ref = AUTH_CHAT_BOT['bot_token_ref']
    chat_bot_token = AUTH_CHAT_BOT['bot_token']

    check_tokens = (event_bot_token, chat_bot_token)
    check_tokens_ref = (event_bot_token_ref, chat_bot_token_ref)

    twitch_session = aiohttp.ClientSession()

    for token_t in zip(check_tokens, check_tokens_ref):
        current_token, current_token_ref = token_t
        headers = {"Authorization": f"OAuth %s" % current_token}

        try:
            async with twitch_session.get(network.TWITCH_TOKEN_VALIDATE, headers=headers) as twitch_resp:
                if twitch_resp.status == 401:
                    raise aiohttp.ClientError('неправильный токен или его время действия истекло')
                if twitch_resp.status > 300 or twitch_resp.status < 200:
                    twitch_error_text = await twitch_resp.text()
                    print('[TWITCH] Не удалось проверить токен: %s' % twitch_error_text)
                    return False
                twitch_token_data = await twitch_resp.json()
        except aiohttp.ClientError as twitch_error:
            print('[TWITCH] Ошибка авторизации:', twitch_error)
            refresh_satus = await refresh_bot_token(current_token_ref)
            if not refresh_satus:
                print('[TWITCH] %s' % ('-' * 80))
                print('[TWITCH] Не удалось автоматически обновить токен, причина должна быть строчкой выше ^^^')
                print('[TWITCH] Сейчас приложение можно закрыть и запустить заново - ошибка может исчезнуть,')
                print('[TWITCH] или попробовать удалить файл "auth.json", чтобы попытаться создать токены заново')
                print('[TWITCH] Так же можно создать токены вручную, инструкция есть на github странице проекта')
                print('[TWITCH] Там же можно создать репорт об этой ошибке (настоятельно рекомендуется)')
                print('[TWITCH] %s' % ('-' * 80))
                threading.Event().wait()
            return False

        login = twitch_token_data['login']
        expires = twitch_token_data['expires_in']
        print('[TWITCH] Токен для "%s" закончится через %s сек.' % (login, expires))

        if current_token_ref == chat_bot_token_ref:
            conn_cls = getattr(bot, '_connection')
            http_cls = getattr(bot, '_http')

            setattr(conn_cls, 'nick', twitch_token_data['login'])
            setattr(conn_cls, 'user_id', int(twitch_token_data['user_id']))

            setattr(http_cls, 'nick', twitch_token_data['login'])
            setattr(http_cls, 'user_id', int(twitch_token_data['user_id']))
            setattr(http_cls, 'client_id', twitch_token_data['client_id'])

            setattr(http_cls, 'session', twitch_session)

        if current_token_ref == event_bot_token_ref:
            if event_bot_channel_id == 0:
                AUTH_EVENT_BOT['work_channel_id'] = int(twitch_token_data['user_id'])
                update_auth()

        await asyncio.sleep(3)  # Prevent flood Twitch API

    return True


def bot_handle(wish_que: queue.Queue, control: Coordinator) -> None:
    time.sleep(3)  # Prevent flood Twitch API

    async def _async_wrap():
        bot = TwitchBot(wish_que, control)
        check_status = await _tokens_check(bot)
        if not check_status:
            return
        await bot.start()

    asyncio.run(_async_wrap())


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
        fp.write('%s,%s,%d,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, _wish_name_normal(wish)))


def make_user_wish(username: str, color: str, count: int) -> Tuple[Gacha, Wish]:
    gacha = Gacha()
    wish_data_list = gacha.generate_wish(count)
    wish = Wish(username, color, count, wish_data_list)
    return gacha, wish


def main():
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
        update_group(animation_group)

        pygame.display.update()


if __name__ == '__main__':
    sys.stderr = logging
    main()
