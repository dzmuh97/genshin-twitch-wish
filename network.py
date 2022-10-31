import os
import sys

import time
import json
import queue
import base64
import random
import string
import chevron
import logging
import threading
import webbrowser

import asyncio
import aiohttp

import twitchio
from twitchio.ext import pubsub
from twitchio.ext import commands

from urllib import parse
from distutils.version import StrictVersion

from functools import wraps

from config import _msg
from config import _log_print
from config import _config_check

from config import __site__
from config import __title__
from config import __version__

from config import CONFIG
from config import LANG_CONFIG

from config import POINTS_TEXT
from config import NOTIFY_TEXT
from config import CHATBOT_TEXT

from config import STATS_MESSAGE
from config import STATUS_MESSAGE

from data import AUTH_SCHEMA
from data import HTML_HISTORY_TEMPLATE_TABLE

from animation import mixer
from animation import Coordinator

from animation import SOUND_IS_WORK

from gacha import Wish
from gacha import Gacha

from db import UserDB

from typing import Dict, List, Tuple, Union, Optional

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

STATE_ALPHABLET = string.ascii_letters + string.digits
TWITCH_APP_CLIENT_ID = '9ykg8n2lg2y808k6veqv6l5o4l0z4e'  # Genshin Wish Simulator

TWITCH_TOKEN_VALIDATE = "https://id.twitch.tv/oauth2/validate"
TWITCH_CODE_URL = 'https://id.twitch.tv/oauth2/authorize'
TWITCH_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'

CHAT_BOT_SCOPES = 'chat:read chat:edit'
EVENT_BOT_SCOPES = 'channel:read:redemptions'
MILTI_BOT_SCOPES = 'chat:read chat:edit channel:read:redemptions'

URL_VERSION = 'https://genshinwishgate.pw/version'

URL_CODE = 'https://genshinwishgate.pw/code_gate'
URL_TOKEN = 'https://genshinwishgate.pw/token_gate/'
URL_TOKEN_REF = 'https://genshinwishgate.pw/refresh'
URL_HISTORY = 'https://genshinwishgate.pw/history'
# URL_HISTORY = 'http://localhost:5555/history'

AUTH_CONFIG = {'chat_bot': {}, 'event_bot': {}}
AUTH_CHAT_BOT = AUTH_CONFIG['chat_bot']
AUTH_EVENT_BOT = AUTH_CONFIG['event_bot']


async def _get_version(local_version) -> None:
    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.get(URL_VERSION) as version_data_raw:
                version_data = await version_data_raw.json()
                logging.debug(_msg('version_success'))
        except aiohttp.ClientSession as ver_error:
            logging.debug(_msg('version_net_error'), ver_error)
            return

    web_version = StrictVersion(version_data['current_version'])
    local_version = StrictVersion(local_version)

    logging.debug(_msg('log_version_info'), web_version, local_version)
    if web_version == local_version:
        return

    _log_print(_msg('version_outdate') % (local_version, web_version))


async def _send_stats(chat_bot_work_channel: str, event_bot_work_channel_id: str, version: str) -> None:
    stats_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stats_data = {'date': stats_time, 'version': version, 'channel': chat_bot_work_channel, 'channel_id': event_bot_work_channel_id}
    stats_data_json = json.dumps(stats_data)
    stat_base64 = base64.urlsafe_b64encode(stats_data_json.encode(encoding='utf-8')).decode(encoding='utf-8')

    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.post(URL_VERSION, json={'base64data': stat_base64}) as _:
                logging.debug(_msg('stats_sended'))
        except aiohttp.ClientError as stats_error:
            logging.debug(_msg('stats_error'), stats_error)


def _threaded_fork(chat_bot_work_channel, event_bot_work_channel_id, version) -> None:
    async def _fork():
        await _send_stats(chat_bot_work_channel, event_bot_work_channel_id, version)
        await _get_version(version)

    asyncio.run(_fork())


async def _get_tw_data(state) -> None:
    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.get(URL_TOKEN + state) as twitch_user_data_raw:
                twitch_user_data = await twitch_user_data_raw.json()
        except aiohttp.ClientError as gate_error:
            _log_print(gate_error)
            return None

    return twitch_user_data


def update_auth() -> None:
    with open('auth.json', 'r', encoding='utf-8') as authf:
        jdata = json.load(authf)

    jdata.update({'chat_bot': AUTH_CHAT_BOT})
    jdata.update({'event_bot': AUTH_EVENT_BOT})

    with open('auth.json', 'w', encoding='utf-8') as authf:
        json.dump(jdata, authf)


async def refresh_bot_token(ref_token: str) -> bool:
    _log_print(_msg('token_refresh_try'))

    refresh_session = aiohttp.ClientSession()
    try:
        async with refresh_session.post(URL_TOKEN_REF, json={'ref_token': ref_token}) as twitch_user_data_raw:
            twitch_user_data = await twitch_user_data_raw.json()
    except aiohttp.ClientError as gate_error:
        _log_print(_msg('token_refresh_error'), gate_error)
        return False

    token_error = twitch_user_data.get('error')
    if not (token_error is None):
        _log_print(_msg('token_refresh_error'), token_error)
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

    _log_print(_msg('token_refresh_ok'))
    update_auth()
    return True


async def _tokens_check(bot: commands.Bot) -> bool:
    _log_print(_msg('twitch_bots_check'))

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
        headers = {'Authorization': 'OAuth %s' % current_token}

        try:
            async with twitch_session.get(TWITCH_TOKEN_VALIDATE, headers=headers) as twitch_resp:
                if twitch_resp.status == 401:
                    raise aiohttp.ClientError(_msg('token_check_error'))
                if twitch_resp.status > 300 or twitch_resp.status < 200:
                    twitch_error_text = await twitch_resp.text()
                    _log_print(_msg('twitch_token_check_error') % twitch_error_text)
                    return False
                twitch_token_data = await twitch_resp.json()
        except aiohttp.ClientError as twitch_error:
            _log_print(_msg('twitch_auth_error'), twitch_error)
            refresh_satus = await refresh_bot_token(current_token_ref)
            if not refresh_satus:
                _log_print(_msg('twitch_empty_format') % ('-' * 80))
                _log_print(_msg('twitch_backend_error_note'))
                _log_print(_msg('twitch_empty_format') % ('-' * 80))
                threading.Event().wait()
            return False

        login = twitch_token_data['login']
        expires = twitch_token_data['expires_in']
        _log_print(_msg('twitch_token_expire_notify') % (login, expires))

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


def render_html_history(filter_nick: str, streamer_nick: str) -> Tuple[int, str]:
    history_cfg = CONFIG['history_file']
    history_enabled = history_cfg['enabled']
    if not history_enabled:
        return -1, ''

    history_path = history_cfg['path']
    if not os.path.exists(history_path):
        return -2, ''

    tmpl_file = LANG_CONFIG['html_template']
    tmpl_path = os.path.join('text', tmpl_file)
    if not os.path.exists(tmpl_path):
        _log_print(_msg('html_history_template_not_found') % tmpl_path)
        return -4, ''

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

    html_rows = ''

    with open(history_path, 'r', encoding='utf-8') as fp:
        for line_num, history_line in enumerate(fp):
            if line_num == 0:  # skip header
                continue

            history_data = history_line.strip().split(',')
            wdate, nickname, _, star, wish_type, wish_name = history_data

            if filter_nick and (filter_nick != nickname.lower()):
                continue

            wish_style = style_map[star]

            if star == '3':
                total_3 += 1

            if star == '4':
                total_4 += 1

            if star == '5':
                total_5 += 1

            table_row_params = dict(
                wish_date=wdate.replace('-', ' '),
                wish_user=nickname,
                wish_count='1' if star == '3' else wishes_map[star],
                wish_type=wish_type,
                wish_style_color=wish_style,
                wish_name=wish_name
            )
            table_row = chevron.render(HTML_HISTORY_TEMPLATE_TABLE, table_row_params)
            html_rows += table_row

            for wish_star in wishes_map:
                wishes_map[wish_star] += 1

            wishes_map[star] = 1
            total += 1

    if total == 0:
        return -3, ''

    total_gems = total * 160

    with open(tmpl_path, 'r', encoding='utf-8') as _tmpl_f:
        html_template = _tmpl_f.read()

    html_params = dict(
        proj_ver=__version__,
        user=filter_nick if filter_nick else _msg('history_all'),
        owner=streamer_nick,
        total_wish=total,
        total_gems=total_gems,
        total_wish3=total_3,
        total_wish4=total_4,
        total_wish5=total_5,
        main_table_content=html_rows
    )
    html_result = chevron.render(html_template, html_params)

    return 0, html_result


def do_background_work(chat_bot_work_channel: str, event_bot_work_channel_id: str, version: str) -> None:
    work_thread = threading.Thread(target=_threaded_fork, args=(chat_bot_work_channel, event_bot_work_channel_id, version))
    work_thread.daemon = True
    work_thread.start()


def interactive_auth() -> None:
    if os.path.exists('auth.json'):
        return

    user_y = input(_msg('auth_start_promt'))
    if user_y != 'y':
        return

    user_channel_raw = input(_msg('auth_channel_promt'))
    user_channel = user_channel_raw.strip()
    if '/' in user_channel:
        input(_msg('auth_channel_error_name'))
        return

    user_y = input(_msg('auth_channel_separ'))
    if user_y != 'y':
        auth_type = 'multi'
    else:
        auth_type = 'solo'

    auth_data = {}
    for bot_type in ('chat', 'redem'):
        state = ''.join(random.choice(STATE_ALPHABLET) for _ in range(32))

        current_scope = MILTI_BOT_SCOPES
        if bot_type == 'chat':
            current_scope = CHAT_BOT_SCOPES if auth_type == 'multi' else MILTI_BOT_SCOPES
        if bot_type == 'redem':
            current_scope = EVENT_BOT_SCOPES if auth_type == 'multi' else MILTI_BOT_SCOPES

        web_data = {
            'response_type': 'code',
            'force_verify': 'true',
            'client_id': TWITCH_APP_CLIENT_ID,
            'redirect_uri': URL_CODE,
            'scope': current_scope,
            'state': state
        }

        browser_url = TWITCH_CODE_URL + '?' + parse.urlencode(web_data)

        if auth_type == 'solo':
            bot_type_text = _msg('auth_bot_type_both')
        else:
            bot_type_text = _msg('auth_bot_type_chat') if bot_type == 'chat' else _msg('auth_bot_type_event')

        input(_msg('auth_browser_promt') % bot_type_text)
        webbrowser.open(browser_url, new=2)
        input(_msg('auth_browser_close'))

        twitch_user_data = asyncio.run(_get_tw_data(state))
        if twitch_user_data is None:
            input(_msg('auth_gate_error'))
            return

        token_error = twitch_user_data.get('error')
        if not (token_error is None):
            input(_msg('auth_token_error'))
            return

        bot_token = twitch_user_data.get('access_token')
        bot_token_ref = twitch_user_data.get('refresh_token')
        if bot_type == 'chat':
            auth_data.update({
                'chat_bot': {
                    'bot_token': bot_token,
                    'bot_token_ref': bot_token_ref,
                    'work_channel': user_channel
                }
            })
        if bot_type == 'redem' or auth_type == 'solo':
            auth_data.update({
                'event_bot': {
                    'channel_token': bot_token,
                    'channel_token_ref': bot_token_ref,
                    'work_channel_id': 0
                }
            })

        if auth_type == 'solo':
            break

        input(_msg('auth_create_success'))

    with open('auth.json', 'w', encoding='utf-8') as auth_f:
        json.dump(auth_data, auth_f)

    input(_msg('auth_end'))
    _log_print('\n')


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

        gconfig = CONFIG['gbot_config']
        self.cmd_timeout = {gkey: 0 for gkey in gconfig.keys()}

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

        _wish_cmd = command_prefix + self.chatbot_cfg['wish_command']
        logging.debug(_msg('log_twitch_init'), chat_bot_token, _wish_cmd, work_channel)

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
        _log_print(_msg('twitch_load_userdata'))
        for user_data in self.user_db.get_all():
            username, *gacha_params = user_data
            user_gacha = Gacha(*gacha_params)
            self.gacha_users.update({username: user_gacha})
        _log_print(_msg('twitch_load_users_total'), len(self.gacha_users))

        if self.chatbot_cfg['enabled']:
            chat_wish_command = self.chatbot_cfg['wish_command']
            command_function = commands.Command(chat_wish_command, self.wish)
            self.add_command(command_function)
            _log_print(_msg('twitch_load_chatbot_command'), chat_wish_command)

        if self.eventbot_cfg['enabled']:
            event_token = AUTH_EVENT_BOT['channel_token']
            event_channel = AUTH_EVENT_BOT['work_channel_id']
            pubsub_topic = pubsub.channel_points(event_token)[event_channel]
            self.sub_topics.append(pubsub_topic)
            _log_print(_msg('twitch_load_eventbot_count'), len(self.eventbot_cfg['rewards']))

        if self.chatbot_cfg['enabled']:
            _log_print(_msg('twitch_load_chat_connect') % AUTH_CHAT_BOT['work_channel'])
        if self.eventbot_cfg['enabled']:
            _log_print(_msg('twitch_load_event_connect') % AUTH_EVENT_BOT['work_channel_id'])

    async def event_ready(self) -> None:
        _log_print(_msg('twitch_chat_connected'), self.nick, self.user_id)
        if self.eventbot_cfg['enabled']:
            await self.pubsub.subscribe_topics(self.sub_topics)
        if self.chatbot_cfg['self_wish']:
            _log_print(_msg('twitch_self_wishes_enabled') % self.chatbot_cfg['self_wish_every'])
            asyncio.Task(self.send_autowish(), loop=self.loop)

    @staticmethod
    async def event_pubsub_error(message: dict) -> None:
        _log_print(_msg('twitch_event_connect_error') % (AUTH_EVENT_BOT['work_channel_id'], message))

    @staticmethod
    async def event_pubsub_nonce(_) -> None:
        _log_print(_msg('twitch_event_connected') % AUTH_EVENT_BOT['work_channel_id'])

    async def send_notify(self, mention: str, wtime: int) -> None:
        notify_text_raw = random.choice(NOTIFY_TEXT)
        try:
            notify_text = notify_text_raw.format(username=mention, command=self.chatbot_wish_command)
        except KeyError as format_error:
            _log_print(_msg('twitch_error_format'), format_error)
            return

        await asyncio.sleep(wtime)
        await self.connected_channels[0].send(notify_text)

    async def send_autowish(self) -> None:
        auto_gacha = Gacha()
        while True:
            _log_print(_msg('twitch_send_autowish'))
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

        logging.debug(_msg('log_twitch_wish_command'), username, user.color)

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
            _log_print(_msg('twitch_error_format'), format_error)
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

        logging.debug(_msg('log_twitch_pubsub_event'), username, reward_title, user_color)

        rewards_map = {}
        for reward in self.eventbot_cfg['rewards']:
            rewards_map.update({reward['event_name']: reward['wish_count']})

        logging.debug(_msg('log_twitch_pubsub_map'), rewards_map)

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
            _log_print(_msg('twitch_error_format'), format_error)
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

        logging.debug(_msg('log_twitch_getcmd_stats'), user)

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
            _log_print(_msg('twitch_error_format'), format_error)
            return

        await ctx.send(answer_text)

    @commands.command()
    async def gbot_status(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_status', user):
            return

        logging.debug(_msg('log_twitch_getcmd_status'), user)

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
            _log_print(_msg('twitch_error_format'), format_error)
            return

        await ctx.send(answer_text)

    @commands.command()
    async def gbot_sound(self, ctx: commands.Context) -> None:
        sound_cfg = CONFIG['sound']

        user = ctx.author
        if not self._srv_bypass('gbot_sound', user):
            return

        logging.debug(_msg('log_twitch_getcmd_sound'), user)

        if user.is_mod or user.is_broadcaster:
            if SOUND_IS_WORK:
                sound_cfg['enabled'] = not sound_cfg['enabled']
                mixer.stop()

            sound_text = _msg('enabled') if sound_cfg['enabled'] else _msg('disabled')
            answer_text = _msg('sound_status') % (user.mention, sound_text)

            await ctx.send(answer_text)

    @commands.command()
    async def gbot_pause(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_pause', user):
            return

        logging.debug(_msg('log_twitch_getcmd_pause'), user)

        if user.is_mod or user.is_broadcaster:
            self.coordinator.que_processing = not self.coordinator.que_processing

            pause_text = _msg('enabled') if self.coordinator.que_processing else _msg('disabled')
            answer_text = _msg('commands_status') % (user.mention, pause_text)

            await ctx.send(answer_text)

    async def _gbot_history_fnc(self, ctx: commands.Context, user_name: str, user_mention: str, user_id: int):
        code, html_history = render_html_history(user_name, self.nick)

        errors_map = {
            1: _msg('history_error_c1'),
            2: _msg('history_error_c2'),
            3: _msg('history_error_c3'),
            4: _msg('history_error_c4'),
            5: _msg('history_error_c5'),
            6: _msg('history_error_c6')
        }

        if code < 0:
            error_response = errors_map[abs(code)] % user_mention
            await ctx.send(error_response)
            return

        channel_id = AUTH_EVENT_BOT['work_channel_id']
        html_history_b64 = base64.urlsafe_b64encode(html_history.encode(encoding='utf-8')).decode(encoding='utf-8')
        json_data = {'user_id': user_id, 'channel_id': channel_id, 'html': html_history_b64}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(URL_HISTORY, json=json_data) as post_data:
                    response = await post_data.json()
            except aiohttp.ClientError as history_error:
                _log_print(_msg('twitch_history_get_error'), history_error)
                error_response = errors_map[5]
                await ctx.send(error_response)
                return

        if not ('url' in response):
            error_response = errors_map[6]
            await ctx.send(error_response)
            return

        history_url = response['url']
        response = _msg('history_command_reply') % (user_mention, history_url)
        await ctx.send(response)

    @commands.command()
    async def gbot_history(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_history', user):
            return

        logging.debug(_msg('log_twitch_getcmd_history'), user)
        await self._gbot_history_fnc(ctx, user.name, user.mention, user.id)

    @commands.command()
    async def gbot_history_all(self, ctx: commands.Context) -> None:
        user = ctx.author
        if not self._srv_bypass('gbot_history_all', user):
            return

        logging.debug(_msg('log_twitch_getcmd_history_all'), user)

        user_id = 0
        user_name = ''
        await self._gbot_history_fnc(ctx, user_name, user.mention, user_id)


def init():
    global AUTH_CONFIG
    global AUTH_CHAT_BOT
    global AUTH_EVENT_BOT

    _test_mode = CONFIG['test_mode']
    if not _test_mode:
        interactive_auth()
        if not os.path.exists('auth.json'):
            sys.exit()
        AUTH_CONFIG = _config_check('auth.json', AUTH_SCHEMA)

    AUTH_CHAT_BOT = AUTH_CONFIG['chat_bot']
    AUTH_EVENT_BOT = AUTH_CONFIG['event_bot']
