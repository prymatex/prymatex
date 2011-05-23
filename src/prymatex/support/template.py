#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Template's module
    http://manual.macromates.com/en/templates
'''

import os, shutil, plistlib
from subprocess import Popen
from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import ensureShellScript, makeExecutableTempFile, ensureEnvironment, deleteFile

class PMXTemplate(PMXBundleItem):
    KEYS = [    'command', 'extension']
    FILE = 'info.plist'
    TYPE = 'template'
    FOLDER = 'Templates'
    PATTERNS = [ '*' ]

    def __init__(self, namespace, hash = None, path = None):
        super(PMXTemplate, self).__init__(namespace, hash, path)
    
    def load(self, hash):
        super(PMXTemplate, self).load(hash)
        for key in PMXTemplate.KEYS:
            setattr(self, key, hash.get(key, None))
    
    def update(self, hash):
        for key in hash.keys():
            if key == "path":
                #Si quieren cambiar el path muevo mis archivos dependientes
                shutil.copytree(self.path, hash[key])
            setattr(self, key, hash[key])
    
    @property
    def hash(self):
        hash = super(PMXTemplate, self).hash
        for key in PMXTemplate.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash
    
    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file = os.path.join(self.path , self.FILE)
        plistlib.writePlist(self.hash, file)
        
    def buildEnvironment(self, directory = "", name = ""):
        env = super(PMXTemplate, self).buildEnvironment()
        env['TM_NEW_FILE'] = os.path.join(directory, name + '.' + self.extension)
        env['TM_NEW_FILE_BASENAME'] = name
        env['TM_NEW_FILE_DIRECTORY'] = directory
        return env
    
    def resolve(self, environment = {}):
        origWD = os.getcwd() # remember our original working directory
        os.chdir(self.path)
        
        command = ensureShellScript(self.command)
        temp_file = makeExecutableTempFile(command)  
        process = Popen([ temp_file ], env = ensureEnvironment(environment))
        process.wait()
        
        deleteFile(temp_file)
        os.chdir(origWD) # get back to our original working directory
        
    @classmethod
    def loadBundleItem(cls, path, namespace):
        info_file = os.path.join(path, cls.FILE)
        try:
            data = plistlib.readPlist(info_file)
            template = cls(namespace, data, path)
            return template
        except Exception, e:
            print "Error in bundle %s (%s)" % (info_file, e)