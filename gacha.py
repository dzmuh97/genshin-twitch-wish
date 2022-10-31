import time
import random
import logging

from dataclasses import dataclass

from config import _msg

from config import DATABASE
from config import BANNER_CONFIG

from typing import Tuple, List


@dataclass
class WishData:
    wish_count: int
    wish_4_garant: int
    wish_5_garant: int
    win_4_garant: int
    win_5_garant: int
    wish_star: str
    wish_star_type: str
    wish_type: str
    wish_meta_type: str
    wish_meta_element: str
    wish_obj_name: str
    wish_obj_text: str


@dataclass
class Wish:
    username: str
    user_color: str
    wish_data_count: int
    wish_data_list: List[WishData]


class Gacha:
    def __init__(self,
                 wish_count: int = 0,
                 wish_4_garant: int = 1,
                 wish_5_garant: int = 1,

                 win_5: bool = False,
                 win_4: bool = False
                 ):
        self.wish_5_garant = wish_5_garant
        self.wish_4_garant = wish_4_garant
        self.wish_count = wish_count
        self.last_wish_time = 0

        self.win_garant_table = {'5': win_5, '4': win_4}
        self._rollback = [0, 0, 0]

        logging.debug(_msg('log_gacha_created'), wish_count, wish_4_garant, wish_5_garant, win_4, win_5)

    @staticmethod
    def _random_tap(chance_percent: float) -> bool:
        return random.choice(range(10000)) <= int(chance_percent * 100)

    def __flip_garant(self, star: str, val: bool) -> None:
        self.win_garant_table[star] = val

    def __rollback(self) -> None:
        self.wish_count, self.wish_4_garant, self.wish_5_garant = self._rollback

    def __roll(self) -> Tuple[str, str]:
        self._rollback = [self.wish_count, self.wish_4_garant, self.wish_5_garant]
        self.wish_count += 1

        wish_garant_starts = BANNER_CONFIG['wish_fi_soft_a']
        wish_5_garant = BANNER_CONFIG['wish_fi_garant']
        wish_5_chance = BANNER_CONFIG['wish_fi_chance']
        wish_4_garant = BANNER_CONFIG['wish_fo_garant']
        wish_4_chance = BANNER_CONFIG['wish_fo_chance']

        if (self.wish_5_garant > wish_garant_starts) and (self.wish_5_garant < wish_5_garant):
            _soft_i = (self.wish_5_garant - wish_garant_starts) / (wish_5_garant - wish_garant_starts)
            _soft_chance = wish_5_chance + _soft_i * 100
            if self._random_tap(_soft_chance):
                self.wish_5_garant = 1
                return '5', 'srnd'
        else:
            if self._random_tap(wish_5_chance):
                self.wish_5_garant = 1
                return '5', 'rnd'

        if self.wish_5_garant % wish_5_garant == 0:
            self.wish_5_garant = 1
            return '5', 'garant'
        else:
            self.wish_5_garant += 1

        if self.wish_4_garant % wish_4_garant == 0:
            self.wish_4_garant = 1
            return '4', 'garant'
        else:
            self.wish_4_garant += 1

        if self._random_tap(wish_4_chance):
            self.wish_4_garant = 1
            return '4', 'rnd'

        return '3', 'rnd'

    def generate_wish(self, count: int) -> List[WishData]:
        self.last_wish_time = int(time.time())

        rolls = []
        roll_i = 0
        while roll_i < count:
            star, star_type = self.__roll()
            if star == '3':
                wtype = 'weapon'
            else:
                wtype = random.choice(['weapon', 'char'])

            if len(DATABASE[star][wtype]) == 0:
                self.__rollback()
                continue

            data = random.choice(DATABASE[star][wtype])
            garant_datas = DATABASE[star].get('garant', [])
            if (len(garant_datas) > 0) and (star in ['4', '5']):
                _win = self.win_garant_table[star]
                _tap = self._random_tap(50)
                if _win or _tap:
                    data = random.choice(garant_datas)
                    self.__flip_garant(star, False)
                    if _win:
                        star_type = 'event_garant'
                    else:
                        star_type = '50/50'
                else:
                    self.__flip_garant(star, True)

            logging.debug(_msg('log_gacha_wish_result'), star, star_type, data)

            win_4, win_5 = self.win_garant_table['4'], self.win_garant_table['5']
            gacha_obj = WishData(self.wish_count, self.wish_4_garant, self.wish_5_garant, win_4, win_5, star, star_type, **data)
            rolls.append(gacha_obj)
            roll_i += 1

        return rolls


def make_user_wish(username: str, color: str, count: int) -> Tuple[Gacha, Wish]:
    gacha = Gacha()
    wish_data_list = gacha.generate_wish(count)
    wish = Wish(username, color, count, wish_data_list)
    return gacha, wish
