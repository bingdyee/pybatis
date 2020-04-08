# -*- coding: utf-8 -*-
import sys, re, json
from threading import Condition
from queue import Queue
from .proxy import ProxyFactory
from .utils import Singleton


class Field:

    def __init__(self, name):
        self.name = name


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        mapper = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mapper[k.lower()] = v
        # romove class's attrs
        for _ in mapper.keys():
            attrs.pop(_)
        # Mapper properties and column
        attrs['__mapper__'] = mapper
        return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMetaclass):

    def __init__(self, **kwargs):
        for k, v in self.__mapper__.items():
            value = kwargs.get(v.name) if kwargs.get(k) is None else kwargs.get(k)
            setattr(self, k, value)

    def __str__(self):
        return str(self.__dict__)

    def __call__(self):
        return self.__dict__

class Connection:

    def __init__(self, conn, pool):
        self.conn = conn
        self.pool = pool
        self.row_factory = lambda c, row: {col[0]: row[idx] for idx, col in enumerate(c.description) }

    def _cursor(self):
        pass

    def select(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        try:
            return [self.row_factory(cursor, row) for row in cursor]
        finally:
            cursor.close()

    def execute(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def release(self):
        self.pool.release(self)
    
    def close(self):
        self.conn.close()

class ConnectionPool:

    def __init__(self, creator, max_active, *args, **kwargs):
        self.max_active = max_active
        self.queue = Queue(max_active)
        self._lock = Condition()
        self._connections = 0
        self._creator = creator.connect
        self._creator_constructor_args = (args, kwargs)

    def get_connection(self):
        self._lock.acquire()
        try:
            if self._connections < self.max_active:
                conn = Connection(self._creator(*self._creator_constructor_args[0], **self._creator_constructor_args[1]), self)
                self.queue.put(conn)
                self._connections += 1
            if self.queue.empty():
                self._lock.wait()
            return self.queue.get()
        finally:
            self._lock.release()

    def release(self, conn):
        self._lock.acquire()
        try:
            self.queue.put(conn)
            self._lock.notifyAll()
        finally:
            self._lock.release()
        

    def __del__(self):
        while not self.queue.empty():
            self.queue.get().close()

class ConnectionManager(dict):

    _pool = None

    def __init__(self):
        pass

    def __missing__(self, key):
        return '?'

    def init_pool(self, *args, **kwargs):
        if MapperConfig._pool is None:
            MapperConfig._pool = ConnectionPool(*args, **kwargs)

    def get_pool(self):
        if MapperConfig._pool is None:
            raise Exception("DB pool is None!")
        return MapperConfig._pool
    

MapperConfig = ConnectionManager()

def MapperHandler(target, func, *args):
    func_name = func.__name__
    annotations = func.__annotations__
    sql = func(*args)
    placeholders = re.findall('{(.+?)}', sql)
    sql = sql.format_map(MapperConfig)
    # params to dict
    param_names = [key for key in annotations.keys()]
    m_params = {}
    for i, param in enumerate(args):
        if isinstance(param, Model):
            m_params.update(param.__dict__)
        else:
            m_params[param_names[i]] = param
    params = [m_params.get(placeholder) for placeholder in placeholders]
    r_type = annotations.get('return')
    with target.pool.get_connection() as conn:
        if func_name.startswith('select'):
            records = conn.select(sql, tuple(params))
            if len(records) == 0:
                return records
            if r_type.__module__ == 'typing':
                if r_type.__args__ and \
                    issubclass(r_type.__args__[0], Model):
                    return [r_type.__args__[0](**record) for record in records]
            if issubclass(r_type, Model):
                return r_type(**records[0])
        conn.execute(sql, tuple(params))
        return True

SingletonMappers = {}

def Mapper(singleton=True):
    def _init(cls):
        def create_proxy(*a, **kw):
            if singleton:
                if cls.__name__ not in SingletonMappers:
                    cls.pool = MapperConfig.get_pool()
                    SingletonMappers[cls.__name__] = ProxyFactory(MapperHandler)(cls)(*a, **kw)
                return SingletonMappers[cls.__name__]
            else:
                return ProxyFactory(MapperHandler)(cls)(*a, **kw)
        return create_proxy
    return _init





