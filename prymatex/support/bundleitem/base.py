#!/usr/bin/env python

import os
import glob

from prymatex.utils import osextra

from ..base import ManagedObject

class BundleItem(ManagedObject):
    KEYS = ( 'name', 'tabTrigger', 'keyEquivalent', 'scope', 'semanticClass', 'bundleUUID' )
    EXTENSION = ''
    FOLDER = ''
    PATTERNS = ()
    DEFAULTS = {}
    
    def __init__(self, uuid, manager, bundle):
        super(BundleItem, self).__init__(uuid, manager)
        self.bundle = bundle

    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in BundleItem.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if key == "scope":
                    self.selector = self.manager.selectorFactory(value)
                elif key == "bundleUUID" and value is not None:
                    value = self.manager.uuidgen(value)
                setattr(self, key, value)

    def load(self, dataHash):
        ManagedObject.load(self, dataHash)
        self.__load_update(dataHash, True)

    def update(self, dataHash):
        ManagedObject.update(self, dataHash)
        self.__load_update(dataHash, False)
    
    def dump(self, allKeys = False):
        dataHash = ManagedObject.dump(self, allKeys)
        for key in BundleItem.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                if key == "bundleUUID" and value is not None:
                    value = self.manager.uuidtotext(value)
                dataHash[key] = value
        return dataHash

    def enabled(self):
        return self.bundle.enabled()

    def variables(self):
        return self.bundle.variables()

    # ---------------- Environment Variables
    def environmentVariables(self):
        return self.bundle.environmentVariables()

    def keyCode(self):
        return self.keyEquivalent
    
    # ---------------- The executor method
    def execute(self, processor):
        raise NotImplementedError()

    @classmethod
    def sourcePaths(cls, baseDirectory):
        sourcePatterns = map(
            lambda pattern: os.path.join(baseDirectory, cls.FOLDER, pattern),
            cls.PATTERNS
        )
        for sourcePattern in sourcePatterns:
            for sourcePath in glob.iglob(sourcePattern):
                yield sourcePath

    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(
            os.path.join(baseDirectory, self.FOLDER, "%%s.%s" % self.EXTENSION), 
            osextra.to_valid_name(self.name))
