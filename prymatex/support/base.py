#!/usr/bin/env python

import os
import glob

from prymatex.support import scripts
from prymatex.utils import six

from prymatex.core import source

class ManagedObject(object):
    PATTERNS = ()
    def __init__(self, uuid, manager):
        super(ManagedObject, self).__init__()
        self.uuid = uuid
        self.manager = manager
        self.sources = {}
        self.current_source = None
        self.static_files = []

    def __eq__(self, other):
        return self.uuid == other.uuid
    
    def __hash__(self):
        return hash(self.uuid)

    @classmethod
    def type(cls):
        "Return a string based on class name"
        return cls.__name__.lower()

    def uuidAsText(self):
        return self.manager.uuidtotext(self.uuid)

    # ----------- Load from dictionary
    def load(self, data_hash):
        self.static_files = []

    # ----------- Update from dictionary
    def update(self, data_hash):
        pass
    
    # ----------- Dump to dictionary
    def dump(self, allKeys=False):
        return { 'uuid': self.uuidAsText() }
    
    def hasChanged(self, data_hash):
        currentHash = self.dump(allKeys=True)
        for key, value in data_hash.items():
            if key not in currentHash or currentHash[key] != value:
                return True
        return False
        
    def enabled(self):
        return self.manager.isEnabled(self.uuid)

    # ------------ Object Sources
    def addSource(self, name, path):
        self.current_source = self.sources.setdefault(name, 
            source.Source(name=name, path=path)
        )

    def removeSource(self, name):
        del self.sources[name]

    def hasSource(self, name):
        return name in self.sources
    
    def sourcePath(self, name):
        return self.sources[name].path

    def setSourcePath(self, name, path):
        source = self.sources[name]
        self.sources[name] = source.newPath(path)

    def sourceHasChanged(self, name):
        source = self.sources[name]
        return source.hasChanged()

    def updateTime(self, name):
        source = self.sources[name]
        self.sources[name] = source.newUpdatedTime()

    # ------------ Current Source, is the source in self.current_source
    def setCurrentSource(self, name):
        assert name in self.sources
        self.current_source = self.sources[name]

    def currentSource(self):
        return self.current_source
        
    def currentSourceName(self):
        return self.current_source.name
    
    def currentSourcePath(self):
        return self.current_source.path

    def addStaticFile(self, static_path):
        self.static_files.append(static_path)

    def removeStaticFile(self, static_path):
        self.static_files.remove(static_path)

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
        sourcePatterns = map(
            lambda pattern: os.path.join(baseDirectory, pattern),
            cls.PATTERNS
        )
        for sourcePattern in sourcePatterns:
            for sourcePath in glob.iglob(sourcePattern):
                yield sourcePath
