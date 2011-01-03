#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Macro's module
        content, name, scope, keyEquivalent, tabTrigger
'''
from pprint import pprint

PMX_MACROS = {}

class PMXMacro(object):
    def __init__(self, hash, name_space = 'default'):
        global PMX_MACROS
        self.name_space = name_space
        for key in [    'name', 'beforeRunningCommand', 'command', 'output', 'input', 'commands', 'tabTrigger',
                        'scope', 'keyEquivalent', 'winCommand', 'fileCaptureRegister', 'scopeType',
                        'lineCaptureRegister', 'capturePattern', 'captureFormatString', 'useGlobalClipboard',
                        'columnCaptureRegister', 'autoScrollOutput', 'fallbackInput']:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Macro '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
            
        PMX_MACROS.setdefault(self.name_space, {})

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXMacro(data)
		
if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/Python.tmbundle/Commands', '*'))
    for f in files:
        command = parse_file(f)