#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import functools

class memoize(object):
    def __init__(self, key_function=lambda *largs, **kwargs: str(largs) + str(kwargs)):
        self.key_function = key_function

    def __call__(self, func):
        cache = func.cache = {}
        @functools.wraps(func)
        def wrapped(*largs, **kwargs):
            key = self.key_function(*largs, **kwargs)
            if key not in cache:
                cache[key] = func(*largs, **kwargs)
            return cache[key]
        return wrapped
