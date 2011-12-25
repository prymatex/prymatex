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
        self.editor = editor
        self.editor.blocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []

    def purgeBlocks(self):
        remove = filter(lambda block: block.userData() is None, self.blocks)
        if remove:
            sIndex = self.blocks.index(remove[0])
            eIndex = self.blocks.index(remove[-1])
            self.beginRemoveRows(QtCore.QModelIndex(), sIndex, eIndex)
            self.blocks = self.blocks[:sIndex] + self.blocks[eIndex + 1:]
            self.endRemoveRows()

    def __contains__(self, block):
        return block in self.blocks
        
    def on_textBlocksRemoved(self, block, length):
        self.purgeBlocks()

    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.blocks):
            return self.createIndex(row, column, self.blocks[row])
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
            return resources.getIcon('bookmarkflag')

    def toggleBookmark(self, block):
        try:
            index = self.blocks.index(block)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.blocks.remove(block)
            self.endRemoveRows()
        except ValueError:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.beginInsertRows(QtCore.QModelIndex(), index, index)
            self.blocks.insert(index, block)
            self.endInsertRows()

    def removeAllBookmarks(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.blocks))
        self.blocks = []
        self.endRemoveRows()
    
    def nextBookmark(self, block):
        if not len(self.blocks): return None
        indexes = map(lambda block: block.blockNumber(), self.blocks)
        index = bisect(indexes, block.blockNumber())
        if index == len(self.blocks):
            index = 0
        return self.blocks[index]
    
    def previousBookmark(self, block):
        if not len(self.blocks): return None
        indexes = map(lambda block: block.blockNumber(), self.blocks)
        index = bisect(indexes, block.blockNumber()) if block not in self.blocks else bisect(indexes, block.blockNumber() - 1)
        if index == 0:
            index = len(self.blocks)
        return self.blocks[index - 1]
    
#=========================================================
# Symbol
#=========================================================
class PMXSymbolListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor): 
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.editor.blocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []

    def _purge_blocks(self, startIndex = None, endIndex = None):
        remove = filter(lambda block: block.userData() is None, self.blocks[startIndex:endIndex])
        print self.blocks, remove
        if remove:
            startIndex = self.blocks.index(remove[0])
            endIndex = self.blocks.index(remove[-1])
            self.beginRemoveRows(QtCore.QModelIndex(), startIndex, endIndex)
            self.blocks = self.blocks[:startIndex] + self.blocks[endIndex + 1:]
            self.endRemoveRows()

    def addSymbolBlock(self, block):
        if block in self.blocks:
            index = self.blocks.index(block)
            self.dataChanged.emit(self.index(index), self.index(index))
        else:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.beginInsertRows(QtCore.QModelIndex(), index, index)
            self.blocks.insert(index, block)
            self.endInsertRows()
    
    def removeSymbolBlock(self, block):
        index = self.blocks.index(block)
        self._purge_blocks(startIndex = index)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.blocks.remove(block)
        self.endRemoveRows()
        
    def on_textBlocksRemoved(self, block, length):
        self._purge_blocks()
            
    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.blocks):
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
            return resources.getIcon('codefunction')
    
    def findBlockIndex(self, block):
        indexes = map(lambda block: block.blockNumber(), self.blocks)
        return bisect(indexes, block.blockNumber()) - 1
    
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

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if isinstance(suggestion, dict):
                if 'display' in suggestion:
                    return suggestion['display']
                elif 'title' in suggestion:
                    return suggestion['title']
            else:
                return suggestion
        elif role == QtCore.Qt.DecorationRole:
            if isinstance(suggestion, dict) and 'image' in suggestion:
                return resources.getIcon(suggestion['image'])
            else:
                return resources.getIcon('inserttext')
        elif role == QtCore.Qt.ToolTipRole:
            return "tooltip help"
