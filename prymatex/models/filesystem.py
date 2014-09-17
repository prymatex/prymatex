#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import sys, os

from prymatex.qt import QtCore, QtGui, QtWidgets
    
class SortFilterFileSystemProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtCore.QSortFilterProxyModel.__init__(self, parent)
        self.application = QtWidgets.QApplication.instance()
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        path = self.sourceModel().filePath(sIndex)
        if os.path.isdir(path): return True
        
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            match = any([fnmatch.fnmatch(path, p) for p in [p.strip() for p in pattern.split(",")]])
            return not match
        return True
      
    def lessThan(self, left, right):
        isleftdir = self.sourceModel().isDir(left)
        isrightdir = self.sourceModel().isDir(right)
        if self.folderFirst and isleftdir and not isrightdir:
            return not self.descending
        elif self.folderFirst and not isleftdir and isrightdir:
            return self.descending
        else:
            leftPath = self.sourceModel().filePath(left)
            rightPath = self.sourceModel().filePath(right)
            return self.application.fileManager.compareFiles(leftPath, rightPath, self.orderBy) < 0

    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtCore.QSortFilterProxyModel.sort(self, 0, order)
    
    def filePath(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().filePath(sIndex)

    def isDir(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().isDir(sIndex)
        
    def dropMimeData(self, mimeData, action, row, col, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True

        sourceIndex = self.mapToSource(parentIndex)
        parentPath = self.sourceModel().filePath(sourceIndex)

        if not os.path.isdir(parentPath):
            return False

        if not mimeData.hasUrls():
            return False

        for url in mimeData.urls():
            srcPath = url.toLocalFile()
            dstPath = os.path.join(parentPath, self.application.fileManager.basename(srcPath))
            if action == QtCore.Qt.CopyAction:
                if os.path.isdir(srcPath):
                    self.application.fileManager.copytree(srcPath, dstPath)
                else:
                    self.application.fileManager.copy(srcPath, dstPath)
            elif action == QtCore.Qt.MoveAction:
                self.application.fileManager.move(srcPath, dstPath)
            elif action == QtCore.Qt.LinkAction:
                self.application.fileManager.link(srcPath, dstPath)
        return True
    
    def mimeTypes(self):
        return ["text/uri-list"]
    
    def flags(self, index):
        defaultFlags = QtCore.QSortFilterProxyModel.flags(self, index)
        if not self.isDir(index):
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled 
