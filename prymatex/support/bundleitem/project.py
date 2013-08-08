#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import glob
import functools

from prymatex.utils import osextra

from .base import PMXBundleItem
from ..staticfile import PMXStaticFile

class PMXProject(PMXBundleItem):
    KEYS = ( 'command', )
    FILE = 'info.plist'
    TYPE = 'project'
    FOLDER = 'Projects'
    PATTERNS = ( '*', )
    DEFAULTS = {
        'name': 'untitled',
        'command': '''if [[ ! -f "$TM_NEW_PROJECT_LOCATION" ]]; then
    TM_YEAR=`date +%Y` \
    TM_DATE=`date +%Y-%m-%d` \
    perl -pe 's/\$\{([^}]*)\}/$ENV{$1}/g' \
        < template_in.txt > "$TM_NEW_PROJECT_LOCATION"
fi"'''}
        
    def __load_update(self, dataHash, initialize):
        for key in PMXProject.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
    
    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)
        
    def dump(self, allKeys = False):
        dataHash = super(PMXProject, self).dump(allKeys)
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
        self.manager.runSystemCommand(
            bundleItem = self, 
            shellCommand = self.command,
            environment = environment,
            asynchronous = True,
            workingDirectory = self.currentSourcePath(),
            callback = functools.partial(self.afterExecute, callback)
        )
        
    def afterExecute(self, callback, context):
        name = context.environment['TM_NEW_PROJECT_NAME']
        location = context.environment['TM_NEW_PROJECT_LOCATION']
        callback(name, location)

    def dataFilePath(self, basePath, baseName = None):
        directory = osextra.path.ensure_not_exists(os.path.join(basePath, self.FOLDER, "%s"), osextra.to_valid_name(baseName or self.name))
        return os.path.join(directory, self.FILE)

    @classmethod
    def dataFilePath(cls, path):
        return os.path.join(path, cls.FILE)
    
    @classmethod
    def staticFilePaths(cls, sourceFilePath):
        templateFilePaths = glob(os.path.join(sourceFilePath, '*'))
        templateFilePaths.remove(cls.dataFilePath(sourceFilePath))
        return templateFilePaths

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