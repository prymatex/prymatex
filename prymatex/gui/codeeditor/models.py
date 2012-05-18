#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bisect import bisect

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.gui.support.models import PMXBundleTreeNode

#=========================================================
# Bookmark
#=========================================================
class PMXBookmarkListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor): 
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        #self.editor.textChanged.connect(self.on_editor_textChanged)
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)
        self.blocks = []
        
    def _purge_blocks(self):
        self.blocks = filter(lambda block: block.userData() is not None, self.blocks)
        self.layoutChanged.emit()

    def __contains__(self, block):
        return block in self.blocks
        
    def on_editor_blocksRemoved(self):
        self._purge_blocks()
        
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
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return "%d - %s" % (block.blockNumber() + 1, block.text().strip())
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
        self.logger = editor.application.getLogger('.'.join([self.__class__.__module__, self.__class__.__name__]))
        self.symbolChanged = False
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.blocks = []
        self.icons = {
            "class": resources.getIcon("bulletred"),
            "block": resources.getIcon("bulletblue"),
            "context": resources.getIcon("bulletpink"),
            "function": resources.getIcon("bulletblue"),
            "typedef": resources.getIcon("bulletyellow"),
            "variable": resources.getIcon("bulletgreen")
        }
        
    def _purge_blocks(self):
        def validSymbolBlock(block):
            return block.userData() is not None and block.userData().symbol != None
        self.blocks = filter(validSymbolBlock, self.blocks)
        
    def on_editor_textChanged(self):
        if self.symbolChanged:
            self.logger.debug("Purgar y actualizar symbols")
            self._purge_blocks()
            self.layoutChanged.emit()
            self.symbolChanged = False

    def addSymbolBlock(self, block):
        if block not in self.blocks:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)
            self.symbolChanged = True

    def removeSymbolBlock(self, block):
        if block in self.blocks:
            index = self.blocks.index(block)
            self.blocks.remove(block)
            self.symbolChanged = True

    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.blocks):
            return self.createIndex(row, column, self.blocks[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.blocks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid() or not self.blocks:
            return None
        block = self.blocks[index.row()]
        userData = block.userData()
        #TODO: Ver donde es que pasa esto de que el userData sea None
        if userData is None:
            return None
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
class PMXCompleterTableModel(QtCore.QAbstractTableModel): 
    def __init__(self, suggestions, editor): 
        QtCore.QAbstractListModel.__init__(self, editor) 
        self.suggestions = suggestions
        self.editor = editor

    def index (self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()
    
    def rowCount(self, parent = None):
        return len(self.suggestions)

    def columnCount(self, parent = None):
        return 2

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
            elif isinstance(suggestion, PMXBundleTreeNode):
                #Es un bundle item
                if index.column() == 0:
                    return suggestion.tabTrigger
                elif index.column() == 1:
                    return suggestion.name
            elif isinstance(suggestion, tuple):
                return suggestion[index.column()]
            elif index.column() == 0:
                return suggestion
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                if isinstance(suggestion, dict) and 'image' in suggestion:
                    return resources.getIcon(suggestion['image'])
                elif isinstance(suggestion, PMXBundleTreeNode):
                    return suggestion.icon
                else:
                    return resources.getIcon('inserttext')
        elif role == QtCore.Qt.ToolTipRole:
            if isinstance(suggestion, dict) and 'tooltip' in suggestion:
                return suggestion['tooltip']
            elif isinstance(suggestion, PMXBundleTreeNode):
                return suggestion.name
        elif role == QtCore.Qt.ForegroundRole:
            return QtCore.Qt.lightGray

    def getSuggestion(self, index):
        return self.suggestions[index.row()]

#=========================================================
# Word Struct for Completer
#=========================================================
class PMXAlreadyTypedWords(object):
    def __init__(self, editor):
        self.editor = editor
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)
        self.words = {}

    def _purge_words(self):
        self.words = dict(filter(lambda (word, blocks): bool(blocks), self.words.iteritems()))

    def _purge_blocks(self):
        def validWordBlock(block):
            return block.userData() is not None and bool(block.userData().words)
        words = {}
        for word, blocks in self.words.iteritems():
            words[word] = filter(validWordBlock, blocks)
        self.words = words

    def on_editor_blocksRemoved(self):
        self._purge_blocks()
        
    def addWordsBlock(self, block, words):
        for word in words:
            blocks = self.words.setdefault(word, [])
            indexes = map(lambda block: block.blockNumber(), blocks)
            index = bisect(indexes, block.blockNumber())
            blocks.insert(index, block)
        
    def removeWordsBlock(self, block, words):
        for word in words:
            self.words[word].remove(block)
        
    def typedWords(self, block = None):
        #Purge words
        self.words = dict(filter(lambda (word, blocks): bool(blocks), self.words.iteritems()))
        return self.words.keys()