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
        self.fileManager = projectManager.fileManager
        
    def rowCount(self, parent):
        parentNode = self.node(parent)
        if not parentNode.isRootNode() and parentNode.isdir and not parentNode._populated:
            self._load_directory(parentNode, parent)
        return parentNode.childCount()

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.nodeName()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def indexForPath(self, path):
        currentIndex = QtCore.QModelIndex()
        while self.rowCount(currentIndex):
            goAhead = False
            for node in self.node(currentIndex).childrenNodes:
                if self.fileManager.issubpath(path, node.path):
                    currentIndex = self.createIndex(node.row(), 0, node)
                    goAhead = True
                    break
            if not goAhead:
                break
        return currentIndex

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
	
    def _update_directory(self, parentNode, parentIndex, notify = False):
        names = os.listdir(parentNode.path)
        addNames = filter(lambda name: parentNode.findChildByName(name) is None, names)
        removeNodes = filter(lambda node: node.nodeName() not in names, parentNode.childrenNodes)
                
        #Quitamos elementos eliminados
        for node in removeNodes:
            if notify:
                self.beginRemoveRows(parentIndex, node.row(), node.row())
            parentNode.removeChild(node)
            if notify:
                self.endRemoveRows()

        #Agregamos elementos nuevos
        if notify: 
            self.beginInsertRows(parentIndex, parentNode.childCount(), parentNode.childCount() + len(addNames) - 1)
        for name in addNames:
            node = FileSystemTreeNode(name, parentNode)
            node._populated = False
            parentNode.appendChild(node)
        if notify: 
            self.endInsertRows()

    def _collect_expanded_subdirs(self, parentNode):
        return filter(lambda node: node.isdir and node._populated, parentNode.childrenNodes)

    def refresh(self, updateIndex):
        updateNode = self.node(updateIndex)
        while not updateNode.isRootNode() and not os.path.exists(updateNode.path):
            updateIndex = updateIndex.parent()
            updateNode = self.node(updateIndex)
        if not updateNode.isRootNode() and updateNode.isdir:
            updateNodes = [ updateNode ]
            while updateNodes:
                node = updateNodes.pop(0)
                self._update_directory(node, self.createIndex(node.row(), 0, node), True)
                updateNodes += self._collect_expanded_subdirs(node)

    def refreshPath(self, path):
        index = self.indexForPath(path)
        self.refresh(index)
    
    def nodeForPath(self, path):
        return self.node(self.indexForPath)

    def projectForPath(self, path):
        for project in self.rootNode.childrenNodes:
            if os.path.commonprefix([project.path, path]) == project.path:
                return project
        
    def filePath(self, index):
        node = self.node(index)
        if not node.isRootNode():
            return node.path
    
    def isDir(self, index):
        node = self.node(index)
        return node.isdir if not node.isRootNode() else False
        
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
