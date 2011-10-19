#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex import resources

#=========================================================
# Bookmark
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

    def data (self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        block = self.blocks[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            return block.text()
        elif role == QtCore.Qt.DecorationRole:
            return resources.ICONS['inserttext']
    
#=========================================================
# Symbol
#=========================================================
class PMXSymbolListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor): 
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.editor.symbolChanged.connect(self.on_symbolChanged)
        self.editor.textBlocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []

    def on_symbolChanged(self, block):
        if block in self.blocks:
            index = self.blocks.index(block)
            userData = block.userData()
            if userData.symbol is None:
                self.beginRemoveRows(QtCore.QModelIndex(), index, index)
                self.blocks.remove(block)
                self.endRemoveRows()
            else:
                self.dataChanged.emit(self.index(index), self.index(index))
        else:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.beginInsertRows(QtCore.QModelIndex(), index, index)
            self.blocks.insert(index, block)
            self.endInsertRows()
    
    def on_textBlocksRemoved(self):
        remove = filter(lambda block: block.userData() is None, self.blocks)
        print remove
        if remove:
            sIndex = self.blocks.index(remove[0])
            eIndex = self.blocks.index(remove[-1])
            self.beginRemoveRows(QtCore.QModelIndex(), sIndex, eIndex)
            self.blocks = self.blocks[:sIndex] + self.blocks[eIndex + 1:]
            self.endRemoveRows()
            
    def index (self, row, column = 0, parent = None):
        if row < len(self.blocks):
            return self.createIndex(row, column, self.blocks[row])
        else:
            return QtCore.QModelIndex()

    def rowCount (self, parent = None):
        return len(self.blocks)

    def data (self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        block = self.blocks[index.row()]
        userData = block.userData()
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            return userData.symbol
        elif role == QtCore.Qt.DecorationRole:
            return resources.ICONS['codefunction']

#=========================================================
# Completer
#=========================================================
class PMXCompleterListModel(QtCore.QAbstractListModel): 
    def __init__(self, suggestions, editor): 
        QtCore.QAbstractListModel.__init__(self, editor) 
        self.suggestions = suggestions 

    def index (self, row, column = 0, parent = None):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount (self, parent = None):
        return len(self.suggestions)

    def data (self, index, role = QtCore.Qt.DisplayRole):
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