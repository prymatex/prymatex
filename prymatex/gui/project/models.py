#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

class PMXWorkspace(object):
    def __init__(self):
        self.children = []

    def __len__(self):
        return len(self.children)
    
    def appendProject(self, project):
        self.children.append(project)
        project.parent = self

    def removeProject(self, project):
        self.children.remove(project)

    #==================================================
    # Tree Node interface
    #==================================================
    def child(self, row, column):
        if len(self.children) > row:
            return self.children[row]

    def childCount(self):
        return len(self.children)

class PMXProjectTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.workspace = PMXWorkspace()

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
    def getAllProjects(self):
        """docstring for getAllProjects"""
        return self.workspace.children
    
    def appendProject(self, project):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.workspace), len(self.workspace))
        self.workspace.appendProject(project)
        self.endInsertRows()
        
    def refreshProject(self, project, relativePath = ""):
        node = project.findDirectoryNode(relativePath)
        parent = self.createIndex(node.row(), 0, node)
        node.doRefresh()