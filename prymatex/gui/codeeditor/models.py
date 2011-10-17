#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex import resources

#=========================================================
# Bookmarks
#=========================================================
class PMXBookmarkListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        
        self.blocks = []

    def index (self, row, column = 0, parent = None):
        if row < len(self.blocks):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount (self, parent = None):
        return len(self.blocks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        block = self.blocks[index.row()]
        userData = block.userData()
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            return userData.symbol
        elif role == QtCore.Qt.DecorationRole:
            return resources.ICONS['inserttext']

#=========================================================
# Symbols
#=========================================================
class PMXSymbolListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        
        self.blocks = []

    def index (self, row, column = 0, parent = None):
        if row < len(self.blocks):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount (self, parent = None):
        return len(self.blocks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        block = self.blocks[index.row()]
        userData = block.userData()
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            return userData.symbol
        elif role == QtCore.Qt.DecorationRole:
            return resources.ICONS['inserttext']

#=========================================================
# Completer
#=========================================================
class PMXCompleterListModel(QtCore.QAbstractListModel): 
    def __init__(self, suggestions, parent=None): 
        QtCore.QAbstractListModel.__init__(self, parent) 
        self.suggestions = suggestions 

    def index (self, row, column = 0, parent = None):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount (self, parent = None):
        return len(self.suggestions)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole, QtCore.Qt.EditRole]:
            if 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.DecorationRole:
            if 'image' in suggestion:
                return QtGui.QIcon(suggestion['image'])
            else:
                return resources.ICONS['inserttext']
        