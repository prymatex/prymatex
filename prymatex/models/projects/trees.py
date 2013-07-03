#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import codecs
import fnmatch

from prymatex.qt import QtCore, QtGui

from prymatex.models.trees import AbstractTreeModel
from prymatex.models.trees import FlatTreeProxyModel
from prymatex.models.configure import SortFilterConfigureProxyModel
from prymatex.models.projects.nodes import FileSystemTreeNode


__all__ = [ 'ProjectTreeModel', 'ProjectTreeProxyModel', 'FileSystemProxyModel', 'ProjectMenuProxyModel' ]

#=========================================
# Models
#=========================================
class ProjectTreeModel(AbstractTreeModel):  
    def __init__(self, projectManager):
        #projectManager is a qObject
        AbstractTreeModel.__init__(self, projectManager)
        self.projectManager = projectManager
        self.fileManager = projectManager.fileManager

    def treeNodeFactory(self, nodeName, nodeParent):
        if nodeParent is not None:
            return FileSystemTreeNode(nodeName, nodeParent)
        else:
            # TODO: Quiza sea mejor hacer un custom root node
            return AbstractTreeModel.treeNodeFactory(self, nodeName, nodeParent)

    def rowCount(self, parent):
        parentNode = self.node(parent)
        if not parentNode.isRootNode() and parentNode.isdir and not parentNode._populated:
            self._load_directory(parentNode, parent)
        return parentNode.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.nodeName()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()


    def indexForPath(self, path):
        currentIndex = QtCore.QModelIndex()
        while self.rowCount(currentIndex):
            goAhead = False
            for node in self.node(currentIndex).childNodes():
                if self.fileManager.issubpath(path, node.path()):
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
        names = self.fileManager.listDirectory(parentNode.path())
        if notify: 
            self.beginInsertRows(parentIndex, 0, len(names) - 1)
        for name in names:
            node = self.treeNodeFactory(name, parentNode)
            parentNode.appendChild(node)
        if notify: 
            self.endInsertRows()
        for child in parentNode.childNodes():
            child._populated = False
        parentNode._populated = True
	
    def _update_directory(self, parentNode, parentIndex, notify = False):
        names = self.fileManager.listDirectory(parentNode.path())
        addNames = [name for name in names if parentNode.findChildByName(name) is None]
        removeNodes = [node for node in parentNode.childNodes() if node.nodeName() not in names]
                
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
            node = self.treeNodeFactory(name, parentNode)
            node._populated = False
            parentNode.appendChild(node)
        if notify: 
            self.endInsertRows()

    def _collect_expanded_subdirs(self, parentNode):
        return [node for node in parentNode.childNodes() if node.isdir and node._populated]

    def refresh(self, updateIndex):
        updateNode = self.node(updateIndex)
        while not updateNode.isRootNode() and not self.fileManager.exists(updateNode.path()):
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
        for project in self.rootNode.childNodes():
            if self.fileManager.issubpath(project.path(), path):
                return project
        
    def filePath(self, index):
        node = self.node(index)
        if not node.isRootNode():
            return node.path()
    
    def isDir(self, index):
        node = self.node(index)
        return node.isdir if not node.isRootNode() else False
        
    def appendProject(self, project):
        project._populated = False
        self.appendNode(project)
    
    def removeProject(self, project):
        self.removeNode(project)

#=========================================
# Proxies
#=========================================
class ProjectTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, projectManager):
        QtGui.QSortFilterProxyModel.__init__(self, projectManager)
        self.projectManager = projectManager
        self.fileManager = projectManager.fileManager
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
        self.nodeFormaters = []
    
    def addNodeFormater(self, formater):
        self.nodeFormaters.append(formater)
        
    def data(self, index, role):
        value = self.sourceModel().data(self.mapToSource(index), role)
        for formater in self.nodeFormaters:
            value = formater(self.node(index), value, role)
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
            match = self.fileManager.fnmatchany(node.path(), pattern.split(","))
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
            return leftNode.name < rightNode.name
        else:
            return self.fileManager.compareFiles(leftNode.path(), rightNode.path(), self.orderBy) < 0

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    
    def refreshPath(self, path):
        return self.sourceModel().refreshPath(path)
        
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

        if not self.fileManager.isdir(parentPath):
            return False

        if not mimeData.hasUrls():
            return False

        updateIndexes = [ parentIndex ]
            
        for url in mimeData.urls():
            srcPath = url.toLocalFile()
            pIndex = self.indexForPath(self.fileManager.dirname(srcPath))
            if pIndex not in updateIndexes:
                updateIndexes.append(pIndex)
            dstPath = self.fileManager.join(parentPath, self.fileManager.basename(srcPath))
            if action == QtCore.Qt.CopyAction:
                if self.fileManager.isdir(srcPath):
                    self.fileManager.copytree(srcPath, dstPath)
                else:
                    self.fileManager.copy(srcPath, dstPath)
            elif action == QtCore.Qt.MoveAction:
                self.fileManager.move(srcPath, dstPath)
            elif action == QtCore.Qt.LinkAction:
                self.fileManager.link(srcPath, dstPath)

        list(map(lambda index: self.refresh(index), updateIndexes))
        return True
    
    def mimeTypes(self):
        return ["text/uri-list"]
        
    def mimeData(self, indexes):
        urls = [QtCore.QUrl.fromLocalFile(self.filePath(index)) for index in indexes]
        mimeData = QtCore.QMimeData()
        mimeData.setUrls(urls)
        return mimeData
        
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction | QtCore.Qt.LinkAction

# TODO: Esto es parte de un intento de hacer un modelo para buscar entre archivos hacer algo con él
class FileSystemProxyModel(FlatTreeProxyModel):
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
        return (xnode.name > ynode.name) - (xnode.name < ynode.name)
    
    def findItemIndex(self, item):
        for num, index in enumerate(self.indexMap()):
            if self.sourceModel().node(index) == item:
                return num
    
    def getAllItems(self):
        items = []
        for index in self.indexMap():
            items.append(self.sourceModel().node(index))
        return items


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
        return not node.isRootNode() and node.enabled()
        
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