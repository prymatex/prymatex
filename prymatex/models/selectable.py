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
        pass
        
        
    def mapToSourceItem(self, index):
        pass


    # ------------- Filter
    def setFilterString(self, string):
        pass


    def filterString(self):
        pass

    
    
#=========================================================
# Selectable Model
#=========================================================
class SelectableModel(QtCore.QAbstractListModel):
    """ data = [{item1}, ... {itemN}]
        item = { 
            display: {} or str, 
            image: QPixmap or icon: QIcon,
            tooltip: str}
    """
    DEFALUT_TEMPLATE = "%s"
    def __init__(self, data, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.data = data

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
    def __init__(self, filterFunction, sortFunction, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__filterFunction = filterFunction
        self.__sortFunction = sortFunction
        self.__filterString = ""

    def initialize(self, selector):
        self.selector = selector

    def filterAcceptsRow(self, sourceRow, sourceParent):
        item = self.sourceModel().item(sourceRow)
        return self.__filterFunction(self.__filterString, item)

    def lessThan(self, left, right):
        leftItem = self.sourceModel().item(left)
        rightItem = self.sourceModel().item(right)
        return self.__sortFunction(leftItem, rightItem)
        
    def setFilterString(self, string):
        self.__filterString = string
        self.invalidate()
        #self.sort(0)
        
    def filterString(self):
        return self.__filterString
        
    def mapToSourceItem(self, index):
        return self.sourceModel().item(self.mapToSource(index))

def selectableModelFactory(parent, iterable, 
    filterFunction = lambda text, item: str(item).find(text) != -1,
    sortFunction = lambda leftItem, rightItem: True):
    assert isinstance(iterable, collections.Iterable)
    model = SelectableProxyModel(filterFunction, sortFunction, parent = parent)
    model.setSourceModel(SelectableModel(list(iterable)))
    return model