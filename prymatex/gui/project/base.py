#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, shutil

from prymatex import resources
from prymatex.core import exceptions
from prymatex.models.tree import TreeNode
from prymatex.utils import plist

"""
currentDocument: Documento actual en el editor
documents: lista de documentos o carpetas, no se muy bien, creo que son los grupos de tm
    {'expanded': True,
     'name': 'source',
     'regexFolderFilter': '!.*/(\\.[^/]*|CVS|_darcs|_MTN|\\{arch\\}|blib|.*~\\.nib|.*\\.(framework|app|pbproj|pbxproj|xcode(proj)?|bundle))$',
     'selected': True,
     'sourceDirectory': ''}
fileHierarchyDrawerWidth: en ancho de la docker de proyectos
metaData: Datos de los editores por cada documento abierto, es un diccionario indexado por la ruta del documento
    {'Classes/MDSettings.h': {'caret': {'column': 20, 'line': 52},
                                       'columnSelection': False,
                                       'firstVisibleColumn': 0,
                                       'firstVisibleLine': 4,
                                       'selectFrom': {'column': 15,
                                                      'line': 52},
                                       'selectTo': {'column': 33,
                                                    'line': 52}},
openDocuments: Documentos abiertos en el editor es una lista, cada entrada de aca tiene una en metaData
showFileHierarchyDrawer: Mostrar la docker
windowFrame: El Tampaño del a ventana de projecto en tm
"""

class FileSystemTreeNode(TreeNode):
    def __init__(self, name, parent = None):
        TreeNode.__init__(self, name, parent)
        self.isdir = os.path.isdir(self.path)
        self.isfile = os.path.isfile(self.path)
        self.ishidden = name.startswith('.')
        self.isproject = isinstance(self, PMXProject)

    @property
    def path(self):
        return os.path.join(self.parentNode.path, self.name)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class PMXProject(FileSystemTreeNode):
    KEYS = [    'name', 'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 'openDocuments', 'showFileHierarchyDrawer', 'windowFrame', 'shellVariables' ]
    FILE = 'info.plist'
    FOLDER = '.pmxproject'
    def __init__(self, directory, hash):
        self.directory = directory
        FileSystemTreeNode.__init__(self, "Project Name")
        self.workingSet = None
        self.manager = None
        self.support = None
        self.load(hash)
    
    def setSupport(self, support):
        self.support = support
        
    @property
    def environment(self):
        env = {
            'TM_PROJECT_DIRECTORY': self.directory,
            'TM_PROJECT_NAME': self.name,
            'TM_PROJECT_PATH': os.path.join(self.path, self.FOLDER) }
        if self.support != None:
            env['TM_PROJECT_SUPPORT'] = self.support
        return env
        
    def load(self, hash):
        for key in PMXProject.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = {}
        for key in PMXProject.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash
        
    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])

    def save(self):
        projectPath = os.path.join(self.directory, self.FOLDER)
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
        filePath = os.path.join(projectPath, self.FILE)
        plist.writePlist(self.hash, filePath)

    def delete(self, removeFiles = False):
        projectPath = os.path.join(self.directory, self.FOLDER)
        shutil.rmtree(projectPath)
        if removeFiles:
            try:
                shutil.rmtree(self.directory)
            except os.OSError:
                pass

    def buildEnvironment(self):
        env = {}
        if isinstance(self.shellVariables, list):
            for var in self.shellVariables:
                if var['enabled']:
                    env[var['variable']] = var['value']
        env.update(self.environment)
        env['TM_SELECTED_FILES'] = ""
        env['TM_SELECTED_FILE'] = ""
        return env

    @classmethod
    def loadProject(cls, path, manager):
        projectPath = os.path.join(path, cls.FOLDER)
        fileInfo = os.path.join(projectPath, cls.FILE)
        if not os.path.isfile(fileInfo):
            raise exceptions.PrymatexFileNotExistsException(fileInfo)
        try:
            data = plist.readPlist(fileInfo)
            project = cls(path, data)
            if os.path.exists(os.path.join(projectPath, 'Support')):
                project.setSupport(os.path.join(projectPath, 'Support'))
            manager.addProject(project)
            return project
        except Exception, e:
            print "Error in project %s (%s)" % (filePath, e)
    
    def setManager(self, manager):
        self.manager = manager
    
    def setWorkingSet(self, workingSet):
        self.workingSet = set

    @property
    def path(self):
        return self.directory
    
    @property
    def icon(self):
        if self.manager.isOpen(self):
            return resources.getIcon("projectopen")
        else:
            return resources.getIcon("projectclose")
    