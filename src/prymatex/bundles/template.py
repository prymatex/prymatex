#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Template's module
    http://manual.macromates.com/en/templates
'''
from pprint import pprint

PMX_TEMPLATES = {}

class PMXTemplate(object):
    def __init__(self, hash, name_space):
        def __init__(self, hash, name_space = 'default'):
            global PMX_TEMPLATES
            self.name_space = name_space
            for key in [    'name']:
                setattr(self, key, hash.pop(key, None))
            
            if hash:
                print "Macro '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
                
            PMX_TEMPLATES.setdefault(self.name_space, {})

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXTemplate(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/C.tmbundle/Templates', '*'))
    for f in files:
        command = parse_file(f)              