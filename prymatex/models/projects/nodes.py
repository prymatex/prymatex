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

__all__ = [ 'FileSystemTreeNode', 'SourceFolderTreeNode', 'ProjectTreeNode' ]

class ProjectItemTreeNodeBase(TreeNodeBase):
    def path(self):
        raise NotImplemented

    isDirectory = lambda self: isinstance(self, FileSystemTreeNode) and os.path.isdir(self.path())
    isFile = lambda self: isinstance(self, FileSystemTreeNode) and os.path.isfile(self.path())
    isHidden = lambda self: isinstance(self, FileSystemTreeNode) and self.nodeName().startswith('.')
    isProject = lambda self: isinstance(self, ProjectTreeNode)
    isSourceFolder = lambda self: isinstance(self, SourceFolderTreeNode)
    
    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, ProjectTreeNode):
                self._project = self._project.nodeParent()
        return self._project

    def itemType(self):
        return ""
        
class FileSystemTreeNode(ProjectItemTreeNodeBase):
    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, ProjectTreeNode):
                self._project = self._project.nodeParent()
        return self._project    

    def path(self):
        return os.path.join(self.nodeParent().path(), self.nodeName())
    
    def icon(self):
        return icons.get_path_icon(self.path())
    
    def itemType(self):
        return icons.get_type(self.path())
  
    def size(self):
        return os.path.getsize(self.path())

    def mtime(self):
        return os.path.getmtime(self.paht())

class SourceFolderTreeNode(ProjectItemTreeNodeBase):
    def __init__(self, path, project):
        super(SourceFolderTreeNode, self).__init__(os.path.basename(path), project)
        self._path = path
    
    def path(self):
        return self._path
        
    def icon(self):
        return icons.get_path_icon(self.path())

    def itemType(self):
        return "Source Folder"
    
    def size(self):
        return os.path.getsize(self.path())

    def mtime(self):
        return os.path.getmtime(self.paht())

class ProjectTreeNode(ProjectItemTreeNodeBase):
    KEYS = [    'name', 'description', 'licence', 'keywords', 'source_folders', 
                'shell_variables', 'bundles' ]
    
    def __init__(self, path, dataHash):
        super(ProjectTreeNode, self).__init__(dataHash.get("name"))
        self._project_path = path
        self.manager = None
        self.namespaceName = ""
        self.load(dataHash)
    
    def nodeType(self):
        return "Project"
            
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
            'TM_PROJECT_FOLDERS': " ".join(["'%s'" % folder for folder in self.source_folders ]),
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
                for folder in self.source_folders:
                    shutil.rmtree(folder)
            except OSError:
                pass
    
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        if isinstance(self.shell_variables, list):
            for var in self.shell_variables:
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
        
    def icon(self):
        return self.manager.resources().get_icon("project")

    # --------------- Bundle Menu
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundles, list):
            self.bundles = []
        self.bundles.append(bundle.uuidAsText())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsText()
        if uuid in self.bundles:
            self.bundles.remove(uuid)
        if not self.bundles:
            self.bundles = None
            
    def hasBundleMenu(self, bundle):
        if self.bundles is None: return False
        return bundle.uuidAsText() in self.bundles
