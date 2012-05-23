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
        for key in dataHash.keys():
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
    
    def __init__(self, uuid, dataHash):
        PMXBundleItem.__init__(self, uuid, dataHash)
        self.files = []                    #Estos son los template files
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXTemplate.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
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

    def buildEnvironment(self, **kwargs):
        env = super(PMXTemplate, self).buildEnvironment()
        fileName = kwargs.get('fileName', '')
        fileDirectory = kwargs.get('fileDirectory', '')
        if fileName and fileDirectory:
            nameWithExtension = "{0}{1}{2}".format(fileName, os.path.extsep, self.extension) if self.extension else fileName
            env['TM_NEW_FILE'] = os.path.join(fileDirectory, nameWithExtension)
            env['TM_NEW_FILE_BASENAME'] = fileName
            env['TM_NEW_FILE_DIRECTORY'] = fileDirectory
        projectName = kwargs.get('projectName', '')
        projectLocation = kwargs.get('projectLocation', '')
        if projectName and projectLocation:
            env['TM_NEW_PROJECT_NAME'] = projectName
            env['TM_NEW_PROJECT_LOCATION'] = projectLocation
            env['TM_NEW_PROJECT_BASENAME'] = os.path.basename(projectLocation)
            env['TM_NEW_PROJECT_DIRECTORY'] = os.path.dirname(projectLocation)
        return env
    
    def execute(self, environment = {}, callback = lambda x: x):
        context = PMXRunningContext(self)
        
        context.asynchronous = False
        context.workingDirectory = self.currentPath
        context.shellCommand, context.environment = prepareShellScript(self.command, environment)

        self.manager.runProcess(context, functools.partial(self.afterExecute, callback))
    
    def afterExecute(self, callback, context):
        #TODO: Ver los errores
        newFileOrPath = context.environment.get('TM_NEW_FILE', context.environment.get('TM_NEW_PROJECT_LOCATION', None))
        callback(newFileOrPath)

    @classmethod
    def loadBundleItem(cls, path, namespace, bundle, manager):
        info = os.path.join(path, cls.FILE)
        templateFilePaths = glob(os.path.join(path, '*'))
        templateFilePaths.remove(info)
        try:
            data = plist.readPlist(info)
            uuid = manager.uuidgen(data.pop('uuid', None))
            template = manager.getManagedObject(uuid)
            if template is None and not manager.isDeleted(uuid):
                template = cls(uuid, data)
                template.setBundle(bundle)
                template.setManager(manager)
                template.addSource(namespace, path)
                template = manager.addBundleItem(template)
                manager.addManagedObject(template)
                #Add files
                for templateFilePath in templateFilePaths:
                    templateFile = PMXTemplateFile(templateFilePath, template)
                    templateFile = manager.addTemplateFile(templateFile)
                    template.files.append(templateFile)
            elif template is not None:
                template.addSource(namespace, path)
            return template
        except Exception, e:
            print "Error in template %s (%s)" % (info, e)

    @classmethod
    def reloadBundleItem(cls, bundleItem, path, namespace, manager):
        map(lambda style: manager.removeTemplateFile(style), bundleItem.files)
        info = os.path.join(path, cls.FILE)
        templateFilePaths = glob(os.path.join(path, '*'))
        templateFilePaths.remove(info)
        data = plist.readPlist(info)
        bundleItem.load(data)
        #Add files
        for templateFilePath in templateFilePaths:
            templateFile = PMXTemplateFile(templateFilePath, bundleItem)
            templateFile = manager.addTemplateFile(templateFile)
            template.files.append(templateFile)