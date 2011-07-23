#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Macro's module
        content, name, scope, keyEquivalent, tabTrigger
'''
from prymatex.support.bundle import PMXBundleItem

class PMXMacro(PMXBundleItem):
    KEYS = [    'commands' ]
    TYPE = 'macro'
    FOLDER = 'Macros'
    EXTENSION = 'tmMacro'
    PATTERNS = [ '*.tmMacro', '*.plist']
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXMacro, self).__init__(uuid, namespace, hash, path)

    def load(self, hash):
        super(PMXMacro, self).load(hash)
        for key in PMXMacro.KEYS:
            setattr(self, key, hash.get(key, None))
    
    @property
    def hash(self):
        hash = super(PMXMacro, self).hash
        for key in PMXMacro.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash
            
    def execute(self, processor):
        processor.startMacro(self)
        for command in self.commands:
            name = command['command'][:-1]
            args = [command['argument']] if 'argument' in command else []
            getattr(processor, name, None)(*args)
        processor.endMacro(self)