#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re
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

__all__ = [ 'FileSystemTreeNode', 'SourceFolderTreeNode', 'ProjectTreeNode', 'ProjectItemTreeNodeBase' ]

class ProjectItemTreeNodeBase(TreeNodeBase):
    def path(self):
        raise NotImplemented

    isDirectory = lambda self: os.path.isdir(self.path())
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

    def icon(self):
        return icons.get_path_icon(self.path())

    def itemType(self):
        return icons.get_type(self.path())
  
    def size(self):
        return os.path.getsize(self.path())

    def mtime(self):
        return os.path.getmtime(self.paht())
        
class FileSystemTreeNode(ProjectItemTreeNodeBase):
    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, ProjectTreeNode):
                self._project = self._project.nodeParent()
        return self._project    

    def path(self):
        return os.path.join(self.nodeParent().path(), self.nodeName())

class SourceFolderTreeNode(ProjectItemTreeNodeBase):
    def __init__(self, path, project):
        super(SourceFolderTreeNode, self).__init__(os.path.basename(path), project)
        self._path = path
    
    def path(self):
        return self._path

    def itemType(self):
        return "Source Folder"
    
class NamespaceFolderTreeNode(ProjectItemTreeNodeBase):
    def __init__(self, namespace, project):
        super(NamespaceFolderTreeNode, self).__init__(namespace.name, project)
        self._namespace = namespace
    
    def namespace(self):
        return self._namespace

    def path(self):
        return self._namespace.path

    def itemType(self):
        return "Namespace Folder"

class ProjectTreeNode(ProjectItemTreeNodeBase):
    KEYS = [    'description', 'licence', 'keywords', 'source_folders', 
                'shell_variables', 'bundles', 'namespace_folders' ]
    
    def __init__(self, name, path):
        super(ProjectTreeNode, self).__init__(name)
        self._project_path = path
        self.manager = None
        self.namespaces = []
        self.namespace_folders = []
        self.bundles = []
        self.source_folders = []

    def path(self):
        return self._project_path
        
    def icon(self):
        return self.manager.resources().get_icon("project")
    
    def itemType(self):
        return "Project"

    # ---------------- Load, update, dump
    def __load_update(self, data_hash, initialize):
        dirname = os.path.dirname(self.path())
        for key in ProjectTreeNode.KEYS:
            if key in data_hash or initialize:
                value = data_hash.get(key, None)
                if value is None and key in ('source_folders', 'bundles', 'namespace_folders'):
                    value = []
                if key in ('source_folders', 'namespace_folders'):
                    value = [
                        os.path.normpath(
                            os.path.join(dirname, os.path.expanduser(v))
                        ) for v in value ]
                setattr(self, key, value)

    def load(self, data_hash):
        self.__load_update(data_hash, True)

    def update(self, data_hash):
        self.__load_update(data_hash, False)

    def dump(self, allKeys=False):
        data_hash = { 'name': self.nodeName() }
        dirname = os.path.dirname(self.path())
        for key in ProjectTreeNode.KEYS:
            value = getattr(self, key, None)
            if allKeys or value:
                if key in ("source_folders", "namespace_folders"):
                    value = [
                        re.sub(
                            "^%s" % config.USER_HOME_PATH, "~", os.path.relpath(v, dirname)
                        ) for v in value ]
                data_hash[key] = value
        return data_hash

    # ---------------- Variables
    @property
    def variables(self):
        if not hasattr(self, '_variables'):
            self._variables = {
            'TM_PROJECT_FOLDERS': " ".join(["'%s'" % folder for folder in self.source_folders ]),
            'TM_PROJECT_NAMESPACES': " ".join(["'%s'" % folder for folder in self.namespace_folders ]),
            'TM_PROJECT_NAME': self.nodeName(),
            'TM_PROJECT_PATH': self.path() }
        return self._variables

    def save(self):
        directory = os.path.dirname(self.path())
        if not os.path.exists(directory):
            os.makedirs(directory)
        json.write_file(self.dump(), self.path())

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

    def reload(self):
        data = json.read_file(self.path())
        self.setNodeName(data["name"])
        self.update(data)

    @classmethod
    def loadProject(cls, project_path, manager):
        if not os.path.isfile(project_path):
            raise exceptions.FileNotExistsException(project_path)
        try:
            data = json.read_file(project_path)
            project = cls(data["name"], project_path)
            project.load(data)
            manager.addProject(project)
            return project
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Error in project %s (%s)" % (project_path, e))
    
    def setManager(self, manager):
        self.manager = manager
    
    # --------------- Source folders
    def addSourceFolder(self, path):
        if path not in self.source_folders:
            self.source_folders.append(path)

    def removeSourceFolder(self, path):
        if path in self.source_folders:
            self.source_folders.remove(path)

    # --------------- namespace folders
    def addNamespace(self, namespace):
        if namespace.path not in self.namespace_folders: 
            self.namespace_folders.append(namespace.path)
        if namespace not in self.namespaces:
            self.namespaces.append(namespace)

    def removeNamespace(self, namespace):
        if path in self.namespace_folders:
            self.namespace_folders.remove(namespace.path)
        if namespace in self.namespaces:
            self.namespaces.remove(namespace)

    # --------------- Bundle Menu
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundles, list):
            self.bundles = []
        self.bundles.append(bundle.uuidAsText())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsText()
        if uuid in self.bundles:
            self.bundles.remove(uuid)
            
    def hasBundleMenu(self, bundle):
        if self.bundles is None: return False
        return bundle.uuidAsText() in self.bundles
