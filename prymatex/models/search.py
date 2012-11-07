#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.models.trees import AbstractNamespaceTreeModel, TreeNodeBase

class GroupTreeNode(TreeNodeBase):
    def __init__(self, name, directory, parent = None):
        self.title = name
        self.directory = directory
        self.identifier = unicode(hash(self.title))
        TreeNodeBase.__init__(self, self.identifier, parent)

    def acceptPath(self, path):
        return os.path.commonprefix([self.directory, path]) == self.directory

    def splitToNamespace(self, path):
        dirName, fileName = os.path.dirname(path), os.path.basename(path)
        return self.identifier + dirName[len(self.directory):], fileName

    def path(self):
        return os.path.join(self.directory)
    
    def icon(self):
        return resources.getIcon(self.path())

class FileFoundTreeNode(TreeNodeBase):
    def __init__(self, name, path, parent = None):
        self.title = name
        self.__path = path
        TreeNodeBase.__init__(self, name, parent)
        
    def path(self):
        return os.path.join(self.__path)
    
    def icon(self):
        return resources.getIcon(self.path())

class DirectoryTreeNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        self.title = name
        TreeNodeBase.__init__(self, name, parent)
        
    def path(self):
        return os.path.join(self.nodeParent().path(), self.nodeName())
    
    def icon(self):
        return resources.getIcon(self.path())

class LineTreeNode(TreeNodeBase):
    def __init__(self, lineNumber, lineContent, parent = None):
        self.title = "%s - %s" % (lineNumber, lineContent.strip())
        self.lineNumber = lineNumber
        self.identifier = unicode(hash(self.title))
        TreeNodeBase.__init__(self, self.identifier, parent)
        
    def path(self):
        return self.nodeParent().path()
    
    def icon(self):
        return resources.getIcon(self.path())

class SearchTreeModel(AbstractNamespaceTreeModel):
    def __init__(self, parent = None):
        AbstractNamespaceTreeModel.__init__(self, separator = os.sep, parent = parent)

    def treeNodeFactory(self, name, parent = None):
        return DirectoryTreeNode(name, parent)
        
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()

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
