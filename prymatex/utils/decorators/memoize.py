#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import functools

def memoized(function):
    '''Simple local cache kept during process execution'''
    # See http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    cache = function.cache = {}

    @functools.wraps(function)
    def memoizer(*largs, **kwargs):
        if largs in cache:
            return cache[largs]
        return cache.setdefault(largs, function(*largs, **kwargs))
    return memoizer
