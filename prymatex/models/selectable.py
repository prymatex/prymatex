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
    """ data
        [({row1}, {row2} ... {rowN}), ....]
    """
    def __init__(self, data, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.data = data

    def item(self, index):
        if index.isValid():
            return self.data[index.row()]

    def rowCount (self, parent = None):
        return len(self.data)
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.data[index.row()]

        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return item.get('title')
        elif role == QtCore.Qt.DecorationRole:
            return item.get('image') or item.get('icon')

class SelectableProxyModel(QtGui.QSortFilterProxyModel, SelectableModelMixin):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__filterString = ""

    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True

    def setFilterString(self, string):
        self.__filterString = string
        self.invalidateFilter()
        
    def filterString(self):
        return self.__filterString
        
    def mapToSourceItem(self, index):
        return self.sourceModel().item(self.mapToSource(index))
