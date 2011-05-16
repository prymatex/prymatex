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
    def __init__(self, namespace, hash = None, path = None):
        super(PMXMacro, self).__init__(namespace, hash, path)

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
        for command in self.commands:
            print command
            name = command['command'][:-1]
            method = getattr(processor, name, None)
            if callable(method):
                method()
