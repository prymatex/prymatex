#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil

from prymatex.core import config
from prymatex.utils import osextra
from prymatex.utils import programs

from .base import ManagedObject

class Bundle(ManagedObject):
    KEYS = ('name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13',
            'description', 'contactName', 'requiredCommands', 'require' )
    FILE = 'info.plist'
    TYPE = 'bundle'
    PATTERNS = ( '*.tmbundle', )
    DEFAULTS = {
        'name': 'Untitled'
    }
    def __init__(self, uuid, manager):
        ManagedObject.__init__(self, uuid, manager)
        self._populated = False

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

    def supportPath(self):
        for name, source in self.sources.items():
            supportPath = os.path.join(source.path, config.PMX_SUPPORT_NAME)
            if os.path.exists(supportPath):
                return supportPath

    # ---------------- Variables
    def shellVariables(self, environment):
        variables = []
        for r in self.require or []:
            bundle = self.manager.getBundle(r["uuid"])
            # TODO: Recursivo ?
            if bundle is not None:
                variables.extend(bundle.shellVariables())
                support = bundle.supportPath()
                if support is not None:
                    variables.append(("TM_%s_BUNDLE_SUPPORT" % r["name"].upper(), support))
        support = self.supportPath()
        if support is not None:
            variables.append(('TM_BUNDLE_SUPPORT', support))
        for program in self.requiredCommands or []:
            if not programs.is_program_installed(program["command"]):
                # Search in locations
                for location in program["locations"]:
                    if os.path.exists(location):
                        variables.append((program["variable"], location))
                        break
        return variables

    # ------------------ Environment variables
    def environmentVariables(self):
        env = {}
        env['TM_BUNDLE_PATH'] = self.currentSourcePath()
        return env

    # --------------- Source Handlers
    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, "%s.tmbundle"), osextra.to_valid_name(self.name))
        
    @classmethod
    def dataFilePath(cls, sourceFilePath):
        return os.path.join(sourceFilePath, cls.FILE)
