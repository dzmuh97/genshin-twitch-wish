CONFIG_SCHEMA = {
        "type": "object",
        "required": ["window_name",
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
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'holodnoelezvie', 'wish_obj_text': '???????????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fileynozh', 'wish_obj_text': '???????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'temniyzhsw', 'wish_obj_text': '???????????? ????????????????\n??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'predvestnik', 'wish_obj_text': '?????????????????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swputeshest', 'wish_obj_text': '??????\n??????????????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'swvsadnik', 'wish_obj_text': '?????? ??????????????????\n????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'beloezhelezogsw', 'wish_obj_text': '?????? ???? ????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dragonbloodgsw', 'wish_obj_text': '?????? ??????????????????\n??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'metalten', 'wish_obj_text': '??????????????????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dubinapereg', 'wish_obj_text': '???????????? ??????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'bolshounebes', 'wish_obj_text': '?????????????? ??????\n?????????????????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernayakist', 'wish_obj_text': '???????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'belayakist', 'wish_obj_text': '?????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'alebardamilelith', 'wish_obj_text': '???????????????? ??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rogatka', 'wish_obj_text': '??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'posulniy', 'wish_obj_text': '??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'voronbow', 'wish_obj_text': '?????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'klatvastrelka', 'wish_obj_text': '???????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'izognutbow', 'wish_obj_text': '?????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'eposdrakon', 'wish_obj_text': '???????? ??\n??????????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'rukovodmagiya', 'wish_obj_text': '??????????????????????\n???? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'potustoristor', 'wish_obj_text': '??????????????????????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'parniynefrit', 'wish_obj_text': '???????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'izumrudshar', 'wish_obj_text': '???????????????????? ??????'}
                ],
                'char': []
        },
        '4': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'chernogorsw', 'wish_obj_text': '????????????????????????\n?????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'cherniysw', 'wish_obj_text': '???????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'ceremonialsw', 'wish_obj_text': '????????????????????????????\n??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'stalnoezh', 'wish_obj_text': '???????????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'pzloba', 'wish_obj_text': '????????????????: ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'oskzhelanie', 'wish_obj_text': '????????????????????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'fleyta', 'wish_obj_text': '??????-????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'favoniy', 'wish_obj_text': '?????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nishozhdeniesw', 'wish_obj_text': '?????? ??????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'aristokratsw', 'wish_obj_text': '?????? ????????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kinowarsw', 'wish_obj_text': '????????????????????\n????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'dragonroar', 'wish_obj_text': '???????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'vspishka', 'wish_obj_text': '?????????????? ???? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'amenoma', 'wish_obj_text': '?????????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladesw', 'wish_obj_text': '??????????????????????\n???????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladerawsw', 'wish_obj_text': '??????????????????????\n???????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'issinbladenowsw', 'wish_obj_text': '????????????????????\n??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'woodsw', 'wish_obj_text': '????????????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'chernogorgws', 'wish_obj_text': '????????????????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'ceremonialgsw', 'wish_obj_text': '????????????????????????????\n?????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'parhaich', 'wish_obj_text': '????????????????:\n??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kolokol', 'wish_obj_text': '??????-??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'swdrackost', 'wish_obj_text': '?????? ??????????????????\n??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'korolgsw', 'wish_obj_text': '??????????????????????\n?????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kasturakiri', 'wish_obj_text': '????????????????????????\n????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'kamenniygsw', 'wish_obj_text': '???????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'zasnezhennoeser', 'wish_obj_text': '??????????????????????\n???????????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'dozhderez', 'wish_obj_text': '????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'favoniygsw', 'wish_obj_text': '?????????????????? ??????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'blagorodvladyka', 'wish_obj_text': '??????????????????????\n?????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'belayaten', 'wish_obj_text': '?????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'akuomaku', 'wish_obj_text': '????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'woodgsw', 'wish_obj_text': '?????????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'chernogorpika', 'wish_obj_text': '????????????????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'smertboy', 'wish_obj_text': '?????????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'rezhushiy', 'wish_obj_text': '?????????????? ??????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pzvezdblesk', 'wish_obj_text': '????????????????:\n???????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pikapolumes', 'wish_obj_text': '???????? ????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'krestkitain', 'wish_obj_text': '??????????-??????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'korolewskkop', 'wish_obj_text': '??????????????????????\n??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'favoniuskopie', 'wish_obj_text': '?????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'drakoniyhrebet', 'wish_obj_text': '?????????? ????????????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'kamennoekop', 'wish_obj_text': '???????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'grozadrakonov', 'wish_obj_text': '?????????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'ulov', 'wish_obj_text': '????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'woodpol', 'wish_obj_text': '????????????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'chernogorbow', 'wish_obj_text': '????????????????????????\n???????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ceremonualbow', 'wish_obj_text': '????????????????????????????\n??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hishnik', 'wish_obj_text': '????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'hamaumi', 'wish_obj_text': '??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sostavnoybow', 'wish_obj_text': '?????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'rzhavyi', 'wish_obj_text': '???????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ppolumesac', 'wish_obj_text': '????????????????:\n??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'ohotnikvotme', 'wish_obj_text': '?????????????? ???? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'odaanemonii', 'wish_obj_text': '?????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'lunamoun', 'wish_obj_text': '???????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'korolevbow', 'wish_obj_text': '?????????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'zelenbow', 'wish_obj_text': '?????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'valsnirvany', 'wish_obj_text': '?????????? ??????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'favoniybow', 'wish_obj_text': '???????????? ??????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'besstrunniy', 'wish_obj_text': '??????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'sumekri', 'wish_obj_text': '????????????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'woodbow', 'wish_obj_text': '????????????????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'dolphbow', 'wish_obj_text': '????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'chernogorcat', 'wish_obj_text': '????????????????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'ceremonmemuary', 'wish_obj_text': '????????????????????????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'solzhemchuzh', 'wish_obj_text': '??????????????????\n??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pyzntar', 'wish_obj_text': '????????????????:\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'plodmerzloty', 'wish_obj_text': '???????? ????????????\n????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pesnstrannika', 'wish_obj_text': '?????????? ??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okosoananiya', 'wish_obj_text': '?????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'okoklatvy', 'wish_obj_text': '?????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'morskoyatlas', 'wish_obj_text': '?????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'korolgrimuar', 'wish_obj_text': '??????????????????????\n??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'hakusin', 'wish_obj_text': '???????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'favoniykodex', 'wish_obj_text': '???????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'dodoko', 'wish_obj_text': '?????????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vinoipesni', 'wish_obj_text': '???????? ?? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'woodcat', 'wish_obj_text': '???????? ??????????????????????'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbruh_skin', 'wish_obj_text': '???????????? ??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean_skin', 'wish_obj_text': '?????? ????????????????\n??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'nina_skin', 'wish_obj_text': '???????? ??????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keka_skin', 'wish_obj_text': '?????????? ????????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'amber', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbara', 'wish_obj_text': '??????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'beidou', 'wish_obj_text': '?????? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'bennett', 'wish_obj_text': '????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'chongyun', 'wish_obj_text': '?????? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'diona', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl_skin', 'wish_obj_text': '?????? ????????????\n????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'goro', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'kaeya', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'lisa', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'ningguang', 'wish_obj_text': '?????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'noelle', 'wish_obj_text': '????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'razor', 'wish_obj_text': '????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'rosaria', 'wish_obj_text': '??????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'sara', 'wish_obj_text': '?????????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sayu', 'wish_obj_text': '??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'sucrose', 'wish_obj_text': '????????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'thoma', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xianling', 'wish_obj_text': '?????? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'xingqiu', 'wish_obj_text': '?????? ????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'xinyan', 'wish_obj_text': '???????? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yanfei', 'wish_obj_text': '?????? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'yunjin', 'wish_obj_text': '?????? ??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'shinobu', 'wish_obj_text': '???????? ????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'heizo', 'wish_obj_text': '???????????????? ????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'dori', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'collei', 'wish_obj_text': '????????????'}
                ]
        },
        '5': {
                'weapon': [
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'haran', 'wish_obj_text': '?????????? ??????????????\n????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'tuman', 'wish_obj_text': '?????????????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'nebesmech', 'wish_obj_text': '???????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'sokol', 'wish_obj_text': '?????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'kromsateld', 'wish_obj_text': '???????????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'klyatwa', 'wish_obj_text': '???????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'sw', 'wish_obj_name': 'omut', 'wish_obj_text': '?????????????????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'pesnsosen', 'wish_obj_text': '?????????? ????????????????\n??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nekovaniy', 'wish_obj_text': '??????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'nebesnoyvel', 'wish_obj_text': '???????????????? ??????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'krasnorog', 'wish_obj_text': '??????????????????????\n????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'gsw', 'wish_obj_name': 'volchuya', 'wish_obj_text': '???????????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'usmiritelbed', 'wish_obj_text': '???????????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'sizushayazhatva', 'wish_obj_text': '?????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'homa', 'wish_obj_text': '?????????? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'pokoritel', 'wish_obj_text': '???????????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nefritkorshun', 'wish_obj_text': '???????????????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'pol', 'wish_obj_name': 'nebesnayaos', 'wish_obj_text': '???????????????? ??????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'elegiyapogib', 'wish_obj_text': '???????????? ????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'polarzvezda', 'wish_obj_text': '???????????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'nebeskrylo', 'wish_obj_text': '???????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'amos', 'wish_obj_text': '?????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'grompulse', 'wish_obj_text': '???????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'aquasimul', 'wish_obj_text': '???????? ????????????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'bow', 'wish_obj_name': 'huntertrope', 'wish_obj_text': '?????????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'pamatopily', 'wish_obj_text': '???????????? ?? ????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'nebesatlas', 'wish_obj_text': '???????????????? ??????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'molitvavetram', 'wish_obj_text': '?????????????? ????????????\n????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'istinakagura', 'wish_obj_text': '???????????? ????????????'},
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'vechnoyesiyanie', 'wish_obj_text': '???????????? ????????????\n????????????'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'albedo', 'wish_obj_text': '??????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ayaka', 'wish_obj_text': '???????????????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'ayto', 'wish_obj_text': '???????????????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc_skin', 'wish_obj_text': '???????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'eula', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ganyu', 'wish_obj_text': '???????? ????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'hutao', 'wish_obj_text': '???? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'itto', 'wish_obj_text': '?????????????? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'kazuha', 'wish_obj_text': '??????????????????\n??????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keqing', 'wish_obj_text': '???? ??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'klee', 'wish_obj_text': '??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'kokomi', 'wish_obj_text': '????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'miko', 'wish_obj_text': '???? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'mona', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'qiqi', 'wish_obj_text': '???? ????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'raiden', 'wish_obj_text': '????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'shenhe', 'wish_obj_text': '???????? ????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'tartaglia', 'wish_obj_text': '????????????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'venti', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'xiao', 'wish_obj_text': '??????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'yoimiya', 'wish_obj_text': '??????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'zhongli', 'wish_obj_text': '???????? ????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'aloy', 'wish_obj_text': '????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'elan', 'wish_obj_text': '?? ????????'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'tighnari', 'wish_obj_text': '??????????????'}
                ]
        }
}

HTML_HISTORY_TEMPLATE_HEADER = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Genshin Twitch Wish Simulator</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.2.0/mdb.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;900&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #25294a;
        }

        .star3 {
            color: #4e7cff;
        }

        .star4 {
            color: #d28fd6;
        }

        .star5 {
            color: #ffb13f;
        }

        thead {
            color: #cbd5e0;
        }

        .stats_table_data {
            font-size: 80px;
            font-weight: 900;
            font-family: 'Montserrat', sans-serif;
            line-height: 50px;
        }

        .star_table_data {
            font-size: 30px;
            font-weight: 900;
            font-family: 'Montserrat', sans-serif;
            line-height: 15px;
        }

        .main_table_data {
            line-height: 12px;
        }
    </style>
</head>
<body>
<div class="row justify-content-center">
<div class="col-auto">
    <table class="table table-sm table-borderless text-center text-white border-light">
      <thead>
        <tr>
            <th scope="col" class="fw-bold">?????????? ????????????</th>
            <th scope="col" class="fw-bold">???????????????????? ??????????????????</th>
        </tr>
      </thead>
      <tbody>
'''

HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STATS = '''
        <tr class="stats_table_data">
            <td>{total_wish}</td>
            <td>{total_gems}</td>
        </tr>
'''

HTML_HISTORY_TEMPLATE_HEAD_TABLE_STATS_PRE = '''</tbody>
    </table>
    <table class="table table-sm table-borderless text-center text-white border-light">
      <thead>
        <tr>
            <th scope="col" class="fw-bold">?????????? 3???</th>
            <th scope="col" class="fw-bold">?????????? 4???</th>
            <th scope="col" class="fw-bold">?????????? 5???</th>
        </tr>
      </thead>
      <tbody>
'''

HTML_HISTORY_TEMPLATE_HEAD_TABLE_ROW_STARS = '''<tr class="star_table_data">
            <td class="star3">{total_wish3}</td>
            <td class="star4">{total_wish4}</td>
            <td class="star5">{total_wish5}</td>
        </tr>
'''

HTML_HISTORY_TEMPLATE_HEAD_TABLE_END = '''</tbody>
    </table>
    <table class="table table-sm table-borderless text-center text-white border-light">
      <thead>
        <tr>
            <th scope="col" class="fw-bold">????????</th>
            <th scope="col" class="fw-bold">??????</th>
            <th scope="col" class="fw-bold">??????????????</th>
            <th scope="col" class="fw-bold">????????????</th>
            <th scope="col" class="fw-bold">????????????????</th>
        </tr>
      </thead>
      <tbody class="main_table_data">
'''

HTML_HISTORY_TEMPLATE_MAIN_TABLE_ROW = '''
<tr><td>{wish_date}</td><td>{wish_user}</td><td>{wish_count}</td><td>{wish_type}</td><td class="{wish_style_color}">{wish_name}</td></tr>
'''

HTML_HISTORY_TEMPLATE_END = '''
      </tbody>
    </table>
</div>
</div>
</body>
</html>
'''
