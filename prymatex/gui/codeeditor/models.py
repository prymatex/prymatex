#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
from bisect import bisect

from prymatex.qt import QtCore, QtGui

from prymatex.core import constants

from prymatex.utils import text
from prymatex.utils.lists import bisect_key
from prymatex.models.selectable import selectableModelFactory
from prymatex.models.support import BundleItemTreeNode

#=========================================================
# Folding
#=========================================================
class FoldingListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        super(FoldingListModel, self).__init__(parent=editor)
        self.editor = editor
        self.foldings = []
        self.flags = []
        self.folded = []
        
        #Connects
        self.editor.highlighter().changed.connect(
            self.on_highlighter_changed
        )
        self.editor.highlighter().aboutToChange.connect(
            self.on_highlighter_aboutToChange
        )
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
                cursor.positionInBlock(), cursor.hasSelection() and cursor.selectedText() or block.text().strip())
        elif role == QtCore.Qt.DecorationRole:
            return self.foldingellipsisImage

    # --------------- Signals   
    def on_highlighter_changed(self, indexes):
        position = self.editor.document().findBlockByNumber(indexes[0]).position()
        remove = [ folding_cursor 
            for folding_cursor in self.foldings \
            if folding_cursor.position() == position ]
        for folding_cursor in remove:
            self._remove_folding_cursor(folding_cursor)
        for index in indexes:
            block = self.editor.document().findBlockByNumber(index)
            self._add_folding(block)

    def on_highlighter_aboutToChange(self):
        self.foldings = []
        self.flags = []
        self.layoutChanged.emit()
        
    def _add_folding(self, block):
        folding_cursor = self.editor.newCursorAtPosition(block.position())
        self.editor.preferenceSettings(folding_cursor).folding(block.text())
        flag = self.editor.preferenceSettings(folding_cursor).folding(block.text())
        if flag != constants.FOLDING_NONE:
            if folding_cursor in self.foldings:
                index = self.foldings.index(folding_cursor)
                self.flags[index] = flag
                self.dataChanged.emit(self.index(index), self.index(index))
            else:
                self._add_folding_cursor(folding_cursor, flag)

    def _add_folding_cursor(self, folding_cursor, flag):
        index = bisect(self.foldings, folding_cursor)
        self.beginInsertRows(QtCore.QModelIndex(), index, index)
        self.foldings.insert(index, folding_cursor)
        self.flags.insert(index, flag)
        self.endInsertRows()

    def _remove_folding_cursor(self, folding_cursor):
        index = self.foldings.index(folding_cursor)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.foldings.remove(folding_cursor)
        self.flags.pop(index)
        self.endRemoveRows()

    # ----------- Public api
    def isFoldingMarker(self, cursor):
        return cursor in self.foldings

    def isFoldingStartMarker(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] == constants.FOLDING_START

    def isFoldingStopMarker(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] == constants.FOLDING_STOP

    def isFoldingIndentedBlockStart(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] == constants.FOLDING_INDENTED_START

    def isFoldingIndentedBlockIgnore(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] == constants.FOLDING_INDENTED_IGNORE

    def isStart(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] in (constants.FOLDING_START, constants.FOLDING_INDENTED_START)

    def isStop(self, cursor):
        return self.isFoldingMarker(cursor) and \
            self.flags[self.foldings.index(cursor)] == constants.FOLDING_STOP

    def isFolded(self, cursor):
        return any((folded[0] == cursor for folded in self.folded))

    def isVisible(self, cursor):
        return not any((start < cursor <= stop for start, stop in self.folded))
        
    def fold(self, start, stop):
        if self.isFolded(start):
            self.unfold(start)
        if not self.isFoldingMarker(start):
            self._add_folding_cursor(start, constants.FOLDING_START)
        self.folded.append((start, stop))
        block = startBlock = start.block()
        while block.isValid():
            # Solo queda visible el primero para marcar el folding
            block.setVisible(block == startBlock)
            if block == stop.block():
                break
            block = block.next()
        self.editor.document().markContentsDirty(
            startBlock.position(), stop.block().position()
        )
    
    def unfold(self, cursor):
        if not self.isFolded(cursor):
            return
        cursors = [ folded for folded in self.folded if folded[0] == cursor ]
        if cursors:
            self.folded.remove(cursors[0])
            # Go!
            start, stop = cursors[0]
            startBlock, endBlock = start.block(), stop.block()
            block = startBlock
            while block.isValid():
                block.setVisible(self.isVisible(
                    self.editor.newCursorAtPosition(block.position())
                ))
                if block == endBlock:
                    break
                block = block.next()

            self.editor.document().markContentsDirty(
                startBlock.position(), endBlock.position()
            )
            settings = self.editor.preferenceSettings(start)
            flag = settings.folding(startBlock.text())
            if flag == constants.FOLDING_NONE:
                self._remove_folding_cursor(start)

    def unfoldall(self):
        # Remove all folded
        self.folded = []
        # Clean custom folding
        remove = [ cursor for cursor in self.foldings \
            if self.editor.preferenceSettings(cursor).folding(cursor.block().text()) == constants.FOLDING_NONE
        ]
        for cursor in remove:
            self._remove_folding_cursor(cursor)

        # Make all visible
        block = self.editor.document().begin()
        while block.isValid():
            block.setVisible(True)
            block = block.next()
        
        self.editor.document().markContentsDirty(
            0, self.editor.document().characterCount()
        )        

#=========================================================
# Bookmark
#=========================================================
class BookmarkListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        QtCore.QAbstractListModel.__init__(self, editor)
        self.editor = editor
        self.bookmarks = []
        
        # Images
        self.icon_bookmark = editor.resources().get_icon('bookmark')

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
                cursor.positionInBlock(), cursor.hasSelection() and cursor.selectedText() or block.text().strip())
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

# https://github.com/textmate/textmate/blob/master/Applications/TextMate/about/Changes.md#2014-10-15-v20-alpha9575
class MarkListModel(QtCore.QAbstractListModel):
    def __init__(self, editor):
        super(QtCore.QAbstractListModel, self).__init__(editor)
        self.editor = editor
        self.icons = {
            "bookmark": editor.resources().get_icon("bookmark"),
            "error": editor.resources().get_icon("error"),
            "warning": editor.resources().get_icon("warning"),
            "search": editor.resources().get_icon("search")
        }
    
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
        #Connects
        self.editor.highlighter().changed.connect(
            self.on_highlighter_changed
        )
        self.editor.highlighter().aboutToChange.connect(
            self.on_highlighter_aboutToChange
        )
     
    # --------------- Signals   
    def on_highlighter_changed(self, indexes):
        position = self.editor.document().findBlockByNumber(indexes[0]).position()
        remove = [ symbol_cursor 
            for symbol_cursor in self.symbols \
            if symbol_cursor.position() == position ]
        for symbol_cursor in remove:
            index = self.symbols.index(symbol_cursor)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.symbols.remove(symbol_cursor)
            self.endRemoveRows()
        for index in indexes:
            block = self.editor.document().findBlockByNumber(index)
            self._add_symbol(block)

    def on_highlighter_aboutToChange(self):
        self.symbols = []
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
            leftScope, rightScope = self.editor.scope(symbol_cursor)
            return self.icons.get(rightScope.root_group()[:2])

    # ------------- Public api
    def symbolCursor(self, index):
        if not index.isValid() or index.row() >= len(self.symbols):
            return QtGui.QTextCursor()
        return index.internalPointer()

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
