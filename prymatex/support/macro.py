#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Macro's module
"""
from prymatex.support.bundle import PMXBundleItem

class PMXMacro(PMXBundleItem):
    KEYS = [ 'commands' ]
    TYPE = 'macro'
    FOLDER = 'Macros'
    EXTENSION = 'tmMacro'
    PATTERNS = [ '*.tmMacro', '*.plist']
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXMacro.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    def dump(self):
        dataHash = super(PMXMacro, self).dump()
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