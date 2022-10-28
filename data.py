_SRV_TEMPLATE = {
        "type": "object",
        "required": [
                "enabled",
                "timeout",
                "permissions",
        ],
        "additionalProperties": False,
        "properties": {
                "enabled": {"type": "boolean"},
                "timeout": {"type": "integer"},
                "permissions": {
                        "type": "object",
                        "required": [
                                "broadcaster",
                                "mod",
                                "vip",
                                "turbo",
                                "subscriber",
                                "user"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "broadcaster": {"type": "boolean"},
                                "mod": {"type": "boolean"},
                                "vip": {"type": "boolean"},
                                "turbo": {"type": "boolean"},
                                "subscriber": {"type": "boolean"},
                                "user": {"type": "boolean"}
                        }
                }
        }
}
CONFIG_SCHEMA = {
        "type": "object",
        "required": ["window_name",
                     "language",
                     "messages",
                     "banner",
                     "chat_bot",
                     "event_bot",
                     "animations",
                     "sound",
                     "history_file",
                     "test_mode"
                     ],
        "additionalProperties": False,
        "properties": {
                "window_name": {"type": "string"},
                "language": {"type": "string"},
                "messages": {"type": "string"},
                "banner": {"type": "string"},
                "chat_bot": {
                        "type": "object",
                        "required": ["enabled",
                                     "wish_command",
                                     "wish_command_prefix",
                                     "wish_global_timeout",
                                     "wish_timeout",
                                     "send_notify",
                                     "wish_count",
                                     "self_wish",
                                     "self_wish_every",
                                     "enable_colors"
                                     ],
                        "additionalProperties": False,
                        "properties": {
                                "enabled": {"type": "boolean"},
                                "wish_command": {"type": "string"},
                                "wish_command_prefix": {"type": "string"},
                                "wish_global_timeout": {"type": "integer"},
                                "wish_timeout": {
                                        "type": "object",
                                        "required": [
                                                "broadcaster",
                                                "mod",
                                                "vip",
                                                "turbo",
                                                "subscriber",
                                                "user"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "broadcaster": {"type": "integer"},
                                                "mod": {"type": "integer"},
                                                "vip": {"type": "integer"},
                                                "turbo": {"type": "integer"},
                                                "subscriber": {"type": "integer"},
                                                "user": {"type": "integer"}
                                        }
                                },
                                "send_notify": {"type": "boolean"},
                                "wish_count": {"type": "integer"},
                                "self_wish": {"type": "boolean"},
                                "self_wish_every": {"type": "integer"},
                                "enable_colors": {"type": "boolean"}
                        }
                },
                "event_bot": {
                        "type": "object",
                        "required": [
                                "enabled",
                                "default_color",
                                "rewards"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "enabled": {"type": "boolean"},
                                "event_name": {"type": "string"},
                                "default_color": {"type": "string"},
                                "rewards": {
                                        "type": "array",
                                        "minItems": 1,
                                        "items": {
                                                "type": "object",
                                                "required": [
                                                        "event_name",
                                                        "wish_count"
                                                ],
                                                "additionalProperties": False,
                                                "properties": {
                                                        "event_name": {"type": "string"},
                                                        "wish_count": {"type": "integer"}
                                                }
                                        }
                                }
                        }
                },
                "animations": {
                        "type": "object",
                        "required": [
                                "chroma_color",
                                "draw_states",
                                "start_delay",
                                "end_delay",
                                "end_delay_milti",
                                "user_background",
                                "fps"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "chroma_color": {"type": "string"},
                                "draw_states": {
                                        "type": "object",
                                        "required": [
                                                "draw_usertext",
                                                "draw_fall",
                                                "draw_wishes"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "draw_usertext": {"type": "boolean"},
                                                "draw_fall": {"type": "boolean"},
                                                "draw_wishes": {"type": "boolean"}
                                        }
                                },
                                "start_delay": {"type": "integer"},
                                "end_delay": {
                                        "type": "object",
                                        "required": [
                                                "3",
                                                "4",
                                                "5"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "3": {"type": "integer"},
                                                "4": {"type": "integer"},
                                                "5": {"type": "integer"}
                                        }
                                },
                                "end_delay_milti": {
                                        "type": "object",
                                        "required": [
                                                "3",
                                                "4",
                                                "5"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "3": {"type": "integer"},
                                                "4": {"type": "integer"},
                                                "5": {"type": "integer"}
                                        }
                                },
                                "user_background": {
                                        "type": "object",
                                        "required": [
                                                "enabled",
                                                "path",
                                                "type"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "enabled": {"type": "boolean"},
                                                "path": {"type": "string"},
                                                "type": {"type": "string"}
                                        }
                                },
                                "font": {
                                        "type": "object",
                                        "required": [
                                                "path",
                                                "user_uid_size",
                                                "wish_name_size"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "path": {"type": "string"},
                                                "user_uid_size": {"type": "integer"},
                                                "wish_name_size": {"type": "integer"}
                                        }
                                },
                                "fps": {"type": "integer"}
                        }
                },
                "sound": {
                        "type": "object",
                        "required": [
                                "enabled",
                                "fall",
                                "3",
                                "4",
                                "5",
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "enabled": {"type": "boolean"},
                                "fall": {"type": "string"},
                                "3": {"type": "string"},
                                "4": {"type": "string"},
                                "5": {"type": "string"},
                        }
                },
                "history_file": {
                        "type": "object",
                        "required": [
                                "enabled",
                                "path",
                                "3",
                                "4",
                                "5",
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "enabled": {"type": "boolean"},
                                "path": {"type": "string"},
                                "3": {"type": "boolean"},
                                "4": {"type": "boolean"},
                                "5": {"type": "boolean"}
                        }
                },
                "gbot_config": {
                        "type": "object",
                        "required": [
                                "gbot_status",
                                "gbot_stats",
                                "gbot_sound",
                                "gbot_pause",
                                "gbot_history",
                                "gbot_history_all"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "gbot_status": _SRV_TEMPLATE,
                                "gbot_stats": _SRV_TEMPLATE,
                                "gbot_sound": _SRV_TEMPLATE,
                                "gbot_pause": _SRV_TEMPLATE,
                                "gbot_history": _SRV_TEMPLATE,
                                "gbot_history_all": _SRV_TEMPLATE
                        }
                },
                "send_dev_stats": {"type": "boolean"},
                "test_mode": {"type": "boolean"}
        }
}

MESSAGES_SCHEMA = {
        "type": "object",
        "required": [
                "user_splash_text",
                "chatbot_text",
                "notify_text",
                "chanel_points_text"
        ],
        "additionalProperties": False,
        "properties": {
                "user_splash_text": {
                        "type": "array",
                        "minItems": 1
                },
                "chatbot_text": {
                        "type": "array",
                        "minItems": 1
                },
                "notify_text": {
                        "type": "array",
                        "minItems": 1
                },
                "chanel_points_text": {
                        "type": "array",
                        "minItems": 1
                },
                "stats_message": {"type": "string"},
                "status_message": {"type": "string"},
        }
}

AUTH_SCHEMA = {
        "type": "object",
        "required": ["chat_bot", "event_bot"],
        "additionalProperties": False,
        "properties": {
                "chat_bot": {
                        "type": "object",
                        "required": ["bot_token", "bot_token_ref", "work_channel"],
                        "additionalProperties": False,
                        "properties": {
                                "bot_token": {"type": "string"},
                                "bot_token_ref": {"type": "string"},
                                "work_channel": {"type": "string"},
                        }
                },
                "event_bot": {
                        "type": "object",
                        "required": ["channel_token", "channel_token_ref", "work_channel_id"],
                        "additionalProperties": False,
                        "properties": {
                                "channel_token": {"type": "string"},
                                "channel_token_ref": {"type": "string"},
                                "work_channel_id": {"type": "integer"},
                        }
                }
        }
}

_BANNER_54_TEMPLATE = {
        "type": "object",
        "required": [
                "char",
                "weapon",
                "garant"
        ],
        "additionalProperties": False,
        "properties": {
                "char": {"type": "array", "items": {"type": "string"}},
                "weapon": {"type": "array", "items": {"type": "string"}},
                "garant": {"type": "array", "items": {"type": "string"}}
        }
}
BANNER_SCHEMA = {
        "type": "object",
        "required": ["banner_name",
                     "wish_fo_garant",
                     "wish_fo_chance",
                     "wish_fi_garant",
                     "wish_fi_chance",
                     "wish_fi_soft_a",
                     "wishes",
                     ],
        "additionalProperties": False,
        "properties": {
                "banner_name": {"type": "string"},
                "wish_fo_garant": {"type": "number"},
                "wish_fo_chance": {"type": "number"},
                "wish_fi_garant": {"type": "number"},
                "wish_fi_chance": {"type": "number"},
                "wish_fi_soft_a": {"type": "number"},
                "wishes": {
                        "type": "object",
                        "required": [
                                "5",
                                "4",
                                "3"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "5": _BANNER_54_TEMPLATE,
                                "4": _BANNER_54_TEMPLATE,
                                "3": {
                                        "type": "object",
                                        "required": [
                                                "weapon"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "weapon": {"type": "array", "items": {"type": "string"}}
                                        }
                                }
                        }
                }
        }
}

DATABASE = {
        '3': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'holodnoelezvie', 'wish_obj_text': 'Холодное лезвие'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fileynozh', 'wish_obj_text': 'Филейный нож'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'temniyzhsw', 'wish_obj_text': 'Тёмный железный\nмеч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'predvestnik', 'wish_obj_text': 'Предвестник зари'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swputeshest', 'wish_obj_text': 'Меч\nпутешественника'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swvsadnik', 'wish_obj_text': 'Меч небесного\nвсадника'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'beloezhelezogsw', 'wish_obj_text': 'Меч из белого\nжелеза'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dragonbloodgsw', 'wish_obj_text': 'Меч драконьей\nкрови'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'metalten', 'wish_obj_text': 'Металлическая\nтень'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dubinapereg', 'wish_obj_text': 'Дубина переговоров'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'bolshounebes', 'wish_obj_text': 'Большой меч\nнебесного всадника'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernayakist', 'wish_obj_text': 'Чёрная кисть'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'belayakist', 'wish_obj_text': 'Белая кисть'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'alebardamilelith', 'wish_obj_text': 'Алебарда Миллелита'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rogatka', 'wish_obj_text': 'Рогатка'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'posulniy', 'wish_obj_text': 'Посыльный'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'voronbow', 'wish_obj_text': 'Лук ворона'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'klatvastrelka', 'wish_obj_text': 'Клятва стрелка'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'izognutbow', 'wish_obj_text': 'Изогнутый лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'eposdrakon', 'wish_obj_text': 'Эпос о\nдраконоборцах'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'rukovodmagiya', 'wish_obj_text': 'Руководство\nпо магии'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'potustoristor', 'wish_obj_text': 'Потусторонняя\nистория'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'parniynefrit', 'wish_obj_text': 'Парный нефрит'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'izumrudshar', 'wish_obj_text': 'Изумрудный шар'}
                ],
                'char': []
        },
        '4': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'chernogorsw', 'wish_obj_text': 'Черногорский\nдлинный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'cherniysw', 'wish_obj_text': 'Чёрный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'ceremonialsw', 'wish_obj_text': 'Церемониальный\nмеч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'stalnoezh', 'wish_obj_text': 'Стальное жало'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'pzloba', 'wish_obj_text': 'Прототип: Злоба'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'oskzhelanie', 'wish_obj_text': 'Осквернённое\nжелание'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fleyta', 'wish_obj_text': 'Меч-флейта'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'favoniy', 'wish_obj_text': 'Меч Фавония'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nishozhdeniesw', 'wish_obj_text': 'Меч нисхождения'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'aristokratsw', 'wish_obj_text': 'Меч аристократов'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kinowarsw', 'wish_obj_text': 'Киноварное\nверетено'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'dragonroar', 'wish_obj_text': 'Драконий рык'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'vspishka', 'wish_obj_text': 'Вспышка во тьме'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'amenoma', 'wish_obj_text': 'Амэнома Кагэути'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladesw', 'wish_obj_text': 'Легендарный\nклинок Иссин'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladerawsw', 'wish_obj_text': 'Легендарный\nклинок Иссин'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladenowsw', 'wish_obj_text': 'Кагоцурубэ\nИссин'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'woodsw', 'wish_obj_text': 'Деревянный\nклинок'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'lunnoesyanie', 'wish_obj_text': 'Лунное сияние\nксифоса'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'chernogorgws', 'wish_obj_text': 'Черногорская\nбритва'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'ceremonialgsw', 'wish_obj_text': 'Церемониальный\nдвуручный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'parhaich', 'wish_obj_text': 'Прототип:\nАрхаичный'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kolokol', 'wish_obj_text': 'Меч-колокол'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'swdrackost', 'wish_obj_text': 'Меч драконьей\nкости'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'korolgsw', 'wish_obj_text': 'Королевский\nдвуручный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kasturakiri', 'wish_obj_text': 'Кацурагикири\nНагамаса'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kamenniygsw', 'wish_obj_text': 'Каменный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'zasnezhennoeser', 'wish_obj_text': 'Заснеженное\nзвёздное серебро'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dozhderez', 'wish_obj_text': 'Дождерез'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'favoniygsw', 'wish_obj_text': 'Двуручный меч\nФавония'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'blagorodvladyka', 'wish_obj_text': 'Благодатный\nвладыка вод'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'belayaten', 'wish_obj_text': 'Белая тень'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'akuomaku', 'wish_obj_text': 'Акуомару'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'woodgsw', 'wish_obj_text': 'Регалия леса'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'akwamarinmaxar', 'wish_obj_text': 'Аквамарин Махары'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernogorpika', 'wish_obj_text': 'Черногорская\nпика'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'smertboy', 'wish_obj_text': 'Смертельный бой'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'rezhushiy', 'wish_obj_text': 'Режущий волны\nплавник'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pzvezdblesk', 'wish_obj_text': 'Прототип:\nЗвёздный блеск'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pikapolumes', 'wish_obj_text': 'Пика полумесяца'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'krestkitain', 'wish_obj_text': 'Крест-копьё\nКитаин'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'korolewskkop', 'wish_obj_text': 'Королевское\nкопьё'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'favoniuskopie', 'wish_obj_text': 'Копьё Фавония'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'drakoniyhrebet', 'wish_obj_text': 'Копьё Драконьего\nхребта'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'kamennoekop', 'wish_obj_text': 'Каменное копьё'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'grozadrakonov', 'wish_obj_text': 'Гроза драконов'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'ulov', 'wish_obj_text': 'Улов'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'woodpol', 'wish_obj_text': 'Пронзающий\nлуну'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'peremenvetrov', 'wish_obj_text': 'Клинок\nперемены ветров'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'chernogorbow', 'wish_obj_text': 'Черногорский\nбоевой лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ceremonualbow', 'wish_obj_text': 'Церемониальный\nлук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hishnik', 'wish_obj_text': 'Хищник'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hamaumi', 'wish_obj_text': 'Хамаюми'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sostavnoybow', 'wish_obj_text': 'Составной лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rzhavyi', 'wish_obj_text': 'Ржавый лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ppolumesac', 'wish_obj_text': 'Прототип:\nПолумесяц'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ohotnikvotme', 'wish_obj_text': 'Охотник во тьме'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'odaanemonii', 'wish_obj_text': 'Ода анемонии'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'lunamoun', 'wish_obj_text': 'Луна Моун'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'korolevbow', 'wish_obj_text': 'Королевский лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'zelenbow', 'wish_obj_text': 'Зелёный лук'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'valsnirvany', 'wish_obj_text': 'Вальс Нирваны\nНочи'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'favoniybow', 'wish_obj_text': 'Боевой лук\nФавония'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'besstrunniy', 'wish_obj_text': 'Бесструнный'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sumekri', 'wish_obj_text': 'Гаснущие\nсумерки'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'woodbow', 'wish_obj_text': 'Приближённый\nкороля'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'dolphbow', 'wish_obj_text': 'Иссушитель'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'chernogorcat', 'wish_obj_text': 'Черногорский\nагат'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'ceremonmemuary', 'wish_obj_text': 'Церемониальные\nмемуары'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'solzhemchuzh', 'wish_obj_text': 'Солнечная\nжемчужина'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pyzntar', 'wish_obj_text': 'Прототип:\nЯнтарь'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'plodmerzloty', 'wish_obj_text': 'Плод вечной\nмерзлоты'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pesnstrannika', 'wish_obj_text': 'Песнь странника'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okosoananiya', 'wish_obj_text': 'Око сознания'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okoklatvy', 'wish_obj_text': 'Око клятвы'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'morskoyatlas', 'wish_obj_text': 'Морской атлас'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'korolgrimuar', 'wish_obj_text': 'Королевский\nгримуар'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'hakusin', 'wish_obj_text': 'Кольцо Хакусин'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'favoniykodex', 'wish_obj_text': 'Кодекс Фавония'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'dodoko', 'wish_obj_text': 'Истории Додоко'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vinoipesni', 'wish_obj_text': 'Вино и песни'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'woodcat', 'wish_obj_text': 'Плод восполнения'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'skitzvezda', 'wish_obj_text': 'Скитающаяся\nзвезда'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbruh_skin', 'wish_obj_text': 'Летний блеск'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean_skin', 'wish_obj_text': 'Сон морского\nбриза'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'nina_skin', 'wish_obj_text': 'Флёр орхидеи'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keka_skin', 'wish_obj_text': 'Яркая лёгкость'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'amber', 'wish_obj_text': 'Эмбер'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbara', 'wish_obj_text': 'Барбара'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'beidou', 'wish_obj_text': 'Бэй Доу'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'bennett', 'wish_obj_text': 'Беннет'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'chongyun', 'wish_obj_text': 'Чун Юнь'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'diona', 'wish_obj_text': 'Диона'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl', 'wish_obj_text': 'Фишль'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl_skin', 'wish_obj_text': 'Сон вечной\nночи'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'goro', 'wish_obj_text': 'Горо'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'kaeya', 'wish_obj_text': 'Кэйа'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'lisa', 'wish_obj_text': 'Лиза'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'ningguang', 'wish_obj_text': 'Нин Гуан'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'noelle', 'wish_obj_text': 'Ноэлль'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'razor', 'wish_obj_text': 'Рэйзор'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'rosaria', 'wish_obj_text': 'Розария'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'sara', 'wish_obj_text': 'Кудзё Сара'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sayu', 'wish_obj_text': 'Саю'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sucrose', 'wish_obj_text': 'Сахароза'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'thoma', 'wish_obj_text': 'Тома'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xianling', 'wish_obj_text': 'Сян Лин'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'xingqiu', 'wish_obj_text': 'Син Цю'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xinyan', 'wish_obj_text': 'Синь Янь'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yanfei', 'wish_obj_text': 'Янь Фэй'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'yunjin', 'wish_obj_text': 'Юнь Цзинь'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'shinobu', 'wish_obj_text': 'Куки Синобу'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'heizo', 'wish_obj_text': 'Сиканоин Хэйдзо'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'dori', 'wish_obj_text': 'Дори'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'collei', 'wish_obj_text': 'Коллеи'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'candace', 'wish_obj_text': 'Кандакия'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'layla', 'wish_obj_text': 'Лайла'}
                ]
        },
        '5': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'haran', 'wish_obj_text': 'Харан гэппаку\nфуцу'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'tuman', 'wish_obj_text': 'Рассекающий туман'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nebesmech', 'wish_obj_text': 'Небесный меч'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'sokol', 'wish_obj_text': 'Меч Сокола'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kromsateld', 'wish_obj_text': 'Кромсатель пиков'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'klyatwa', 'wish_obj_text': 'Клятва свободы'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'omut', 'wish_obj_text': 'Драгоценный омут'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'ierofankey', 'wish_obj_text': 'Ключ иерофании'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'pesnsosen', 'wish_obj_text': 'Песнь разбитых\nсосен'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nekovaniy', 'wish_obj_text': 'Некованый'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nebesnoyvel', 'wish_obj_text': 'Небесное величие'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'krasnorog', 'wish_obj_text': 'Краснорогий\nкамнеруб'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'volchuya', 'wish_obj_text': 'Волчья погибель'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'usmiritelbed', 'wish_obj_text': 'Усмиритель бед'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'sizushayazhatva', 'wish_obj_text': 'Сияющая жатва'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'homa', 'wish_obj_text': 'Посох Хомы'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pokoritel', 'wish_obj_text': 'Покоритель вихря'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nefritkorshun', 'wish_obj_text': 'Нефритовый коршун'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nebesnayaos', 'wish_obj_text': 'Небесная ось'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'alyhpeskov', 'wish_obj_text': 'Посох алых\nпесков'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'elegiyapogib', 'wish_obj_text': 'Элегия погибели'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'polarzvezda', 'wish_obj_text': 'Полярная звезда'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'nebeskrylo', 'wish_obj_text': 'Небесное крыло'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'amos', 'wish_obj_text': 'Лук Амоса'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'grompulse', 'wish_obj_text': 'Громовой пульс'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'aquasimul', 'wish_obj_text': 'Аква симулякрум'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'huntertrope', 'wish_obj_text': 'Охотничья тропа'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pamatopily', 'wish_obj_text': 'Память о пыли'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'nebesatlas', 'wish_obj_text': 'Небесный атлас'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'molitvavetram', 'wish_obj_text': 'Молитва святым\nветрам'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'istinakagura', 'wish_obj_text': 'Истина кагура'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vechnoyesiyanie', 'wish_obj_text': 'Вечное лунное\nсияние'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'snovidenysnochey', 'wish_obj_text': 'Сновидения\nтысячи ночей'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'albedo', 'wish_obj_text': 'Альбедо'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ayaka', 'wish_obj_text': 'Камисато Аяка'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'ayto', 'wish_obj_text': 'Камисато Аято'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc', 'wish_obj_text': 'Дилюк'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc_skin', 'wish_obj_text': 'Алая ночь'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'eula', 'wish_obj_text': 'Эола'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ganyu', 'wish_obj_text': 'Гань Юй'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'hutao', 'wish_obj_text': 'Ху Тао'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'itto', 'wish_obj_text': 'Аратаки Итто'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean', 'wish_obj_text': 'Джинн'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'kazuha', 'wish_obj_text': 'Каэдэхара\nКадзуха'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keqing', 'wish_obj_text': 'Кэ Цин'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'klee', 'wish_obj_text': 'Кли'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'kokomi', 'wish_obj_text': 'Кокоми'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'miko', 'wish_obj_text': 'Яэ Мико'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'mona', 'wish_obj_text': 'Мона'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'qiqi', 'wish_obj_text': 'Ци Ци'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'raiden', 'wish_obj_text': 'Райдэн'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'shenhe', 'wish_obj_text': 'Шэнь Хэ'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'tartaglia', 'wish_obj_text': 'Тарталья'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'venti', 'wish_obj_text': 'Венти'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'xiao', 'wish_obj_text': 'Сяо'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yoimiya', 'wish_obj_text': 'Ёимия'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'zhongli', 'wish_obj_text': 'Чжун Ли'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'aloy', 'wish_obj_text': 'Элой'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'elan', 'wish_obj_text': 'Е Лань'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'tighnari', 'wish_obj_text': 'Тигнари'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'nilou', 'wish_obj_text': 'Нилу'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'cyno', 'wish_obj_text': 'Сайно'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'nahida', 'wish_obj_text': 'Нахида'}
                ]
        }
}

TEXT = {
        'config_check_error_load': '[MAIN] Error loading json file (%s) : %s',
        'config_check_error_check': '[MAIN] Error checking json file (%s) : %s',
        'text_load_not_found': '[MAIN] Translate file not found: %s',
        'press_to_exit': '\nPress any button to exit > ',
        'load_databse_load_pre': '[MAIN] Loading banner "%s" ..',
        'load_database_item_not_found': 'banner loading error: %s*%s:%s not found',
        'load_database_item_wrong_params': 'banner loading error: %s*%s:%s <> %s*%s:%s',
        'load_database_item_zero_items': 'banner loading error: not a single item is loaded',
        'db_import_old_start': '[DB] Start importing the old database...',
        'db_import_old_users_count': '[DB] Users found in the old database:',
        'db_import_old_users_total': '[DB] Users imported:',
        'db_import_old_deleted': '[DB] The old database is deleted!',
        'cord_gacha_br': '[GACHA]',
        'cord_result_for': 'Result for',
        'twitch_load_userdata': '[TWITCH] Loading user data..',
        'twitch_load_users_total': '[TWITCH] Data uploaded. The total number of users in the database:',
        'twitch_load_chatbot_command': '[TWITCH] Chat-bot enabled, command:',
        'twitch_load_eventbot_count': '[TWITCH] Channel points enabled, rewards activated:',
        'twitch_load_chat_connect': '[TWITCH] Connecting to chat on channel %s..',
        'twitch_load_event_connect': '[TWITCH] Connecting to %d channel\'s points..',
        'twitch_chat_connected': '[TWITCH] Connected. Chat-bot data:',
        'twitch_self_wishes_enabled': '[TWITCH] Bot self-wishes are enabled every %d sec.',
        'twitch_event_connect_error': '[TWITCH] Failed to connect to channel points [ %d ] -> %s',
        'twitch_event_connected': '[TWITCH] Successfully connected to channel points [ %d ]',
        'twitch_error_format': '[TWITCH] Formatting error in the reply:',
        'twitch_send_autowish': '[TWITCH] Sending an auto-message..',
        'twitch_history_get_error': '[TWITCH] Error receiving history file:',
        'token_refresh_try': '[TWITCH] Trying to update twitch token..',
        'token_refresh_error': '[AUTH] Failed to update twitch token:',
        'token_refresh_ok': '[TWITCH] Token successfully updated, twitch bot will be restarted..',
        'twitch_bots_check': '[TWITCH] Checking twitch bot data..',
        'twitch_token_check_error': '[TWITCH] Failed to verify twitch token: %s',
        'twitch_auth_error': '[TWITCH] Authorization error:',
        'twitch_empty_format': '[TWITCH] %s',
        'twitch_backend_error_note': '[TWITCH] Failed to automatically update the twitch token, the reason should be the line above ^^^\n[TWITCH] Now you can close the application and restart it - the error may disappear,\n[TWITCH] or try deleting the "auth.json" file to try to create twitch tokens again\n[TWITCH] You can also create tokens manually, the instructions are available on the project\'s github page\n[TWITCH] There you can also report this error (highly recommended)',
        'twitch_token_expire_notify': '[TWITCH] Twitch token for "%s" will expire in %d sec.',
        'main_start': '[MAIN] Launching..',
        'main_twitch_bot_started': '[MAIN] Twitch bot launched',
        'main_twitch_bot_disabled': '[MAIN] Twitch bot disabled',
        'main_fps': '[MAIN] FPS set to',
        'main_twitch_bot_restart': '[MAIN] Twitch bot died, restart it..',
        'log_gacha_created': '[GACHA] Created gacha with params: w:%d g4:%d g5:%d w4:%d w5:%d',
        'log_gacha_wish_result': '[GACHA] Wish result: %s %s %s',
        'log_db_created': '[DB] Created a new connection to the database',
        'log_db_table_create': '[DB] There is no user table, we create it..',
        'log_db_old_update': '[DB] The version of the database is out of date, update the table: %s',
        'log_db_old_import': '[DB] Started downloading data from the old database (<=1.3)',
        'log_db_method_getall': '[DB] Called method get_all',
        'log_db_method_get': '[DB] Called method "get" with: %s',
        'log_db_method_push': '[DB] Called method "push" with: %s, %s',
        'log_db_method_update': '[DB] Called method "update" with: %s, %s',
        'log_panel_created': '[PANEL] A new animation control panel was created',
        'log_panel_none_check': '[PANEL] BUG? Called method "_t_load_chunk", but "cur_wish_data" == None',
        'log_panel_call_chunk_load': '[PANEL] Called method "_t_load_chunk" with: %s',
        'log_panel_call_chunk_time': '[PANEL] Method "_t_load_chunk" loaded data in %d sec.',
        'log_panel_state_idle': '[PANEL] Panel status: IDLE',
        'log_panel_state_init': '[PANEL] Panel status: INIT',
        'log_panel_init_wish_params': '[PANEL] Fall animation has params: wish_stars=%s, multi=%s',
        'log_panel_init_load_time': '[PANEL] Initial data for the animation loaded in %d sec.',
        'log_panel_init_anim': '[PANEL] Initializing animation with data: %s',
        'log_panel_init_loaded_uback': '[PANEL] Loaded custom background: %s',
        'log_panel_state_clear': '[PANEL] Panel status: CLEAR',
        'log_twitch_init': '[TWITCH] Initializing Twitch bot, params: %s, %s, %s',
        'log_twitch_wish_command': '[TWITCH] Received command "wish": %s, %s',
        'log_twitch_pubsub_event': '[TWITCH] Received event pubsub_channel_points: %s, %s, %s',
        'log_twitch_pubsub_map': '[TWITCH] pubsub_channel_points rewards_map: %s',
        'log_twitch_getcmd_stats': '[TWITCH] Received command "gbot_stats": %s',
        'log_twitch_getcmd_status': '[TWITCH] Received command "gbot_status": %s',
        'log_twitch_getcmd_sound': '[TWITCH] Received command "gbot_sound": %s',
        'log_twitch_getcmd_pause': '[TWITCH] Received command "gbot_pause": %s',
        'log_twitch_getcmd_history': '[TWITCH] Received command "gbot_history": %s',
        'log_twitch_getcmd_history_all': '[TWITCH] Received command "gbot_history_all": %s',
        'wish_garant_type_1': 'soft pity',
        'wish_garant_type_2': 'random guarantee',
        'wish_garant_type_3': 'guarantee',
        'wish_garant_type_4': 'random',
        'wish_garant_type_5': '50/50',
        'enabled': 'enabled',
        'disabled': 'disabled',
        'sound_status': '%s sound: %s',
        'commands_status': '%s command processing: %s'
}

HTML_HISTORY_TEMPLATE_TABLE = r'<tr class="filtered_items"><td>{{ wish_date }}</td><td>{{ wish_user }}</td><td>{{ wish_count }}</td><td>{{ wish_type }}</td><td class="{{ wish_style_color }}">{{ wish_name }}</td></tr>'
