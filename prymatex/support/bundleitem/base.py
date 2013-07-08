#!/usr/bin/env python

import os

from prymatex.utils import osextra

from ..base import PMXManagedObject

class PMXBundleItem(PMXManagedObject):
    KEYS = ( 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass' )
    TYPE = ''
    EXTENSION = ''
    PATTERNS = ()
    DEFAULTS = {}
    
    def __init__(self, uuid):
        PMXManagedObject.__init__(self, uuid)
        self.bundle = None

    def setBundle(self, bundle):
        self.bundle = bundle
    
    def enabled(self):
        return self.bundle.enabled()

    def __load_update(self, dataHash, initialize):
        for key in PMXBundleItem.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if key == "scope":
                    self.selector = self.manager.createScopeSelector(value)
                setattr(self, key, value)

    def load(self, dataHash):
        self.__load_update(dataHash, True)
        
    def update(self, dataHash):
        self.__load_update(dataHash, False)
    
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

    def createDataFilePath(self, basePath, baseName = None):
        return osextra.path.ensure_not_exists(os.path.join(basePath, self.FOLDER, "%%s.%s" % self.EXTENSION), osextra.to_valid_name(baseName or self.name))
