#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Macro's module
"""
from prymatex.support.bundle import PMXBundleItem

class PMXMacro(PMXBundleItem):
    KEYS = ( 'commands', )
    TYPE = 'macro'
    FOLDER = 'Macros'
    EXTENSION = 'tmMacro'
    PATTERNS = ( '*.tmMacro', '*.plist')
    
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
    
    def dump(self):
        dataHash = PMXBundleItem.dump(self)
        for key in PMXMacro.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
            
    def execute(self, processor):
        processor.startMacro(self)
        for command in self.commands:
            name = command['command'][:-1]
            args = [command['argument']] if 'argument' in command else []
            getattr(processor, name, None)(*args)
        processor.endMacro(self)