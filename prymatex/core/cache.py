#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from functools import wraps
import sha

from PyQt4 import QtCore

from prymatex.core.plugin import PMXBaseComponent


class PMXCacheManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.memoize = {}

    def buildKey(self, content):
        """docstring for buildKey"""
        return sha.sha(content).hexdigest()

def memoized(function):
    full_func_name = function.__module__ + '.' + function.func_name
    cacheManager = QtCore.QCoreApplication.instance().cacheManager
    @wraps(function)
    def _memoized(*largs, **kwargs):
        key = (largs, tuple(kwargs.items()))
        memento = cacheManager.memoize.setdefault(full_func_name, {})
        return memento.setdefault(key, function(*largs, **kwargs))
    return _memoized
    
def removeMemoizedArgument(key):
    cacheManager = QtCore.QCoreApplication.instance().cacheManager
    for full_func_name, memento in cacheManager.memoize.iteritems():
        cacheManager.memoize[full_func_name] = dict(filter(lambda (mkey, mvalue): key in mkey[0] or any(map(lambda kwarg: key in kwargs, mkey[1])), memento.iteritems()))

def removeMemoizedFunction(function):
    full_func_name = function.__module__ + '.' + function.func_name
    cacheManager = QtCore.QCoreApplication.instance().cacheManager
    try:
        del cacheManager.memoize[full_func_name]
    except KeyError as error:
        pass