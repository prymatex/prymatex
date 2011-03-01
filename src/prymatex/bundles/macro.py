#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Macro's module
        content, name, scope, keyEquivalent, tabTrigger
'''
from pprint import pprint
from prymatex.bundles.base import PMXBundleItem

class PMXMacro(PMXBundleItem):
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXMacro, self).__init__(hash, name_space, path)
        for key in [    'beforeRunningCommand', 'command', 'output', 'input', 'commands', 
                        'winCommand', 'fileCaptureRegister', 'scopeType', 'useGlobalClipboard',
                        'lineCaptureRegister', 'capturePattern', 'captureFormatString', 
                        'columnCaptureRegister', 'autoScrollOutput', 'fallbackInput', 'e_commands']:
            setattr(self, key, hash.get(key, None))