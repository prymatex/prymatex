#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.base import PMXWorkspace, PMXProjectItem

class PMXProjectTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.manager = manager
        self.workspace = PMXWorkspace()

    def populateNode(self, node, index):
        path = node.path
        node.isdir = os.path.isdir(path)
        if node.isdir:
            self.manager.fileWatcher.addPath(path)
            names = os.listdir(path)
            self.beginInsertRows(index, 0, len(names))  
            for name in names:
                newNode = PMXProjectItem(name, self)
                newNode.parent = node
                node.children.append(newNode)
            self.endInsertRows()
        node.populated = True
        
    def data(self, index, role):  
        node = self.getNode(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def rowCount(self, parent):
        parentNode = self.getNode(parent)
        if not parentNode.populated:
            self.populateNode(parentNode, parent)
        return parentNode.childCount()

    def columnCount(self, parent):  
        return 1

    def index(self, row, column, parent = QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row, column)
        
        if childItem:
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
    def filePath(self, index):
        return index.internalPointer().path
    
    def getAllProjects(self):
        """docstring for getAllProjects"""
        return self.workspace.children
    
    def appendProject(self, project):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.workspace), len(self.workspace))
        self.workspace.appendProject(project)
        self.endInsertRows()
        
    def refreshProject(self, project, path = ""):
        node = project.findDirectoryNode(relativePath)
        parent = self.createIndex(node.row(), 0, node)
        node.doRefresh()