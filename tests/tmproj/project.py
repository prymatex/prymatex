#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs

from PyQt4 import QtCore, QtGui

class PMXProjectsTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.root = PMXWorkspace()

    def rowCount(self, parent):
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parent = self.root
        else:  
            parent = parent.internalPointer()  

        return parent.childCount()

    def columnCount(self, parent):  
        return 1

    def data(self, index, role):  
        if not index.isValid():  
            return None
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return item.name
        elif role == QtCore.Qt.DecorationRole:
            item = index.internalPointer()
            return item.icon

    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def index(self, row, column, parent):
        if not parent.isValid():
            parent = self.root
        else:
            parent = parent.internalPointer()
        
        child = parent.child(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()  

        child = index.internalPointer()
        parent = child.parent
        if parent == self.root:
            return QtCore.QModelIndex()

        row = parent.row()

        return self.createIndex(row, 0, parent)

class PMXWorkspace(object):
    def __init__(self):
        self.projects = []

    #==================================================
    # Tree Node interface
    #==================================================
    def appendChild(self, project):
        self.projects.append(project)
        project.parent = self

    def removeChild(self, project):
        self.projects.remove(project)
        
    def child(self, row):
        if len(self.projects) > row:
            return self.projects[row]

    def childCount(self):
        return len(self.projects)

class PMXProject(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.isFolder = True
    
    def get_full_path(self):
        '''
        Returns the full path of the project
        '''
        return self.path
