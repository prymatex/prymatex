#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.utils.tree import TreeNode
from prymatex.gui.project.base import FileSystemTreeNode

class PMXProjectTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.manager = manager
        self.workspace = TreeNode("Workspace")

    def data(self, index, role):
        node = self.getNode(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def rowCount(self, parent):
        parentNode = self.getNode(parent)
        return parentNode.childCount()

    def columnCount(self, parent):
        return 1

    def index(self, row, column, parent = QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        
        if childItem is not None:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent

        if parentNode == self.workspace:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.workspace

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

    def filePath(self, index):
        return index.internalPointer().path
    
    def appendProject(self, project):
        self.beginInsertRows(QtCore.QModelIndex(), self.workspace.childCount(), self.workspace.childCount())
        self.workspace.appendChild(project)
        self.endInsertRows()
        index = self.index(project.row(), 0, QtCore.QModelIndex())
        self._load_directory(project, index)
    
    def removeProject(self, project):
        self.beginRemoveRows(QtCore.QModelIndex(), project.row(), project.row())
        self.workspace.removeChild(project)
        self.endRemoveRows()
        
    def getAllProjects(self):
        """docstring for getAllProjects"""
        return self.workspace.children
        