#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil

from prymatex.utils import encoding
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
            self.sources[namespace] = (path, os.path.exists(path) and os.path.getmtime(path) or 0)

    def hasSources(self):
        return bool(self.sources)
        
    def relocateSource(self, namespace, path):
        shutil.move(self.path(namespace), path)
        self.sources[namespace] = (path, os.path.getmtime(path))

    def staticPaths(self):
        return []

    def addStaticFile(self, staticPath):
        self.statics.append(staticPath)

    def removeStaticFile(self, staticPath):
        self.statics.remove(staticPath)
        
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
        
class PMXBundle(PMXManagedObject):
    KEYS = (    'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13',
                'description', 'contactName', 'requiredCommands', 'require' )
    FILE = 'info.plist'
    TYPE = 'bundle'
    def __init__(self, uuid):
        PMXManagedObject.__init__(self, uuid)
        self.__supportPath = None

    def hasSupportPath(self):
        return self.__supportPath is not None
        
    def setSupportPath(self, supportPath):
        self.__supportPath = supportPath
    
    def supportPath(self):
        return self.__supportPath
    
    def relocateSupport(self, path):
        try:
            # TODO Ver que pasa si ya existe support
            shutil.copytree(self.supportPath(), path, symlinks = True)
            self.setSupportPath(path)
        except:
            pass
    
    def load(self, dataHash):
        for key in PMXBundle.KEYS:
            setattr(self, key, dataHash.get(key, None))

    def update(self, dataHash):
        for key in PMXBundle.KEYS:
            if not dataHash.has_key(key):
                continue
            setattr(self, key, dataHash[key])
    
    def dump(self):
        dataHash = super(PMXBundle, self).dump()
        for key in PMXBundle.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                dataHash[key] = value
        return dataHash

    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        environment['TM_BUNDLE_PATH'] = self.currentPath()
        if self.hasSupportPath():
            environment['TM_BUNDLE_SUPPORT'] = self.supportPath()
        return environment

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

class PMXBundleItem(PMXManagedObject):
    KEYS = ( 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass' )
    TYPE = ''
    FOLDER = ''
    EXTENSION = ''
    PATTERNS = []
    def __init__(self, uuid):
        PMXManagedObject.__init__(self, uuid)
        self.bundle = None

    def setBundle(self, bundle):
        self.bundle = bundle
    
    def enabled(self):
        return self.bundle.enabled()

    def load(self, dataHash):
        for key in PMXBundleItem.KEYS:
            value = dataHash.get(key, None)
            if key == "scope":
                self.selector = self.manager.createScopeSelector(value)
            setattr(self, key, value)

    def update(self, dataHash):
        for key in PMXBundleItem.KEYS:
            if not dataHash.has_key(key):
                continue
            value = dataHash[key]
            if key == "scope":
                self.scopeSelector = self.manager.createScopeSelector(value)
            setattr(self, key, value)
                
    def dump(self):
        dataHash = super(PMXBundleItem, self).dump()
        for key in PMXBundleItem.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                dataHash[key] = value
        return dataHash

    def isChanged(self, dataHash):
        for key in dataHash.keys():
            if getattr(self, key) != dataHash[key]:
                return True
        return False

    def environmentVariables(self):
        return self.bundle.environmentVariables()
    
    def execute(self, processor):
        pass

class PMXStaticFile(object):
    TYPE = 'staticfile'
    def __init__(self, path, parentItem):
        self.path = path
        self.name = os.path.basename(path)
        self.parentItem = parentItem

    def hasNamespace(self, namespace):
        return self.parentItem.hasNamespace(namespace)
        
    def enabled(self):
        return self.parentItem.enabled()
        
    def getFileContent(self):
        content = ""
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                content = encoding.from_fs(f.read())
        return content
    
    def setFileContent(self, content):
        if os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write(encoding.to_fs(content))
    content = property(getFileContent, setFileContent)

    def update(self, dataHash):
        for key in list(dataHash.keys()):
            setattr(self, key, dataHash[key])
    
    def relocate(self, path):
        if os.path.exists(self.path):
            shutil.move(self.path, path)
        self.name = os.path.basename(path)
    
    def save(self, basePath = None):
        path = os.path.join(basePath, self.name) if basePath is not None else self.path
        with open(path, 'w') as f:
            f.write(encoding.to_fs(self.content))
        self.path = path

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