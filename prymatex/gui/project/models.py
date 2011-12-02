#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

class PMXWorkspace(object):
    def __init__(self):
        self.fileSystem = QtGui.QDirModel()
        self.projects = []

    def __len__(self):
        return len(self.projects)
    
    def appendProject(self, project):
        self.projects.append(project)
        project.setWorkspace(self)

    def removeProject(self, project):
        self.projects.remove(project)
        
    #==================================================
    # Tree Node interface
    #==================================================
    def child(self, row, column):
        if len(self.projects) > row:
            return self.projects[row]

    def childCount(self):
        return len(self.projects)

class PMXProject(object):
    def __init__(self, name, path):
        self._name = name
        self.rootPath = path
        self.workspace = None
        self.children = []
    
    @property
    def fileSystem(self):
        return self.workspace.fileSystem
    
    def setWorkspace(self, workspace):
        self.workspace = workspace
        self.rootIndex = workspace.fileSystem.index(self.rootPath)

    #==================================================
    # Tree Node interface
    #==================================================
    def icon(self):
        return None
        
    def name(self):
        return self._name
    
    def child(self, row, column):
        child = self.rootIndex.child(row, column)
        path = self.fileSystem.filePath(child)
        item = PMXProjectItem(path, self)
        item.setParent(self)
        self.children.append(item)
        return item
    
    def row(self):
        return self.parent().projects.index(self)
    
    def parent(self):
        return self.workspace
    
    def childCount(self):
        return self.fileSystem.rowCount(self.rootIndex)

class PMXProjectItem(object):
    def __init__(self, path, project):
        self.path = path
        self.project = project
        self._parent = None
        self.children = []

    @property
    def fileSystem(self):
        return self.project.fileSystem
        
    def setParent(self, parent):
        self._parent = parent

    #==================================================
    # Tree Node interface
    #==================================================
    def icon(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.fileIcon(index)
        
    def name(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.fileName(index)
    
    def childCount(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.rowCount(index)
    
    def child(self, row, column):
        index = self.fileSystem.index(self.path)
        child = index.child(row, column)
        path = self.fileSystem.filePath(child)
        item = PMXProjectItem(path, self.project)
        item.setParent(self)
        self.children.append(item)
        return item
    
    def row(self):
        return self.parent().children.index(self)
    
    def parent(self):
        return self._parent

class PMXProjectTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.workspace = PMXWorkspace()

    def data(self, index, role):  
        node = self.getNode(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()

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
        parentNode = node.parent()

        if parentNode == self.workspace:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self.workspace

    def addProject(self, name, path):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.workspace), len(self.workspace))
        self.workspace.appendProject(PMXProject(name, path))
        self.endInsertRows()
