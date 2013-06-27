#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent
from prymatex.utils import encoding

class ManagedStorageMixin(object):
    def setManager(self, manager):
        self.manager = manager

    def sync(self):
        pass

    def close(self):
        pass

class SingleFileStorage(ManagedStorageMixin):
    def __init__(self, path):
        self.path = path
        self.objs = shelve.open(self.path)

    def build_key(self, key):
        return str(hash(key))

    def __contains__(self, key):
        return self.build_key(key) in self.objs

    def get(self, key):
        return self.objs[self.build_key(key)]

    def set(self, key, item):
        self.objs[self.build_key(key)] = item

    def setdefault(self, key, item):
        return self.objs.setdefault(self.build_key(key), item)

    def sync(self):
        self.objs.sync()

    def close(self):
        self.objs.close()

class MemoryStorage(dict, ManagedStorageMixin):
    pass

class StorageManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.cacheDirectory = application.currentProfile.value('PMX_CACHE_PATH')
        self.storages = []

    def buildFileName(self, text):
        """docstring for buildFileName"""
        return hashlib.md5(encoding.force_bytes(text)).hexdigest()

    def __add_storage(self, storage):
        storage.setManager(self)
        self.storages.append(storage)

    def singleFileStorage(self, storageName):
        fileName = self.buildFileName(storageName)
        storagePath = os.path.join(self.cacheDirectory, fileName)
        storage = SingleFileStorage(storagePath)
        self.__add_storage(storage)
        return storage

    def memoryStorage(self, value):
        storage = MemoryStorage()
        self.__add_storage(storage)
        return storage

    def sync(self):
        for storage in self.storages:
            storage.sync()

    def close(self):
        for storage in self.storages:
            storage.close()
