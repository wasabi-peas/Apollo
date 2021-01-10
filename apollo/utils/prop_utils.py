# -*- coding: utf-8 -*-
"""doc string"""


class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


if __name__ == '__main__':
    pass
