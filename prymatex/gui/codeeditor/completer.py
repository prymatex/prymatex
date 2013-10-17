#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string
from functools import reduce

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.utils.sourcecode import asciify
from prymatex.models.support import BundleItemTreeNode

COMPLETER_CHARS = list(string.ascii_letters)

# ===================================
# Completer Base Model
# ===================================
class CompletionBaseModel(QtCore.QAbstractTableModel):
    def __init__(self, editor):
        QtCore.QAbstractTableModel.__init__(self, editor)
        self.editor = editor
        self.ready = False
        self.prefix = ""
        self.suggestions = []

    def isReady(self):
        return self.ready

    def setCompletionPrefix(self, prefix):
        self.prefix = prefix

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

    def fill(self):
        self.ready = True

    def clear(self):
        self.suggestions = []
        self.ready = False
    
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

# ===================================
# Custom completer models
# ===================================
class WordsCompletionModel(CompletionBaseModel):
    def __init__(self, editor):
        CompletionBaseModel.__init__(self, editor)
        self.editor.registerBlockUserDataHandler(self)
        self.words = []

    # -------------------- Process User Data
    def contributeToBlockUserData(self, userData):
        userData.words = set()

    def processBlockUserData(self, text, block, userData):
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

    def fill(self):
        CompletionBaseModel.fill(self)
        leftSettings, rightSettings = self.editor.settings()
        suggestions = set(self.words)
        if self.prefix in suggestions:
            suggestions.remove(self.prefix)
        suggestions.update(rightSettings.completions)
        self.suggestions = sorted(list(suggestions))

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return suggestion
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon('insert-text')

    def insertCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.insertText(suggestion)

class TabTriggerItemsCompletionModel(CompletionBaseModel):
    def fill(self):
        CompletionBaseModel.fill(self)
        leftScope, rightScope = self.editor.scope()
        self.suggestions = self.editor.application.supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)

    def allowOneSuggestion(self, isPrefix):
        return True
        
    def columnCount(self, parent = None):
        return 2
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            #Es un bundle item
            if index.column() == 0:
                return suggestion.tabTrigger
            elif index.column() == 1:
                return suggestion.name
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            return suggestion.icon
        elif role == QtCore.Qt.ToolTipRole:
            return suggestion.name

    def insertCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.removeSelectedText()
        self.editor.insertBundleItem(suggestion)

class SuggestionsCompletionModel(CompletionBaseModel):
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0 and 'image' in suggestion:
                return resources.getIcon(suggestion['image'])
        elif role == QtCore.Qt.ToolTipRole:
            if 'tool_tip' in suggestion:
                if 'tool_tip_format' in suggestion:
                    print(suggestion["tool_tip_format"])
                return suggestion['tool_tip']

    def insertCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        if 'display' in suggestion:
            cursor.insertText(suggestion['display'])
        elif 'title' in suggestion:
            cursor.insertText(suggestion['title'])

# ===================================
# Completer
# ===================================
class CodeEditorCompleter(QtGui.QCompleter):
    def __init__(self, editor):
        QtGui.QCompleter.__init__(self, editor)
        self.editor = editor
        self.startCursorPosition = None
        self.explicitLaunch = False
        
        # Popup table view
        self.setPopup(QtGui.QTableView())

        # Models
        self.completionModels = [ ]

        # Config popup table view
        self.popup().setAlternatingRowColors(True)
        #self.popup().setWordWrap(False)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setMinimumHeight(200)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

        self.setWidget(self.editor)
    
    def clear(self):
        self.setModel(None)
        self.setCompletionPrefix("")
        self.startCursorPosition = None
        for model in self.completionModels:
            model.clear()

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
                self.complete(self.editor.cursorRect(), model = self.nextModel(self.model()))
                if self.explicitLaunch:
                    return self.model() is not None
                else:
                    self.explicitLaunch = True
                    return not self.explicitLaunch
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.popup().hide()
        elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.currentWord(direction="left")
            self.explicitLaunch = True
            self.complete(self.editor.cursorRect(), prefix = alreadyTyped)
        return False

    def post_key_event(self, event):
        if self.popup().isVisible():
            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()
            
            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                if not self.setCurrentRow(0):
                    self.complete(self.editor.cursorRect(), model = self.nextModel(self.model()))
                if self.model() is None:
                    self.popup().hide()
            else:
                self.popup().hide()
        elif asciify(event.text()) in COMPLETER_CHARS and not event.modifiers():
            alreadyTyped, start, end = self.editor.currentWord(direction="left")
            if end - start >= self.editor.wordLengthToComplete:
                self.explicitLaunch = False
                self.complete(self.editor.cursorRect(), prefix = alreadyTyped)

    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        self.model().insertCompletion(sIndex)
    
    def setCurrentRow(self, index):
        if QtGui.QCompleter.setCurrentRow(self, index):
            self.popup().setCurrentIndex(self.completionModel().index(index, 0))
            return self.completionCount() > 1 or \
                self.model().allowOneSuggestion(self.completionPrefix() == self.currentCompletion())
        return False

    def setCompletionPrefix(self, prefix):
        for model in self.completionModels:
            model.setCompletionPrefix(prefix)
        QtGui.QCompleter.setCompletionPrefix(self, prefix)
    
    def setModel(self, model):
        if model:
            if not model.isReady():
                model.fill()
            # Esto esta bueno pero cuando cambias de modelo tenes que hacer algo mas
            #self.setModelSorting(model.modelSorting())
            #self.setCaseSensitivity(model.caseSensitivity())
        QtGui.QCompleter.setModel(self, model)
    
    def addModel(self, completionModel):
        self.completionModels.append(completionModel)
    
    def nextModel(self, model = None):
        if model is None:
            model = self.completionModels[-1]
        return self.completionModels[
            (self.completionModels.index(model) + 1) % len(self.completionModels)]

    def ensureSuggestionsSetModel(self, model):
        doit = True
        current = model
        while doit:
            self.setModel(model)
            if self.setCurrentRow(0):
                break
            model = self.nextModel(model)
            if model == current:
                doit = False
        if not doit:
            self.setModel(None)
        return doit
    
    def complete(self, rect, model = None, prefix = None):

        # Clear
        if not self.popup().isVisible():
            self.clear()
        
        # Prefix
        if prefix is not None:
            self.setCompletionPrefix(prefix)
            self.startCursorPosition = self.editor.textCursor().position() - len(prefix)
        
        # Model
        if self.ensureSuggestionsSetModel(model or self.nextModel()):
            self.fixPopupView()
            return QtGui.QCompleter.complete(self, rect)
