CONFIG_SCHEMA = {
        "type": "object",
        "required": ["CONFIG", "MESSAGES"],
        "additionalProperties": False,
        "properties": {
                "CONFIG": {
                        "type": "object",
                        "required": ["window_name",
                                     "chat_bot",
                                     "event_bot",
                                     "animations",
                                     "sound",
                                     "history_file",
                                     "wish_fo_garant",
                                     "wish_fo_chance",
                                     "wish_fi_garant",
                                     "wish_fi_chance",
                                     "wish_fi_soft_a",
                                     "test_mode"
                                     ],
                        "additionalProperties": False,
                        "properties": {
                                "window_name": {"type": "string"},
                                "chat_bot": {
                                        "type": "object",
                                        "required": ["enabled",
                                                     "bot_token",
                                                     "work_channel",
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
                                                "bot_token": {"type": "string"},
                                                "work_channel": {"type": "string"},
                                                "wish_command": {"type": "string"},
                                                "wish_command_prefix": {"type": "string"},
                                                "wish_global_timeout": {"type": "integer"},
                                                "wish_timeout": {
                                                        "type": "object",
                                                        "required": [
                                                                "broadcaster",
                                                                "mod",
                                                                "subscriber",
                                                                "user"
                                                        ],
                                                        "additionalProperties": False,
                                                        "properties": {
                                                                "broadcaster": {"type": "integer"},
                                                                "mod": {"type": "integer"},
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
                                                "channel_token",
                                                "work_channel_id",
                                                "default_color",
                                                "rewards"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "enabled": {"type": "boolean"},
                                                "channel_token": {"type": "string"},
                                                "work_channel_id": {"type": "integer"},
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
                                                "start_delay",
                                                "end_delay",
                                                "end_delay_milti",
                                                "user_background",
                                                "fps"
                                        ],
                                        "additionalProperties": False,
                                        "properties": {
                                                "chroma_color": {"type": "string"},
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
                                "wish_fo_garant": {"type": "number"},
                                "wish_fo_chance": {"type": "number"},
                                "wish_fi_garant": {"type": "number"},
                                "wish_fi_chance": {"type": "number"},
                                "wish_fi_soft_a": {"type": "number"},
                                "send_dev_stats": {"type": "boolean"},
                                "test_mode": {"type": "boolean"}
                        }
                },
                "MESSAGES": {
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
                                "stats_message": {"type": "string"}
                        }
                }
        }
}

DATABASE = {
        '3': {
                'weapon': [
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'holodnoelezvie', 'cwish_wname': 'Холодное лезвие'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'fileynozh', 'cwish_wname': 'Филейный нож'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'temniyzhsw', 'cwish_wname': 'Тёмный железный\nмеч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'predvestnik', 'cwish_wname': 'Предвестник зари'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'swputeshest', 'cwish_wname': 'Меч\nпутешественника'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'swvsadnik', 'cwish_wname': 'Меч небесного\nвсадника'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'beloezhelezogsw', 'cwish_wname': 'Меч из белого\nжелеза'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'dragonbloodgsw', 'cwish_wname': 'Меч драконьей\nкрови'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'metalten', 'cwish_wname': 'Металлическая\nтень'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'dubinapereg', 'cwish_wname': 'Дубина переговоров'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'bolshounebes', 'cwish_wname': 'Большой меч\nнебесного всадника'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'chernayakist', 'cwish_wname': 'Чёрная кисть'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'belayakist', 'cwish_wname': 'Белая кисть'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'alebardamilelith', 'cwish_wname': 'Алебарда Миллелита'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'rogatka', 'cwish_wname': 'Рогатка'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'posulniy', 'cwish_wname': 'Посыльный'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'voronbow', 'cwish_wname': 'Лук ворона'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'klatvastrelka', 'cwish_wname': 'Клятва стрелка'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'izognutbow', 'cwish_wname': 'Изогнутый лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'eposdrakon', 'cwish_wname': 'Эпос о\nдраконоборцах'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'rukovodmagiya', 'cwish_wname': 'Руководство\nпо магии'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'potustoristor', 'cwish_wname': 'Потусторонняя\nистория'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'parniynefrit', 'cwish_wname': 'Парный нефрит'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'izumrudshar', 'cwish_wname': 'Изумрудный шар'}
                ],
                'char': []
        },
        '4': {
                'weapon': [
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'chernogorsw', 'cwish_wname': 'Черногорский\nдлинный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'cherniysw', 'cwish_wname': 'Чёрный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'ceremonialsw', 'cwish_wname': 'Церемониальный\nмеч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'stalnoezh', 'cwish_wname': 'Стальное жало'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'pzloba', 'cwish_wname': 'Прототип: Злоба'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'oskzhelanie', 'cwish_wname': 'Осквернённое\nжелание'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'fleyta', 'cwish_wname': 'Меч-флейта'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'favoniy', 'cwish_wname': 'Меч Фавония'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'nishozhdeniesw', 'cwish_wname': 'Меч нисхождения'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'aristokratsw', 'cwish_wname': 'Меч аристократов'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'kinowarsw', 'cwish_wname': 'Киноварное\nверетено'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'dragonroar', 'cwish_wname': 'Драконий рык'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'vspishka', 'cwish_wname': 'Вспышка во тьме'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'amenoma', 'cwish_wname': 'Амэнома Кагэути'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'chernogorgws', 'cwish_wname': 'Черногорская\nбритва'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'ceremonialgsw', 'cwish_wname': 'Церемониальный\nдвуручный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'parhaich', 'cwish_wname': 'Прототип:\nАрхаичный'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'kolokol', 'cwish_wname': 'Меч-колокол'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'swdrackost', 'cwish_wname': 'Меч драконьей\nкости'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'korolgsw', 'cwish_wname': 'Королевский\nдвуручный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'kasturakiri', 'cwish_wname': 'Кацурагикири\nНагамаса'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'kamenniygsw', 'cwish_wname': 'Каменный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'zasnezhennoeser', 'cwish_wname': 'Заснеженное\nзвёздное серебро'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'dozhderez', 'cwish_wname': 'Дождерез'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'favoniygsw', 'cwish_wname': 'Двуручный меч\nФавония'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'blagorodvladyka', 'cwish_wname': 'Благодатный\nвладыка вод'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'belayaten', 'cwish_wname': 'Белая тень'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'akuomaku', 'cwish_wname': 'Акуомару'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'chernogorpika', 'cwish_wname': 'Черногорская\nпика'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'smertboy', 'cwish_wname': 'Смертельный бой'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'rezhushiy', 'cwish_wname': 'Режущий волны\nплавник'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'pzvezdblesk', 'cwish_wname': 'Прототип:\nЗвёздный блеск'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'pikapolumes', 'cwish_wname': 'Пика полумесяца'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'krestkitain', 'cwish_wname': 'Крест-копьё\nКитаин'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'korolewskkop', 'cwish_wname': 'Королевское\nкопьё'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'favoniuskopie', 'cwish_wname': 'Копьё Фавония'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'drakoniyhrebet', 'cwish_wname': 'Копьё Драконьего\nхребта'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'kamennoekop', 'cwish_wname': 'Каменное копьё'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'grozadrakonov', 'cwish_wname': 'Гроза драконов'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'ulov', 'cwish_wname': 'Улов'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'chernogorbow', 'cwish_wname': 'Черногорский\nбоевой лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'ceremonualbow', 'cwish_wname': 'Церемониальный\nлук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'hishnik', 'cwish_wname': 'Хищник'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'hamaumi', 'cwish_wname': 'Хамаюми'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'sostavnoybow', 'cwish_wname': 'Составной лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'rzhavyi', 'cwish_wname': 'Ржавый лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'ppolumesac', 'cwish_wname': 'Прототип:\nПолумесяц'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'ohotnikvotme', 'cwish_wname': 'Охотник во тьме'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'odaanemonii', 'cwish_wname': 'Ода анемонии'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'lunamoun', 'cwish_wname': 'Луна Моун'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'korolevbow', 'cwish_wname': 'Королевский лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'zelenbow', 'cwish_wname': 'Зелёный лук'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'valsnirvany', 'cwish_wname': 'Вальс Нирваны\nНочи'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'favoniybow', 'cwish_wname': 'Боевой лук\nФавония'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'besstrunniy', 'cwish_wname': 'Бесструнный'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'sumekri', 'cwish_wname': 'Гаснущие\nсумерки'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'chernogorcat', 'cwish_wname': 'Черногорский\nагат'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'ceremonmemuary', 'cwish_wname': 'Церемониальные\nмемуары'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'solzhemchuzh', 'cwish_wname': 'Солнечная\nжемчужина'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'pyzntar', 'cwish_wname': 'Прототип:\nЯнтарь'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'plodmerzloty', 'cwish_wname': 'Плод вечной\nмерзлоты'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'pesnstrannika', 'cwish_wname': 'Песнь странника'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'okosoananiya', 'cwish_wname': 'Око сознания'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'okoklatvy', 'cwish_wname': 'Око клятвы'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'morskoyatlas', 'cwish_wname': 'Морской атлас'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'korolgrimuar', 'cwish_wname': 'Королевский\nгримуар'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'hakusin', 'cwish_wname': 'Кольцо Хакусин'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'favoniykodex', 'cwish_wname': 'Кодекс Фавония'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'dodoko', 'cwish_wname': 'Истории Додоко'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'vinoipesni', 'cwish_wname': 'Вино и песни'}
                ],
                'char': [
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'amber', 'cwish_wname': 'Эмбер'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'barbara', 'cwish_wname': 'Барбара'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'beidou', 'cwish_wname': 'Бэй Доу'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'bennett', 'cwish_wname': 'Беннет'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'chongyun', 'cwish_wname': 'Чун Юнь'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'diona', 'cwish_wname': 'Диона'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'fischl', 'cwish_wname': 'Фишль'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'goro', 'cwish_wname': 'Горо'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'kaeya', 'cwish_wname': 'Кэйа'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'lisa', 'cwish_wname': 'Лиза'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'ningguang', 'cwish_wname': 'Нин Гуан'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'noelle', 'cwish_wname': 'Ноэлль'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'razor', 'cwish_wname': 'Рэйзор'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'rosaria', 'cwish_wname': 'Розария'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'sara', 'cwish_wname': 'Кудзё Сара'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'sayu', 'cwish_wname': 'Саю'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'sucrose', 'cwish_wname': 'Сахароза'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'thoma', 'cwish_wname': 'Тома'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'xianling', 'cwish_wname': 'Сян Лин'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'xingqiu', 'cwish_wname': 'Син Цю'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'xinyan', 'cwish_wname': 'Синь Янь'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'yanfei', 'cwish_wname': 'Янь Фэй'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'yunjin', 'cwish_wname': 'Юнь Цзинь'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'shinobu', 'cwish_wname': 'Куки Синобу'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'heizo', 'cwish_wname': 'Сиканоин Хэйдзо'}
                ]
        },
        '5': {
                'weapon': [
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'haran', 'cwish_wname': 'Харан гэппаку\nфуцу'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'tuman', 'cwish_wname': 'Рассекающий туман'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'nebesmech', 'cwish_wname': 'Небесный меч'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'sokol', 'cwish_wname': 'Меч Сокола'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'kromsateld', 'cwish_wname': 'Кромсатель пиков'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'klyatwa', 'cwish_wname': 'Клятва свободы'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'sw', 'cwish_cname': 'omut', 'cwish_wname': 'Драгоценный омут'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'pesnsosen', 'cwish_wname': 'Песнь разбитых\nсосен'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'nekovaniy', 'cwish_wname': 'Некованый'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'nebesnoyvel', 'cwish_wname': 'Небесное величие'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'krasnorog', 'cwish_wname': 'Краснорогий\nкамнеруб'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'gsw', 'cwish_cname': 'volchuya', 'cwish_wname': 'Волчья погибель'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'usmiritelbed', 'cwish_wname': 'Усмиритель бед'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'sizushayazhatva', 'cwish_wname': 'Сияющая жатва'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'homa', 'cwish_wname': 'Посох Хомы'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'pokoritel', 'cwish_wname': 'Покоритель вихря'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'nefritkorshun', 'cwish_wname': 'Нефритовый коршун'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'pol', 'cwish_cname': 'nebesnayaos', 'cwish_wname': 'Небесная ось'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'elegiyapogib', 'cwish_wname': 'Элегия погибели'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'polarzvezda', 'cwish_wname': 'Полярная звезда'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'nebeskrylo', 'cwish_wname': 'Небесное крыло'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'amos', 'cwish_wname': 'Лук Амоса'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'grompulse', 'cwish_wname': 'Громовой пульс'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'bow', 'cwish_cname': 'aquasimul', 'cwish_wname': 'Аква симулякрум'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'pamatopily', 'cwish_wname': 'Память о пыли'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'nebesatlas', 'cwish_wname': 'Небесный атлас'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'molitvavetram', 'cwish_wname': 'Молитва святым\nветрам'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'istinakagura', 'cwish_wname': 'Истина кагура'},
                        {'cwish_wtype': 'weapon', 'cwish_wmetatype': 'weapon', 'cwish_wmetaelem': 'cat', 'cwish_cname': 'vechnoyesiyanie', 'cwish_wname': 'Вечное лунное\nсияние'}
                ],
                'char': [
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'albedo', 'cwish_wname': 'Альбедо'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'ayaka', 'cwish_wname': 'Камисато Аяка'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'ayto', 'cwish_wname': 'Камисато Аято'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'diluc', 'cwish_wname': 'Дилюк'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'eula', 'cwish_wname': 'Эола'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'ganyu', 'cwish_wname': 'Гань Юй'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'hutao', 'cwish_wname': 'Ху Тао'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'itto', 'cwish_wname': 'Аратаки Итто'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'jean', 'cwish_wname': 'Джинн'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'kazuha', 'cwish_wname': 'Каэдэхара Кадзуха'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'keqing', 'cwish_wname': 'Кэ Цин'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'klee', 'cwish_wname': 'Кли'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'kokomi', 'cwish_wname': 'Кокоми'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'miko', 'cwish_wname': 'Яэ Мико'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'mona', 'cwish_wname': 'Мона'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'qiqi', 'cwish_wname': 'Ци Ци'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'electro', 'cwish_cname': 'raiden', 'cwish_wname': 'Райдэн'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'shenhe', 'cwish_wname': 'Шэнь Хэ'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'tartaglia', 'cwish_wname': 'Тарталья'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'venti', 'cwish_wname': 'Венти'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'anemo', 'cwish_cname': 'xiao', 'cwish_wname': 'Сяо'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'pyro', 'cwish_cname': 'yoimiya', 'cwish_wname': 'Ёимия'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'geo', 'cwish_cname': 'zhongli', 'cwish_wname': 'Чжун Ли'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'cryo', 'cwish_cname': 'aloy', 'cwish_wname': 'Элой'},
                        {'cwish_wtype': 'char', 'cwish_wmetatype': 'element', 'cwish_wmetaelem': 'hydro', 'cwish_cname': 'elan', 'cwish_wname': 'Е Лань'}
                ]
        }
}