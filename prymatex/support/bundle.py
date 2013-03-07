#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil
from copy import copy

from prymatex.utils import plist
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

    def load(self, dataHash):
        raise NotImplemented

    def update(self, dataHash):
        raise NotImplemented
    
    def save(self, namespace):
        raise NotImplemented

    def delete(self, namespace):
        raise NotImplemented

    def uuidAsUnicode(self):
        return unicode(self.uuid).upper()

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

    @property
    def isProtected(self):
        return self.manager.protectedNamespace in self.namespaces
        
    @property
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
    
    def updateMtime(self, namespace):
        path = self.sources[namespace][self._PATH]
        self.sources[namespace] = (path, os.path.getmtime(path))

    def setDirty(self):
        for namespace in self.namespaces:
            self.sources[namespace] = (self.sources[namespace][self._PATH], 0)

    def setManager(self, manager):
        self.manager = manager

class PMXBundle(PMXManagedObject):
    KEYS = [    'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]
    FILE = 'info.plist'
    TYPE = 'bundle'
    def __init__(self, uuid, dataHash):
        PMXManagedObject.__init__(self, uuid)
        self.populated = False
        self.support = None    #supportPath
        self.load(dataHash)

    def hasSupport(self):
        return self.support is not None
        
    def setSupport(self, support):
        self.support = support
            
    def relocateSupport(self, path):
        assert self.hasSupport(), "bundle has not support"
        try:
            # TODO Ver que pasa si ya existe support
            shutil.copytree(self.support, path, symlinks = True)
            self.support = path
        except:
            pass
        
    def load(self, dataHash):
        for key in PMXBundle.KEYS:
            setattr(self, key, dataHash.get(key, None))

    def update(self, dataHash):
        for key in dataHash.keys():
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
        if not os.path.exists(self.path(namespace)):
            os.makedirs(self.path(namespace))
        file = os.path.join(self.path(namespace), self.FILE)
        plist.writePlist(self.hash, file)
        self.updateMtime(namespace)

    def delete(self, namespace):
        #No se puede borrar si tiene items, sub archivos o subdirectorios
        os.unlink(os.path.join(self.path(namespace), self.FILE))
        try:
            #Este a diferencia de los items borra todo el directorio
            shutil.rmtree(self.path(namespace))
        except:
            pass
    
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        environment['TM_BUNDLE_PATH'] = self.currentPath
        if self.support != None:
            environment['TM_BUNDLE_SUPPORT'] = self.support
        return environment
        
    @classmethod
    def loadBundle(cls, path, namespace, manager):
        info_file = os.path.join(path, cls.FILE)
        try:
            data = plist.readPlist(info_file)
            uuid = manager.uuidgen(data.pop('uuid', None))
            bundle = manager.getManagedObject(uuid)
            if bundle is None and not manager.isDeleted(uuid):
                bundle = cls(uuid, data)
                bundle.setManager(manager)
                bundle.addSource(namespace, path)
                bundle = manager.addBundle(bundle)
                manager.addManagedObject(bundle)
            elif bundle is not None:
                bundle.addSource(namespace, path)
            return bundle
        except Exception, e:
            print "Error in laod bundle %s (%s)" % (info_file, e)

    @classmethod
    def reloadBundle(cls, bundle, path, namespace, manager):
        info_file = os.path.join(path, cls.FILE)
        data = plist.readPlist(info_file)
        bundle.load(data)

class PMXBundleItem(PMXManagedObject):
    KEYS = [ 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass' ]
    TYPE = ''
    FOLDER = ''
    EXTENSION = ''
    PATTERNS = []
    def __init__(self, uuid, dataHash):
        PMXManagedObject.__init__(self, uuid)
        self.bundle = None
        self.load(dataHash)

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
        for key in dataHash.keys():
            value = dataHash[key]
            if key == "scope":
                self.selector = scope.Selector(value)
            setattr(self, key, value)
    
    def isChanged(self, dataHash):
        for key in dataHash.keys():
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
        
    @classmethod
    def loadBundleItem(cls, path, namespace, bundle, manager):
        try:
            data = plist.readPlist(path)
            uuid = manager.uuidgen(data.pop('uuid', None))
            item = manager.getManagedObject(uuid)
            if item is None and not manager.isDeleted(uuid):
                item = cls(uuid, data)
                item.setBundle(bundle)
                item.setManager(manager)
                item.addSource(namespace, path)
                item = manager.addBundleItem(item)
                manager.addManagedObject(item)
            elif item is not None:
                item.addSource(namespace, path)
            return item
        except Exception, e:
            print "Error in bundle item %s (%s)" % (path, e)
    
    @classmethod
    def reloadBundleItem(cls, bundleItem, path, namespace, manager):
        data = plist.readPlist(path)
        bundleItem.load(data)

    def execute(self, processor):
        pass
        
class PMXRunningContext(object):
    TEMPLATE = u"""Item Name: {itemName}
    Asynchronous: {asynchronous}
    Working Directory: {workingDirectory}
    Input:  Type {inputType}, Value {inputValue}
    Environment: {environment}
    Output: Type {outputType}, Value {outputValue}
    """
    def __init__(self, bundleItem, shellCommand, environment):
        self.bundleItem = bundleItem
        self.inputType, self.inputValue = None, None
        self.shellCommand = shellCommand
        self.environment = environment
        self.asynchronous = False
        self.outputValue = self.outputType = None
        self.workingDirectory = None
        
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

    def description(self):
        return self.bundleItem.name or "No Name"
        
    def removeTempFile(self):
        if os.path.exists(self.tempFile):
            utils.deleteFile(self.tempFile)