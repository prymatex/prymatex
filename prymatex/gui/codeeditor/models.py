#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
from bisect import bisect

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.utils import sourcecode
from prymatex.models.selectable import selectableModelFactory
from prymatex.models.support import BundleItemTreeNode

#=========================================================
# Bookmark
#=========================================================
class BookmarkListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor): 
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.blocks = []
        # Connect
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)

    def __contains__(self, block):
        return block in self.blocks

    # -------- Signals
    def on_editor_blocksRemoved(self):
        # FIXME: Nunca es None el userdata
        #self.blocks = [ block for block in self.blocks if self.editor.blockUserData(block) is not None ]
        self.layoutChanged.emit()

    def on_document_contentsChange(self, position, removed, added):
        pass
        
    # --------- List Model api
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
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return "%d - %s" % (block.blockNumber() + 1, block.text().strip())
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon('bookmarkflag')

    # ----------- Public api
    def lineNumbers(self):
        return [block.lineNumber() for block in self.blocks]

    def toggleBookmark(self, block):
        try:
            index = self.blocks.index(block)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.blocks.remove(block)
            self.endRemoveRows()
        except ValueError:
            indexes = [block.blockNumber() for block in self.blocks]
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
        indexes = [block.blockNumber() for block in self.blocks]
        index = bisect(indexes, block.blockNumber())
        if index == len(self.blocks):
            index = 0
        return self.blocks[index]

    def previousBookmark(self, block):
        if not len(self.blocks): return None
        indexes = [block.blockNumber() for block in self.blocks]
        index = bisect(indexes, block.blockNumber()) if block not in self.blocks else bisect(indexes, block.blockNumber() - 1)
        if index == 0:
            index = len(self.blocks)
        return self.blocks[index - 1]

#=========================================================
# Bookmark Selectable Model
#=========================================================  
def bookmarkSelectableModelFactory(editor):
    # Data function    
    def bookmarkData():
        return [dict(display = block.text(), image = resources.getIcon('bookmarkflag')) 
            for block in editor.bookmarkListModel.blocks]

    return selectableModelFactory(editor, bookmarkData, 
        filterFunction = lambda text, item: item["display"].find(text) != -1)


#=========================================================
# Symbol
#=========================================================
class SymbolListModel(QtCore.QAbstractListModel): 
    ICONS = {
        "class": resources.getIcon("symbol-class"),
        "block": resources.getIcon("symbol-block"),
        "context": resources.getIcon("symbol-context"),
        "function": resources.getIcon("symbol-function"),
        "typedef": resources.getIcon("symbol-typedef"),
        "variable": resources.getIcon("symbol-variable")
    }
    def __init__(self, editor): 
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.blocks = []
        self.editor.registerBlockUserDataHandler(self)
        #Connects
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)
        self.editor.aboutToHighlightChange.connect(self.on_editor_aboutToHighlightChange)
        
    # -------------- Block User Data Handler Methods
    def contributeToBlockUserData(self, userData):
        userData.symbol = None

    def processBlockUserData(self, text, block, userData):
        token, scope = self.editor.findScopes(
            block = block,
            scope_filter = lambda scope: scope.settings.showInSymbolList,
            firstOnly = True)
        
        symbol = scope.settings.transformSymbol(text[token.start:token.end]) if scope else None
        
        if userData.symbol != symbol:
            userData.symbol = symbol
            if block in self.blocks:
                index = self.blocks.index(block)
                if symbol is None:
                    self.beginRemoveRows(QtCore.QModelIndex(), index, index)
                    self.blocks.remove(block)
                    self.endRemoveRows()
                else:
                    self.dataChanged.emit(self.index(index), self.index(index))
            else:
                indexes = [ b.blockNumber() for b in self.blocks ]
                index = bisect(indexes, block.blockNumber())
                self.beginInsertRows(QtCore.QModelIndex(), index, index)
                self.blocks.insert(index, block)
                self.endInsertRows()

    # ----------- Signals
    def on_editor_blocksRemoved(self):
        def validSymbolBlock(block):
            return bool(self.editor.blockUserData(block).symbol)
        self.blocks = list(filter(validSymbolBlock, self.blocks))
        self.layoutChanged.emit()

    def on_editor_aboutToHighlightChange(self):
        for block in self.blocks:
            self.editor.blockUserData(block).symbol = None
        self.blocks = []
        self.layoutChanged.emit()

    # ----------- Model api
    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.blocks):
            return self.createIndex(row, column, self.blocks[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.blocks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.blocks):
            return None
        
        userData = self.editor.blockUserData(self.blocks[index.row()])
        if userData:
            if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
                return userData.symbol
            elif role == QtCore.Qt.DecorationRole:
                #userData.rootGroup(pos)
                return resources.getIcon("scope-root-entity")


    # ------------- Public api
    def findBlockIndex(self, block):
        indexes = [b.blockNumber() for b in self.blocks]
        blockIndex = bisect(indexes, block.blockNumber()) - 1
        if blockIndex == -1:
            blockIndex = 0
        return blockIndex

#=========================================================
# Bookmark Selectable Model
#=========================================================  
def symbolSelectableModelFactory(editor):
    # Data function    
    def symbolData():
        return [dict(data = block, display = editor.blockUserData(block).symbol, image = resources.getIcon("symbol-class")) for block in editor.symbolListModel.blocks]

    return selectableModelFactory(editor, symbolData, 
        filterFunction = lambda text, item: item["display"].find(text) != -1)

#=========================================================
# Completer
#=========================================================
class PMXCompleterTableModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent): 
        QtCore.QAbstractListModel.__init__(self, parent) 
        self.columns = 1
        self.suggestions = []

    def setSuggestions(self, suggestions):
        self.suggestions = suggestions
        self.columns = 2 if any([isinstance(s, BundleItemTreeNode) for s in suggestions]) else 1
        self.layoutChanged.emit()

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.suggestions)

    def columnCount(self, parent = None):
        return self.columns

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if isinstance(suggestion, dict) and index.column() == 0:
                if 'display' in suggestion:
                    return suggestion['display']
                elif 'title' in suggestion:
                    return suggestion['title']
            elif isinstance(suggestion, BundleItemTreeNode):
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
                elif isinstance(suggestion, BundleItemTreeNode):
                    return suggestion.icon
                else:
                    return resources.getIcon('inserttext')
        elif role == QtCore.Qt.ToolTipRole:
            if isinstance(suggestion, dict) and 'tool_tip' in suggestion:
                if 'tool_tip_format' in suggestion:
                    print(suggestion["tool_tip_format"])
                return suggestion['tool_tip']
            elif isinstance(suggestion, BundleItemTreeNode):
                return suggestion.name
        elif role == QtCore.Qt.ForegroundRole:
            return QtCore.Qt.lightGray

    def getSuggestion(self, index):
        return self.suggestions[index.row()]

#=========================================================
# Word Struct for Completer
#=========================================================
class AlreadyTypedWords(object):
    def __init__(self, editor):
        self.editor = editor
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)
        self.documentWords = set()
        self.editor.registerBlockUserDataHandler(self)

    def contributeToBlockUserData(self, userData):
        userData.words = set()

    def processBlockUserData(self, text, block, userData):
        words = set()
        
        for token in userData.tokens()[::-1]:
            group = self.editor.scope(scopeHash = token.scopeHash).group or ""
            words.update([(group, word) for word in self.editor.RE_WORD.findall(token.chunk) ])
        
        # TODO: Una mejor estructura para las palabras y sus grupos
        if userData.words != words:
            #Quitar el block de las palabras anteriores
            self.documentWords.difference_update(
                userData.words.difference(words)
            )
            
            #Agregar las palabras nuevas
            self.documentWords.update(words)
            userData.words = words

    def on_editor_blocksRemoved(self):
        """ Quitar palabras que no van mas """
        # TODO: purgar
        print("purgar")
            
    def typedWords(self):
        return self.documentWords

#=========================================================
# Bundle Item Selectable Model
#=========================================================  
def bundleItemSelectableModelFactory(editor):
    # Data function    
    def bundleItemData():
        leftScope, rightScope = editor.scope(direction = "both")
        return [dict(data = bundleItem, 
                template = "<table width='100%%'><tr><td>%(name)s - %(bundle)s</td><td align='right'>%(trigger)s</td></tr></table>",
                display = { 
                    "name": bundleItem.name, 
                    "bundle": bundleItem.bundle.name,
                    "trigger": bundleItem.trigger()
                }, 
                image = resources.getIcon("bundle-item-%s" % bundleItem.TYPE)) for bundleItem in editor.application.supportManager.getActionItemsByScope(leftScope.path, rightScope.path)]

    # Filter function        
    def bundleItemFilter(text, item):
        return not text or text.lower() in item["data"].name.lower()

    return selectableModelFactory(editor, bundleItemData, filterFunction=bundleItemFilter)
