#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil
from copy import copy

from prymatex.utils import plist
from prymatex.utils import encoding
from prymatex.support import scope, utils

"""
Este es el unico camino -> http://manual.macromates.com/en/
http://manual.macromates.com/en/bundles
http://blog.macromates.com/2005/introduction-to-scopes/
http://manual.macromates.com/en/scope_selectors.html
"""

class PMXManagedObject(object):
    _PATH = 0
    _MTIME = 1
    def __init__(self, uuid):
        self.uuid = uuid
        self.namespaces = []
        self.sources = {}
        self.manager = None
        self.populated = False
        # TODO: mover esto a los bundle item
        self.statics = []

    def load(self, dataHash):
        raise NotImplemented

    def update(self, dataHash):
        raise NotImplemented
    
    def save(self, namespace):
        raise NotImplemented

    def delete(self, namespace):
        raise NotImplemented

    def uuidAsUnicode(self):
        return str(self.uuid).upper()

    def populate(self):
        self.populated = True
    
    @property
    def enabled(self):
        return self.manager.isEnabled(self.uuid)
                
    @property
    def hash(self):
        return { 'uuid': self.uuidAsUnicode() }

    def path(self, namespace):
        return self.sources[namespace][self._PATH]

    @property
    def currentPath(self):
        return self.sources[self.currentNamespace][self._PATH]

    def isProtected(self):
        return self.manager.protectedNamespace() in self.namespaces
        
    def isSafe(self):
        return len(self.namespaces) > 1
    
    def hasNamespace(self, namespace):
        return namespace in self.namespaces

    @property
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
        if os.path.exists(self.path(namespace)):
            shutil.move(self.path(namespace), path)
            self.sources[namespace] = (path, os.path.getmtime(path))
        else:
            self.sources[namespace] = (path, 0)

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
        for key in list(dataHash.keys()):
            setattr(self, key, dataHash[key])
    
    @property
    def hash(self):
        dataHash = super(PMXBundle, self).hash
        for key in PMXBundle.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash

    def save(self, namespace):
        # TODO: todo esto mandarlo al manager
        if not os.path.exists(self.path(namespace)):
            os.makedirs(self.path(namespace))
        dataFile = self.dataFilePath(self.path(namespace))
        plist.writePlist(self.hash, dataFile)
        self.updateMtime(namespace)

    def delete(self, namespace):
        #No se puede borrar si tiene items, sub archivos o subdirectorios
        os.unlink(self.dataFilePath(self.path(namespace)))
        try:
            #Este a diferencia de los items borra todo el directorio
            shutil.rmtree(self.path(namespace))
        except:
            pass
    
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        environment['TM_BUNDLE_PATH'] = self.currentPath
        if self.hasSupportPath():
            environment['TM_BUNDLE_SUPPORT'] = self.supportPath()
        return environment

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

class PMXBundleItem(PMXManagedObject):
    KEYS = [ 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass' ]
    TYPE = ''
    FOLDER = ''
    EXTENSION = ''
    PATTERNS = []
    def __init__(self, uuid):
        PMXManagedObject.__init__(self, uuid)
        self.bundle = None

    def setBundle(self, bundle):
        self.bundle = bundle
    
    @property
    def enabled(self):
        return self.bundle.enabled

    def load(self, dataHash):
        for key in PMXBundleItem.KEYS:
            value = dataHash.get(key, None)
            if key == "scope":
                self.selector = scope.Selector(value)
            setattr(self, key, value)

    def update(self, dataHash):
        for key in list(dataHash.keys()):
            value = dataHash[key]
            if key == "scope":
                self.selector = scope.Selector(value)
            setattr(self, key, value)

    def isChanged(self, dataHash):
        for key in list(dataHash.keys()):
            if getattr(self, key) != dataHash[key]:
                return True
        return False

    @property
    def hash(self):
        dataHash = super(PMXBundleItem, self).hash
        for key in PMXBundleItem.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash

    def save(self, namespace):
        #TODO: Si puedo garantizar el guardado con el manager puedo controlar los mtime en ese punto
        dir = os.path.dirname(self.path(namespace))
        if not os.path.exists(dir):
            os.makedirs(dir)
        plist.writePlist(self.hash, self.path(namespace))
        self.updateMtime(namespace)
    
    def delete(self, namespace):
        os.unlink(self.path(namespace))
        folder = os.path.dirname(self.path(namespace))
        try:
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(folder)
        except:
            pass
    
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
        
    @property
    def enabled(self):
        return self.parentItem.enabled
        
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
        self.shellCommand, self.environment, self.tempFile = utils.prepareShellScript(self.shellCommand, self.environment)
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
            utils.deleteFile(self.tempFile)

