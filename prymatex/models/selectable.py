#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import collections

from prymatex import resources
from prymatex.qt import QtCore, QtGui

#=========================================================
# Mixin for selector dialog
#=========================================================
class SelectableModelMixin(object):
    def initialize(self, selector):
        self.selector = selector
        
        
    def item(self, index):
        pass


    # ------------- Sort
    def isSortable(self):
        return False


    # ------------- Filter
    def isFilterable(self):
        return False


    def setFilterString(self, string):
        pass


    def filterString(self):
        pass

    
    
#=========================================================
# Selectable Model
#=========================================================
class SelectableModel(QtCore.QAbstractListModel, SelectableModelMixin):
    DEFALUT_TEMPLATE = "%s"
    def __init__(self, dataFunction, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__dataFunction = dataFunction
        

    def initialize(self, selector):
        self.data = self.__dataFunction()


    def item(self, index):
        if isinstance(index, QtCore.QModelIndex) and index.isValid():
            return self.data[index.row()]
        if isinstance(index, int) and index < len(self.data):
            return self.data[index]


    def rowCount (self, parent = None):
        return len(self.data)
    
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.data[index.row()]
        
        if role in [ QtCore.Qt.DisplayRole ]:
            display = item.get('display')
            if isinstance(display, dict):
                template = item.get('template') or self.DEFALUT_TEMPLATE
                return template % display
            else:
                return display
        elif role == QtCore.Qt.DecorationRole:
            return item.get('image') or item.get('icon')
        elif role == QtCore.Qt.ToolTipRole and 'tooltip' in item:
            return item['tooltip']

class SelectableProxyModel(QtGui.QSortFilterProxyModel, SelectableModelMixin):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__filterFunction = None
        self.__sortFunction = None
        self.__filterString = ""


    def initialize(self, selector):
        self.sourceModel().initialize(selector)
        self.selector = selector


    def filterAcceptsRow(self, sourceRow, sourceParent):
        if not self.__filterFunction: return True
        item = self.sourceModel().item(sourceRow)
        return self.__filterFunction(self.__filterString, item)


    def lessThan(self, left, right):
        if not self.__sortFunction: return True
        leftItem = self.sourceModel().item(left)
        rightItem = self.sourceModel().item(right)
        return self.__sortFunction(leftItem, rightItem)
    
    
    def item(self, index):
        return self.sourceModel().item(self.mapToSource(index))
    
    # --------- Sort
    def setSortFunction(self, sortFunction):
        self.__sortFunction = sortFunction
        
        
    def isSortable(self):
        return self.__sortFunction is not None
        
        
    # --------- Filter
    def setFilterFunction(self, filterFunction):
        self.__filterFunction = filterFunction
        
        
    def isFilterable(self):
        return self.__filterString is not None


    def setFilterString(self, string):
        self.__filterString = string
        self.invalidate()
        #self.sort(0)


    def filterString(self):
        return self.__filterString
        
        
def selectableModelFactory(parent, dataFunction, 
    filterFunction = None, sortFunction = None):
    model = SelectableModel(dataFunction, parent = parent)
    if filterFunction or sortFunction:
        proxy = SelectableProxyModel(parent = parent)
        if filterFunction is not None:
            proxy.setFilterFunction(filterFunction)
        if sortFunction is not None:
            proxy.setSortFunction(sortFunction)
        proxy.setSourceModel(model)
        model = proxy
    return model