#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
from bisect import bisect
from collections import OrderedDict

from prymatex.qt import QtCore, QtGui

from prymatex.utils import text
from prymatex.utils.lists import bisect_key
from prymatex.models.selectable import selectableModelFactory
from prymatex.models.support import BundleItemTreeNode

#=========================================================
# Folding
#=========================================================
class FoldingTreeModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        super(FoldingTreeModel, self).__init__(parent=editor)
        self.editor = editor
        self.foldings = []
        self.flags = []
        
        self.editor.document().contentsChange.connect(self.on_document_contentsChange)

        #Connects
        self.editor.aboutToHighlightChange.connect(self.on_editor_aboutToHighlightChange)
        self.editor.highlightReady.connect(self.on_editor_highlightingReady)
        self.editor.highlightChanged.connect(self.on_editor_highlightChanged)

        # Images
        self.foldingellipsisImage = self.editor.resources().get_image(":/sidebar/folding-ellipsis.png")

    # --------- List Model api
    def index(self, row, column = 0, parent = None):
        if 0 <= row < len(self.foldings):
            return self.createIndex(row, column, self.foldings[row])
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.foldings)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        cursor = self.foldings[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            block = cursor.block()
            return "L%d, C%d - %s" % (block.blockNumber() + 1,
                cursor.columnNumber(), cursor.hasSelection() and cursor.selectedText() or block.text().strip())
        elif role == QtCore.Qt.DecorationRole:
            return self.foldingellipsisImage

    # --------------- Signals   
    def on_document_contentsChange(self, position, removed, added):
        block = self.editor.document().findBlock(position)
        if removed:
            remove = [ folding_cursor 
                for folding_cursor in self.foldings \
                if folding_cursor.position() == position ]
            for folding_cursor in remove:
                index = self.foldings.index(folding_cursor)
                self.beginRemoveRows(QtCore.QModelIndex(), index, index)
                self.foldings.remove(folding_cursor)
                self.flags.pop(index)
                self.endRemoveRows()
        if added:
            last = self.editor.document().findBlock(position + added)
            while True:
                self._add_folding(block)
                if block == last:
                    break
                block = block.next()

    def on_editor_aboutToHighlightChange(self):
        self.foldings = []
        self.flags = []
        self.editor.document().contentsChange.disconnect(self.on_document_contentsChange)
        self.layoutChanged.emit()
    
    def on_editor_highlightingReady(self):
        block = self.editor.document().begin()
        while block.isValid():
            self._add_folding(block)
            block = block.next()
        print(self.foldings)
        print(self.flags)

    def on_editor_highlightChanged(self):
        self.editor.document().contentsChange.connect(self.on_document_contentsChange)
        self.layoutChanged.emit()
        
    def _add_folding(self, block):
        folding_cursor = self.editor.newCursorAtPosition(block.position())
        settings = self.editor.preferenceSettings(folding_cursor)
        flag = settings.folding(block.text())
        if flag != settings.FOLDING_NONE:
            if folding_cursor in self.foldings:
                index = self.foldings.index(folding_cursor)
                self.flags[index] = flag
                self.dataChanged.emit(self.index(index), self.index(index))
            else:
                index = bisect(self.foldings, folding_cursor)
                self.beginInsertRows(QtCore.QModelIndex(), index, index)
                self.foldings.insert(index, folding_cursor)
                self.flags.insert(index, flag)
                self.endInsertRows()
                
#=========================================================
# Bookmark
#=========================================================
class BookmarkListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.bookmarks = []
        
        # Images
        self.icon_bookmark = editor.resources().get_icon('bookmarks')

    # -------- Signals
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
            block = cursor.block()
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
            ("meta", "class"): editor.resources().get_icon("symbol-class"),
            ("meta", "block"): editor.resources().get_icon("symbol-block"),
            ("meta", "context"): editor.resources().get_icon("symbol-context"),
            ("meta", "function"): editor.resources().get_icon("symbol-function"),
            ("meta", "typedef"): editor.resources().get_icon("symbol-typedef"),
            ("meta", "variable"): editor.resources().get_icon("symbol-variable")
        }
        
        self.editor.document().contentsChange.connect(self.on_document_contentsChange)
        
        #Connects
        self.editor.aboutToHighlightChange.connect(self.on_editor_aboutToHighlightChange)
        self.editor.highlightReady.connect(self.on_editor_highlightingReady)
        self.editor.highlightChanged.connect(self.on_editor_highlightChanged)
     
    # --------------- Signals   
    def on_document_contentsChange(self, position, removed, added):
        block = self.editor.document().findBlock(position)
        if removed:
            remove = [ symbol_cursor 
                for symbol_cursor in self.symbols \
                if symbol_cursor.position() == position ]
            for symbol_cursor in remove:
                index = self.symbols.index(symbol_cursor)
                self.beginRemoveRows(QtCore.QModelIndex(), index, index)
                self.symbols.remove(symbol_cursor)
                self.endRemoveRows()
        if added:
            last = self.editor.document().findBlock(position + added)
            while True:
                self._add_symbol(block)
                if block == last:
                    break
                block = block.next()

    def on_editor_aboutToHighlightChange(self):
        self.symbols = []
        self.editor.document().contentsChange.disconnect(self.on_document_contentsChange)
        self.layoutChanged.emit()
    
    def on_editor_highlightingReady(self):
        block = self.editor.document().begin()
        while block.isValid():
            self._add_symbol(block)
            block = block.next()
    
    def on_editor_highlightChanged(self):
        self.editor.document().contentsChange.connect(self.on_document_contentsChange)
        self.layoutChanged.emit()

    def _add_symbol(self, block):
        symbol_cursor = self.editor.newCursorAtPosition(block.position())
        settings = self.editor.preferenceSettings(symbol_cursor)
        if settings.showInSymbolList:
            if symbol_cursor in self.symbols:
                index = self.symbols.index(symbol_cursor)
                self.dataChanged.emit(self.index(index), self.index(index))
            else:
                index = bisect(self.symbols, symbol_cursor)
                self.beginInsertRows(QtCore.QModelIndex(), index, index)
                self.symbols.insert(index, symbol_cursor)
                self.endInsertRows()

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
        
        symbol_cursor = self.symbols[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
            settings = self.editor.preferenceSettings(symbol_cursor)
            return settings.transformSymbol(symbol_cursor.block().text())
        elif role == QtCore.Qt.DecorationRole:
            leftScope, rightScope = self.editor.scope(symbol_cursor, auxiliary=False)
            return self.icons.get(rightScope.root_group()[:2])

    # ------------- Public api
    def findSymbolIndex(self, cursor):
        position = bisect(self.symbols, cursor) - 1
        return position > 0 and position or 0
    
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
