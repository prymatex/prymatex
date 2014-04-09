#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil

from prymatex.utils import osextra
from prymatex.utils import programs

from .base import ManagedObject

class Bundle(ManagedObject):
    KEYS = ('name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13',
            'description', 'contactName', 'requiredCommands', 'require' )
    FILE = 'info.plist'
    TYPE = 'bundle'
    SUPPORT = 'Support'
    PATTERNS = ( '*.tmbundle', )
    DEFAULTS = {
        'name': 'Untitled'
    }
    def __init__(self, uuid, manager):
        ManagedObject.__init__(self, uuid, manager)
        self._populated = False
        self._variables = None

    def setPopulated(self, populated):
        self._populated = populated

    def isPopulated(self):
        return self._populated

    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in Bundle.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))

    def load(self, dataHash):
        ManagedObject.load(self, dataHash)
        self.__load_update(dataHash, True)
        # Remove cached values
        self._variables = None

    def update(self, dataHash):
        ManagedObject.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self, allKeys = False):
        dataHash = ManagedObject.dump(self, allKeys)
        for key in Bundle.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                dataHash[key] = value
        return dataHash

    # ---------------- Variables
    def variables(self):
        if self._variables is None:
            self._variables = {}
            for name, source in self.sources.items():
                supportPath = os.path.join(source.path, self.SUPPORT)
                if os.path.exists(supportPath):
                    self._variables['TM_BUNDLE_SUPPORT'] = supportPath
                    break
            for program in self.requiredCommands or []:
                if not programs.is_program_installed(program["command"]):
                    # Search in locations
                    for location in program["locations"]:
                        if os.path.exists(location):
                            self._variables[program["variable"]] = location
                            break
        return self._variables.copy()

    # ------------------ Environment variables
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        environment['TM_BUNDLE_PATH'] = self.currentSourcePath()
        environment.update(self.variables())
        return environment

    # --------------- Source Handlers
    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, "%s.tmbundle"), osextra.to_valid_name(self.name))
        
    @classmethod
    def dataFilePath(cls, sourceFilePath):
        return os.path.join(sourceFilePath, cls.FILE)
