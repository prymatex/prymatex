#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Preferences's module
    http://manual.macromates.com/en/preferences_items.html
'''

from prymatex.bundles.base import PMXBundleItem

class PMXPreference(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXPreference, self).__init__(hash, name_space)
        for key in [ 'settings' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Preference '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))