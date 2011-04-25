#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Macro's module
        content, name, scope, keyEquivalent, tabTrigger
'''
from pprint import pprint
from prymatex.bundles.base import PMXBundleItem

class PMXMacro(PMXBundleItem):
    path_patterns = ['Macros/*.tmMacro', 'Macros/*.plist']
    bundle_collection = 'macros'
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXMacro, self).__init__(hash, name_space, path)
        for key in [    'commands', ]:
            setattr(self, key, hash.get(key, None))