import os
import sys
import logging

import json
import jsonschema

from typing import Dict

from data import TEXT, DATABASE_TEXT
from data import DATABASE as _DATABASE
from data import CONFIG_SCHEMA, MESSAGES_SCHEMA, BANNER_SCHEMA

__title__ = 'genshin-twitch-wish'
__site__ = 'github.com/dzmuh97/genshin-twitch-wish'
__version__ = '2.3.0'

CONFIG = {}
BANNER_CONFIG = {}
DATABASE = {}
USER_SPLASH_TEXT = {}
CHATBOT_TEXT = {}
NOTIFY_TEXT = {}
POINTS_TEXT = {}
STATS_MESSAGE = {}
STATUS_MESSAGE = {}
SOUND_CONFIG = {}
LANG_CONFIG = {}


def _wish_name_normal(name: str) -> str:
    return name.replace('\n', ' ')


def _msg(_msg_type: str) -> str:
    return TEXT.get(_msg_type, '(msg error: unknown msg type "%s")' % _msg_type)


def _log_print(*args, **kwargs) -> None:
    log_text = ' '.join(str(arg) for arg in args)
    logging.info(log_text)
    print(*args, **kwargs)


def _load_json(json_file: str) -> Dict:
    try:
        json_data = json.loads(open(json_file, 'r', encoding='utf-8').read())
    except (json.JSONDecodeError, ValueError) as json_error:
        _log_print(_msg('config_check_error_load') % (json_file, json_error))
        sys.exit(input(_msg('press_to_exit')))
    except FileNotFoundError as file_error:
        _log_print(_msg('config_check_error_load') % (json_file, file_error))
        sys.exit(input(_msg('press_to_exit')))
    return json_data


def _config_check(json_file: str, schema: Dict) -> Dict:
    config = _load_json(json_file)

    try:
        jsonschema.validate(config, schema=schema)
    except jsonschema.ValidationError as json_error:
        _log_print(_msg('config_check_error_check') % (json_file, json_error))
        sys.exit(input(_msg('press_to_exit')))

    return config


def _load_text(text_file: str) -> Dict:
    empty = {'text': {}}
    _text_path = os.path.join('text', '%s.json' % text_file)

    if (not text_file) or (text_file == 'default'):
        _log_print(_msg('text_load_null'))
        return empty

    if not os.path.exists(_text_path):
        _log_print(_msg('text_load_not_found') % _text_path)
        return empty

    return _load_json(_text_path)


def _items_merge(items_file: str) -> None:
    _items_path = os.path.join('text', '%s.json' % items_file)

    if (not items_file) or (items_file == 'default'):
        _log_print(_msg('items_load_null'))
        return

    if not os.path.exists(_items_path):
        _log_print(_msg('items_load_not_found') % _items_path)
        return

    items_text = _load_json(_items_path)['items']
    DATABASE_TEXT.update(items_text)


def _items_text_load() -> None:
    def _int_iter() -> Dict:
        for star in _DATABASE:
            itypes = _DATABASE[star]
            for itype in itypes:
                items = itypes[itype]
                for item_data in items:
                    yield item_data

    for item in _int_iter():
        item_obj_name = item['wish_obj_name']
        item_text = DATABASE_TEXT[item_obj_name]
        item.update({'wish_obj_text': item_text})


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
    _log_print(_msg('load_databse_load_pre') % base_name, end=' ')

    wishes = config['wishes']
    for ban_star in wishes:
        for ban_wtype in ['char', 'weapon', 'garant']:
            items = wishes[ban_star].get(ban_wtype, [])
            for ban_item in items:

                filtered_data = filter(lambda x: ban_item == _wish_name_normal(x[0]['wish_obj_text']), items_linear)
                try:
                    item_data = next(filtered_data)
                except StopIteration:
                    _log_print(_msg('load_database_item_not_found') % (ban_star, ban_wtype, ban_item))
                    sys.exit(input(_msg('press_to_exit')))

                db_item, db_star, db_wtype = item_data

                if ban_wtype in ['char', 'weapon']:
                    if ban_star != db_star or ban_wtype != db_wtype:
                        _text_params = (ban_star, ban_wtype, ban_item, db_star, db_wtype, db_item['wish_obj_text'])
                        _log_print(_msg('load_database_item_wrong_params') % _text_params)
                        sys.exit(input(_msg('press_to_exit')))
                    total += 1

                data_template[ban_star][ban_wtype].append(db_item)
                stats[ban_star][ban_wtype] += 1

    if total == 0:
        _log_print(_msg('load_database_item_zero_items'))
        sys.exit(input(_msg('press_to_exit')))

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
    _log_print(stat_text)
    return data_template


def init():
    global CONFIG
    global BANNER_CONFIG
    global DATABASE
    global USER_SPLASH_TEXT
    global CHATBOT_TEXT
    global NOTIFY_TEXT
    global POINTS_TEXT
    global STATS_MESSAGE
    global STATUS_MESSAGE
    global SOUND_CONFIG
    global LANG_CONFIG

    CONFIG = _config_check('config.json', CONFIG_SCHEMA)
    LANG_CONFIG = CONFIG['language']

    _text = _load_text(LANG_CONFIG['text'])
    TEXT.update(_text['text'])

    _items_merge(LANG_CONFIG['wish_items'])
    _items_text_load()

    _banner_path = os.path.join('banners', '%s.json' % CONFIG['banner'])
    BANNER_CONFIG = _config_check(_banner_path, BANNER_SCHEMA)
    DATABASE = _load_database(BANNER_CONFIG)

    _messages_path = os.path.join('text', '%s.json' % LANG_CONFIG['messages'])
    _messages = _config_check(_messages_path, MESSAGES_SCHEMA)
    USER_SPLASH_TEXT = _messages['user_splash_text']
    CHATBOT_TEXT = _messages['chatbot_text']
    NOTIFY_TEXT = _messages['notify_text']
    POINTS_TEXT = _messages['channel_points_text']
    STATS_MESSAGE = _messages['stats_message']
    STATUS_MESSAGE = _messages['status_message']

    SOUND_CONFIG = CONFIG['sound']
