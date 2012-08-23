#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import fnmatch

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.base import PMXProject
from prymatex.gui.configure.proxies import PMXConfigureProxyModel
from prymatex.models.proxies import FlatTreeProxyModel

class PMXProjectTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, projectManager):
        QtGui.QSortFilterProxyModel.__init__(self, projectManager)
        self.projectManager = projectManager
        self.fileManager = self.projectManager.fileManager
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
        self.nodeFormaters = []
    
    def addNodeFormater(self, formater):
        self.nodeFormaters.append(formater)
        
    def data(self, index, role):
        sIndex = self.mapToSource(index)
        value = self.sourceModel().data(sIndex, role)
        node = self.node(index)
        if not node.isRootNode():
            for formater in self.nodeFormaters:
                value = formater(node, value, role)
        return value

    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        if node.isproject: return True
        #TODO: Esto depende de alguna configuracion tambien
        if node.ishidden: return False
        if node.isdir: return True
        
        regexp = self.filterRegExp()        
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            #TODO: Hacerlo en el fileManager
            match = any(map(lambda p: fnmatch.fnmatch(node.path, p), map(lambda p: p.strip(), pattern.split(","))))
            return not match
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        leftNode = self.sourceModel().node(left)
        rightNode = self.sourceModel().node(right)
        if self.folderFirst and leftNode.isdir and not rightNode.isdir:
            return not self.descending
        elif self.folderFirst and not leftNode.isdir and rightNode.isdir:
            return self.descending
        elif self.orderBy == "name" and rightNode.isproject and leftNode.isproject:
            return cmp(leftNode.name, rightNode.name) < 0
        else:
            return self.fileManager.compareFiles(leftNode.path, rightNode.path, self.orderBy) < 0

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    
    def refresh(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().refresh(sIndex)
    
    def indexForPath(self, path):
        sIndex = self.sourceModel().indexForPath(path)
        if sIndex.isValid():
            return self.mapFromSource(sIndex)
        return sIndex
        
    def filePath(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().filePath(sIndex)
    
    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
        
    def isDir(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().isDir(sIndex)

    #=======================================================
    # Drag and Drop support
    #=======================================================
    def flags(self, index):
        defaultFlags = QtGui.QSortFilterProxyModel.flags(self, index)
        if not self.isDir(index):
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled 

    def dropMimeData(self, mimeData, action, row, col, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True

        parentPath = self.filePath(parentIndex)

        if not os.path.isdir(parentPath):
            return False

        if not mimeData.hasUrls():
            return False

        updateIndexes = [ parentIndex ]
            
        for url in mimeData.urls():
            srcPath = url.toLocalFile()
            pIndex = self.indexForPath(self.fileManager.dirname(srcPath))
            if pIndex not in updateIndexes:
                updateIndexes.append(pIndex)
            dstPath = os.path.join(parentPath, self.fileManager.basename(srcPath))
            if action == QtCore.Qt.CopyAction:
                if os.path.isdir(srcPath):
                    self.fileManager.copytree(srcPath, dstPath)
                else:
                    self.fileManager.copy(srcPath, dstPath)
            elif action == QtCore.Qt.MoveAction:
                self.fileManager.move(srcPath, dstPath)
            elif action == QtCore.Qt.LinkAction:
                self.fileManager.link(srcPath, dstPath)

        map(lambda index: self.refresh(index), updateIndexes)
        return True
    
    def mimeTypes(self):
        return ["text/uri-list"]
        
    def mimeData(self, indexes):
        urls = map(lambda index: QtCore.QUrl.fromLocalFile(self.filePath(index)), indexes)
        mimeData = QtCore.QMimeData()
        mimeData.setUrls(urls)
        return mimeData
        
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction | QtCore.Qt.LinkAction

class PMXFileSystemProxyModel(FlatTreeProxyModel):
    def __init__(self, parent = None):
        FlatTreeProxyModel.__init__(self, parent)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        return node.isfile and not node.ishidden
        
    def comparableValue(self, index):
        node = self.sourceModel().node(index)
        return node.name.lower()
    
    def compareIndex(self, xindex, yindex):
        xnode = self.sourceModel().node(xindex)
        ynode = self.sourceModel().node(yindex)
        return cmp(xnode.name, ynode.name)
    
    def findItemIndex(self, item):
        for num, index in enumerate(self.indexMap()):
            if self.sourceModel().node(index) == item:
                return num
    
    def getAllItems(self):
        items = []
        for index in self.indexMap():
            items.append(self.sourceModel().node(index))
        return items

class PMXPropertiesProxyModel(PMXConfigureProxyModel):
    def __init__(self, parent = None):
        PMXConfigureProxyModel.__init__(self, parent)
        self.fileSystemItem = None
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        if self.fileSystemItem is None:
            return False
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        if not node.acceptFileSystemItem(self.fileSystemItem):
            return False
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            return regexp.indexIn(node.filterString()) != -1
        return True
    
    def setFilterFileSystem(self, fileSystemItem):
        self.fileSystemItem = fileSystemItem
        self.setFilterRegExp("")

#=========================================
# Project Bundle Menu
#=========================================
class ProjectMenuProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, projectManager):
        super(ProjectMenuProxyModel, self).__init__(projectManager)
        self.projectManager = projectManager
        self.currentProject = None
        
    def setCurrentProject(self, project):
        self.currentProject = project

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(index)
        return not node.isRootNode() and node.enabled
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def data(self, index, role):
        if self.sourceModel() is None or self.currentProject is None:
            return None

        sIndex = self.mapToSource(index)
        if role == QtCore.Qt.CheckStateRole:
            bundle = self.sourceModel().node(sIndex)
            return QtCore.Qt.Checked if self.currentProject.hasBundleMenu(bundle) else QtCore.Qt.Unchecked
        else:
            return self.sourceModel().data(sIndex, role)

    def setData(self, index, value, role):
        if self.sourceModel() is None or self.currentProject is None:
            return False
            
        sIndex = self.mapToSource(index)    
        if role == QtCore.Qt.CheckStateRole:
            bundle = self.sourceModel().node(sIndex)
            if value:
                self.projectManager.addProjectBundleMenu(self.currentProject, bundle)
            else:
                self.projectManager.removeProjectBundleMenu(self.currentProject, bundle)
            return True
        return False