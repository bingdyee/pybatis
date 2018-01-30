# -*- coding:utf-8 -*-
"""
@File      : field.py
@Software  : SingularAI
@Time      : 2018/1/29 10:37
@Author    : yubb
"""


class Field(object):

    __slots__ = ("name", "column_type")

    """
    保存数据库表的字段名和字段类型
    """
    default_type = None

    def __init__(self, name, column_type=None):
        self.name = name
        if not column_type:
            column_type = self.__getattribute__('default_type').upper()
        else:
            column_type = column_type.upper()
            if not column_type.startswith(self.__getattribute__('default_type').upper()):
                raise BadTypeError(column_type)
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class BadTypeError(Exception):
    err_info = 'Unknow Type: %s'

    def __init__(self, info):
        super(BadTypeError, self).__init__(BadTypeError.err_info % info)


class ModelMetaclass(type):
    """
    控制Model对象的创建
    """

    def __new__(mcs, name, bases, attrs):
        mapper = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mapper[k] = v
        # romove class's attrs
        for _ in mapper.keys():
            attrs.pop(_)
        # Table's name
        attrs['__table__'] = 'tb_' + name.lower()
        # Mapper properties and column
        attrs['__mapper__'] = mapper
        return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class Varchar(Field):
    """
    varchar
    """

    default_type = 'varchar'

    def __init__(self, name, column_type=None):
        super(Varchar, self).__init__(name, column_type)


class Char(Field):
    """
    char
    """

    default_type = 'char'

    def __init__(self, name, column_type=None):
        super(Char, self).__init__(name, column_type)


class Int(Field):
    """
    int
    """

    default_type = 'int'

    def __init__(self, name, column_type=None):
        super(Int, self).__init__(name, column_type)


class Bigint(Field):
    """
    bigint
    """

    default_type = 'bigint'

    def __init__(self, name, column_type=None):
        super(Bigint, self).__init__(name, column_type)


class Double(Field):
    """
    double
    """

    default_type = 'double'

    def __init__(self, name, column_type=None):
        super(Double, self).__init__(name, column_type)


class Timestamp(Field):
    """
    time
    """
    default_type = 'datetime'

    def __init__(self, name):
        super(Timestamp, self).__init__(name, Timestamp.default_type)


class Blob(Field):
    """
    blob
    """

    default_type = 'blob'

    def __init__(self, name, column_type=None):
        super(Blob, self).__init__(name, column_type)


class Demo(Model):

    id = Bigint('id')
    name = Varchar('name')
    password = Varchar('password')
    sex = Char('sex')
    age = Int('age')
    birth = Timestamp('birth')
    email = Varchar('email')


# Test
u = Demo(id=0,
         name='Author',
         password='just-so-so',
         sex='男',
         age=25,
         birth='1994-10-23 00:00:00',
         email='fetaxyu@gmail.com', )
