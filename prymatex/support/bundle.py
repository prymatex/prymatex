#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil
from copy import copy

from prymatex.utils import plist

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

    @property
    def enabled(self):
        return self.manager.isEnabled(self.uuid)
                
    @property
    def hash(self):
        return { 'uuid': unicode(self.uuid).upper() }

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

    def setSupport(self, support):
        self.support = support
        
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
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(self.path(namespace))
        except:
            pass
            
    def buildEnvironment(self):
        env = copy(self.manager.buildEnvironment())
        env['TM_BUNDLE_PATH'] = self.path
        if self.support != None:
            env['TM_BUNDLE_SUPPORT'] = self.support
        return env

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
    KEYS = [ 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]
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
            setattr(self, key, dataHash.get(key, None))
    
    def update(self, dataHash):
        for key in dataHash.keys():
            setattr(self, key, dataHash[key])
    
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
    
    def buildEnvironment(self, **kwargs):
        env = self.bundle.buildEnvironment()
        return env
        
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
    def __init__(self, bundleItem):
        self.bundleItem = bundleItem
        self.inputType, self.inputValue = None, None
        self.shellCommand, self.environment = "", {}
        self.asynchronous = False
        self.outputValue = self.outputType = None
        self.workingDirectory = None
        
    def description(self):
        return self.bundleItem.name