#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template's module
http://manual.macromates.com/en/templates
"""

import os
from glob import glob
import functools

from prymatex.utils import osextra

from .base import PMXBundleItem
from ..staticfile import PMXStaticFile

class PMXTemplate(PMXBundleItem):
    KEYS = ( 'command', 'extension')
    FILE = 'info.plist'
    TYPE = 'template'
    FOLDER = 'Templates'
    PATTERNS = ( '*', )
    DEFAULTS = {
        'name': 'untitled',
        'extension': 'txt',
        'command': '''if [[ ! -f "$TM_NEW_FILE" ]]; then
    TM_YEAR=`date +%Y` \
    TM_DATE=`date +%Y-%m-%d` \
    perl -pe 's/\$\{([^}]*)\}/$ENV{$1}/g' \
        < template_in.txt > "$TM_NEW_FILE"
fi"'''
}
    
    def __load_update(self, dataHash, initialize):
        for key in PMXTemplate.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
    
    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)
    
    def dump(self, includeNone = False):
        dataHash = super(PMXTemplate, self).dump(includeNone)
        for key in PMXTemplate.KEYS:
            value = getattr(self, key, None)
            if includeNone or value != None:
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
        self.manager.runSystemCommand(
            bundleItem = self,
            shellCommand = self.command,
            environment = environment,
            workingDirectory = self.sourcePath(),
            asynchronous = True,
            callback = functools.partial(self.afterExecute, callback)
        )
    
    def afterExecute(self, callback, context):
        filePath = context.environment.get('TM_NEW_FILE', None)
        callback(filePath)

    def createDataFilePath(self, basePath, baseName = None):
        directory = osextra.path.ensure_not_exists(os.path.join(basePath, self.FOLDER, "%s"), osextra.to_valid_name(baseName or self.name))
        return os.path.join(directory, self.FILE)

    @classmethod
    def dataFilePath(cls, sourcePath):
        return os.path.join(sourcePath, cls.FILE)
    
    @classmethod
    def staticFilePaths(cls, sourceFilePath):
        templateFilePaths = glob(os.path.join(sourceFilePath, '*'))
        templateFilePaths.remove(cls.dataFilePath(sourceFilePath))
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