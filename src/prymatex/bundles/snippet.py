#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''

PMX_SNIPPETS = {}

class PMXSnippet(object):
    def __init__(self, hash, name_space = 'default'):
        
        self.name_space = name_space
        for key in [    'name', 'content', 'scope', 'tabTrigger', 'keyEquivalent', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Snippet '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
        
        PMX_SNIPPETS.setdefault(self.name_space, {})

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXSnippet(data)
		
if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/Python.tmbundle/Snippets', '*'))
    for f in files:
        snippet = parse_file(f)