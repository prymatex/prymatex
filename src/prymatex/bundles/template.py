#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Template's module
    http://manual.macromates.com/en/templates
    TM_NEW_FILE — the full path, including the name of the file to be generated (i.e. the one the user entered in the GUI).
    TM_NEW_FILE_BASENAME — the base name of the file to be generated. If TM_NEW_FILE is /tmp/foo.txt then this variable would be foo without the folder name and the file extension.
    TM_NEW_FILE_DIRECTORY — the folder name of the file to be generated.
'''

import os, stat, plistlib, tempfile
from subprocess import Popen, PIPE, STDOUT
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.base import PMXBundleItem

class PMXTemplate(PMXBundleItem):
    path_patterns = ['Templates/*']
    bundle_collection = 'templates'
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXTemplate, self).__init__(hash, name_space, path)
        for key in [    'command', 'extension']:
            setattr(self, key, hash.get(key, None))
    
    def setBundle(self, bundle):
        super(PMXTemplate, self).setBundle(bundle)
        bundle.TEMPLATES.append(self)
    
    def resolve(self, environment = {}):
        origWD = os.getcwd() # remember our original working directory
        os.chdir(self.path)
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        file = os.fdopen(descriptor, 'w+')
        file.write(self.command.encode('utf8'))
        file.close()
        os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        process = Popen([name], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = environment, shell=True)
        process.stdin.close()
        print process.stdout.read()
        process.stdout.close()
        os.chdir(origWD) # get back to our original working directory
        
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