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
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.blocks = []
        
    def _purge_blocks(self):
        self.blocks = filter(lambda block: block.userData() is not None, self.blocks)
        self.layoutChanged.emit()

    def __contains__(self, block):
        return block in self.blocks
        
    def on_editor_textChanged(self):
        #TODO: solo hacer las acciones si tengo nuevo estado de folding motivado por un remove o un add
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
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.blocks = []
        self.icons = {
            "class": resources.getIcon("code-class"),
            "block": resources.getIcon("code-block"),
            "context": resources.getIcon("code-context"),
            "function": resources.getIcon("code-function"),
            "typedef": resources.getIcon("code-typedef"),
            "variable": resources.getIcon("code-variable")
        }

    def on_editor_textChanged(self):
        #TODO: solo hacer las acciones si tengo nuevo estado de folding motivado por un remove o un add
        self._purge_blocks()

    def _purge_blocks(self):
        def validSymbolBlock(block):
            return block.userData() is not None and block.userData().symbol != None
        self.blocks = filter(validSymbolBlock, self.blocks)
        self.layoutChanged.emit()

    def addSymbolBlock(self, block):
        if block not in self.blocks:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)

    def removeSymbolBlock(self, block):
        if block in self.blocks:
            index = self.blocks.index(block)
            self.blocks.remove(block)

    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.blocks):
            return self.createIndex(row, column, self.blocks[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.blocks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        block = self.blocks[index.row()]
        userData = block.userData()
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            return userData.symbol
        elif role == QtCore.Qt.DecorationRole:
            for name, icon in self.icons.iteritems():
                if userData.isWordInScopes(name):
                    return icon
            return self.icons["typedef"]
    
    def findBlockIndex(self, block):
        self._purge_blocks()
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