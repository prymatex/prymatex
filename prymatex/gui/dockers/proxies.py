#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from __future__ import print_function
import fnmatch
import os
from PyQt4 import QtCore, QtGui
import sys
    
class PMXFileSystemProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.application = QtGui.QApplication.instance()
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        path = self.sourceModel().filePath(sIndex)
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            accept = any(map(lambda p: fnmatch.fnmatch(path, p), map(lambda p: p.strip(), pattern.split(",")))) if not os.path.isdir(path) else True
            return accept
        return True
    
    def columnCount(self, parent):
        return 1
        
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
            return self.application.fileManager.compareFiles(leftPath, rightPath, self.orderBy)

    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
        
    def filePath(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().filePath(sIndex)
    
    
    
    def dropMimeData(self, mimeData, action, row, col, parentIndex):
        #print action
        if action == QtCore.Qt.IgnoreAction:
            print ("Ignore")
            return True
        """
        Qt::CopyAction
        Qt::MoveAction
        Qt::LinkAction
        Qt::ActionMask
        Qt::IgnoreAction
        Qt::TargetMoveAction
        """
        index = self.index(row, col, parentIndex)
        sourceIndex = self.mapToSource(parentIndex)
        destPath = self.sourceModel().filePath(sourceIndex)
        print("La ruta es:", destPath)
        
        if not os.path.isdir(destPath):
            return False
        # TODO: Simple selection restricts the number of urls to 1
        url = mimeData.urls()[0]
        fromPath = os.path.dirname(url.toLocalFile()) 
        if fromPath == destPath: 
            print("Origen", fromPath, "destino", destPath, sep = " ")
            return False
        
        if not mimeData.hasUrls():
            return False
        if action is QtCore.Qt.CopyAction:
            return True
        elif action is QtCore.Qt.MoveAction:
            return True
        elif action is QtCore.Qt.LinkAction:
            return True
        return False
    
    def mimeTypes(self):
        return ["text/uri-list"]
    
    def flags(self, index):
        sourceIndex = self.mapToSource(index)
        defaultFlags = super(PMXFileSystemProxyModel, self).flags(index)
        if not self.sourceModel().isDir(self.mapToSource(index)):
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled 
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled 