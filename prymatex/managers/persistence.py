#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent

class ManagedCacheMixin(object):
    def setManager(self, manager):
        self.manager = manager

    def sync(self):
        pass

class SingleFileCache(ManagedCacheMixin):
    def __init__(self, path):
        self.path = path

class MemoryCache(dict, ManagedCacheMixin):
    pass

class PersistenceManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.cacheDirectory = application.currentProfile.value('PMX_CACHE_PATH')
        self.caches = []

    def buildFileName(self, text):
        """docstring for buildKey"""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def singleFileCache(self, cacheName):
        fileName = self.buildFileName(cacheName)
        print(os.path.join(self.cacheDirectory, fileName))
    
    def memoryCache(self, value):
        cache = MemoryCache()
        cache.setManager(self)
        self.caches.append(cache)
        return cache

    def sync(self):
        for cache in self.caches:
            cache.sync()
