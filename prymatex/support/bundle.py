#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil

from prymatex.utils import osextra
from prymatex.utils import programs

from .base import PMXManagedObject

class PMXBundle(PMXManagedObject):
    KEYS = ('name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13',
            'description', 'contactName', 'requiredCommands', 'require' )
    FILE = 'info.plist'
    TYPE = 'bundle'
    PATTERNS = ( '*.tmbundle', )
    DEFAULTS = {
        'name': 'Untitled'
    }
    def __init__(self, uuid, manager):
        PMXManagedObject.__init__(self, uuid, manager)
        self.populated = False

    def populate(self):
        self.populated = True

    def __load_update(self, dataHash, initialize):
        for key in PMXBundle.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))

    def load(self, dataHash):
        PMXManagedObject.load(self, dataHash)
        self.variables = None
        self.__load_update(dataHash, True)
        
    def update(self, dataHash):
        PMXManagedObject.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self):
        dataHash = PMXManagedObject.dump(self)
        for key in PMXBundle.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                dataHash[key] = value
        return dataHash

    # ---------------- Bundle Variables
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        environment['TM_BUNDLE_PATH'] = self.sourcePath()
        if self.variables is None:
            self.variables = {}
            for name, source in self.sources.items():
                supportPath = os.path.join(source.path, "Support")
                if os.path.exists(supportPath):
                    self.variables['TM_BUNDLE_SUPPORT'] = supportPath
                    break
            if self.requiredCommands:
                for program in self.requiredCommands:
                    if not programs.is_program_installed(program["command"]):
                        # Search in locations
                        for location in program["locations"]:
                            if os.path.exists(location):
                                self.variables[program["variable"]] = location
                                break
        environment.update(self.variables)
        return environment

    # --------------- Source Handlers
    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, "%s.tmbundle"), osextra.to_valid_name(self.name))
        
    @classmethod
    def dataFilePath(cls, sourceFilePath):
        return os.path.join(sourceFilePath, cls.FILE)
