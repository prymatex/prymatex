#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui

from prymatex.models.tree import TreeNode as TreeNodeBase
from prymatex.models.configure import ConfigureTreeNode

from prymatex import resources
from prymatex.core import exceptions
from prymatex.utils import plist

__all__ = [ FileSystemNode, ProjectNode, PropertyTreeNode ]

#=========================================
# Nodes
#=========================================
class FileSystemNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)
        self.isdir = os.path.isdir(self.path())
        self.isfile = os.path.isfile(self.path())
        self.ishidden = name.startswith('.')
        self.isproject = isinstance(self, ProjectNode)

    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, ProjectNode):
                self._project = self._project.nodeParent()
        return self._project    

    def path(self):
        return os.path.join(self.nodeParent().path(), self.nodeName())
    
    def icon(self):
        return resources.getIcon(self.path())
    
class ProjectNode(FileSystemNode):
    KEYS = [    'name', 'description', 'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 
                'openDocuments', 'showFileHierarchyDrawer', 'windowFrame', 'shellVariables', 'bundleMenu' ]
    FILE = 'info.plist'
    FOLDER = '.pmxproject'
    
    def __init__(self, directory, dataHash):
        self.directory = directory
        self.projectPath = os.path.join(self.path(), self.FOLDER)
        FileSystemNode.__init__(self, dataHash.get("name"))
        self.workingSet = None
        self.manager = None
        self.namespace = None
        self.load(dataHash)
    
    def environment(self):
        env = {
            'TM_PROJECT_DIRECTORY': self.directory,
            'TM_PROJECT_NAME': self.nodeName(),
            'TM_PROJECT_PATH': self.projectPath,
            'TM_PROJECT_NAMESPACE': self.namespace }
        env.update(self.manager.supportProjectEnvironment(self))
        return env

    def load(self, hash):
        for key in ProjectNode.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)

    def dataHash(self):
        dataHash = {}
        for key in ProjectNode.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
        
    def update(self, dataHash):
        for key in dataHash.keys():
            setattr(self, key, dataHash[key])

    def save(self):
        path = self.projectPath
        
        if not os.path.exists(path):
            os.makedirs(path)
        filePath = os.path.join(self.projectPath, self.FILE)
        plist.writePlist(self.dataHash(), filePath)

    def delete(self, removeFiles = False):
        shutil.rmtree(self.projectPath)
        if removeFiles:
            try:
                shutil.rmtree(self.directory)
            except OSError:
                pass
    
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        if isinstance(self.shellVariables, list):
            for var in self.shellVariables:
                if var['enabled']:
                    environment[var['variable']] = var['value']
        environment.update(self.environment())
        return environment

    @classmethod
    def loadProject(cls, path, manager):
        projectPath = os.path.join(path, cls.FOLDER)
        fileInfo = os.path.join(projectPath, cls.FILE)
        if not os.path.isfile(fileInfo):
            raise exceptions.FileNotExistsException(fileInfo)
        try:
            data = plist.readPlist(fileInfo)
            project = cls(path, data)
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
            return resources.getIcon("project-development")

    #==========================================
    # Bundle Menu 
    #==========================================
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundleMenu, list):
            self.bundleMenu = []
        self.bundleMenu.append(bundle.uuidAsUnicode())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsUnicode()
        if uuid in self.bundleMenu:
            self.bundleMenu.remove(uuid)
        if not self.bundleMenu:
            self.bundleMenu = None
            
    def hasBundleMenu(self, bundle):
        if self.bundleMenu is None: return False
        return bundle.uuidAsUnicode() in self.bundleMenu

#=========================================
# Properties Tree Node
#=========================================
class PropertyTreeNode(ConfigureTreeNode):
    def __init__(self, name, parent = None):
        ConfigureTreeNode.__init__(self, name, parent)

    def acceptFileSystemItem(self, fileSystemItem):
        return True
        
    def edit(self, fileSystemItem):
        pass
