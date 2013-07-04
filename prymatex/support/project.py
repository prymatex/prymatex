#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, codecs
import functools
from glob import glob

from prymatex.support.bundle import (PMXBundleItem, PMXStaticFile, 
    PMXRunningContext)

from prymatex.utils import plist
   
class PMXProject(PMXBundleItem):
    KEYS = [ 'command' ]
    FILE = 'info.plist'
    TYPE = 'project'
    FOLDER = 'Projects'
    PATTERNS = [ '*' ]
        
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXProject.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    def dump(self):
        dataHash = super(PMXProject, self).dump()
        for key in PMXProject.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash

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
            context.workingDirectory = self.currentPath()
            self.manager.runProcess(context, functools.partial(self.afterExecute, callback))

    def afterExecute(self, callback, context):
        name = context.environment['TM_NEW_PROJECT_NAME']
        location = context.environment['TM_NEW_PROJECT_LOCATION']
        callback(name, location)

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

    def staticPaths(self):
        projectFilePaths = glob(os.path.join(self.currentPath(), '*'))
        projectFilePaths.remove(self.dataFilePath(self.currentPath()))
        return projectFilePaths

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
            projectFile = PMXStaticFile(projectFilePath, bundleItem)
            projectFile = manager.addStaticFile(projectFile)
            project.files.append(projectFile)