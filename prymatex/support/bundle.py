#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, plistlib, shutil
from copy import copy

from prymatex.support.utils import readPlist

'''
    Este es el unico camino -> http://manual.macromates.com/en/
    http://manual.macromates.com/en/bundles
    http://blog.macromates.com/2005/introduction-to-scopes/
    http://manual.macromates.com/en/scope_selectors.html
'''

#Deprecar menu
class PMXMenuNode(object):
    MENU_SPACE = '-' * 36
    def __init__(self, name = None, items = [], excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.submenus = submenus
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != self.MENU_SPACE, self.items)))
        for uuid, submenu in self.submenus.iteritems():
            self[uuid] = PMXMenuNode(**submenu)

    @property
    def hash(self):
        hash = { 'items': self.items }
        if self.name != None:
            hash['name'] = self.name
        if self.excludedItems:
            hash['excludedItems'] = self.excludedItems
        if self.submenus:
            hash['submenus'] = {}
        for uuid in self.submenus.keys():
            submenu = self[uuid]
            if submenu != None:
                hash['submenus'].update( { uuid: submenu.hash } )
        return hash
            
    def __contains__(self, key):
        return key in self.main or any(map(lambda submenu: key in submenu, filter(lambda x: isinstance(x, PMXMenuNode), self.main.values())))

    def __getitem__(self, key):
        try:
            return self.main[key]
        except KeyError:
            for submenu in filter(lambda x: isinstance(x, PMXMenuNode), self.main.values()):
                if key in submenu:
                    return submenu[key]
        raise KeyError(key)
    
    def __setitem__(self, key, menu):
        if key in self.main:
            self.main[key] = menu
        else:
            for submenu in filter(lambda x: isinstance(x, PMXMenuNode), self.main.values()):
                if key in submenu:
                    submenu[key] = menu

    def iteritems(self):
        items = self.items
        if self.excludedItems:
            items = filter(lambda x: not x in self.excludedItems, items)
        for item in items:
            if item != self.MENU_SPACE:
                yield (item, self[item])
            else:
                yield (self.MENU_SPACE, self.MENU_SPACE)

class PMXManagedObject(object):
    def __init__(self, uuid, namespace, path):
        self.uuid = uuid
        self.namespaces = [ namespace ]
        self.path = path
        self.manager = None
    
    @property
    def isProtected(self):
        return self.manager.protectedNamespace in self.namespaces
        
    @property
    def isSafe(self):
        return len(self.namespaces) > 1
        
    @property
    def hash(self):
        return { 'uuid': unicode(self.uuid).upper() }
    
    def addNamespace(self, namespace):
        if namespace not in self.namespaces:
            index = self.manager.nsorder.index(namespace)
            if index < len(self.namespaces):
                self.namespaces.insert(index, namespace)
            else:
                self.namespaces.append(namespace)
    
    def setManager(self, manager):
        self.manager = manager
        
    def relocate(self, path):
        if os.path.exists(self.path):
            shutil.move(self.path, path)
    
class PMXBundle(PMXManagedObject):
    KEYS = [    'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]
    FILE = 'info.plist'
    TYPE = 'bundle'
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXBundle, self).__init__(uuid, namespace, path)
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
        #if self.mainMenu != None:
        #    self.mainMenu = PMXMenuNode(**self.mainMenu)

    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])
    
    @property
    def hash(self):
        hash = super(PMXBundle, self).hash
        for key in PMXBundle.KEYS:
            value = getattr(self, key)
            if value != None:
                #if key in ['mainMenu']:
                #    value = self.mainMenu.hash
                hash[key] = value
        return hash

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file = os.path.join(self.path , self.FILE)
        plistlib.writePlist(self.hash, file)

    def delete(self):
        #No se puede borrar si tiene items, sub archivos o subdirectorios
        os.unlink(os.path.join(self.path, self.FILE))
        try:
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(self.path)
        except os.OSError:
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
            data = readPlist(info_file)
            uuid = manager.uuidgen(data.pop('uuid', None))
            bundle = manager.getManagedObject(uuid)
            if bundle is None and not manager.isDeleted(uuid):
                bundle = cls(uuid, namespace, data, path)
                #Add and promote, capture bundle
                bundle.enabled = manager.isEnabled(bundle.uuid)
                bundle = manager.addBundle(bundle)
                manager.addManagedObject(bundle)
            elif bundle is not None:
                bundle.addNamespace(namespace)
        except Exception, e:
            print "Error in bundle %s (%s)" % (info_file, e)

class PMXBundleItem(PMXManagedObject):
    KEYS = [ 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]
    TYPE = ''
    FOLDER = ''
    EXTENSION = ''
    PATTERNS = []
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXBundleItem, self).__init__(uuid, namespace, path)
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
        plistlib.writePlist(self.hash, self.path)
    
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
            data = readPlist(path)
            uuid = manager.uuidgen(data.pop('uuid', None))
            item = manager.getManagedObject(uuid)
            if item is None and not manager.isDeleted(uuid):
                item = cls(uuid, namespace, data, path)
                #danger!!! add and populate
                item.setBundle(bundle)
                item = manager.addBundleItem(item)
                manager.addManagedObject(item)
            elif item is not None:
                item.addNamespace(namespace)
        except Exception, e:
            print "Error in bundle item %s (%s)" % (path, e)
    
    def execute(self, processor):
        pass
        