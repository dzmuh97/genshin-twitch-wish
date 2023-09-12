import os
import gc
import cv2
import time
import queue
import pygame
import random
import logging

from pygame import mixer

from itertools import cycle, zip_longest

from config import _msg
from config import _log_print
from config import _wish_name_normal

from config import CONFIG
from config import SOUND_CONFIG

from config import USER_SPLASH_TEXT

from gacha import Wish
from gacha import WishData

from typing import Union, Tuple, List, Dict, Optional

BaseDrawClass = Union['StaticImage', 'AnimatedVideo']
DrawDataChunk = Union[BaseDrawClass, List[BaseDrawClass]]
DrawData = Dict[str, DrawDataChunk]

SOUND_IS_WORK = False
SOUND = {}

USERTEXT_COLOR = pygame.Color(255, 255, 255, 0)
USERTEXT_OUTLINE = pygame.Color(0, 0, 0, 0)
WISH_BLACK_COLOR = pygame.Color(0, 0, 0)


class Coordinator:
    def __init__(self, wish_que: queue.Queue, animl: List[BaseDrawClass]):
        self.states_list: List[str] = ['idle', 'init', 'draw_usertext', 'draw_fall', 'draw_wishes', 'clear']
        self.current_wish: Optional[Wish] = None
        self.current_wish_data: Optional[WishData] = None
        self.current_draw_objs: DrawData = {}
        self.current_draw_objs_played: Dict[str, bool] = {}
        self.used_sound: List[mixer.Sound] = []

        self.sound_cfg = CONFIG['sound']
        self.animation_cfg = CONFIG['animations']

        self.states = cycle(self.states_list)
        self.current_state = next(self.states)

        self.animations_list = animl
        self.wish_que = wish_que

        self.que_processing = True
        logging.debug(_msg('log_panel_created'))

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
            logging.debug(_msg('log_panel_none_check'))
            return

        wish_data = self.current_wish_data

        _t = time.time()
        logging.debug(_msg('log_panel_call_chunk_load'), wish_data)

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

        background_delay = self.animation_cfg['end_delay_multi' if is_multi_star else 'end_delay'][wish_stars]

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

        logging.debug(_msg('log_panel_call_chunk_time'), time.time() - _t)

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

        logging.debug(_msg('log_panel_state_idle'))

        self.current_wish = wish

        for wish_data in wish.wish_data_list:
            t = time.localtime()
            current_time = time.strftime('%H:%M:%S', t)
            _log_print(_msg('cord_gacha_br'), '[%s]' % current_time,
                       _msg('cord_result_for'), wish.username,
                       '#%d' % wish_data.wish_count,
                       'g4#%d' % wish_data.wish_4_garant,
                       'g5#%d' % wish_data.wish_5_garant,
                       'w4#%d' % wish_data.win_4_garant,
                       'w5#%d' % wish_data.win_5_garant,
                       wish_data.wish_star, '* ->', _wish_name_normal(wish_data.wish_obj_text),
                       '[%s]' % wish_garant_type(wish_data.wish_star_type))

            history_cfg = CONFIG['history_file']
            if history_cfg[wish_data.wish_star]:
                write_history(wish.username, wish_data.wish_count, wish_data.wish_star,
                              wish_garant_type(wish_data.wish_star_type), wish_data.wish_obj_text)

        return True

    def state_init(self) -> bool:
        logging.debug(_msg('log_panel_state_init'))
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

        logging.debug(_msg('log_panel_init_wish_params'), wish_stars, is_multi_star)

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

        logging.debug(_msg('log_panel_init_load_time'), time.time() - _t)
        logging.debug(_msg('log_panel_init_anim'), self.current_draw_objs)

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

        logging.debug(_msg('log_panel_init_loaded_uback'), self.current_draw_objs['user_background'])
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
        logging.debug(_msg('log_panel_state_clear'))
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
                self.rect = self.image.get_rect()
                self.rect.center = self.rect_copy.center

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
        self.image = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], 'BGR')

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
    wdate = time.strftime('%d.%m.%Y-%H:%M:%S', history_time)
    with open(history_path, 'a', encoding='utf-8') as fp:
        fp.write('%s,%s,%d,%s,%s,%s\n' % (wdate, nickname, wish_count, star, wtype, _wish_name_normal(wish)))


def wish_garant_type(gtype: str) -> str:
    star_types = {
        'srnd': _msg('wish_garant_type_1'),
        'garant': _msg('wish_garant_type_2'),
        'event_garant': _msg('wish_garant_type_3'),
        'rnd': _msg('wish_garant_type_4'),
        '50/50': _msg('wish_garant_type_5')
    }

    return star_types[gtype]


def init():
    global SOUND
    global SOUND_IS_WORK

    try:
        mixer.init()
        SOUND_IS_WORK = True
    except pygame.error:
        SOUND_IS_WORK = False

    if SOUND_CONFIG['enabled'] and (not SOUND_IS_WORK):
        SOUND_CONFIG['enabled'] = False

    if SOUND_CONFIG['enabled']:
        SOUND = {
            'fall': mixer.Sound(os.path.join('sound', SOUND_CONFIG['fall'])),
            '3': mixer.Sound(os.path.join('sound', SOUND_CONFIG['3'])),
            '4': mixer.Sound(os.path.join('sound', SOUND_CONFIG['4'])),
            '5': mixer.Sound(os.path.join('sound', SOUND_CONFIG['5']))
        }
