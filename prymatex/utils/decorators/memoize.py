#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import collections
import functools

#https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*largs, **kwargs):
        key = str(largs) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*largs, **kwargs)
        return cache[key]
    return memoizer
