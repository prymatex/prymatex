#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources

#=========================================================
# Mixin for selector dialog
#=========================================================
class SelectableModelMixin(object):
    def mapToSourceRow(self, index):
        pass

    def setFilterRegExp(self, regexp):
        pass


#=========================================================
# Selectable Model
#=========================================================
class SelectableModel(QtCore.QAbstractTableModel):
    """ data
        [({row1}, {row2} ... {rowN}), ....]
    """
    def __init__(self, data, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.data = data

    def itemRow(self, index):
        if index.isValid():
            return self.data[index.row()]

    def index(self, row, column, parent = None):
        return self.createIndex(row, column, self.data[row][column])
    
    def rowCount (self, parent = None):
        return len(self.data)
        
    def columnCount(self, parent):
        return self.data and len(self.data[0]) or 0

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.data[index.row()][index.column()]
        
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return item.get('title')
        elif role == QtCore.Qt.DecorationRole:
            return item.get('image') or item.get('icon')

class SelectableProxyModel(QtGui.QSortFilterProxyModel, SelectableModelMixin):
    def mapToSourceRow(self, index):
        return self.sourceModel().itemRow(self.mapToSource(index))

