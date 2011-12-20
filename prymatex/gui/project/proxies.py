#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.base import PMXProject
from prymatex.gui.dockers.proxies import ORDERS

class PMXProjectTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.orderBy = "name"
        self.folderFirst = True
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        if isinstance(item, PMXProject):
            #Filtrar por sets
            regexp = self.filterRegExp()
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
            
    def lessThan(self, left, right):
        leftPath = self.sourceModel().filePath(left)
        rightPath = self.sourceModel().filePath(right)
        return ORDERS[self.orderBy](leftPath, rightPath, self.folderFirst)

    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
