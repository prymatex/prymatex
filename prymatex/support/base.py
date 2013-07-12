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

    # ----------- Load from dictionary
    def load(self, dataHash):
        self.statics = []

    # ----------- Update from dictionary
    def update(self, dataHash):
        pass
    
    # ----------- Dump to dictionary
    def dump(self):
        return { 'uuid': self.uuidAsUnicode() }
    
    def uuidAsUnicode(self):
        return str(self.uuid).upper()

    def enabled(self):
        return self.manager.isEnabled(self.uuid)
    
    def setSource(self, name):
        assert name in self.sources
        self.pointer = name

    def addSource(self, name, path):
        mtime = os.path.exists(path) and os.path.getmtime(path) or 0
        self.sources[name] = Source(name = name, path = path, mtime = mtime)
        if self.pointer is None:
            self.pointer = name

    def removeSource(self, name):
        del self.sources[name]

    def hasSource(self, name):
        return name in self.sources
    hasNamespace = hasSource
    
    def sourceName(self):
        return self.pointer
    
    def sourcePath(self, name = None):
        return self.sources[name or self.pointer].path
    
    def sourceChanged(self, sourceName):
        source = self.sources[sourceName]
        return source.mtime != os.path.getmtime(source.path)

    def updateMtime(self, sourceName):
        source = self.sources[sourceName]
        self.sources[sourceName] = source._replace(mtime = os.path.getmtime(source.path))

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

class PMXRunningContext(object):
    TEMPLATE = """Item Name: {itemName}
    Asynchronous: {asynchronous}
    Working Directory: {workingDirectory}
    Input:  Type {inputType}, Value {inputValue}
    Environment: {environment}
    Output: Type {outputType}, Value {outputValue}
    """
    def __init__(self, bundleItem, shellCommand, environment):
        self.bundleItem = bundleItem
        self.inputType = self.inputValue = None
        self.shellCommand = shellCommand
        self.process = None
        self.environment = environment
        self.asynchronous = False
        self.outputValue = self.outputType = None
        self.workingDirectory = None

    def setShellCommand(self, shellCommand):
        # Set new shell command clean old values
        self.removeTempFile()
        self.inputType = self.inputValue = None
        self.outputValue = self.outputType = None
        self.shellCommand = shellCommand

    def __enter__(self):
        #Build the full las environment with gui environment and support environment
        self.shellCommand, self.environment, self.tempFile = scripts.prepareShellScript(self.shellCommand, self.environment)
        return self

    def __exit__(self, type, value, traceback):
        if not self.asynchronous:
            self.removeTempFile()

    def __unicode__(self):
        return self.TEMPLATE.format(
                itemName = self.bundleItem.name,
                asynchronous = self.asynchronous,
                workingDirectory = self.workingDirectory,
                inputType = self.inputType,
                inputValue = self.inputValue,
                environment = self.environment,
                outputType = self.outputType,
                outputValue = self.outputValue
        )

    def __str__(self):
        return self.TEMPLATE.format(
                itemName = self.bundleItem.name,
                asynchronous = self.asynchronous,
                workingDirectory = self.workingDirectory,
                inputType = self.inputType,
                inputValue = self.inputValue,
                environment = self.environment,
                outputType = self.outputType,
                outputValue = self.outputValue
        )

    def isBundleItem(self, bundleItem):
        return self.bundleItem == bundleItem

    def description(self):
        return self.bundleItem.name or "No Name"
        
    def removeTempFile(self):
        if os.path.exists(self.tempFile):
            scripts.deleteFile(self.tempFile)