#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent

class PythonObjectsCache(object):
    pass

class PersistenceManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.caches = []
        
    def buildKey(self, content):
        """docstring for buildKey"""
        return hashlib.sha1(content.encode("utf-8")).hexdigest()
        
    def sync(self):
        for cache in self.caches:
            cache.sync()
