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
                     "banner",
                     "chat_bot",
                     "event_bot",
                     "animations",
                     "sound",
                     "history_file",
                     "gbot_config",
                     "send_dev_stats",
                     "test_mode"
                     ],
        "additionalProperties": False,
        "properties": {
                "window_name": {"type": "string"},
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
                                "end_delay_multi",
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
                                "end_delay_multi": {
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
                "language": {
                        "type": "object",
                        "required": [
                                "text",
                                "wish_items",
                                "messages",
                                "html_template"
                        ],
                        "additionalProperties": False,
                        "properties": {
                                "text": {"type": "string"},
                                "wish_items": {"type": "string"},
                                "messages": {"type": "string"},
                                "html_template": {"type": "string"}
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
                "channel_points_text"
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
                "channel_points_text": {
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
                     "lang"
                     ],
        "additionalProperties": False,
        "properties": {
                "banner_name": {"type": "string"},
                "wish_fo_garant": {"type": "number"},
                "wish_fo_chance": {"type": "number"},
                "wish_fi_garant": {"type": "number"},
                "wish_fi_chance": {"type": "number"},
                "wish_fi_soft_a": {"type": "number"},
                "lang": {"type": "string"},
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

DATABASE_TEXT = {}

TEXT = {}

DATABASE = {
        '3': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'holodnoelezvie'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fileynozh'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'temniyzhsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'predvestnik'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swputeshest'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swvsadnik'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'beloezhelezogsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dragonbloodgsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'metalten'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dubinapereg'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'bolshounebes'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernayakist'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'belayakist'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'alebardamilelith'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rogatka'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'posulniy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'voronbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'klatvastrelka'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'izognutbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'eposdrakon'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'rukovodmagiya'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'potustoristor'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'parniynefrit'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'izumrudshar'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'yantzhemg'},
                ],
                'char': []
        },
        '4': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'chernogorsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'cherniysw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'ceremonialsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'stalnoezh'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'pzloba'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'oskzhelanie'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fleyta'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'favoniy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nishozhdeniesw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'aristokratsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kinowarsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'dragonroar'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'vspishka'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'amenoma'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladesw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladerawsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladenowsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'woodsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'lunnoesyanie'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'zloyzont'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'chernogorgws'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'ceremonialgsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'parhaich'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kolokol'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'swdrackost'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'korolgsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kasturakiri'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kamenniygsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'zasnezhennoeser'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dozhderez'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'favoniygsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'blagorodvladyka'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'belayaten'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'akuomaku'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'woodgsw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'akwamarinmaxar'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernogorpika'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'smertboy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'rezhushiy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pzvezdblesk'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pikapolumes'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'krestkitain'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'korolewskkop'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'favoniuskopie'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'drakoniyhrebet'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'kamennoekop'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'grozadrakonov'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'ulov'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'woodpol'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'peremenvetrov'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'chernogorbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ceremonualbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hishnik'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hamaumi'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sostavnoybow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rzhavyi'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ppolumesac'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ohotnikvotme'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'odaanemonii'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'lunamoun'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'korolevbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'zelenbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'valsnirvany'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'favoniybow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'besstrunniy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sumekri'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'woodbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'dolphbow'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'chernogorcat'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'ceremonmemuary'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'solzhemchuzh'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pyzntar'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'plodmerzloty'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pesnstrannika'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okosoananiya'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okoklatvy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'morskoyatlas'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'korolgrimuar'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'hakusin'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'favoniykodex'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'dodoko'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vinoipesni'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'woodcat'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'skitzvezda'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'balladoffyjarods'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'finaleofthedeep'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fleuvecendre'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'flowingpurity'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'gswmailedflower'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ibispiecer'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'righfulreward'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'sacrificialjade'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'scionblazingsun'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'songofstilness'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'talkingsting'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'tidalshado'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'wolffang'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'balladboundless'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'dockhandassist'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'powersaw'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'prospectorfrill'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rangegauge'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbruh_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean_skin2'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'nina_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keka_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'amber_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'rosaria_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'mona_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'kaeya_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'klee_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ayaka_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'amber'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbara'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'beidou'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'bennett'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'chongyun'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'diona'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'goro'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'kaeya'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'lisa'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'ningguang'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'noelle'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'razor'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'rosaria'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'sara'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sayu'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sucrose'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'thoma'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xianling'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'xingqiu'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xinyan'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yanfei'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'yunjin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'shinobu'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'heizo'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'dori'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'collei'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'candace'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'layla'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'faruzan'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'freminet'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'kaveh'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'linette'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'yaoyao'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'momoka'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'mika'}
                ]
        },
        '5': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'haran'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'tuman'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nebesmech'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'sokol'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kromsateld'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'klyatwa'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'omut'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'ierofankey'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'pesnsosen'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nekovaniy'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nebesnoyvel'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'krasnorog'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'volchuya'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'usmiritelbed'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'sizushayazhatva'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'homa'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pokoritel'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nefritkorshun'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nebesnayaos'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'alyhpeskov'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'elegiyapogib'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'polarzvezda'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'nebeskrylo'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'amos'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'grompulse'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'aquasimul'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'huntertrope'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pamatopily'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'nebesatlas'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'molitvavetram'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'istinakagura'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vechnoyesiyanie'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'snovidenysnochey'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'catkolokol'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'firstmagickfreat'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'gswbeaconreedsea'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'jadefallplender'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swfoliarincosion'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'cashflowvision'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'eternalflow'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'albedo'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ayaka'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'ayto'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'eula'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ganyu'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'hutao'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'itto'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'kazuha'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keqing'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'klee'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'kokomi'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'miko'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'mona'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'qiqi'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'raiden'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'shenhe'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'tartaglia'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'venti'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'xiao'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yoimiya'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'zhongli'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'aloy'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'elan'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'tighnari'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'nilou'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'cyno'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'nahida'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'wanderer'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'alhatham'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'baizhuer'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'dehya'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'liney'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'neuvillette'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'wriothesley'}
                ]
        }
}

HTML_HISTORY_TEMPLATE_TABLE = r'{ date: "{{ wish_date }}", user: "{{ wish_user }}", count: "{{ wish_count }}", type: "{{ wish_type }}", name: "{{ wish_name }}", star: "{{ wish_style_color }}" },'
