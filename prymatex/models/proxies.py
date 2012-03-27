#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.utils.lists import bisect_key

class FlatTreeProxyModel(QtCore.QAbstractItemModel):
    """
    Proxy for create flat models from tree models
    """
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__indexMap = []
        self.__sourceModel = None

    def indexMap(self):
        return self.__indexMap
    
    def sourceModel(self):
        return self.__sourceModel
        
    def setSourceModel(self, model):
        if model == self.__sourceModel:
            return
        if self.__sourceModel is not None:
            self.__sourceModel.disconnect(self)
        self.__sourceModel = model
        self.__sourceModel.dataChanged.connect(self.on_sourceModel_dataChanged)
        self.__sourceModel.rowsInserted.connect(self.on_sourceModel_rowsInserted)
        self.__sourceModel.rowsAboutToBeRemoved.connect(self.on_sourceModel_rowsAboutToBeRemoved)
        self.__sourceModel.layoutChanged.connect(self.on_sourceModel_layoutChanged)
    
    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
    
    def comparableValue(self, index):
        return 0
        
    def compareIndex(self, xindex, yindex):
        return 0
    
    def mapToSource(self, proxyIndex):
        return self.__indexMap[proxyIndex.row()]

    def mapFromSource(self, sourceIndex):
        return self.index(self.__indexMap.index(sourceIndex), 0)
            
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if self.__sourceModel is None:
            return QtCore.QVariant()
        
        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()
        
        return self.__sourceModel.data(self.__sourceModel.index(row, 0, parent), role)

    def flags(self, index):
        if self.__sourceModel is None or not index.isValid():  
            return QtCore.Qt.NoItemFlags
        flags = self.__sourceModel.flags(self.modelIndex(index))
        #Strip all writable flags and make sure we can select it
        return (flags & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable)) | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        
    def hasChildren(self, index):
        return False

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        return len(self.__indexMap)

    def modelIndex(self, proxyIndex):
        if proxyIndex.isValid():
            row = proxyIndex.row()
            if row < len(self.__indexMap):
                return self.__indexMap[row]
        return QtCore.QModelIndex()
    
    #=========================================
    # source model handler
    #=========================================
    def on_sourceModel_dataChanged(self, topLeft, bottomRight):
        #Remove indexes
        if topLeft in self.__indexMap:
            self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(topLeft))
    
    def on_sourceModel_rowsInserted(self, parent, start, end):
        for i in xrange(start, end + 1):
            index = self.__sourceModel.index(i, 0, parent)
            if self.filterAcceptsRow(i, parent):
                position = bisect_key(self.__indexMap, index, lambda index: self.comparableValue(index))
                self.beginInsertRows(QtCore.QModelIndex(), position, position)
                self.__indexMap.insert(position, index)
                self.endInsertRows()
    
    def on_sourceModel_rowsAboutToBeRemoved(self, parent, start, end):
        #Remove indexes
        for i in xrange(start, end + 1):
            sIndex = self.sourceModel().index(i, 0, parent)
            if sIndex in self.__indexMap:
                self.beginRemoveRows(QtCore.QModelIndex(), self.__indexMap.index(sIndex), self.__indexMap.index(sIndex))
                self.__indexMap.remove(sIndex)
                self.endRemoveRows()

    def on_sourceModel_layoutChanged(self):
        print "cambio el layout"