#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Macro's module
        content, name, scope, keyEquivalent, tabTrigger
'''
from pprint import pprint
from prymatex.bundles.base import PMXBundleItem

class PMXMacro(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXMacro, self).__init__(hash, name_space)
        for key in [    'beforeRunningCommand', 'command', 'output', 'input', 'commands', 
                        'winCommand', 'fileCaptureRegister', 'scopeType', 'useGlobalClipboard',
                        'lineCaptureRegister', 'capturePattern', 'captureFormatString', 
                        'columnCaptureRegister', 'autoScrollOutput', 'fallbackInput', 'e_commands']:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Macro '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))unningCommand', 'command', 'output', 'input', 'commands', 
                        'winCommand', 'fileCaptureRegister', 'scopeType', 