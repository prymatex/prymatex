#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

class PMXWorkspace(object):
    def __init__(self):
        self.projects = []

    def __len__(self):
        return len(self.projects)
        
    #==================================================
    # Tree Node interface
    #==================================================
    def appendProject(self, project):
        self.projects.append(project)
        project.parent = self

    def removeProject(self, project):
        self.projects.remove(project)
        
    def child(self, row):
        if len(self.projects) > row:
            return self.projects[row]

    def rowCount(self):
        return len(self.projects)

class PMXProject(object):
    def __init__(self, name, path):
        self.name = name
        self.fileSystemModel = QtGui.QFileSystemModel()
        self.fileSystemModel.setRootPath(path)
        self.fileSystemModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)

class PMXProjectsTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.workspace = PMXWorkspace()
        self.indices = []

    def rowCount(self, parent):
        if not parent.isValid():
            node = self.workspace
        else:
            node = parent.internalPointer()
        if node is self.workspace:
            return node.rowCount()
        return 0
        
    def columnCount(self, parent):  
        return 1

    def data(self, index, role):  
        if not index.isValid():  
            return None
        item = index.internalPointer()
        if isinstance(item, PMXProject) and role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return item.name

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if not parent.isValid():
            node = self.workspace
        else:
            node = parent.internalPointer()
        if node is self.workspace:
            project = node.child(row)
            if project:
                return self.createIndex(row, column, project)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()  

        node = index.internalPointer()
        if node == self.workspace:
            return QtCore.QModelIndex()
        elif isinstance(node, PMXProject):
            row = self.workspace.projects.index(node)
            return self.createIndex(row, 0, self.workspace)
        else:
            return QtCore.QModelIndex()

    def addProject(self, name, path):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.workspace), len(self.workspace))
        self.workspace.appendProject(PMXProject(name, path))
        self.endInsertRows()
