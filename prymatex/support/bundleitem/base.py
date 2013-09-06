#!/usr/bin/env python

import os
from glob import glob
from functools import reduce

from prymatex.utils import osextra

from ..base import PMXManagedObject

class PMXBundleItem(PMXManagedObject):
    KEYS = ( 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass' )
    TYPE = ''
    EXTENSION = ''
    FOLDER = ''
    PATTERNS = ()
    DEFAULTS = {}
    
    def __init__(self, uuid, manager, bundle):
        PMXManagedObject.__init__(self, uuid, manager)
        self.bundle = bundle

    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in PMXBundleItem.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if key == "scope":
                    self.selector = self.manager.selectorFactory(value)
                setattr(self, key, value)

    def load(self, dataHash):
        PMXManagedObject.load(self, dataHash)
        self.__load_update(dataHash, True)

    def update(self, dataHash):
        PMXManagedObject.update(self, dataHash)
        self.__load_update(dataHash, False)
    
    def dump(self, allKeys = False):
        dataHash = PMXManagedObject.dump(self, allKeys)
        for key in PMXBundleItem.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                dataHash[key] = value
        return dataHash

    def enabled(self):
        return self.bundle.enabled()

    # ---------------- Environment Variables
    def environmentVariables(self):
        return self.bundle.environmentVariables()

    def keyCode(self):
        return self.keyEquivalent
    
    # ---------------- The executor method
    def execute(self, processor):
        pass

    @classmethod
    def sourcePaths(cls, baseDirectory):
        patterns = map(lambda pattern: os.path.join(baseDirectory, cls.FOLDER, pattern), cls.PATTERNS)
        return reduce(lambda x, y: x + glob(y), patterns, [])
    
    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, self.FOLDER, "%%s.%s" % self.EXTENSION), osextra.to_valid_name(self.name))
