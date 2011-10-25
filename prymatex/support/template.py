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
from prymatex.support.utils import prepareShellScript

class PMXTemplateFile(object):
    TYPE = 'templatefile'
    def __init__(self, path, template):
        self.path = path
        self.name = os.path.basename(path)
        self.template = template

    @property
    def enabled(self):
        return self.template.enabled
        
    def getFileContent(self):
        if os.path.exists(self.path):
            f = codecs.open(self.path, 'r', 'utf-8')
            content = f.read()
            f.close()
            return content
    
    def setFileContent(self, content):
        if os.path.exists(self.path):
            f = codecs.open(self.path, 'w', 'utf-8')
            f.write(content)
            f.close()
    content = property(getFileContent, setFileContent)

    def save(self, basePath = None):
        path = os.path.join(basePath, self.name) if basePath is not None else self.path
        f = codecs.open(path, 'w', 'utf-8')
        f.write(self.content)
        f.close()
        self.path = path
    
class PMXTemplate(PMXBundleItem):
    KEYS = [    'command', 'extension']
    FILE = 'info.plist'
    TYPE = 'template'
    FOLDER = 'Templates'
    PATTERNS = [ '*' ]

    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXTemplate, self).__init__(uuid, namespace, hash, path)
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
        for file in self.files:
            if file.path != self.path:
                file.save(self.path)

    def buildEnvironment(self, directory = "", name = ""):
        env = super(PMXTemplate, self).buildEnvironment()
        env['TM_NEW_FILE'] = os.path.join(directory, name + '.' + self.extension)
        env['TM_NEW_FILE_BASENAME'] = name
        env['TM_NEW_FILE_DIRECTORY'] = directory
        return env
    
    def resolve(self, environment = {}):
        origWD = os.getcwd() # remember our original working directory
        os.chdir(self.path)
        
        command, env = prepareShellScript(self.command, environment)
          
        process = Popen(command, env = env)
        process.wait()
        
        os.chdir(origWD) # get back to our original working directory
        
    @classmethod
    def loadBundleItem(cls, path, namespace, bundle, manager):
        info = os.path.join(path, cls.FILE)
        paths = glob(os.path.join(path, '*'))
        paths.remove(info)
        try:
            data = plistlib.readPlist(info)
            uuid = manager.uuidgen(data.pop('uuid', None))
            template = manager.getManagedObject(uuid)
            if template is None and not manager.isDeleted(uuid):
                template = cls(uuid, namespace, data, path)
                template.setBundle(bundle)
                template = manager.addBundleItem(template)
                for path in paths:
                    file = PMXTemplateFile(path, template)
                    file = manager.addTemplateFile(file)
                    template.files.append(file)
                manager.addManagedObject(template)
            elif template is not None:
                template.addNamespace(namespace)
            return template
        except Exception, e:
            print "Error in bundle %s (%s)" % (info, e)