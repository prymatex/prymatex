#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''

from prymatex.bundles.base import PMXBundleItem

class PMXSnippet(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))