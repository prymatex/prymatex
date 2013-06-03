#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, codecs
import functools
from glob import glob

from prymatex.support.bundle import PMXBundleItem, PMXRunningContext
from prymatex.support.utils import prepareShellScript
from prymatex.support.template import PMXTemplateFile
from prymatex.utils import plist
   
class PMXProject(PMXBundleItem):
    KEYS = [ 'command' ]
    FILE = 'info.plist'
    TYPE = 'project'
    FOLDER = 'Projects'
    PATTERNS = [ '*' ]
    
    def __init__(self, uuid):
        PMXBundleItem.__init__(self, uuid)
        self.files = []                    #Estos son los project files
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXProject.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    @property
    def hash(self):
        dataHash = super(PMXProject, self).hash
        for key in PMXProject.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
    
    def save(self, namespace):
        if not os.path.exists(self.path(namespace)):
            os.makedirs(self.path(namespace))
        projectFile = os.path.join(self.path(namespace), self.FILE)
        plist.writePlist(self.hash, projectFile)
        
        #Hora los archivos del project
        for projectFile in self.files:
            if projectFile.path != self.path(namespace):
                projectFile.save(self.path(namespace))
                
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

    def buildEnvironment(self, projectName, projectLocation, localVars = False):
        env = super(PMXProject, self).environmentVariables() if not localVars else {}
        env['TM_NEW_PROJECT_NAME'] = projectName
        env['TM_NEW_PROJECT_LOCATION'] = projectLocation
        env['TM_NEW_PROJECT_BASENAME'] = os.path.basename(projectLocation)
        env['TM_NEW_PROJECT_DIRECTORY'] = os.path.dirname(projectLocation)
        return env
    
    def execute(self, environment = {}, callback = lambda x: x):
        with PMXRunningContext(self, self.command, environment) as context:
            context.asynchronous = True
            context.workingDirectory = self.currentPath
            self.manager.runProcess(context, functools.partial(self.afterExecute, callback))
            
    def afterExecute(self, callback, context):
        name = context.environment['TM_NEW_PROJECT_NAME']
        location = context.environment['TM_NEW_PROJECT_LOCATION']
        callback(name, location)

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

    @classmethod
    def loadBundleItem(cls, path, namespace, bundle, manager):
        info = os.path.join(path, cls.FILE)
        projectFilePaths = glob(os.path.join(path, '*'))
        projectFilePaths.remove(info)
        try:
            data = plist.readPlist(info)
            uuid = manager.uuidgen(data.pop('uuid', None))
            project = manager.getManagedObject(uuid)
            if project is None and not manager.isDeleted(uuid):
                project = cls(uuid, data)
                project.setBundle(bundle)
                project.setManager(manager)
                project.addSource(namespace, path)
                project = manager.addBundleItem(project)
                manager.addManagedObject(project)
                #Add files
                for projectFilePath in projectFilePaths:
                    projectFile = PMXTemplateFile(projectFilePath, project)
                    projectFile = manager.addTemplateFile(projectFile)
                    project.files.append(projectFile)
            elif project is not None:
                project.addSource(namespace, path)
            return project
        except Exception as e:
            print("Error in project %s (%s)" % (info, e))

    @classmethod
    def reloadBundleItem(cls, bundleItem, path, namespace, manager):
        list(map(lambda style: manager.removeTemplateFile(style), bundleItem.files))
        info = os.path.join(path, cls.FILE)
        projectFilePaths = glob(os.path.join(path, '*'))
        projectFilePaths.remove(info)
        data = plist.readPlist(info)
        bundleItem.load(data)
        #Add files
        for projectFilePath in projectFilePaths:
            projectFile = PMXTemplateFile(projectFilePath, bundleItem)
            projectFile = manager.addTemplateFile(projectFile)
            project.files.append(projectFile)