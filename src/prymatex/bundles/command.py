#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module    
'''
import os, stat, tempfile
from subprocess import Popen, PIPE, STDOUT
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.base import PMXBundleItem

class PMXCommand(PMXBundleItem):
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXCommand, self).__init__(hash, name_space, path)
        for key in [    'fileCaptureRegister', 'columnCaptureRegister', 'inputFormat', 'disableOutputAutoIndent',
                        'lineCaptureRegister', 'command', 'capturePattern', 'output', 'dontFollowNewOutput',
                        'input', 'beforeRunningCommand', 'autoScrollOutput', 'bundlePath', 'standardInput',
                        'winCommand', 'fallbackInput', 'captureFormatString', 'standardOutput', 'beforeRunningScript' ]:
            setattr(self, key, hash.get(key, None))
        self.value = ""
        
    def __str__(self):
        return self.value
    
    def resolve(self, environment = {}):
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        file = os.fdopen(descriptor, 'w+')
        file.write(self.command.encode('utf8'))
        file.close()
        os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        process = Popen([name], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = environment, shell=True)
        process.stdin.close()
        self.value = process.stdout.read()
        process.stdout.close()

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
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
        command.resolve(environment = environment)