#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Template's module
    http://manual.macromates.com/en/templates
'''

import os, shutil, plistlib, codecs
from glob import glob
from subprocess import Popen
from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import ensureShellScript, makeExecutableTempFile, ensureEnvironment, deleteFile

class PMXTemplateFile(object):
    TYPE = 'templatefile'
    def __init__(self, name, template):
        self.name = name
        self.template = template
        
    def getFileContent(self):
        file = os.path.join(self.template.path, self.name)
        f = codecs.open(file, 'r', 'utf-8')
        content = f.read()
        f.close()
        return content
    
    def setFileContent(self, content):
        file = os.path.join(self.template.path, self.name)
        if os.path.exists(file):
            f = codecs.open(file, 'w', 'utf-8')
            f.write(content)
            f.close()
    content = property(getFileContent, setFileContent)

class PMXTemplate(PMXBundleItem):
    KEYS = [    'command', 'extension']
    FILE = 'info.plist'
    TYPE = 'template'
    FOLDER = 'Templates'
    PATTERNS = [ '*' ]

    def __init__(self, namespace, hash = None, path = None):
        super(PMXTemplate, self).__init__(namespace, hash, path)
        self.files = []
    
    def load(self, hash):
        super(PMXTemplate, self).load(hash)
        for key in PMXTemplate.KEYS:
            setattr(self, key, hash.get(key, None))
    
    def update(self, hash):
        for key in hash.keys():
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
        #Hora los archivos del template
        files = []
        for file in self.files:
            name = os.path.basename(file)
            dir = os.path.dirname(file)
            if dir != self.path:
                newfile = os.path.join(dir , name)
                shutil.copy(file, newfile)
                files.append(newfile)
            else:
                files.append(file)
        self.files = files

    def addFile(self, file):
        name = os.path.basename(file)
        self.files.append(PMXTemplateFile(name, self))
    
    def getTemplateFiles(self):
        return self.files

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
        info = os.path.join(path, cls.FILE)
        files = glob(os.path.join(path, '*'))
        files.remove(info)
        try:
            data = plistlib.readPlist(info)
            template = cls(namespace, data, path)
            for file in files:
                template.addFile(file)
            return template
        except Exception, e:
            print "Error in bundle %s (%s)" % (info, e)