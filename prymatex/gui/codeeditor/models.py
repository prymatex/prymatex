#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
from bisect import bisect

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.utils import text as texttools
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
        self.blocks = filter(lambda block: block.userData() is not None, self.blocks)
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
        return map(lambda block: block.lineNumber(), self.blocks)

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
# Bookmark Selectable Model
#=========================================================  
def bookmarkSelectableModelFactory(editor):
    # Data function    
    def bookmarkData():
        leftScope, rightScope = editor.scope(direction = "both")
        return map(lambda block: 
            dict(display = block.text(), image = resources.getIcon('bookmarkflag')),
            editor.bookmarkListModel.blocks)

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
        startStop, settings = self.editor.findScopes(
            block = block,
            attribute = 'settings',
            scope_filter = lambda attr: attr.showInSymbolList,
            firstOnly = True)

        symbol = settings.transformSymbol(text[slice(*startStop)]) if settings else None

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
                indexes = map(lambda block: block.blockNumber(), self.blocks)
                index = bisect(indexes, block.blockNumber())
                self.beginInsertRows(QtCore.QModelIndex(), index, index)
                self.blocks.insert(index, block)
                self.endInsertRows()


    # ----------- Signals
    def on_editor_blocksRemoved(self):
        def validSymbolBlock(block):
            return block.userData() is not None and block.userData().symbol is not None
        self.blocks = filter(validSymbolBlock, self.blocks)
        self.layoutChanged.emit()


    def on_editor_aboutToHighlightChange(self):
        for block in self.blocks:
            block.userData().symbol = None
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
        userData = self.blocks[index.row()].userData()
        if userData:
            if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:
                return userData.symbol
            elif role == QtCore.Qt.DecorationRole:
                #userData.rootGroup(pos)
                return resources.getIcon("scope-root-entity")


    # ------------- Public api
    def findBlockIndex(self, block):
        indexes = map(lambda block: block.blockNumber(), self.blocks)
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
        return map(lambda block: 
            dict(data = block, display = block.userData().symbol, image = resources.getIcon("symbol-class")),
            editor.symbolListModel.blocks)

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
        self.columns = 2 if any(map(lambda s: isinstance(s, BundleItemTreeNode), suggestions)) else 1
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
                    print suggestion["tool_tip_format"]
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
        self.words = {}
        self.groups = {}
        self.editor.registerBlockUserDataHandler(self)

    def contributeToBlockUserData(self, userData):
        userData.words = []
        
    def processBlockUserData(self, text, block, userData):
        words = []
        for chunk in userData.lineChunks():
            scopeGroup = self.editor.scope(blockPosition = chunk[0][0])
            words += map(
                lambda match: ((chunk[0][0] + match.span()[0], chunk[0][0] + match.span()[1]), match.group(), scopeGroup), 
                self.editor.RE_WORD.finditer(chunk[1]))
        if userData.words != words:
            #Quitar el block de las palabras anteriores
            self.removeWordsBlock(block, filter(lambda word: word not in words, userData.words))
            
            #Agregar las palabras nuevas
            self.addWordsBlock(block, filter(lambda word: word not in userData.words, words))
            userData.words = words


    def _purge_words(self):
        """ Limpiar palabras """
        self.words = dict(filter(lambda (word, blocks): bool(blocks), self.words.iteritems()))
        self.groups = dict(map(lambda (group, words): (group, filter(lambda word: word in self.words, words)), self.groups.iteritems()))

    def __purge_blocks(self):
        """ Quitar bloques que no van mas """
        def validWordBlock(block):
            return block.userData() is not None and bool(block.userData().words)
        words = {}
        for word, blocks in self.words.iteritems():
            words[word] = filter(validWordBlock, blocks)
        self.words = words

    def on_editor_blocksRemoved(self):
        self.__purge_blocks()

    def addWordsBlock(self, block, words):
        for index, word, group in words:
            #Blocks
            blocks = self.words.setdefault(word, [])
            if block not in blocks:
                indexes = map(lambda block: block.blockNumber(), blocks)
                index = bisect(indexes, block.blockNumber())
                blocks.insert(index, block)
            #Words
            words = self.groups.setdefault(group, [])
            if word not in words:
                position = bisect(words, word)
                words.insert(position, word)

    def removeWordsBlock(self, block, words):
        for index, word, group in words:
            #Blocks
            if block in self.words[word]:
                self.words[word].remove(block)
            if word in self.groups[group]:
                self.groups[group].remove(word)

    def typedWords(self):
        self._purge_words()
        return self.groups.copy()

#=========================================================
# Bundle Item Selectable Model
#=========================================================  
def bundleItemSelectableModelFactory(editor):
    # Data function    
    def bundleItemData():
        leftScope, rightScope = editor.scope(direction = "both")
        return map(lambda bundleItem: 
            dict(data = bundleItem, 
                template = "<table width='100%%'><tr><td>%(name)s - %(bundle)s</td><td align='right'>%(trigger)s</td></tr></table>",
                ratio = 1.0,
                display = { 
                    "name": bundleItem.name, 
                    "bundle": bundleItem.bundle.name, 
                    "trigger": bundleItem.trigger
                }, 
                image = resources.getIcon("bundle-item-%s" % bundleItem.TYPE)),
            editor.application.supportManager.getActionItems(leftScope, rightScope))


    # Filter function        
    def bundleItemFilter(text, item):
        name = item["data"].name
        if text:
            index = 0
            slices = []
            item["ratio"] = difflib.SequenceMatcher(None, text.lower(), name.lower()).quick_ratio()
            if len(text) > 4 and item["ratio"] < 0.4: return False
            for m in texttools.subsearch(text, name, ignoreCase = True):
                slices.append(name[index:m[2]])
                slices.append("<strong>" + name[m[2]:m[3]] + "</strong>")
                index = m[3]
            slices.append(name[index:])
            name = "".join(slices)
        item["display"]["name"] = name
        return True


    # Sort function
    def bundleItemSort(leftItem, rightItem):
        return leftItem["ratio"] > rightItem["ratio"]

    return selectableModelFactory(editor, bundleItemData, filterFunction=bundleItemFilter,
            sortFunction=bundleItemSort)
