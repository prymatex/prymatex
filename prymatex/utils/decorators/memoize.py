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
        if largs in cache:
            return cache[largs]
        return cache.setdefault(largs, function(*largs, **kwargs))
    return memoizer

def dynamic_memoized(function):
    memento = DYNAMIC_MEMOIZED_CACHE[function] = {}
    @functools.wraps(function)
    def memoizer(*largs, **kwargs):
        if largs in memento:
            return memento[largs]
        return memento.setdefault(largs, function(*largs, **kwargs))
    return memoizer

def remove_memoized_argument(key, function = None, condition = lambda f, key, mkey: key in mkey):
    def remove_memento_items(function, memento):
        for mkey, mvalue in list(memento.items()):
            if condition(function, key, mkey):
                del memento[mkey]
    if function is None:
        for function, memento in DYNAMIC_MEMOIZED_CACHE.items():
            remove_memento_items(function, memento)
    elif function in DYNAMIC_MEMOIZED_CACHE:
        remove_memento_items(function, DYNAMIC_MEMOIZED_CACHE[function])
        
def remove_memoized_function(function):
    for mfunction in list(DYNAMIC_MEMOIZED_CACHE.keys()):
        if mfunction.__name__ == function.__name__:
            print("limpiando", mfunction)
            DYNAMIC_MEMOIZED_CACHE[mfunction].clear()
