#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.models.tree import NamespaceTreeModel, TreeNode

class GroupTreeNode(TreeNode):
    def __init__(self, name, directory, parent = None):
        self.title = name
        self.directory = directory
        self.identifier = unicode(hash(self.title))
        TreeNode.__init__(self, self.identifier, parent)

    def acceptPath(self, path):
        return os.path.commonprefix([self.directory, path]) == self.directory

    def splitToNamespace(self, path):
        dirName, fileName = os.path.dirname(path), os.path.basename(path)
        return self.identifier + dirName[len(self.directory):], fileName

    @property
    def path(self):
        return os.path.join(self.directory)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class FileFoundTreeNode(TreeNode):
    def __init__(self, name, path, parent = None):
        self.title = name
        self.__path = path
        TreeNode.__init__(self, name, parent)
        
    @property
    def path(self):
        return os.path.join(self.__path)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class DirectoryTreeNode(TreeNode):
    def __init__(self, name, parent = None):
        self.title = name
        TreeNode.__init__(self, name, parent)
        
    @property
    def path(self):
        return os.path.join(self.parentNode.path, self.name)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class LineTreeNode(TreeNode):
    def __init__(self, lineNumber, lineContent, parent = None):
        self.title = "%s - %s" % (lineNumber, lineContent.strip())
        self.lineNumber = lineNumber
        self.identifier = unicode(hash(self.title))
        TreeNode.__init__(self, self.identifier, parent)
        
    @property
    def path(self):
        return self.parentNode.path
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class PMXSearchTreeModel(NamespaceTreeModel):
    def __init__(self, parent = None):
        NamespaceTreeModel.__init__(self, separator = os.sep, parent = parent)
        self.proxyNodeFactory = self.createProxyFileFoundNode

    def createProxyFileFoundNode(self, name, parent):
        return DirectoryTreeNode(name, parent)
        
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def addGroup(self, name, directory):
        #Estos son los roots, agregar un default group para cuando se busque en otros lugares o el por defecto
        groupNode = GroupTreeNode(name, directory)
        self.addNode(groupNode)
        
    def addFileFound(self, filePath, lines):
        #Buscar coincidencia con grupo para manejar el nombre
        for group in self.rootNode.childrenNodes:
            if group.acceptPath(filePath):
                namespace, fileName = group.splitToNamespace(filePath)
                foundNode = FileFoundTreeNode(fileName, filePath)
                for line in lines:
                    lineNode = LineTreeNode(*line)
                    foundNode.appendChild(lineNode)
                self.addNamespaceNode(namespace, foundNode)
