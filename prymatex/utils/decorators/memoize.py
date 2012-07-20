#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import functools

DYNAMIC_MEMOIZED_CACHE = {}

def memoized(function):
    '''Simple local cache kept during process execution'''
    # See http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    cache = function.cache = {}

    @functools.wraps(function)
    def memoizer(*largs, **kwargs):
        return cache.setdefault(largs, function(*largs, **kwargs))
    return memoizer

def dynamic_memoized(function):
    full_func_name = function.__module__ + '.' + function.func_name
    @functools.wraps(function)
    def memoizer(*largs, **kwargs):
        memento = DYNAMIC_MEMOIZED_CACHE.setdefault(full_func_name, {})
        return memento.setdefault(largs, function(*largs, **kwargs))
    return memoizer

def remove_memoized_argument(key):
    for full_func_name, memento in DYNAMIC_MEMOIZED_CACHE.memoize.iteritems():
        DYNAMIC_MEMOIZED_CACHE[full_func_name] = dict(filter(lambda (mkey, mvalue): key in mkey[0] or any(map(lambda kwarg: key in kwargs, mkey[1])), memento.iteritems()))

def remove_memoized_function(function):
    full_func_name = function.__module__ + '.' + function.func_name
    if full_func_name in DYNAMIC_MEMOIZED_CACHE:
        del DYNAMIC_MEMOIZED_CACHE[full_func_name]