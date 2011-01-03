#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module
    Env:    TM_CURRENT_LINE,
            TM_SUPPORT_PATH: Support dentro de textmate
            TM_INPUT_START_LINE_INDEX,
            TM_LINE_INDEX: 
            TM_LINE_NUMBER: Numero de linea
            TM_SELECTED_SCOPE:
            TM_CURRENT_WORD:
            TM_FILEPATH,
            TM_DIRECTORY,
            TM_BUNDLE_SUPPORT: Support dentro del bundle
            TM_SELECTED_TEXT
'''
import os, stat, tempfile
from subprocess import Popen, PIPE

PMX_COMMANDS = {}

class PMXCommand(object):
    def __init__(self, hash, name_space = 'default'):
        global PMX_COMMANDS
        self.name_space = name_space
        for key in [    'name', 'fileCaptureRegister', 'columnCaptureRegister',
                        'lineCaptureRegister', 'scope', 'command', 'capturePattern', 'output',
                        'keyEquivalent', 'input', 'beforeRunningCommand', 'autoScrollOutput',
                        'winCommand', 'fallbackInput', 'captureFormatString' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Command '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
        
        PMX_COMMANDS.setdefault(self.name_space, {})
        
    def execute(self):
        descriptor, name = tempfile.mkstemp()
        os.write(descriptor, self.command.encode('utf8'))
        os.chmod(name, stat.S_IEXEC)
        Popen([name], env = {"TM_LINE_NUMBER": "1"})
        
def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXCommand(data)
		
if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/Python.tmbundle/Commands', '*'))
    for f in files:
        command = parse_file(f)
        print command.name
        command.execute()