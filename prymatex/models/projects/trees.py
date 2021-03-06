#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.models.trees import AbstractTreeModel
from prymatex.models.trees import FlatTreeProxyModel
from prymatex.models.configure import SortFilterConfigureProxyModel
from prymatex.models.projects.nodes import (ProjectTreeNode, FileSystemTreeNode, SourceFolderTreeNode, NamespaceFolderTreeNode)

from prymatex.utils import fnmatch
from prymatex.utils import glob

__all__ = [ 'ProjectTreeModel', 'ProjectTreeProxyModel', 'FileSystemProxyModel', 'ProjectMenuProxyModel' ]

# ------------- Project Model
class ProjectTreeModel(AbstractTreeModel):  
    def __init__(self, projectManager):
        super(ProjectTreeModel, self).__init__(parent=projectManager)
        self.projectManager = projectManager
        self.fileManager = projectManager.fileManager
        self.supportManager = projectManager.supportManager
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.directoryChanged.connect(self.refreshPath)
        self.fileSystemWatcher.fileChanged.connect(self.refreshPath)
        self.supportManager.propertiesChanged.connect(self.refreshPath)

    def rowCount(self, parent):
        node = self.node(parent)
        if not node.isRootNode() and not node._populated:
            if node.isProject():
                self._load_project(node, parent)
            elif node.isDirectory():
                self._load_directory(node, parent)
        return node.childrenCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.nodeName()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()

    def indexForPath(self, path):
        for project in self.projects():
            current_index = self.createIndex(project.row(), 0, project)
            if project.path() == path:
                return current_index
            while self.rowCount(current_index):
                go_ahead = False
                for node in self.node(current_index).children():
                    if self.fileManager.issubpath(path, node.path()):
                        current_index = self.createIndex(node.row(), 0, node)
                        if self.fileManager.commonpath(path, node.path()) == path:
                            return current_index
                        go_ahead = True
                        break
                if not go_ahead:
                    break
        return QtCore.QModelIndex()

    # -------------- Custom load methods
    def _load_directory_names(self, node):
        properties = self.supportManager.getPropertiesSettings(node.path())
        names = glob.globdir(node.path(), properties.fileBrowserGlob)
        return [ name for name in names if properties.pathInBrowser(
            os.path.join(node.path(), name)
        )]
             
    def _load_directory(self, node, index, notify=False):
        names = self._load_directory_names(node)
        if notify: 
            self.beginInsertRows(index, 0, len(names) - 1)
        for name in names:
            child_node = FileSystemTreeNode(name, node)
            node.appendChild(child_node)
        if notify: 
            self.endInsertRows()
        for child in node.children():
            child._populated = False
        node._populated = True
        self.fileSystemWatcher.addPath(node.path())
	
    def _load_project(self, node, index, notify=False):
        if notify: 
            self.beginInsertRows(index, 0, len(names) - 1)
        for folder in node.source_folders:
            child_node = SourceFolderTreeNode(folder, node)
            node.appendChild(child_node)
        for namespace in node.namespaces:
            child_node = NamespaceFolderTreeNode(namespace, node)
            node.appendChild(child_node)
        if notify: 
            self.endInsertRows()
        for child in node.children():
            child._populated = False
        node._populated = True
        self.fileSystemWatcher.addPath(node.path())

    def _update_directory(self, parent_node, parent_index, notify=False):
        names = self._load_directory_names(parent_node)
        addNames = [name for name in names if parent_node.findChildByName(name) is None]
        removeNodes = [node for node in parent_node.children() if node.nodeName() not in names]
                
        #Quitamos elementos eliminados
        for node in removeNodes:
            if notify:
                self.beginRemoveRows(parent_index, node.row(), node.row())
            parent_node.removeChild(node)
            if notify:
                self.endRemoveRows()

        #Agregamos elementos nuevos
        if notify: 
            self.beginInsertRows(parent_index, parent_node.childrenCount(), parent_node.childrenCount() + len(addNames) - 1)
        for name in addNames:
            node = FileSystemTreeNode(name, parent_node)
            node._populated = False
            parent_node.appendChild(node)
        if notify: 
            self.endInsertRows()

    def _update_project(self, parent_node, parent_index, notify=False):
        parent_node.reload()
        source_names = [os.path.basename(path) for path in parent_node.source_folders]
        source_folders = [path for path in parent_node.source_folders \
            if parent_node.findChildByName(os.path.basename(path)) is None]
        namespace_names = [ns.name for ns in parent_node.namespaces]
        namespaces = [ns for ns in parent_node.namespaces \
            if parent_node.findChildByName(ns.name) is None]
        names = source_names + namespace_names
        remove_nodes = [node for node in parent_node.children() \
            if node.nodeName() not in names]

        #Quitamos elementos eliminados
        for node in remove_nodes:
            if notify:
                self.beginRemoveRows(parent_index, node.row(), node.row())
            parent_node.removeChild(node)
            if notify:
                self.endRemoveRows()

        #Agregamos elementos nuevos
        if notify: 
            self.beginInsertRows(parent_index, parent_node.childrenCount(), parent_node.childrenCount() + len(source_folders) + len(namespaces) - 1)
        for path in source_folders:
            node = SourceFolderTreeNode(path, parent_node)
            node._populated = False
            parent_node.appendChild(node)
        for namespace in namespaces:
            node = NamespaceFolderTreeNode(namespace, parent_node)
            node._populated = False
            parent_node.appendChild(node)
        if notify: 
            self.endInsertRows()    

    def _collect_expanded_subdirs(self, parent_node):
        return [node for node in parent_node.children() if node.isDirectory() and node._populated]

    def refresh(self, updateIndex):
        updateNode = self.node(updateIndex)
        while not updateNode.isRootNode() and not self.fileManager.exists(updateNode.path()):
            updateNode = updateNode.nodeParent()
        if not updateNode.isRootNode():
            updateNodes = [ updateNode ]
            while updateNodes:
                node = updateNodes.pop(0)
                if node.isDirectory():
                    self._update_directory(node, self.createIndex(node.row(), 0, node), True)
                elif node.isProject():
                    self._update_project(node, self.createIndex(node.row(), 0, node), True)
                updateNodes += self._collect_expanded_subdirs(node)

    def refreshPath(self, path):
        self.refresh(self.indexForPath(path))
    
    def nodeForPath(self, path):
        return self.node(self.indexForPath(path))

    def projectForPath(self, path):
        for project in self.projects():
            for source_folder in project.folders:
                if self.fileManager.issubpath(source_folder.path(), path):
                    return project
        
    def filePath(self, index):
        node = self.node(index)
        if not node.isRootNode():
            return node.path()
    
    def isDirectory(self, index):
        node = self.node(index)
        return node.isDirectory() if not node.isRootNode() else False

    def appendProject(self, project):
        project._populated = False
        self.appendNode(project)
    
    def removeProject(self, project):
        self.removeNode(project)

    def projects(self):
        return self.rootNode.children()

#=========================================
# Proxies
#=========================================
class ProjectTreeProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, projectManager):
        QtCore.QSortFilterProxyModel.__init__(self, projectManager)
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
        
        if isinstance(node, ProjectTreeNode): return True
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            return fnmatch.fnmatch(node.path(), pattern)
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        leftNode = self.sourceModel().node(left)
        rightNode = self.sourceModel().node(right)
        if leftNode.isRootNode() or rightNode.isRootNode():
            return False
        elif self.folderFirst and leftNode.isDirectory() and not rightNode.isDirectory():
            return not self.descending
        elif self.folderFirst and not leftNode.isDirectory() and rightNode.isDirectory():
            return self.descending
        elif self.orderBy == "name" and isinstance(rightNode, ProjectTreeNode) and isinstance(leftNode, ProjectTreeNode):
            return leftNode.nodeName() < rightNode.nodeName()
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
    
    def sortBy(self, orderBy, folderFirst=True, descending=False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtCore.QSortFilterProxyModel.sort(self, 0, order)
        
    def isDirectory(self, index):
        return self.sourceModel().isDirectory(self.mapToSource(index))

    #=======================================================
    # Drag and Drop support
    #=======================================================
    def flags(self, index):
        defaultFlags = QtCore.QSortFilterProxyModel.flags(self, index)
        if not self.isDirectory(index):
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
        return node.isFile() and not node.isHidden()
        
    def comparableValue(self, index):
        node = self.sourceModel().node(index)
        return node.nodeName().lower()
    
    def compareIndex(self, xindex, yindex):
        xnode = self.sourceModel().node(xindex)
        ynode = self.sourceModel().node(yindex)
        return (xnode.nodeName() > ynode.nodeName()) - (xnode.nodeName() < ynode.nodeName())
    
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
class ProjectMenuProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, projectManager):
        super(ProjectMenuProxyModel, self).__init__(projectManager)
        self.projectManager = projectManager
        self.currentProject = None
        
    def setCurrentProject(self, project):
        self.currentProject = project

    def filterAcceptsRow(self, row, parent):
        source_model = self.sourceModel()
        index = source_model.index(row, 0, parent)
        node = source_model.node(index)
        item = node.bundleItem()
        return not node.isRootNode() and item.enabled()
        
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
