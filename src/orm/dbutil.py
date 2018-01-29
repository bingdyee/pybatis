# -*-coding:utf-8-*-
import sqlite3
from tools.common import Singleton


@Singleton
class DBUtils:

    """For sqlite3"""

    def __init__(self, path=None):
        self.pools = {}
        self.cur_session = None
        if path:
            conn = sqlite3.connect(path)
            conn.text_factory = str
            self.pools[path] = conn
            self.cur_session = conn

    def close(self):
        for session in self.pools.values():
            if session:
                session.close()

    def execute(self, sql, data=None):
        cursor = None
        try:
            cursor = self.cur_session.cursor()
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            result = [rs for rs in cursor]
            self.cur_session.commit()
            return result if result else None
        except Exception as e:
            self.cur_session.rollback()
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()

    def set_instance(self, path):
        if path in self.pools:
            return self.pools[path]
        conn = sqlite3.connect(path)
        conn.text_factory = str
        self.pools[path] = conn
        self.cur_session = conn


class MySQL:

    """For MySQL"""

    def __init__(self):
        pass




