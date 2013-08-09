#!/usr/bin/env python

import os
from glob import glob
from functools import reduce
from collections import namedtuple

from prymatex.support import scripts
from prymatex.utils import six

Source = namedtuple("Source", "name path mtime")

class PMXManagedObject(object):
    PATTERNS = ()
    def __init__(self, uuid, manager):
        self.uuid = uuid
        self.manager = manager
        self.sources = {}
        self.pointer = None

    def uuidAsText(self):
        return six.text_type(self.uuid).upper()

    # ----------- Load from dictionary
    def load(self, dataHash):
        self.statics = []

    # ----------- Update from dictionary
    def update(self, dataHash):
        pass
    
    # ----------- Dump to dictionary
    def dump(self, allKeys = False):
        return { 'uuid': self.uuidAsText() }
    
    def hasChanged(self, dataHash):
        currentHash = self.dump(allKeys = True)
        for key, value in dataHash.items():
            if key not in currentHash or currentHash[key] != value:
                return True
        return False
        
    def enabled(self):
        return self.manager.isEnabled(self.uuid)

    # ------------ Object Sources
    def addSource(self, name, path):
        mtime = os.path.exists(path) and os.path.getmtime(path) or 0
        self.sources[name] = Source(name = name, path = path, mtime = mtime)
        if self.pointer is None:
            self.pointer = name

    def removeSource(self, name):
        del self.sources[name]

    def hasSource(self, name):
        return name in self.sources
    
    def sourcePath(self, name):
        return self.sources[name].path

    def setSourcePath(self, name, path):
        source = self.sources[name]
        self.sources[name] = source._replace(path = path, mtime = os.path.getmtime(path))

    def sourceChanged(self, name):
        source = self.sources[name]
        return source.mtime != os.path.getmtime(source.path)

    def updateMtime(self, name):
        source = self.sources[name]
        self.sources[name] = source._replace(mtime = os.path.getmtime(source.path))

    # ------------ Current Source, is the source in self.pointer
    def setCurrentSource(self, name):
        assert name in self.sources
        self.pointer = name

    def currentSourceName(self):
        return self.pointer
    
    def currentSourcePath(self):
        return self.sourcePath(self.pointer)

    def addStaticFile(self, staticPath):
        self.statics.append(staticPath)

    def removeStaticFile(self, staticPath):
        self.statics.remove(staticPath)

    def createSourcePath(self, baseDirectory):
        return baseDirectory

    @classmethod
    def staticFilePaths(cls, baseDirectory):
        return []

    @classmethod
    def dataFilePath(cls, sourcePath):
        return sourcePath
    
    @classmethod
    def sourcePaths(cls, baseDirectory):
        patterns = map(lambda pattern: os.path.join(baseDirectory, pattern), cls.PATTERNS)
        return reduce(lambda x, y: x + glob(y), patterns, [])
