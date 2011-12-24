#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeModel
from prymatex.gui.project.base import FileSystemTreeNode

class PMXProjectTreeModel(TreeModel):  
    def __init__(self, manager, parent = None):
        self.manager = manager
        TreeModel.__init__(self, parent)
        self.fileWatcher = QtCore.QFileSystemWatcher()
        self.fileWatcher.directoryChanged.connect(self.refreshProjectByPath)
    
    def refreshProjectByPath(self, path):
        index = self.indexForPath(path)
        self.refresh(index)
    
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def indexForPath(self, path):
        node = self.nodeForPath(path)
        return self.createIndex(node.row(), 0, node)
        
    #========================================================================
    # Custom methods
    #========================================================================
    def _load_directory(self, parentNode, parentIndex):
        names = os.listdir(parentNode.path)
        self.beginInsertRows(parentIndex, 0, len(names) - 1)
        for name in names:
            node = FileSystemTreeNode(name, parentNode)
            parentNode.appendChild(node)
        self.endInsertRows()
        for child in parentNode.children:
            if child.isdir:
                index = self.index(child.row(), 0, parentIndex)
                self._load_directory(child, index)
        self.fileWatcher.addPath(parentNode.path)

    def refresh(self, parentIndex):
        parentNode = self.node(parentIndex)
        add = os.listdir(parentNode.path)
        remove = []
        for child in parentNode.children:
            if child.name in add:
                add.remove(child.name)
            else:
                remove.append(child)
        for child in remove:
            self.beginRemoveRows(parentIndex, child.row(), child.row())
            parentNode.removeChild(child)
            self.endRemoveRows()
        newNodes = []
        if add:
            self.beginInsertRows(parentIndex, parentNode.childCount(), parentNode.childCount() + len(add) - 1)
            for name in add:
                node = FileSystemTreeNode(name, parentNode)
                parentNode.appendChild(node)
                newNodes.append(node)
            self.endInsertRows()
        for child in newNodes:
            if child.isdir:
                index = self.index(child.row(), 0, parentIndex)
                self._load_directory(child, index)
                
    def nodeForPath(self, path):
        currentNode = self.rootNode
        while currentNode.children:
            for node in currentNode.children:
                if os.path.commonprefix([node.path, path]) == path:
                    return node
                if os.path.commonprefix([node.path, path]) == node.path:
                    currentNode = node
                    break
        if currentNode != self.rootNode:   
            return currentNode
            
    def filePath(self, index):
        return index.internalPointer().path
    
    def appendProject(self, project):
        self.beginInsertRows(QtCore.QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
        self.rootNode.appendChild(project)
        self.endInsertRows()
        index = self.index(project.row(), 0, QtCore.QModelIndex())
        self._load_directory(project, index)
    
    def removeProject(self, project):
        self.beginRemoveRows(QtCore.QModelIndex(), project.row(), project.row())
        self.rootNode.removeChild(project)
        self.endRemoveRows()

        