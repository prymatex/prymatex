#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template's module
http://manual.macromates.com/en/templates
"""

import os, shutil, codecs
import functools
from glob import glob

from prymatex.support.bundle import (PMXBundleItem, PMXStaticFile, 
    PMXRunningContext)

from prymatex.utils import plist
    
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
    
    def dump(self):
        dataHash = super(PMXTemplate, self).dump()
        for key in PMXTemplate.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash

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
            context.workingDirectory = self.currentPath()
            self.manager.runProcess(context, functools.partial(self.afterExecute, callback))
    
    def afterExecute(self, callback, context):
        filePath = context.environment.get('TM_NEW_FILE', None)
        callback(filePath)

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)

    def staticPaths(self):
        templateFilePaths = glob(os.path.join(self.currentPath(), '*'))
        templateFilePaths.remove(self.dataFilePath(self.currentPath()))
        return templateFilePaths

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
            templateFile = PMXStaticFile(templateFilePath, bundleItem)
            templateFile = manager.addStaticFile(templateFile)
            bundleItem.files.append(templateFile)