#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import PMXBundleItem

class PMXMacro(PMXBundleItem):
    KEYS = ( 'commands', )
    TYPE = 'macro'
    FOLDER = 'Macros'
    EXTENSION = 'tmMacro'
    PATTERNS = ( '*.tmMacro', '*.plist')
    DEFAULTS = {
        'name': 'untitled',
    }
    def __load_update(self, dataHash, initialize):
        for key in PMXMacro.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))

    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)

    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self, allKeys = False):
        dataHash = PMXBundleItem.dump(self, allKeys)
        for key in PMXMacro.KEYS:
            value = getattr(self, key, None)
            if allKeys or value != None:
                dataHash[key] = value
        return dataHash

    def execute(self, processor):
        processor.beginExecution(self)
        for command in self.commands:
            name = command['command'][:-1]
            args = [command['argument']] if 'argument' in command else []
            getattr(processor, name, None)(*args)
        processor.endExecution(self)
