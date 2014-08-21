#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
from bisect import bisect

from prymatex.qt import QtCore, QtGui

from prymatex.utils import text
from prymatex.utils.lists import bisect_key
from prymatex.models.selectable import selectableModelFactory
from prymatex.models.support import BundleItemTreeNode

#=========================================================
# Bookmark
#=========================================================
class BookmarkListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.bookmarks = []
        self.icon_bookmark = editor.resources().get_icon('bookmarks')
        # Connect
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)

    # -------- Signals
    def on_editor_blocksRemoved(self):
        self.layoutChanged.emit()

    def on_document_contentsChange(self, position, removed, added):
        pass
        
    # --------- List Model api
    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.bookmarks):
            return self.createIndex(row, column, self.bookmarks[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.bookmarks)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        cursor = self.bookmarks[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            block =  cursor.block()
            return "L%d, C%d - %s" % (block.blockNumber() + 1,
                cursor.columnNumber(), cursor.hasSelection() and cursor.selectedText() or block.text().strip())
        elif role == QtCore.Qt.DecorationRole:
            return self.icon_bookmark

    # ----------- Public api
    def bookmark(self, row):
        return self.bookmarks[row]

    def lineNumbers(self):
        return [cursor.block().lineCount() for cursor in self.bookmarks]

    def toggleBookmark(self, cursor):
        if cursor in self.bookmarks:
            index = self.bookmarks.index(cursor)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.bookmarks.remove(cursor)
            self.endRemoveRows()
        else:
            position = bisect_key(self.bookmarks, cursor, lambda cursor: cursor.position())
            self.beginInsertRows(QtCore.QModelIndex(), position, position)
            self.bookmarks.insert(position, cursor)
            self.endInsertRows()

    def removeAllBookmarks(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.bookmarks))
        self.bookmarks = []
        self.endRemoveRows()
    
    def nextBookmark(self, cursor):
        if self.bookmarks:
            position = bisect_key(self.bookmarks, cursor, lambda cursor: cursor.position()) % len(self.bookmarks)
            return self.bookmarks[position]

    def previousBookmark(self, cursor):
        if self.bookmarks:
            position = bisect_key(self.bookmarks, cursor, lambda cursor: cursor.position()) % len(self.bookmarks)
            return self.bookmarks[position - (cursor in self.bookmarks and 2 or 1)]

    def bookmarksCount(self, block):
        return len([c for c in self.bookmarks if c.block() == block])

#=========================================================
# Bookmark Selectable Model
#=========================================================  
def bookmarkSelectableModelFactory(editor):
    # Data function
    def bookmarkData():
        return [dict(bookmark=editor.bookmarkListModel.bookmark(row),
                display=editor.bookmarkListModel.data(editor.bookmarkListModel.index(row)),
                image=editor.resources().get_icon('bookmarks')) 
            for row in range(len(editor.bookmarkListModel.bookmarks))]

    return selectableModelFactory(editor, bookmarkData, 
        filterFunction = lambda text, item: item["display"].find(text) != -1)

#=========================================================
# Symbol
#=========================================================
class SymbolListModel(QtCore.QAbstractListModel): 
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.symbols = []
        self.icons = {
		"class": editor.resources().get_icon("symbol-class"),
		"block": editor.resources().get_icon("symbol-block"),
		"context": editor.resources().get_icon("symbol-context"),
		"function": editor.resources().get_icon("symbol-function"),
		"typedef": editor.resources().get_icon("symbol-typedef"),
		"variable": editor.resources().get_icon("symbol-variable")
	    }

        self.editor.registerBlockUserDataHandler(self)

        #Connects
        self.editor.blocksRemoved.connect(self.on_editor_blocksRemoved)
        self.editor.aboutToHighlightChange.connect(self.on_editor_aboutToHighlightChange)
        
    # -------------- Block User Data Handler Methods
    def contributeToBlockUserData(self, userData):
        userData.symbol = None

    def processBlockUserData(self, text, cursor, block, userData):
        symbol = None
        settings = self.editor.preferenceSettings(cursor)
        if settings.showInSymbolList:
            symbol = settings.transformSymbol(text)
        
        if userData.symbol != symbol:
            userData.symbol = symbol
            if cursor in self.symbols:
                index = self.symbols.index(cursor)
                if symbol is None:
                    self.beginRemoveRows(QtCore.QModelIndex(), index, index)
                    self.symbols.remove(cursor)
                    self.endRemoveRows()
                else:
                    self.dataChanged.emit(self.index(index), self.index(index))
            else:
                position = bisect_key(self.symbols, cursor, lambda cursor: cursor.position())
                self.beginInsertRows(QtCore.QModelIndex(), position, position)
                self.symbols.insert(position, cursor)
                self.endInsertRows()

    # ----------- Signals
    def on_editor_blocksRemoved(self):
        def validSymbolBlock(cursor):
            return bool(self.editor.blockUserData(cursor.block()).symbol)
        self.symbols = list(filter(validSymbolBlock, self.symbols))
        self.layoutChanged.emit()

    def on_editor_aboutToHighlightChange(self):
        for cursor in self.symbols:
            self.editor.blockUserData(cursor.block()).symbol = None
        self.symbols = []
        self.layoutChanged.emit()

    # ----------- Model api
    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.symbols):
            return self.createIndex(row, column, self.symbols[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.symbols)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.symbols):
            return None
        
        userData = self.editor.blockUserData(self.symbols[index.row()].block())
        if userData:
            if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
                return userData.symbol
            elif role == QtCore.Qt.DecorationRole:
                return self.icons["typedef"]

    # ------------- Public api
    def findBlockIndex(self, block):
        position = bisect_key(self.symbols, block, lambda cursor: cursor.block().position()) - 1
        if position == -1:
            position = 0
        return position
    
#=========================================================
# Bookmark Selectable Model
#=========================================================  
def symbolSelectableModelFactory(editor):
    # Data function    
    def symbolData():
        return [dict(data = block, display = editor.blockUserData(block).symbol, image = editor.resources().get_icon("symbol-class")) for block in editor.symbolListModel.blocks]

    return selectableModelFactory(editor, symbolData, 
        filterFunction = lambda text, item: item["display"].find(text) != -1)
    
#=========================================================
# Bundle Item Selectable Model
#=========================================================  
def bundleItemSelectableModelFactory(editor):
    # Data function    
    def bundleItemData():
        leftScope, rightScope = editor.scope()
        return [dict(data=bundleItem, 
                template="<table width='100%%'><tr><td>%(name)s - %(bundle)s</td><td align='right'>%(trigger)s</td></tr></table>",
                display={ 
                    "name": bundleItem.name, 
                    "bundle": bundleItem.bundle.name,
                    "trigger": bundleItem.trigger()
                },
                match=bundleItem.name.upper(),
                image=editor.resources().get_icon("bundle-item-%s" % bundleItem.type())) for bundleItem in editor.application.supportManager.getActionItemsByScope(leftScope, rightScope)]

    # Filter function        
    def bundleItemFilter(pattern, item):
        return text.fuzzy_match(pattern.upper(), item["match"])

    return selectableModelFactory(editor, bundleItemData, filterFunction=bundleItemFilter)
