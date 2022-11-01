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

DATABASE_TEXT = {
        # 3 SW
        'holodnoelezvie':       'Cool Steel',
        'fileynozh':            'Fillet Blade',
        'temniyzhsw':           'Dark Iron\nSword',
        'predvestnik':          'Harbinger\nof Dawn',
        'swputeshest':          'Traveler’s\nHandy Sword',
        'swvsadnik':            'Skyrider Sword',
        # 3 GSW
        'beloezhelezogsw':      'White Iron\nGreatsword',
        'dragonbloodgsw':       'Bloodtainted\nGreatsword',
        'metalten':             'Ferrous Shadow',
        'dubinapereg':          'Debate Club',
        'bolshounebes':         'Skyrider\nGreatsword',
        # 3 POL
        'chernayakist':         'Black Tassel',
        'belayakist':           'White Tassel',
        'alebardamilelith':     'Halberd',
        # 3 BOW
        'rogatka':              'Slingshot',
        'posulniy':             'Messenger',
        'voronbow':             'Raven Bow',
        'klatvastrelka':        'Sharpshooter’s\nOath',
        'izognutbow':           'Recurve Bow',
        # 3 CAT
        'eposdrakon':           'Thrilling Tales\nof Dragon Slayers',
        'rukovodmagiya':        'Magic Guide',
        'potustoristor':        'Otherworldly\nStory',
        'parniynefrit':         'Twin Nephrite',
        'izumrudshar':          'Emerald Orb',
        'yantzhemg':            'Amber Bead',
        # 4 SW
        'chernogorsw':          'Blackcliff\nLongsword',
        'cherniysw':            'The Black\nSword',
        'ceremonialsw':         'Sacrificial\nSword',
        'stalnoezh':            'Iron Sting',
        'pzloba':               'Prototype\nRancour',
        'oskzhelanie':          'Festering\nDesire',
        'fleyta':               'The Flute',
        'favoniy':              'Favonius Sword',
        'nishozhdeniesw':       'Sword of\nDescension',
        'aristokratsw':         'Royal Longsword',
        'kinowarsw':            'Cinnabar\nSpindle',
        'dragonroar':           'Lion’s Roar',
        'vspishka':             'The Alley\nFlash',
        'amenoma':              'Amenoma Kageuchi',
        'issinbladesw':         'Prized\nIsshin Blade',
        'issinbladerawsw':      'Prized\nIsshin Blade',
        'issinbladenowsw':      'Kagotsurube\nIsshin',
        'woodsw':               'Sapwood Blade',
        'lunnoesyanie':         'Xiphos’\nMoonlight',
        # 4 GSW
        'chernogorgws':         'Blackcliff\nSlasher',
        'ceremonialgsw':        'Sacrificial\nGreatsword',
        'parhaich':             'Prototype\nArchaic',
        'kolokol':              'The Bell',
        'swdrackost':           'Serpent Spine',
        'korolgsw':             'Royal\nGreatsword',
        'kasturakiri':          'Katsuragikiri\nNagamasa',
        'kamenniygsw':          'Lithic Blade',
        'zasnezhennoeser':      'Snow-Tombed\nStarsilver',
        'dozhderez':            'Rainslasher',
        'favoniygsw':           'Favonius\nGreatsword',
        'blagorodvladyka':      'Luxurious\nSea-Lord',
        'belayaten':            'Whiteblind',
        'akuomaku':             'Akuoumaru',
        'woodgsw':              'Forest Regalia',
        'akwamarinmaxar':       'Makhaira\nAquamarine',
        'chernogorpika':        'Blackcliff Pole',
        'smertboy':             'Deathmatch',
        'rezhushiy':            'Wavebreaker’s\nFin',
        # 4 POL
        'pzvezdblesk':          'Prototype\nStarglitter',
        'pikapolumes':          'Crescent Pike',
        'krestkitain':          'Kitain\nCross Spear',
        'korolewskkop':         'Royal Spear',
        'favoniuskopie':        'Favonius Lance',
        'drakoniyhrebet':       'Dragonspine\nSpear',
        'kamennoekop':          'Lithic Spear',
        'grozadrakonov':        'Dragon’s Bane',
        'ulov':                 '“The Catch”',
        'woodpol':              'Moonpiercer',
        'peremenvetrov':        'Missive\nWindspear',
        # 4 BOW
        'chernogorbow':         'Blackcliff\nWarbow',
        'ceremonualbow':        'Sacrificial\nBow',
        'hishnik':              'Predator',
        'hamaumi':              'Hamayumi',
        'sostavnoybow':         'Compound\nBow',
        'rzhavyi':              'Rust',
        'ppolumesac':           'Prototype\nCrescent',
        'ohotnikvotme':         'Alley Hunter',
        'odaanemonii':          'Windblume Ode',
        'lunamoun':             'Mouun’s Moon',
        'korolevbow':           'Royal Bow',
        'zelenbow':             'The Viridescent\nHunt',
        'valsnirvany':          'Mitternachts\nWaltz',
        'favoniybow':           'Favonius Warbow',
        'besstrunniy':          'The Stringless',
        'sumekri':              'Fading Twilight',
        'woodbow':              'King’s Squire',
        'dolphbow':             'End of the Line',
        # 4 CAT
        'chernogorcat':         'Blackcliff\nAgate',
        'ceremonmemuary':       'Sacrificial\nFragments',
        'solzhemchuzh':         'Solar Pearl',
        'pyzntar':              'Prototype\nAmber',
        'plodmerzloty':         'Frostbearer',
        'pesnstrannika':        'The Widsith',
        'okosoananiya':         'Eye\nof Perception',
        'okoklatvy':            'Oathsworn Eye',
        'morskoyatlas':         'Mappa Mare',
        'korolgrimuar':         'Royal Grimoire',
        'hakusin':              'Hakushin Ring',
        'favoniykodex':         'Favonius Codex',
        'dodoko':               'Dodoco Tales',
        'vinoipesni':           'Wine and Song',
        'woodcat':              'Fruit\nof Fulfillment',
        'skitzvezda':           'Wandering\nEvenstar',
        # 4 SKIN
        'barbruh_skin':         'Summertime\nSparkle',
        'jean_skin':            'Sea Breeze\nDandelion',
        'nina_skin':            'Orchid’s\nEvening Gown',
        'keka_skin':            'Opulent\nSplendor',
        'fischl_skin':          'Ein\nImmernachtstraum',
        # 4 CHAR
        'amber':                'Amber',
        'barbara':              'Barbara',
        'beidou':               'Beidou',
        'bennett':              'Bennett',
        'chongyun':             'Chongyun',
        'diona':                'Diona',
        'fischl':               'Fischl',
        'goro':                 'Gorou',
        'kaeya':                'Kaeya',
        'lisa':                 'Lisa',
        'ningguang':            'Ningguang',
        'noelle':               'Noelle',
        'razor':                'Razor',
        'rosaria':              'Rosaria',
        'sara':                 'Kujou Sara',
        'sayu':                 'Sayu',
        'sucrose':              'Sucrose',
        'thoma':                'Thoma',
        'xianling':             'Xiangling',
        'xingqiu':              'Xingqiu',
        'xinyan':               'Xinyan',
        'yanfei':               'Yanfei',
        'yunjin':               'Yun Jin',
        'shinobu':              'Kuki Shinobu',
        'heizo':                'Shikanoin Heizou',
        'dori':                 'Dori',
        'collei':               'Collei',
        'candace':              'Candace',
        'layla':                'Layla',
        # 5 SW
        'haran':                'Haran Geppaku\nFutsu',
        'tuman':                'Mistsplitter\nReforged',
        'nebesmech':            'Skyward Blade',
        'sokol':                'Aquila Favonia',
        'kromsateld':           'Summit Shaper',
        'klyatwa':              'Freedom-Sworn',
        'omut':                 'Primordial\nJade Cutter',
        'ierofankey':           'Key of Khaj-Nisut',
        # 5 GSW
        'pesnsosen':            'Song\nof Broken Pines',
        'nekovaniy':            'The Unforged',
        'nebesnoyvel':          'Skyward Pride',
        'krasnorog':            'Redhorn\nStonethresher',
        'volchuya':             'Wolf’s Gravestone',
        # 5 POL
        'usmiritelbed':         'Calamity\nQueller',
        'sizushayazhatva':      'Engulfing\nLightning',
        'homa':                 'Staff of Homa',
        'pokoritel':            'Vortex\nVanquisher',
        'nefritkorshun':        'Primordial Jade\nWinged-Spear',
        'nebesnayaos':          'Skyward Spine',
        'alyhpeskov':           'Staff of the\nScarlet Sands',
        # 5 BOW
        'elegiyapogib':         'Elegy for\nthe End',
        'polarzvezda':          'Polar Star',
        'nebeskrylo':           'Skyward Harp',
        'amos':                 'Amos’ Bow',
        'grompulse':            'Thundering\nPulse',
        'aquasimul':            'Aqua Simulacra',
        'huntertrope':          'Hunter’s Path',
        # 5 CAT
        'pamatopily':           'Memory of Dust',
        'nebesatlas':           'Skyward Atlas',
        'molitvavetram':        'Lost Prayer\nto the Sacred Winds',
        'istinakagura':         'Kagura’s Verity',
        'vechnoyesiyanie':      'Everlasting\nMoonglow',
        'snovidenysnochey':     'A Thousand\nFloating Dreams',
        # 5 SKIN
        'diluc_skin':           'Red Dead of Night',
        # 5 CHAR
        'albedo':               'Albedo',
        'ayaka':                'Kamisato Ayaka',
        'ayto':                 'Kamisato Ayato',
        'diluc':                'Diluc',
        'eula':                 'Eula',
        'ganyu':                'Ganyu',
        'hutao':                'Hu Tao',
        'itto':                 'Arataki Itto',
        'jean':                 'Jean',
        'kazuha':               'Kaedehara Kazuha',
        'keqing':               'Keqing',
        'klee':                 'Klee',
        'kokomi':               'Sangonomiya Kokomi',
        'miko':                 'Yae Miko',
        'mona':                 'Mona',
        'qiqi':                 'Qiqi',
        'raiden':               'Raiden Shogun',
        'shenhe':               'Shenhe',
        'tartaglia':            'Tartaglia',
        'venti':                'Venti',
        'xiao':                 'Xiao',
        'yoimiya':              'Yoimiya',
        'zhongli':              'Zhongli',
        'aloy':                 'Aloy',
        'elan':                 'Yelan',
        'tighnari':             'Tighnari',
        'nilou':                'Nilou',
        'cyno':                 'Cyno',
        'nahida':               'Nahida'
}
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
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'skitzvezda'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbruh_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'anemo', 'wish_obj_name': 'jean_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'nina_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'keka_skin'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'amber'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'barbara'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'beidou'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'bennett'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'chongyun'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'diona'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'electro', 'wish_obj_name': 'fischl_skin'},
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
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'layla'}
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
                        {'wish_type': 'weapon', 'wish_meta_type': 'weapon', 'wish_meta_element': 'cat', 'wish_obj_name': 'snovidenysnochey'}
                ],
                'char': [
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'geo', 'wish_obj_name': 'albedo'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'cryo', 'wish_obj_name': 'ayaka'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'hydro', 'wish_obj_name': 'ayto'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc'},
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'pyro', 'wish_obj_name': 'diluc_skin'},
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
                        {'wish_type': 'char', 'wish_meta_type': 'element', 'wish_meta_element': 'dendro', 'wish_obj_name': 'nahida'}
                ]
        }
}

TEXT = {
        'config_check_error_load': '[MAIN] Error loading json file (%s) : %s',
        'config_check_error_check': '[MAIN] Error checking json file (%s) : %s',
        'text_load_not_found': '[MAIN] Translation file not found: %s',
        'text_load_null': '[MAIN] Translation file not specified, use default language',
        'items_load_null': '[MAIN] Items file not specified, use default set',
        'items_load_not_found': '[MAIN] Items file not found: %s',
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
        'token_check_error': 'wrong token or it has expired',
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
        'log_panel_call_chunk_time': '[PANEL] Method "_t_load_chunk" loaded data in %s sec.',
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
        'commands_status': '%s command processing: %s',
        'history_error_c1': '%s streamer\'s wish history recording is turned off :(',
        'history_error_c2': '%s no history of wish yet, try later :(',
        'history_error_c3': '%s you\'re not in the wish history yet, try later :(',
        'history_error_c4': '%s failed to load history, ask streamer to check config file :(',
        'history_error_c5': '%s failed to load history, try later :(',
        'history_error_c6': '%s failed to create history link, try later :(',
        'history_command_reply': '%s wish history: %s',
        'history_all': 'all viewers',
        'html_history_template_not_found': '[HTML] Template for wish history not found: %s',
        'version_success': '[UPDATE] Version information received',
        'version_net_error': '[UPDATE] Failed to get version information: %s',
        'log_version_info': '[UPDATE] web=%s, local=%s',
        'version_outdate': '[UPDATE] Outdated simulator version - installed: %s, available: %s',
        'stats_sended': '[STATS] Statistics sent',
        'stats_error': '[STATS] Failed to send statistics: %s',
        'auth_start_promt': 'Unable to find "auth.json" file, start authorization on Twitch? [y/n]: ',
        'auth_channel_promt': '[AUTH] Enter name of channel where simulator will be used (only nickname, not link to channel): ',
        'auth_channel_error_name': '[AUTH] Channel name contains invalid characters! Press ENTER to continue: ',
        'auth_channel_separ': '[AUTH] Will we use one account for chat-bot and channel points? [y/n]: ',
        'auth_bot_type_both': 'chat-bot and streamer account for channel points',
        'auth_bot_type_chat': 'chat-bot',
        'auth_bot_type_event': 'streamer account for channel points',
        'auth_browser_promt': '\nNow a new tab will be opened in standard web browser\nThis will request access to bot\'s account\nMake sure to check following:\n\n- address in address bar should be: "id.twitch.tv"\n- application name: "Genshin Wish Simulator"\n- on page must be nickname of account that you want to use as bot\n\n>>> Now we are setting up an account for: %s <<<\n\nPress ENTER to begin: ',
        'auth_browser_close': '\n[AUTH] Confirm access in web browser window that opens and press ENTER when you close that window: ',
        'auth_gate_error': '[AUTH] Failed to query gate for a token! Press ENTER to continue: ',
        'auth_token_error': '[AUTH] Failed to create token. The reason was stated in browser window after logging in. Press ENTER to continue: ',
        'auth_create_success': '[AUTH] All went fine, account is set up. Press ENTER to continue: ',
        'auth_end': '\nAccount data is stored in "auth.json"\nDo not pass this file on to anyone and do not show its contents on stream!\nTo start setting up accounts again, simply delete "auth.json" from simulator folder\nPress ENTER to continue: '
}

HTML_HISTORY_TEMPLATE_TABLE = r'<tr class="filtered_items"><td>{{ wish_date }}</td><td>{{ wish_user }}</td><td>{{ wish_count }}</td><td>{{ wish_type }}</td><td class="{{ wish_style_color }}">{{ wish_name }}</td></tr>'
