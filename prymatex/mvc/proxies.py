#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

def bisect(elements, element, function):
    if not elements:
        return 0
    else:
        index = len(elements) / 2
        comp = function(elements[index], element)
        if comp > 0:
            index = index - 1 if index > 0 else 0
            return index + bisect(elements[:index], element, function)
        elif comp < 0:
            index = index + 1 if index < len(elements) else len(elements)
            return index + bisect(elements[index:], element, function)
        else:
            return index

class PMXFlatBaseProxyModel(QtCore.QAbstractItemModel):
    '''
        Proxy for create flat models from tree models
    '''
    def __init__(self, parent = None):
        super(PMXFlatBaseProxyModel, self).__init__(parent)
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
        self.__sourceModel.rowsRemoved.connect(self.on_sourceModel_rowsRemoved)
        self.__sourceModel.layoutChanged.connect(self.on_sourceModel_layoutChanged)
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
    
    def compareIndex(self, xindex, yindex):
        return 0
    
    def mapToSource(self, proxyIndex):
        return self.__indexMap[proxyIndex.row()]

    def mapFromSource(self, sourceIndex):
        return self.__indexMap.index(sourceIndex)
            
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

    def index(self, row, column, parent):
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
        print "cambiaron los datos", topLeft, bottomRight
    
    def on_sourceModel_rowsInserted(self, parent, start, end):
        for i in xrange(start, end + 1):
            index = self.__sourceModel.index(i, 0, parent)
            if self.filterAcceptsRow(i, parent):
                position = bisect(self.__indexMap, index, lambda xindex, yindex: self.compareIndex(xindex, yindex))
                self.__indexMap.insert(position, index)
    
    def on_sourceModel_rowsRemoved(self, parent, start, end):
        #Remove indexes
        self.__indexMap = filter(lambda index: index.parent() != parent or index.row() not in range(start, end + 1), self.__indexMap)

    def on_sourceModel_layoutChanged(self):
        print "cambio el layout"
    