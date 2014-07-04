#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string
from functools import reduce

from prymatex.qt import QtCore, QtGui

from prymatex import resources
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

    def setCompletionPrefix(self, prefix):
        self.prefix = prefix

    def setEditor(self, editor):
        self.editor = editor

    def allowOneSuggestion(self, isPrefix):
        return not isPrefix

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
    
    def insertCompletion(self, index):
        raise NotImplemented

# ===================================
# Custom completer models
# ===================================
class WordsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(WordsCompletionModel, self).__init__(**kwargs)
        self.words = []
        self.suggestions = []

    def setEditor(self, editor):
        #TODO: Que pasa si ya tiene bloques
        super(WordsCompletionModel, self).setEditor(editor)
        self.editor.registerBlockUserDataHandler(self)
        
    # -------------------- Process User Data
    def contributeToBlockUserData(self, userData):
        userData.words = set()

    def processBlockUserData(self, text, cursor, block, userData):
        words = set(
            reduce(lambda w1, w2: w1 + w2,
                map(lambda token: self.editor.RE_WORD.findall(token.chunk),
                    userData.tokens()[::-1]
                )
        , []))

        if userData.words != words:
            #Quitar las palabras anteriores
            for word in userData.words.difference(words):
                self.words.remove(word)

            #Agregar las palabras nuevas
            self.words.extend(words)

            userData.words = words

    def modelSorting(self):
        return QtGui.QCompleter.CaseSensitivelySortedModel

    def fillModel(self, callback):
        settings = self.editor.settings()
        self.suggestions = set(self.words)
        if self.prefix in self.suggestions:
            self.suggestions.remove(self.prefix)
        self.suggestions.update(settings.completions)
        if self.suggestions:
            self.suggestions = sorted(list(self.suggestions))
            callback(self)

    def isReady(self):
        return bool(self.suggestions)

    def insertCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.insertText(suggestion)
        
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
            return resources.get_icon('insert-text')


class TabTriggerItemsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(TabTriggerItemsCompletionModel, self).__init__(**kwargs)
        self.triggers = []

    def fillModel(self, callback):
        leftScope, rightScope = self.editor.scope()
        self.triggers = self.editor.application.supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)
        if self.triggers:
            callback(self)

    def allowOneSuggestion(self, isPrefix):
        return True
        
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

    def isReady(self):
        return bool(self.triggers)

    def insertCompletion(self, index):
        trigger = self.triggers[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.removeSelectedText()
        self.editor.insertBundleItem(trigger)

class SuggestionsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(SuggestionsCompletionModel, self).__init__(**kwargs)
        self.suggestions = []
        self.completionCallback = None

    def setSuggestions(self, suggestions):
        self.suggestions = suggestions
        def callback(suggestion):
            currentWord, start, end = self.editor.currentWord()
            cursor = self.editor.newCursorAtPosition(start, end)
            if 'display' in suggestion:
                cursor.insertText(suggestion['display'])
            elif 'title' in suggestion:
                cursor.insertText(suggestion['title'])
        self.setCompletionCallback(callback)

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
        suggestion = self.suggestion(index)
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
                return resources.get_icon(suggestion['image'])
        elif role == QtCore.Qt.ToolTipRole:
            if 'tool_tip' in suggestion:
                if 'tool_tip_format' in suggestion:
                    print(suggestion["tool_tip_format"])
                return suggestion['tool_tip']

    def fillModel(self, callback):
        pass

    def isReady(self):
        return bool(self.suggestions)

    def insertCompletion(self, index):
        self.completionCallback(self.suggestions[index.row()])

    def allowOneSuggestion(self, isPrefix):
        return self.callback is not None

# ===================================
# Completer
# ===================================
class CodeEditorCompleter(QtGui.QCompleter):
    def __init__(self, editor):
        super(CodeEditorCompleter, self).__init__(parent = editor)
        self.editor = editor
        self.startCursorPosition = None
        self.explicitLaunch = False

        # Models
        self.completionModels = [ ]

        self.completerTask = None
        
        # Popup table view
        self.setPopup(QtGui.QTableView())
        self.popup().setAlternatingRowColors(True)
        #self.popup().setWordWrap(False)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setMinimumHeight(200)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.activated[QtCore.QModelIndex].connect(self.activatedCompletion)
        self.highlighted[QtCore.QModelIndex].connect(self.highlightedCompletion)

        self.setWidget(self.editor)

    def setPalette(self, palette):
        self.popup().setPalette(palette)

    def fixPopupView(self):
        self.popup().resizeColumnsToContents()
        self.popup().resizeRowsToContents()
        width = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.model().columnCount()):
            width += self.popup().sizeHintForColumn(columnIndex)
        self.popup().setMinimumWidth(width)
    
    def pre_key_event(self, event):
        if self.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab):
                event.ignore()
                return True
            elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
                #Proximo modelo
                if self.trySetNextModel():
                    self.complete(self.editor.cursorRect())
                    self.explicitLaunch = True
                    return not self.explicitLaunch
                else:
                    self.popup().hide()
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.popup().hide()
        elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.currentWord(direction="left")
            self.explicitLaunch = True
            self.runCompleter(self.editor.cursorRect(), alreadyTyped)
        return False

    def post_key_event(self, event):
        if self.popup().isVisible():
            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()
            
            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                if not self.setCurrentRow(0) and self.trySetNextModel():
                    self.complete(self.editor.cursorRect())
                elif self.model() is None:
                    self.popup().hide()
            else:
                self.popup().hide()
        elif text.asciify(event.text()) in COMPLETER_CHARS:
            alreadyTyped, start, end = self.editor.currentWord(direction="left")
            if end - start >= self.editor.wordLengthToComplete:
                self.explicitLaunch = False
                self.runCompleter(self.editor.cursorRect(), alreadyTyped)

    def activatedCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        self.model().insertCompletion(sIndex)
        
    def highlightedCompletion(self, index):
        pass
        
    def setCurrentRow(self, index):
        if QtGui.QCompleter.setCurrentRow(self, index):
            self.popup().setCurrentIndex(self.completionModel().index(index, 0))
            isPrefix = self.completionPrefix() == self.currentCompletion()
            return not isPrefix or \
                (self.completionCount() == 1 and self.model().allowOneSuggestion(isPrefix)) or \
                self.explicitLaunch
        return False

    def setCompletionPrefix(self, prefix):
        for model in self.completionModels:
            model.setCompletionPrefix(prefix)
        QtGui.QCompleter.setCompletionPrefix(self, prefix)
    
    def setModel(self, model):
        # Esto esta bueno pero cuando cambias de modelo tenes que hacer algo mas
        #self.setModelSorting(model.modelSorting())
        #self.setCaseSensitivity(model.caseSensitivity())
        QtGui.QCompleter.setModel(self, model)

    def trySetModel(self, model):
        self.setModel(model)
        if self.setCurrentRow(0):
            self.fixPopupView()
        else:
            self.setModel(None)
        return self.model() is not None
        
    def registerModel(self, completionModel):
        self.completionModels.append(completionModel)
        completionModel.setEditor(self.editor)
    
    def unregisterModel(self, completionModel):
        self.completionModels.remove(completionModel)
        completionModel.setEditor(None)

    def trySetNextModel(self):
        current = model = self.model()
        while True:
            index = (self.completionModels.index(model) + 1) % len(self.completionModels)
            model = self.completionModels[index]
            if model.isReady() and self.trySetModel(model):
                return True
            if current == model:
                break
        return False

    def runCompleter(self, rect, prefix):
        if self.completerTask and self.completerTask.running():
            self.completerTask.cancel()
        self.setCompletionPrefix(prefix)
        self.startCursorPosition = self.editor.textCursor().position() - len(prefix)
        self.setModel(None)
        def _go(model):
            #TODO: Aca hacer magia con ponderaciones de modelos
            if self.model() is None and self.trySetModel(model):
                self.complete(rect)
        def _fill():
            for model in self.completionModels:
                yield model.fillModel(_go)
        self.completerTask = self.editor.application.schedulerManager.task(_fill())
