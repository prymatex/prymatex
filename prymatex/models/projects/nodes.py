#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui

from prymatex.core import config

from prymatex.models.trees import TreeNodeBase
from prymatex.models.configure import ConfigureTreeNode

from prymatex.core import exceptions
from prymatex.utils import plist
import shutil

__all__ = [ 'FileSystemTreeNode', 'ProjectTreeNode' ]

#=========================================
# Nodes
#=========================================
class FileSystemTreeNode(TreeNodeBase):
    FileIconProvider = QtGui.QFileIconProvider()
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)
        self.isdir = os.path.isdir(self.path())
        self.isfile = os.path.isfile(self.path())
        self.ishidden = name.startswith('.')
        self.isproject = isinstance(self, ProjectTreeNode)

    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, ProjectTreeNode):
                self._project = self._project.nodeParent()
        return self._project    

    def path(self):
        return os.path.join(self.nodeParent().path(), self.nodeName())
    
    def relpath(self):
        return os.path.join(self.nodeParent().relpath(), self.nodeName())
    
    def icon(self):
        # TODO:
	#QFileIconProvider::Computer	0
	#QFileIconProvider::Desktop	1
	#QFileIconProvider::Trashcan	2
	#QFileIconProvider::Network	3
	#QFileIconProvider::Drive	4
	#QFileIconProvider::Folder	5
	#QFileIconProvider::File	6
        return self.FileIconProvider.icon(QtCore.QFileInfo(self.path()))
    
    # TODO: Cambiar la signatura type
    def type(self):
        if self.isproject:
            return "Project"
        else:
            return self.FileIconProvider.type(QtCore.QFileInfo(self.path()))
  
    def size(self):
        return os.path.getsize(self.path())

    def mtime(self):
        return os.path.getmtime(self.paht())

class ProjectTreeNode(FileSystemTreeNode):
    KEYS = [    'name', 'description', 'licence', 'keywords', 
                'currentDocument', 'metaData', 'openDocuments',
                'shellVariables', 'bundleMenu' ]
    
    def __init__(self, directory, dataHash):
        self.directory = directory
        self.projectPath = os.path.join(self.path(), config.PMX_HOME_NAME)
        FileSystemTreeNode.__init__(self, dataHash.get("name"))
        self.workingSet = None
        self.manager = None
        self.namespaceName = ""
        self.load(dataHash)
    
    # ----------- Load, update and dump
    def load(self, hash):
        for key in ProjectTreeNode.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)

    def update(self, dataHash):
        for key in list(dataHash.keys()):
            setattr(self, key, dataHash[key])

    def dataHash(self):
        dataHash = {}
        for key in ProjectTreeNode.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
    
    # ---------------- Variables
    @property
    def variables(self):
        if not hasattr(self, '_variables'):
            self._variables = {
            'TM_PROJECT_DIRECTORY': self.directory,
            'TM_PROJECT_NAME': self.nodeName(),
            'TM_PROJECT_PATH': self.projectPath,
            'TM_PROJECT_NAMESPACE': self.namespaceName }
        return self._variables
    
    def save(self):
        path = self.projectPath
        
        if not os.path.exists(path):
            os.makedirs(path)
        filePath = os.path.join(self.projectPath, config.PMX_DESCRIPTOR_NAME)
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
        environment.update(self.variables)
        return environment

    @classmethod
    def loadProject(cls, path, manager):
        projectPath = os.path.join(path, config.PMX_HOME_NAME)
        fileInfo = os.path.join(projectPath, config.PMX_DESCRIPTOR_NAME)
        if not os.path.isfile(fileInfo):
            raise exceptions.FileNotExistsException(fileInfo)
        try:
            data = plist.readPlist(fileInfo)
            project = cls(path, data)
            manager.addProject(project)
            return project
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Error in project %s (%s)" % (path, e))
    
    def setManager(self, manager):
        self.manager = manager
    
    def setWorkingSet(self, workingSet):
        self.workingSet = set

    def path(self):
        return self.directory
    
    def relpath(self):
        return os.path.basename(self.directory)
        
    def icon(self):
        if self.manager.isOpen(self):
            return self.manager.resources().get_icon("project-development")

    # --------------- Bundle Menu
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundleMenu, list):
            self.bundleMenu = []
        self.bundleMenu.append(bundle.uuidAsText())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsText()
        if uuid in self.bundleMenu:
            self.bundleMenu.remove(uuid)
        if not self.bundleMenu:
            self.bundleMenu = None
            
    def hasBundleMenu(self, bundle):
        if self.bundleMenu is None: return False
        return bundle.uuidAsText() in self.bundleMenu
