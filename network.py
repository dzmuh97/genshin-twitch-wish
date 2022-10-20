import os
import time
import json
import base64
import random
import string
import logging
import threading
import webbrowser

import asyncio
import aiohttp

from urllib import parse
from distutils.version import StrictVersion

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


async def _get_version(local_version) -> None:
    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.get(URL_VERSION) as version_data_raw:
                version_data = await version_data_raw.json()
                logging.debug('[UPDATE] Информация о версии получена')
        except aiohttp.ClientSession as ver_error:
            logging.debug('[UPDATE] Ошибка получения информации о версии: %s', ver_error)
            return

    web_version = StrictVersion(version_data['current_version'])
    local_version = StrictVersion(local_version)

    logging.debug('[UPDATE] web=%s, local=%s', web_version, local_version)
    if web_version == local_version:
        return

    print('[UPDATE] Используется устаревшая версия - установлена: %s, доступна: %s' % (local_version, web_version))


async def _send_stats(chat_bot_work_channel: str, event_bot_work_channel_id: str, version: str) -> None:
    stats_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stats_data = {'date': stats_time, 'version': version, 'channel': chat_bot_work_channel, 'channel_id': event_bot_work_channel_id}
    stats_data_json = json.dumps(stats_data)
    stat_base64 = base64.urlsafe_b64encode(stats_data_json.encode(encoding='utf-8')).decode(encoding='utf-8')

    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.post(URL_VERSION, json={'base64data': stat_base64}) as _:
                logging.debug('[STATS] Статистика отправлена')
        except aiohttp.ClientError as stats_error:
            logging.debug('[STATS] Ошибка отправки статистики: %s', stats_error)


def _threaded_fork(chat_bot_work_channel, event_bot_work_channel_id, version):
    async def _fork():
        await _send_stats(chat_bot_work_channel, event_bot_work_channel_id, version)
        await _get_version(version)

    asyncio.run(_fork())


def do_background_work(chat_bot_work_channel: str, event_bot_work_channel_id: str, version: str) -> None:
    work_thread = threading.Thread(target=_threaded_fork, args=(chat_bot_work_channel, event_bot_work_channel_id, version))
    work_thread.daemon = True
    work_thread.start()


async def _get_tw_data(state):
    async with aiohttp.ClientSession() as aio_session:
        try:
            async with aio_session.get(URL_TOKEN + state) as twitch_user_data_raw:
                twitch_user_data = await twitch_user_data_raw.json()
        except aiohttp.ClientError as gate_error:
            print(gate_error)
            return None

    return twitch_user_data


def interactive_auth() -> None:
    if os.path.exists('auth.json'):
        return

    user_y = input('[AUTH] Не удалось найти файл auth.json, начать авторизацию на Twitch? [y/n]: ')
    if user_y != 'y':
        return

    user_channel_raw = input(
        '[AUTH] Введите название канала, где будет использоваться симулятор (только ник, не ссылка): ')
    user_channel = user_channel_raw.strip()
    if '/' in user_channel:
        input('[AUTH] Название канала содержит недопустимые символы! [ENTER]: ')
        return

    user_y = input('[AUTH] Будем использовать один аккаунт для чат-бота и баллов канала? [y/n]: ')
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
            bot_type_text = 'чат-бот и аккаунт стримера для баллов канала'
        else:
            bot_type_text = 'чат-бот' if bot_type == 'chat' else 'аккаунт стримера для баллов канала'

        warn_text = ('\nСейчас будет открыта новая вкладка в вашем стандартном браузере\n'
                     'В ней будет запрос на доступ к аккаунту бота\n\n'
                     'Обязательно проверьте следующе:\n'
                     '- в адресной строке должен быть адрес: id.twitch.tv\n'
                     '- название приложения: Genshin Wish Simulator\n'
                     '- на странице должен быть указан ник именно того акаунта, который вы хотите использовать в качестве бота\n\n'
                     '>>> Сейчас мы настраиваем аккаунт для: ' + bot_type_text + ' <<<\n\nНажмите ENTER чтобы продолжить: ')

        input(warn_text)
        webbrowser.open(browser_url, new=2)
        input('\n[AUTH] Подтвердите доступ в открывшемся окне и нажмите ENTER когда закроете окно браузера: ')

        twitch_user_data = asyncio.run(_get_tw_data(state))
        if twitch_user_data is None:
            input('[AUTH] Не удалось сделать запрос к шлюзу для получения токена! [ENTER]: ')
            return

        token_error = twitch_user_data.get('error')
        if not (token_error is None):
            input('[AUTH] Не удалось создать токен. Причина была указана во вкладке браузера после авторизации [ENTER]: ')
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

        input('[AUTH] Все прошло хорошо, аккаунт настроен. Нажмите ENTER чтобы продолжить: ')

    with open('auth.json', 'w', encoding='utf-8') as auth_f:
        json.dump(auth_data, auth_f)

    end_text = ('\nДанные аккаунтов записаны в auth.json\n'
                'Не передавайте никому этот файл и не показывайте его содержимое на стриме!\n'
                'Чтобы начать настройку аккаунтов заново просто удалите auth.json из папки с симулятором\n'
                '[ENTER]: ')
    input(end_text)
    print('\n')
