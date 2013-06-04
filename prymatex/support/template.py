#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template's module
http://manual.macromates.com/en/templates
"""

import os, shutil, codecs
import functools
from glob import glob

from prymatex.support.bundle import PMXBundleItem, PMXRunningContext
from prymatex.support.utils import prepareShellScript
from prymatex.utils import plist

class PMXTemplateFile(object):
    TYPE = 'templatefile'
    def __init__(self, path, template):
        self.path = path
        self.name = os.path.basename(path)
        self.template = template

    def hasNamespace(self, namespace):
        return self.template.hasNamespace(namespace)
        
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

    def update(self, dataHash):
        for key in list(dataHash.keys()):
            setattr(self, key, dataHash[key])
    
    def relocate(self, path):
        if os.path.exists(self.path):
            shutil.move(self.path, path)
        self.name = os.path.basename(path)
    
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
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXTemplate.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    def populate(self):
        PMXBundleItem.populate(self)
        templateFilePaths = glob(os.path.join(self.currentPath, '*'))
        templateFilePaths.remove(self.dataFilePath(self.currentPath))
        self.files = [ self.manager.addTemplateFile(PMXTemplateFile(tp, self)) for 
            tp in templateFilePaths]

    @property
    def hash(self):
        dataHash = super(PMXTemplate, self).hash
        for key in PMXTemplate.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
    
    def save(self, namespace):
        if not os.path.exists(self.path(namespace)):
            os.makedirs(self.path(namespace))
        file = os.path.join(self.path(namespace), self.FILE)
        plist.writePlist(self.hash, file)
        
        #Hora los archivos del template
        for file in self.files:
            if file.path != self.path(namespace):
                file.save(self.path(namespace))
                
        #TODO: Si puedo garantizar el guardado con el manager puedo controlar los mtime en ese punto
        self.updateMtime(namespace)
        
    def delete(self, namespace):
        for file in self.files:
            os.unlink(file.path)
        os.unlink(os.path.join(self.path(namespace), self.FILE))
        os.rmdir(self.path(namespace))
        folder = os.path.dirname(self.path(namespace))
        try:
            #El ultimo apaga la luz, elimina el directorio base
            os.rmdir(folder)
        except:
            pass

    def buildEnvironment(self, fileName, fileDirectory, localVars = False):
        env = super(PMXTemplate, self).environmentVariables() if not localVars else {}
        nameWithExtension = "{0}{1}{2}".format(fileName, os.path.extsep, self.extension) if self.extension else fileName
        env['TM_NEW_FILE'] = os.path.join(fileDirectory, nameWithExtension)
        env['TM_NEW_FILE_BASENAME'] = fileName
        env['TM_NEW_FILE_DIRECTORY'] = fileDirectory
        return env
    
    def execute(self, environment = {}, callback = lambda x: x):
        with PMXRunningContext(self, self.command, environment) as context:
            context.asynchronous = False
            context.workingDirectory = self.currentPath
            self.manager.runProcess(context, functools.partial(self.afterExecute, callback))
    
    def afterExecute(self, callback, context):
        filePath = context.environment.get('TM_NEW_FILE', None)
        callback(filePath)

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

    @classmethod
    def reloadBundleItem(cls, bundleItem, path, namespace, manager):
        list(map(lambda style: manager.removeTemplateFile(style), bundleItem.files))
        info = os.path.join(path, cls.FILE)
        templateFilePaths = glob(os.path.join(path, '*'))
        templateFilePaths.remove(info)
        data = plist.readPlist(info)
        bundleItem.load(data)
        #Add files
        for templateFilePath in templateFilePaths:
            templateFile = PMXTemplateFile(templateFilePath, bundleItem)
            templateFile = manager.addTemplateFile(templateFile)
            bundleItem.files.append(templateFile)