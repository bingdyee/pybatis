# -*- coding:utf-8 -*-
from connection import ConnectionPool
from utils import Singleton


@Singleton
class JdbcTemplate:

    def __init__(self, user, password, database,
                 port=3306,
                 pool_name='DataSources',
                 host='localhost',
                 pool_resize_boundary=50,
                 enable_auto_resize=True,
                 max_pool_size=10):
        config = {
            'pool_name': pool_name,
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'pool_resize_boundary': pool_resize_boundary,
            'enable_auto_resize': enable_auto_resize,
            'max_pool_size': max_pool_size
        }
        self.pool = ConnectionPool(**config)

    def query(self, sql, where):
        with self.pool.cursor() as cursor:
            cursor.execute(sql, where)
            return [_ for _ in cursor]

    def execute(self, sql, data=None):
        with self.pool.cursor() as cursor:
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

    def insert(self, sql, data):
        with self.pool.cursor() as cursor:
            if isinstance(data, list):
                result = cursor.executemany(sql, data)
            else:
                result = cursor.execute(sql, data)
            return result

    def close(self):
        self.pool.close()



