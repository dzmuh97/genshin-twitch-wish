__ascii__ = r'''
   ___             _    _        _____        _ _      _     __      ___    _      ___ _           _      _           
  / __|___ _ _  __| |_ (_)_ _   |_   _|_ __ _(_) |_ __| |_   \ \    / (_)__| |_   / __(_)_ __ _  _| |__ _| |_ ___ _ _ 
 | (_ / -_) ' \(_-< ' \| | ' \    | | \ V  V / |  _/ _| ' \   \ \/\/ /| (_-< ' \  \__ \ | '  \ || | / _` |  _/ _ \ '_|
  \___\___|_||_/__/_||_|_|_||_|   |_|  \_/\_/|_|\__\__|_||_|   \_/\_/ |_/__/_||_| |___/_|_|_|_\_,_|_\__,_|\__\___/_|  
  
 https://github.com/dzmuh97/genshin-twitch-wish
'''
print(__ascii__)

import os
import sys

import time
import logging

_script_path = os.path.realpath(sys.argv[0])
_script_dir = os.path.dirname(_script_path)

os.chdir(_script_dir)
if not os.path.exists('logs'):
    os.makedirs('logs')

_time_stamp = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    filename=os.path.join('logs', '%s.log' % _time_stamp),
                    filemode='w',
                    encoding='utf-8',
                    level=logging.DEBUG)

import queue
import threading

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

import config
config.init()

import animation
animation.init()

import network
network.init()

from config import _msg
from config import _log_print
from config import __version__

from config import CONFIG

from network import bot_handle
from network import do_background_work

from network import AUTH_CHAT_BOT
from network import AUTH_EVENT_BOT

from animation import draw_group
from animation import update_group

from animation import Coordinator

from gacha import make_user_wish


def _err_logger(msg: str) -> None:
    for msg_line in msg.strip().splitlines():
        message_line_strip = msg_line.strip()
        if len(message_line_strip) > 0:
            logging.error(message_line_strip)


logging.write = _err_logger
sys.stderr = logging

pygame.init()
pygame.display.set_caption(CONFIG['window_name'])

programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)


def create_bot_thread(wish_que: queue.Queue, control: Coordinator) -> threading.Thread:
    bot_thread = threading.Thread(target=bot_handle, args=(wish_que, control))
    bot_thread.daemon = True
    return bot_thread


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
    _log_print(_msg('main_start'))

    coordinator = Coordinator(wish_que, animation_group)

    if chatbot_cfg['enabled'] or eventbot_cfg['enabled']:
        twitch_bot_thread = create_bot_thread(wish_que, coordinator)
        twitch_bot_thread.start()
        twitch_bot_start = True
        _log_print(_msg('main_twitch_bot_started'))
        if CONFIG['send_dev_stats']:
            chat_bot_work_channel = AUTH_CHAT_BOT['work_channel']
            event_bot_work_channel_id = AUTH_EVENT_BOT['work_channel_id']
            do_background_work(chat_bot_work_channel, event_bot_work_channel_id, __version__)
    else:
        _log_print(_msg('main_twitch_bot_disabled'))

    animation_cfg = CONFIG['animations']
    _log_print(_msg('main_fps'), animation_cfg['fps'])
    while True:
        fps.tick(animation_cfg['fps'])

        if twitch_bot_start and (not twitch_bot_thread.is_alive()):
            twitch_bot_thread.join()
            _log_print(_msg('main_twitch_bot_restart'))
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
    main()
