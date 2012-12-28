#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources

#=========================================================
# Mixin for selector dialog
#=========================================================
class SelectableModelMixin(object):
    def mapToSourceItem(self, index):
        pass

    def setFilterString(self, string):
        pass

    def filterString(self):
        pass

#=========================================================
# Selectable Model
#=========================================================
class SelectableModel(QtCore.QAbstractListModel):
    """ data = [{item1}, ... {itemN}]
        item = { display: {}, image, icon, tooltip}
    """
    DEFALUT_TEMPLATE = "%(title)s"
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
            template = item.get('template', self.DEFALUT_TEMPLATE)
            display = item.get('display', { 'title': item.get('title', '')})
            return template % display
        elif role == QtCore.Qt.DecorationRole:
            return item.get('image') or item.get('icon')
        elif role == QtCore.Qt.ToolTipRole and 'tooltip' in item:
            return item['tooltip']

class SelectableProxyModel(QtGui.QSortFilterProxyModel, SelectableModelMixin):
    def __init__(self, filterFunction, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__filterFunction = filterFunction
        self.__filterString = ""
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        item = self.sourceModel().item(sourceRow)
        return self.__filterFunction(self.__filterString, item)

    def setFilterString(self, string):
        self.__filterString = string
        self.invalidateFilter()
        
    def filterString(self):
        return self.__filterString
        
    def mapToSourceItem(self, index):
        return self.sourceModel().item(self.mapToSource(index))
