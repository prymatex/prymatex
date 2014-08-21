#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string
from functools import reduce

from prymatex.qt import QtCore, QtGui, Qt

from prymatex.core import config
from prymatex.utils import text
from prymatex.models.support import BundleItemTreeNode

COMPLETER_CHARS = list(string.ascii_letters)

# ===================================
# Completer Base Model
# ===================================
class CompletionBaseModel(QtCore.QAbstractTableModel):
    def __init__(self, **kwargs):
        super(CompletionBaseModel, self).__init__(**kwargs)
        self.editor = None
        self.prefix = None

    def completionPrefix(self):
        return self._prefix
        
    def setCompletionPrefix(self, prefix):
        self._prefix = prefix

    def setEditor(self, editor):
        self.editor = editor

    def setCurrentRow(self, index, completion_count):
        return False
    
    def modelSorting(self):
        #QCompleter.UnsortedModel
        #QCompleter.CaseSensitivelySortedModel
        #QCompleter.CaseInsensitivelySortedModel
        return QtGui.QCompleter.UnsortedModel

    def caseSensitivity(self):
        #QtCore.Qt.CaseInsensitive
        #QtCore.Qt.CaseSensitive
        return QtCore.Qt.CaseSensitive

    def fillModel(self, callback):
        raise NotImplemented
    
    def isReady(self):
        raise NotImplemented
    
    def activatedCompletion(self, index):
        raise NotImplemented

    def highlightedCompletion(self, index):
        raise NotImplemented

# ===================================
# Custom completer models
# ===================================
class WordsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(WordsCompletionModel, self).__init__(**kwargs)
        self.words = []
        self.suggestions = []
        self.icon = QtGui.QIcon()

    def setEditor(self, editor):
        #TODO: Que pasa si ya tiene bloques
        super(WordsCompletionModel, self).setEditor(editor)
        self.editor.registerBlockUserDataHandler(self)
        self.icon = self.editor.resources().get_icon('insert-text')
        
    # -------------------- Process User Data
    def contributeToBlockUserData(self, userData):
        userData.words = set()

    def processBlockUserData(self, text, cursor, block, userData):
        userData.words = set(
            reduce(lambda w1, w2: w1 + w2,
                map(lambda token: config.RE_WORD.findall(token.chunk),
                    userData.tokens()[::-1]
                )
        , []))

    def modelSorting(self):
        return QtGui.QCompleter.CaseSensitivelySortedModel

    def fillModel(self, callback):
        # TODO Palabras mas proximas al cursor o mas utilizadas
        self.suggestions = set()
        block = self.editor.document().begin()
        while block.isValid():
            self.suggestions.update(self.editor.blockUserData(block).words)
            block = block.next()

        settings = self.editor.preferenceSettings()
        if self.prefix in self.suggestions:
            self.suggestions.remove(self.prefix)
        self.suggestions.update(settings.completions)
        if self.suggestions:
            self.suggestions = sorted(list(self.suggestions))
            callback(self)

    def isReady(self):
        return bool(self.suggestions)

    def activatedCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.insertText(suggestion)
        
    def highlightedCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        print(suggestion)

    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 1

    def rowCount(self, parent = None):
        return len(self.suggestions)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()
            
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return suggestion
        elif role == QtCore.Qt.DecorationRole:
            return self.icon
        elif role == QtCore.Qt.ToolTipRole:
            return suggestion
        elif role == QtCore.Qt.MatchRole:
            #return text.fuzzy_match(self.prefix, suggestion) and self.prefix or suggestion
            return suggestion
    
    def setCurrentRow(self, index, completion_count):
        suggestion = self.suggestions[index.row()]
        return completion_count > 1 or suggestion != self.completionPrefix()
        
class TabTriggerItemsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(TabTriggerItemsCompletionModel, self).__init__(**kwargs)
        self.triggers = []

    def fillModel(self, callback):
        leftScope, rightScope = self.editor.scope()
        self.triggers = self.editor.application().supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)
        if self.triggers:
            callback(self)
    
    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 2

    def rowCount(self, parent = None):
        return len(self.triggers)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.triggers):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.triggers[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            #Es un bundle item
            if index.column() == 0:
                return suggestion.tabTrigger
            elif index.column() == 1:
                return suggestion.name
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            return suggestion.icon()
        elif role == QtCore.Qt.ToolTipRole:
            return suggestion.name
        elif role == QtCore.Qt.MatchRole:
            return suggestion.tabTrigger

    def isReady(self):
        return bool(self.triggers)

    def activatedCompletion(self, index):
        trigger = self.triggers[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.removeSelectedText()
        self.editor.insertBundleItem(trigger, textCursor = cursor)

    def highlightedCompletion(self, index):
        trigger = self.triggers[index.row()]
        print(trigger)
        
    def setCurrentRow(self, index, completion_count):
        return completion_count > 0

class SuggestionsCompletionModel(CompletionBaseModel):
    #display The title to display in the suggestions list
    #insert Snippet to insert after selection
    #image An image name, see the :images option
    #match Typed text to filter on (defaults to display)

    def __init__(self, **kwargs):
        super(SuggestionsCompletionModel, self).__init__(**kwargs)
        self.suggestions = []
        self.completionCallback = None

    def setSuggestions(self, suggestions):
        self.suggestions = suggestions

    def setCompletionCallback(self, callback):
        self.completionCallback = callback

    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 1

    def rowCount(self, parent = None):
        return len(self.suggestions)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role == QtCore.Qt.DisplayRole:
            if 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.EditRole:
            if 'match' in suggestion:
                return suggestion['match']
            elif 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0 and 'image' in suggestion:
                return self.editor.resources().get_icon(suggestion['image'])
        elif role == QtCore.Qt.ToolTipRole:
            if 'tooltip' in suggestion:
                if 'tooltip_format' in suggestion:
                    print(suggestion["tooltip_format"])
                return suggestion['tooltip']
        elif role == QtCore.Qt.MatchRole:
            return suggestion['display']

    def fillModel(self, callback):
        pass

    def isReady(self):
        return bool(self.suggestions)

    def activatedCompletion(self, index):
        self.completionCallback(self.suggestions[index.row()])

    def highlightedCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        print(suggestion)

    def setCurrentRow(self, index, completion_count):
        suggestion = self.suggestions[index.row()]
        return suggestion.get('insert') != self.completionPrefix()

# ===================================
# Completer
# ===================================
class CodeEditorCompleter(QtGui.QCompleter):
    def __init__(self, editor):
        super(CodeEditorCompleter, self).__init__(parent = editor)
        self.editor = editor
        self.startCursorPosition = None
        self.explicit_launch = False

        # Models
        self.completionModels = [ ]

        self.completerTasks = [ ]
        
        # Role
        self.setCompletionRole(QtCore.Qt.MatchRole)
        
        # Popup table view
        self.setPopup(QtGui.QTableView())
        self.popup().setAlternatingRowColors(True)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setStretchLastSection(True)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.activated[QtCore.QModelIndex].connect(self.activatedCompletion)
        self.highlighted[QtCore.QModelIndex].connect(self.highlightedCompletion)

        self.setWidget(self.editor)

    def setPalette(self, palette):
        self.popup().setPalette(palette)
        self.popup().viewport().setPalette(palette)

    def isVisible(self):
        return self.completionMode() == QtGui.QCompleter.PopupCompletion and self.popup().isVisible()

    def hide(self):
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().hide()
        self.startCursorPosition = None

    def fixPopupView(self):
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().resizeColumnsToContents()
            self.popup().resizeRowsToContents()
            print(self.popup().width(), self.popup().height())
            width = self.popup().verticalScrollBar().sizeHint().width()
            for columnIndex in range(self.model().columnCount()):
                width += self.popup().sizeHintForColumn(columnIndex)
            self.popup().setMinimumWidth(width > 200 and width or 200)
            print(self.popup().sizeHintForRow(1), self.completionCount())
            height = self.popup().sizeHintForRow(1) * self.completionCount()
            self.popup().setMinimumHeight(height > 400 and 400 or height)
            print(self.popup().width(), self.popup().height())
            
    def pre_key_event(self, event):
        if self.isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab):
                event.ignore()
                return True
            elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
                #Proximo modelo
                if self.trySetNextModel():
                    self.complete(self.editor.cursorRect())
                    self.explicit_launch = True
                    return not self.explicit_launch
                else:
                    self.hide()
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.hide()
        elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.explicit_launch = True
            self.setCompletionPrefix(alreadyTyped)
            self.runCompleter(self.editor.cursorRect())
        return False

    def post_key_event(self, event):
        if self.isVisible():
            current_prefix = self.completionPrefix()
            maxPosition = self.startCursorPosition + len(current_prefix) + 1
            cursor = self.editor.textCursor()
            
            if not (self.startCursorPosition <= cursor.position() <= maxPosition):
                self.hide()
                return
            cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
            new_prefix = cursor.selectedText()
            if new_prefix == current_prefix:
                return
            self.setCompletionPrefix(new_prefix)
            if not self.setCurrentRow(0) and not self.trySetNextModel():
                self.hide()
                return
            self.complete(self.editor.cursorRect())
        elif text.asciify(event.text()) in COMPLETER_CHARS:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            if end - start >= self.editor.wordLengthToComplete:
                self.explicit_launch = False
                self.setCompletionPrefix(alreadyTyped)
                self.runCompleter(self.editor.cursorRect())

    def activatedCompletion(self, index):
        self.model().activatedCompletion(self.completionModel().mapToSource(index))
        
    def highlightedCompletion(self, index):
        self.model().highlightedCompletion(self.completionModel().mapToSource(index))
        
    def setCurrentRow(self, index):
        if not QtGui.QCompleter.setCurrentRow(self, index):
            return False
        cIndex = self.completionModel().index(index, 0)
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().setCurrentIndex(cIndex)
        return self.model().setCurrentRow(
            self.completionModel().mapToSource(cIndex), self.completionCount())

    def setCompletionPrefix(self, prefix):
        self.startCursorPosition = self.editor.textCursor().position() - len(prefix or "")
        for model in self.completionModels:
            model.setCompletionPrefix(prefix)
        QtGui.QCompleter.setCompletionPrefix(self, prefix)
        if self.model() is not None:
            self.fixPopupView()
    
    def setModel(self, model):
        # Esto esta bueno pero cuando cambias de modelo tenes que hacer algo mas
        #self.setModelSorting(model.modelSorting())
        #self.setCaseSensitivity(model.caseSensitivity())
        QtGui.QCompleter.setModel(self, model)

    def trySetModel(self, model):
        current_model = self.model()
        if model not in self.completionModels:
            return False
        self.setModel(model)
        if self.setCurrentRow(0):
            self.fixPopupView()
        else:
            self.setModel(current_model)
        return self.model() != current_model
        
    def registerModel(self, completionModel):
        self.completionModels.append(completionModel)
        completionModel.setEditor(self.editor)
    
    def unregisterModel(self, completionModel):
        self.completionModels.remove(completionModel)
        completionModel.setEditor(None)

    def trySetNextModel(self):
        current = model = self.model() or self.completionModels[-1]
        while True:
            index = (self.completionModels.index(model) + 1) % len(self.completionModels)
            model = self.completionModels[index]
            if model.isReady() and self.trySetModel(model):
                return True
            if current == model:
                break
        return False

    def runCompleter(self, rect, model = None):
        if self.isVisible():
            if (model is not None and self.trySetModel(model)) or self.explicit_launch:
                self.complete(rect)
        elif not self.isVisible():
            for completerTask in self.completerTasks:
                completerTask.cancel()
            self.setModel(None)
            def _go(model):
                # First win
                if self.model() is None and self.trySetModel(model):
                    self.complete(rect)
            if model is not None:
                _go(model)
            self.completerTasks = self.editor.application().schedulerManager.tasks(
                lambda model: model.fillModel(_go), self.completionModels)
