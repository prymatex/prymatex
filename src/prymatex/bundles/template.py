#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Template's module
    http://manual.macromates.com/en/templates
'''
import os, stat, plistlib, tempfile
from subprocess import Popen, PIPE, STDOUT
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.base import PMXBundleItem

class PMXTemplate(PMXBundleItem):
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXTemplate, self).__init__(hash, name_space, path)
        for key in [    'command', 'extension']:
            setattr(self, key, hash.get(key, None))
            
    def resolve(self, environment = {}):
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        file = os.fdopen(descriptor, 'w+')
        file.write(self.command.encode('utf8'))
        file.close()
        os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        process = Popen([name], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = environment, shell=True)
        process.stdin.close()
        print process.stdout.read()
        process.stdout.close()
        
    @classmethod
    def loadBundleItem(cls, path, name_space = 'prymatex'):
        info_file = os.path.join(path, 'info.plist')
        try:
            data = plistlib.readPlist(info_file)
            template = cls(data, name_space, path)
        except Exception, e:
            print "Error in bundle %s (%s)" % (info_file, e)
            return None
        return template