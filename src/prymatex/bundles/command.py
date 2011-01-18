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
    * Meta -> (cinta de 4 esquinas) -> arroba (@)
    * Control es ^
    * Shift es la $
    * Backspace -> ^?
    * supr -> ?M-^\?
    * Alt -> ~
    
'''
import os, stat, tempfile
from subprocess import Popen, PIPE, STDOUT
from prymatex.bundles.base import PMXBundleItem

class PMXCommand(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXCommand, self).__init__(hash, name_space)
        for key in [    'fileCaptureRegister', 'columnCaptureRegister', 'inputFormat', 'disableOutputAutoIndent',
                        'lineCaptureRegister', 'command', 'capturePattern', 'output', 'dontFollowNewOutput',
                        'input', 'beforeRunningCommand', 'autoScrollOutput', 'bundlePath', 'standardInput',
                        'winCommand', 'fallbackInput', 'captureFormatString', 'standardOutput', 'beforeRunningScript' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Command '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
        
    def execute(self, environment):
        texto = "a = {'uno': 1, 'dos': 2}"
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        os.write(descriptor, self.command.encode('utf8'))
        os.chmod(name, stat.S_IEXEC)
        process = Popen([name], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = environment)
        process.stdin.write(texto)
        process.stdin.close();
        print process.stdout.read()
        process.stdout.close()
        #os.unlink(name)
        
def parse_file(filename):
    import plistlib
    data = plistlib.readPlistFromString(filename)
    return PMXCommand(data)

if __name__ == '__main__':
    from glob import glob
    files = glob(os.path.join('../share/Bundles/Python.tmbundle/Commands', '*'))
    environment = { "TM_BUNDLE_SUPPORT": "../share/Bundles/Python.tmbundle/Support",
                    "TM_SUPPORT_PATH": "../share/Support",
                    "TM_CURRENT_WORD": "def",
                    "TM_LINE_NUMBER": "2"}
    environment.update(os.environ)
    for f in files:
        command = parse_file(f)
        print command.name
        command.execute(environment)