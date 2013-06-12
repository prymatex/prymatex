#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent
from prymatex.utils import encoding

class ManagedCacheMixin(object):
    def setManager(self, manager):
        self.manager = manager

    def sync(self):
        pass
    
    def close(self):
        pass

class SingleFileCache(ManagedCacheMixin):
    def __init__(self, path):
        self.path = path
        self.objs = shelve.open(self.path)

    def __contains__(self, key):
        key = self.manager.buildKey(key)
        return key in self.objs
    
    def get(self, key):
        key = self.manager.buildKey(key)
        return self.objs[key]
    
    def set(self, key, item):
        key = self.manager.buildKey(key)
        return self.objs.set(key, item)

    def setdefault(self, key, item):
        key = self.manager.buildKey(key)
        return self.objs.setdefault(key, item)

    def sync(self):
        self.objs.sync()
        
    def close(self):
        self.objs.close()

class MemoryCache(dict, ManagedCacheMixin):
    pass

class CacheManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.cacheDirectory = application.currentProfile.value('PMX_CACHE_PATH')
        self.caches = []

    def buildKey(self, text):
        """docstring for buildKey"""
        return hashlib.md5(encoding.force_bytes(text)).hexdigest()

    def __add_cache(self, cache):
        cache.setManager(self)
        self.caches.append(cache)
        
    def singleFileCache(self, cacheName):
        fileName = self.buildKey(cacheName)
        cachePath = os.path.join(self.cacheDirectory, fileName)
        cache = SingleFileCache(cachePath)
        self.__add_cache(cache)
        return cache
        
    def memoryCache(self, value):
        cache = MemoryCache()
        self.__add_cache(cache)
        return cache

    def sync(self):
        for cache in self.caches:
            cache.sync()

    def close(self):
        for cache in self.caches:
            cache.close()
