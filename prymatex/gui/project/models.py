#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeModel
from prymatex.gui.project.base import FileSystemTreeNode
from prymatex.gui.configure.models import PMXConfigureTreeNode

class PMXProjectTreeModel(TreeModel):  
    def __init__(self, projectManager):
        #projectManager is a qObject
        TreeModel.__init__(self, projectManager)
        self.projectManager = projectManager
        
    def rowCount(self, parent):
        parentNode = self.node(parent)
        if not parentNode.isRootNode() and parentNode.isdir and not parentNode._populated:
            self._load_directory(parentNode, parent)
        return parentNode.childCount()

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def refreshProjectByPath(self, path):
        index = self.indexForPath(path)
        self.refresh(index)
    
    def indexForPath(self, path):
        node = self.nodeForPath(path)
        index = self.createIndex(node.row(), 0, node) if node != None else QtCore.QModelIndex()
        return index
        
    #========================================================================
    # Custom methods
    #========================================================================
    def _load_directory(self, parentNode, parentIndex, notify = False):
        names = os.listdir(parentNode.path)
        if notify: 
            self.beginInsertRows(parentIndex, 0, len(names) - 1)
        for name in names:
            node = FileSystemTreeNode(name, parentNode)
            parentNode.appendChild(node)
        if notify: 
            self.endInsertRows()
        for child in parentNode.childrenNodes:
            child._populated = False
        parentNode._populated = True
	
    def refresh(self, index):
        node = self.node(index)
        while not node.isRootNode() and not os.path.exists(node.path):
            index = index.parent()
            node = self.node(index)
        #TODO: mejorar esto de la verificacion con el root node
        if not node.isRootNode() and node.isdir:
            self.beginRemoveRows(index, 0, node.childCount() - 1)
            for child in node.childrenNodes:
                node.removeAllChild()
            self.endRemoveRows()
            self._load_directory(node, index, True)
            
    def nodeForPath(self, path):
        currentNode = self.rootNode
        while currentNode.childrenNodes:
            goAhead = False
            for node in currentNode.childrenNodes:
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
        for project in self.rootNode.childrenNodes:
            if os.path.commonprefix([project.path, path]) == project.path:
                return project
        
    def filePath(self, index):
        node = self.node(index)
        if not node.isRootNode():
            return node.path
    
    def isDir(self, index):
        try:
            return index.internalPointer().isdir
        except AttributeError as _exc:
            # Not in tree, should check through python 
            print index.data()
            return False
    
    def appendProject(self, project):
        project._populated = False
        self.beginInsertRows(QtCore.QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
        self.rootNode.appendChild(project)
        self.endInsertRows()
    
    def removeProject(self, project):
        self.beginRemoveRows(QtCore.QModelIndex(), project.row(), project.row())
        self.rootNode.removeChild(project)
        self.endRemoveRows()

#=========================================
# Properties Tree Model
#=========================================
class PMXPropertyTreeNode(PMXConfigureTreeNode):
    def __init__(self, name, parent = None):
        PMXConfigureTreeNode.__init__(self, name, parent)

    def acceptFileSystemItem(self, fileSystemItem):
        return True
        
    def edit(self, fileSystemItem):
        pass