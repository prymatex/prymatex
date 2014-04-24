#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import shelve
import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexComponent
from prymatex.utils import encoding

class ManagedStorage(object):
    def setManager(self, manager):
        self.manager = manager

    def make_key(self, key):
        return key

    def add(self, key, value):
        raise NotImplementedError('subclasses of ManagedStorage must provide an add() method')

    def get(self, key, default=None):
        raise NotImplementedError('subclasses of ManagedStorage must provide a get() method')

    def setdefault(self, key, default = None):
        raise NotImplementedError('subclasses of ManagedStorage must provide a setdefault() method')

    def set(self, key, value):
        raise NotImplementedError('subclasses of ManagedStorage must provide a set() method')

    def delete(self, key):
        raise NotImplementedError('subclasses of ManagedStorage must provide a delete() method')

    def has_key(self, key):
        return self.get(key) is not None

    def __contains__(self, key):
        # This is a separate method, rather than just a copy of has_key(),
        # so that it always has the same functionality as has_key(), even
        # if a subclass overrides it.
        return self.has_key(key)

    def clear(self):
        raise NotImplementedError('subclasses of ManagedStorage must provide a clear() method')

    def close(self, **kwargs):
        pass

class SingleFileStorage(ManagedStorage):
    def __init__(self, path):
        self.path = path
        self.objs = shelve.open(self.path, protocol = 2)

    def make_key(self, key):
        return str(hash(key))

    def get(self, key, default = None):
        return self.objs.get(self.make_key(key), default)

    def setdefault(self, key, default = None):
        return self.objs.setdefault(self.make_key(key), default)

    def set(self, key, value):
        self.objs[self.make_key(key)] = value

    def close(self):
        self.objs.close()

class MemoryStorage(dict, ManagedStorage):
    pass

class StorageManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(StorageManager, self).__init__(**kwargs)
        self.cacheDirectory = self.application.currentProfile.value('PMX_CACHE_PATH')
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

    def close(self):
        for storage in self.storages:
            storage.close()
