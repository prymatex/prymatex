#!/usr/bin/env python

import os
from prymatex.support import scope, scripts

class PMXManagedObject(object):
    _PATH = 0
    _MTIME = 1
    def __init__(self, uuid):
        self.uuid = uuid
        self.namespaces = []
        self.sources = {}
        self.manager = None
        self.populated = False
        self.statics = []

    # ----------- Load from dictionary
    def load(self, dataHash):
        raise NotImplemented

    # ----------- Update from dictionary
    def update(self, dataHash):
        raise NotImplemented
    
    # ----------- Dump to dictionary
    def dump(self):
        return { 'uuid': self.uuidAsUnicode() }
    
    def uuidAsUnicode(self):
        return str(self.uuid).upper()

    def populate(self):
        self.populated = True
    
    def enabled(self):
        return self.manager.isEnabled(self.uuid)
    
    def path(self, namespace):
        return self.sources[namespace][self._PATH]

    def currentPath(self):
        return self.sources[self.currentNamespace()][self._PATH]

    def isProtected(self):
        return self.manager.protectedNamespace() in self.namespaces
        
    def isSafe(self):
        return len(self.namespaces) > 1
    
    def hasNamespace(self, namespace):
        return namespace in self.namespaces

    def currentNamespace(self):
        return self.namespaces[-1]

    def sourceChanged(self, namespace):
        return self.sources[namespace][self._MTIME] != os.path.getmtime(self.sources[namespace][self._PATH])

    def removeSource(self, namespace):
        if namespace in self.namespaces:
            self.namespaces.remove(namespace)
            self.sources.pop(namespace)

    def addSource(self, namespace, path):
        if namespace not in self.namespaces:
            index = self.manager.nsorder.index(namespace)
            if index < len(self.namespaces):
                self.namespaces.insert(index, namespace)
            else:
                self.namespaces.append(namespace)
            self.setSource(namespace, path)
            
    def setSource(self, namespace, path):
        self.sources[namespace] = (path, 0)

    def hasSources(self):
        return bool(self.sources)

    def staticPaths(self):
        return []

    def addStaticFile(self, staticPath):
        self.statics.append(staticPath)

    def removeStaticFile(self, staticPath):
        self.statics.remove(staticPath)
        
    def createDataFilePath(self, basePath, baseName = None):
        return os.path.join(basePath, baseName or '')

    @classmethod
    def dataFilePath(cls, path):
        return path
        
    def updateMtime(self, namespace):
        path = self.sources[namespace][self._PATH]
        self.sources[namespace] = (path, os.path.getmtime(path))

    def setDirty(self):
        for namespace in self.namespaces:
            self.sources[namespace] = (self.sources[namespace][self._PATH], 0)

    def setManager(self, manager):
        self.manager = manager

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