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
        index = self.createIndex(node.row(), 0, node) if node != None else QtCore.QModelIndex()
        return index
        
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

    def refresh(self, index):
        node = self.node(index)
        while not os.path.exists(node.path):
            index = index.parent()
            node = self.node(index)
        #TODO: Ver que pasa si llegamos al root, quiere decir que el project no esta mas
        if node.isdir:
            self.beginRemoveRows(index, 0, node.childCount() - 1)
            for child in node.children:
                node.removeAllChild()
            self.endRemoveRows()
            self._load_directory(node, index)
            
    def nodeForPath(self, path):
        currentNode = self.rootNode
        while currentNode.children:
            goAhead = False
            for node in currentNode.children:
                prefix = os.path.commonprefix([node.path, path])
                if prefix == path:
                    return node
                elif prefix == node.path:
                    currentNode = node
                    goAhead = True
                    break
            if not goAhead:
                break
        if currentNode != self.rootNode:
            return currentNode

    def projectForPath(self, path):
        for project in self.rootNode.children:
            if os.path.commonprefix([project.path, path]) == project.path:
                return project
        
    def filePath(self, index):
        return index.internalPointer().path
    
    def isDir(self, index):
        return index.internalPointer().isdir
    
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
    