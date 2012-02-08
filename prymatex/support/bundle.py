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
    def __init__(self, uuid):
        self.uuid = uuid
        self.namespaces = []
        self.sources = {}
        self.manager = None
    
    @property
    def path(self):
        return self.sources[self.namespaces[-1]]

    @property
    def isProtected(self):
        return self.manager.protectedNamespace in self.namespaces
        
    @property
    def isSafe(self):
        return len(self.namespaces) > 1
        
    @property
    def hash(self):
        return { 'uuid': unicode(self.uuid).upper() }
    
    def hasNamespace(self, namespace):
        return namespace in self.namespaces

    def addSource(self, namespace, path):
        if namespace not in self.namespaces:
            index = self.manager.nsorder.index(namespace)
            if index < len(self.namespaces):
                self.namespaces.insert(index, namespace)
            else:
                self.namespaces.append(namespace)
            self.sources[namespace] = path
    
    def setManager(self, manager):
        self.manager = manager

    def relocate(self, path):
        if os.path.exists(self.path):
            shutil.move(self.path, path)
        self.sources[self.namespaces[-1]] = path

class PMXBundle(PMXManagedObject):
    KEYS = [    'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]
    FILE = 'info.plist'
    TYPE = 'bundle'
    def __init__(self, uuid, hash):
        PMXManagedObject.__init__(self, uuid)
        self.enabled = True
        self.populated = False
        self.support = None    #supportPath
        self.load(hash)

    def setSupport(self, support):
        self.support = support
        
    def load(self, hash):
        for key in PMXBundle.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)

    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])
    
    @property
    def hash(self):
        hash = super(PMXBundle, self).hash
        for key in PMXBundle.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file = os.path.join(self.path, self.FILE)
        plist.writePlist(self.hash, file)

    def delete(self):
        #No se puede borrar si tiene items, sub archivos o subdirectorios
        os.unlink(os.path.join(self.path, self.FILE))
        try:
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(self.path)
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
                #Add and promote, capture bundle
                bundle.enabled = manager.isEnabled(bundle.uuid)
                bundle = manager.addBundle(bundle)
                manager.addManagedObject(bundle)
            bundle.addSource(namespace, path)
        except Exception, e:
            print "Error in laod bundle %s (%s)" % (info_file, e)

    @classmethod
    def reloadBundle(cls, path, namespace, manager):
        info_file = os.path.join(path, cls.FILE)
        #TODO: Ver si se modifico el archivo para no cargar al pedo
        try:
            data = plist.readPlist(info_file)
            uuid = manager.uuidgen(data.pop('uuid', None))
            bundle = manager.getManagedObject(uuid)
            #TODO: Hacer el reload
        except Exception, e:
            print "Error in reload bundle %s (%s)" % (info_file, e)
            
class PMXBundleItem(PMXManagedObject):
    KEYS = [ 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]
    TYPE = ''
    FOLDER = ''
    EXTENSION = ''
    PATTERNS = []
    def __init__(self, uuid, hash):
        PMXManagedObject.__init__(self, uuid)
        self.bundle = None
        self.load(hash)

    def setBundle(self, bundle):
        self.bundle = bundle
    
    @property
    def enabled(self):
        return self.bundle.enabled
    
    def load(self, hash):
        for key in PMXBundleItem.KEYS:
            setattr(self, key, hash.get(key, None))
    
    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])
    
    def isChanged(self, hash):
        for key in hash.keys():
            if getattr(self, key) != hash[key]:
                return True
        return False
    
    @property
    def hash(self):
        hash = super(PMXBundleItem, self).hash
        for key in PMXBundleItem.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash

    def save(self):
        dir = os.path.dirname(self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        plist.writePlist(self.hash, self.path)
    
    def delete(self):
        os.unlink(self.path)
        dir = os.path.dirname(self.path)
        try:
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(dir)
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
                #danger!!! add and populate
                item.setBundle(bundle)
                item = manager.addBundleItem(item)
                manager.addManagedObject(item)
            item.addSource(namespace, path)
        except Exception, e:
            print "Error in bundle item %s (%s)" % (path, e)
    
    @classmethod
    def reloadBundleItem(cls, path, namespace, bundle, manager):
        try:
            data = plist.readPlist(path)
            uuid = manager.uuidgen(data.pop('uuid', None))
            item = manager.getManagedObject(uuid)
            #TODO: Hacer el reload
        except Exception, e:
            print "Error in bundle item %s (%s)" % (path, e)

    def execute(self, processor):
        pass
        