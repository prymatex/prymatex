#!/usr/bin/env python

import os
from glob import glob
from functools import reduce

from prymatex.utils import osextra
from prymatex.utils import programs

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
        PMXManagedObject.load(self, dataHash)
        self.variables = None
        self.__load_update(dataHash, True)

    def update(self, dataHash):
        PMXManagedObject.update(self, dataHash)
        self.__load_update(dataHash, False)
    
    def dump(self):
        dataHash = PMXManagedObject.dump(self)
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
        environment = self.bundle.environmentVariables()
        if self.variables is None:
            self.variables = {}
            if hasattr(self, 'requiredCommands') and self.requiredCommands:
                for program in self.requiredCommands:
                    if not programs.is_program_installed(program["command"]):
                        # Search in locations
                        for location in program["locations"]:
                            if os.path.exists(location):
                                self.variables[program["variable"]] = location
                                break
        environment.update(self.variables)
        return environment
        
    def execute(self, processor):
        pass

    @classmethod
    def sourcePaths(cls, baseDirectory):
        patterns = map(lambda pattern: os.path.join(baseDirectory, cls.FOLDER, pattern), cls.PATTERNS)
        return reduce(lambda x, y: x + glob(y), patterns, [])
    
    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, self.FOLDER, "%%s.%s" % self.EXTENSION), osextra.to_valid_name(self.name))
