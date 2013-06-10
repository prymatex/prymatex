#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent

class SingleFileCache(object):
    def __init__(self, manager, path):
        self.manager = manager
        self.path = path

class MemoryCache(object):
    def __init__(self, manager):
        self.manager = manager
        self.objects = {}
    
    def set(self, key, values):
        self.objects[key] = value

class PersistenceManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.cacheDirectory = application.currentProfile.value('PMX_CACHE_PATH')
        self.caches = []

    def buildFileName(self, text):
        """docstring for buildKey"""
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    def singleFileCache(self, value):
        fileName = self.buildFileName(value)
        print os.path.join(self.cacheDirectory, fileName)

    def sync(self):
        for cache in self.caches:
            cache.sync()
