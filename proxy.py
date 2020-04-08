# -*- coding: utf-8 -*-
from types import MethodType

class Proxy:

    def __init__(self, target, handler):
        self.target = target
        self.handler = handler

    def __call__(self, func):
        def invoke(*args, **kwargs):
            return self.handler(self.target, func, *args, **kwargs)
        return invoke

    def __getattr__(self, attr):
        if hasattr(self.target, attr):
            prop = getattr(self.target, attr)
            return self.__call__(prop) if isinstance(prop, MethodType) else prop
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.target.__class__, attr))

def ProxyFactory(handler):
    def init(cls):
        def create_proxy(*args, **kwargs):
            target = cls(*args, **kwargs)
            return Proxy(target, handler)
        return create_proxy
    return init

