# -*- coding: utf-8 -*-
import os
import time


instances = {}


def Singleton(cls, *args, **kw):
    """
    Singleton decorator
    """
    global instances

    def _singleton(*args, **kw):
        if cls.__name__ not in instances:
            instances[cls.__name__] = cls(*args, **kw)
        return instances[cls.__name__]
    return _singleton


def list_files(path):
    """
    list files under path
    """
    fs = os.walk(path)
    files = []
    for x in fs:
        if x[2]:
            files += [os.path.join(x[0], _) for _ in x[2]]
    return files


def format_time(fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime(time.time()))


def exec_cmd(cmd):
    """
    exec system command
    """
    with os.popen(cmd, 'r') as msg:
        for line in msg:
            print(line.rstrip())

