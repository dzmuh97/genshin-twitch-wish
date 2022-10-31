import os

import pickle
import sqlite3
import logging

from config import _msg
from config import _log_print

from gacha import Gacha

from typing import List, Tuple, Optional

DbUserTuple = Tuple[str, int, int, int, bool, bool]


class UserDB:
    database = 'database.sqlite'
    database_old = 'database.sql'
    old_to_new = ['win_4', 'win_5']

    def __init__(self):
        self.conn = sqlite3.connect(self.database)
        logging.debug(_msg('log_db_created'))
        if not self._check_table():
            logging.debug(_msg('log_db_table_create'))
            self._create_table()
        for new_column in self.old_to_new:
            if not self._check_column(new_column):
                logging.debug(_msg('log_db_old_update'), new_column)
                self._create_column(new_column)
        self._restore_old()

    def _restore_old(self) -> None:
        if not os.path.exists(self.database_old):
            return

        logging.debug(_msg('log_db_old_import'))

        _log_print(_msg('db_import_old_start'))
        with open(self.database_old, mode='rb') as f:
            data = pickle.loads(f.read())

        i_users = 0
        _log_print(_msg('db_import_old_users_count'), len(data))
        for user, gacha in data.items():
            user = user.lower()
            setattr(gacha, 'win_garant_table', {'5': 0, '4': 0})

            check = self.get(user)
            if check:
                self.update(user, gacha)
                continue

            self.push(user, gacha)
            i_users += 1

        _log_print(_msg('db_import_old_users_total'), i_users)
        os.remove(self.database_old)
        _log_print(_msg('db_import_old_deleted'), )

    def _create_column(self, column: str) -> None:
        cur = self.conn.cursor()
        payload = "ALTER TABLE users ADD COLUMN %s INTEGER DEFAULT 0;" % column
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def _check_column(self, column: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM pragma_table_info('users') WHERE name=?;", (column,))
        ret = cur.fetchone()
        cur.close()

        if ret is None:
            return False

        return True

    def _check_table(self) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        ret = cur.fetchone()
        cur.close()

        if ret is None:
            return False

        return True

    def _create_table(self) -> None:
        cur = self.conn.cursor()
        payload = "CREATE TABLE users (username TEXT PRIMARY KEY, wish_count INTEGER, wish_4_garant INTEGER, wish_5_garant INTEGER, win_4 INTEGER, win_5 INTEGER);"
        cur.execute(payload)
        self.conn.commit()
        cur.close()

    def get_all(self) -> List[DbUserTuple]:
        logging.debug(_msg('log_db_method_getall'))
        cur = self.conn.cursor()
        payload = "SELECT * FROM users;"
        cur.execute(payload)
        data = cur.fetchall()
        cur.close()

        return data

    def get(self, username) -> Optional[DbUserTuple]:
        logging.debug(_msg('log_db_method_get'), username)
        cur = self.conn.cursor()
        payload = "SELECT * FROM users WHERE username=?;"
        cur.execute(payload, (username,))
        data = cur.fetchone()
        cur.close()

        return data

    def push(self, username: str, gacha: Gacha) -> None:
        logging.debug(_msg('log_db_method_push'), username, gacha)
        cur = self.conn.cursor()
        payload = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?);"
        win_4, win_5 = gacha.win_garant_table['4'], gacha.win_garant_table['5']
        cur.execute(payload, (username, gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, win_4, win_5))
        self.conn.commit()
        cur.close()

    def update(self, username: str, gacha: Gacha) -> None:
        logging.debug(_msg('log_db_method_update'), username, gacha)
        cur = self.conn.cursor()
        payload = "UPDATE users SET wish_count=?, wish_4_garant=?, wish_5_garant=?, win_4=?, win_5=? WHERE username=?;"
        win_4, win_5 = gacha.win_garant_table['4'], gacha.win_garant_table['5']
        cur.execute(payload, (gacha.wish_count, gacha.wish_4_garant, gacha.wish_5_garant, win_4, win_5, username))
        self.conn.commit()
        cur.close()
