#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import icons

from prymatex.core import config

from prymatex.models.trees import TreeNodeBase
from prymatex.models.configure import ConfigureTreeNode

from prymatex.core import exceptions
from prymatex.utils import json
import shutil

__all__ = [ 'FileSystemTreeNode', 'ProjectTreeNode' ]

#=========================================
# Nodes
#=========================================
class FileSystemTreeNode(TreeNodeBase):
    FileIconProvider = QtWidgets.QFileIconProvider()
    def __init__(self, name, parent=None):
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
        return icons.get_path_icon(self.path())
    
    # TODO: Cambiar la signatura type
    def type(self):
        if self.isproject:
            return "Project"
        else:
            return icons.get_type(self.path())
  
    def size(self):
        return os.path.getsize(self.path())

    def mtime(self):
        return os.path.getmtime(self.paht())

class SourceFolderTreeNode(FileSystemTreeNode):
    def __init__(self, path, project):
        self._path = path
        super(SourceFolderTreeNode, self).__init__(os.path.basename(path), project)
    
    def path(self):
        return self._path

class ProjectTreeNode(FileSystemTreeNode):
    KEYS = [    'name', 'description', 'licence', 'keywords', 'folders', 
                'currentDocument', 'metaData', 'openDocuments',
                'shellVariables', 'bundleMenu' ]
    
    def __init__(self, path, dataHash):
        self._project_path = path
        super(ProjectTreeNode, self).__init__(dataHash.get("name"))
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
            'TM_PROJECT_FOLDERS': " ".join(["'%s'" % folder for folder in self.folders ]),
            'TM_PROJECT_NAME': self.nodeName(),
            'TM_PROJECT_PATH': self.path(),
            'TM_PROJECT_NAMESPACE': self.namespaceName }
        return self._variables

    def save(self):
        directory = os.path.dirname(self.path())
        if not os.path.exists(directory):
            os.makedirs(directory)
        json.write_file(self.dataHash(), self.path())

    def delete(self, removeFiles=False):
        shutil.rmtree(self.path())
        if removeFiles:
            try:
                for folder in self.folders:
                    shutil.rmtree(folder)
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
    def loadProject(cls, project_path, manager):
        if not os.path.isfile(project_path):
            raise exceptions.FileNotExistsException(project_path)
        try:
            data = json.read_file(project_path)
            project = cls(project_path, data)
            manager.addProject(project)
            return project
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Error in project %s (%s)" % (project_path, e))
    
    def setManager(self, manager):
        self.manager = manager
    
    def path(self):
        return self._project_path
    
    def relpath(self):
        return os.path.basename(self._project_path)
        
    def icon(self):
        if self.manager.isOpen(self):
            return self.manager.resources().get_icon("project")

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
