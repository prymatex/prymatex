#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string
from functools import reduce

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.utils.sourcecode import asciify
from prymatex.models.support import BundleItemTreeNode

COMPLETER_CHARS = list(string.ascii_letters) + [ chr(QtCore.Qt.Key_Period) ]

# ===================================
# Completer Base Model
# ===================================
class CompletionBaseModel(QtCore.QAbstractTableModel):
    def __init__(self, editor):
        QtCore.QAbstractTableModel.__init__(self, editor)
        self.editor = editor
        self.ready = False
        self.suggestions = []

    def isReady(self):
        return self.ready

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

    def fill(self):
        CompletionBaseModel.fill(self)
        leftSettings, rightSettings = self.editor.settings()
        suggestions = set(self.words)
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
        currentWord, start, end = self.editor.currentWord(search = False)
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.insertText(suggestion)

class TabTriggerItemsCompletionModel(CompletionBaseModel):
    def fill(self):
        CompletionBaseModel.fill(self)
        leftScope, rightScope = self.editor.scope()
        self.suggestions = self.editor.application.supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)

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
        currentWord, start, end = self.editor.currentWord(search = False)
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
        currentWord, start, end = self.editor.currentWord(search = False)
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
        self.explicitRunning = False

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

        #QCompleter::PopupCompletion	0	Current completions are displayed in a popup window.
        #QCompleter::InlineCompletion	2	Completions appear inline (as selected text).
        #QCompleter::UnfilteredPopupCompletion	1	All possible completions are displayed in a popup window with the most likely suggestion indicated as current.
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        #self.setModelSorting(QtGui.QCompleter.CaseSensitivelySortedModel)
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

        self.setWidget(self.editor)

    def fixPopupView(self):
        self.popup().resizeColumnsToContents()
        self.popup().resizeRowsToContents()
        width = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.model().columnCount()):
            width += self.popup().sizeHintForColumn(columnIndex)
        self.popup().setMinimumWidth(width)

    def close(self):
        # Clean completer
        for model in self.completionModels:
            model.clear()
        self.popup().hide()
        self.setModel(None)
        self.startCursorPosition = None
        self.explicitRunning = False

    def pre_key_event(self, event):
        if self.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab):
                event.ignore()
                return True
            elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier and self.nextModel():
                self.complete(self.editor.cursorRect())
                return self.explicitRunning
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.close()
        elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.currentWord(
                direction="left", search=False)
            self.setCompletionPrefix(alreadyTyped)
            self.complete(self.editor.cursorRect())
        return False

    def post_key_event(self, event):
        if self.popup().isVisible():
            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()

            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                if self.setCurrentRow(0) and (self.completionCount() > 1 or self.completionPrefix() != self.currentCompletion()):
                    self.fixPopupView()
                elif self.nextModel():
                    self.complete(self.editor.cursorRect())
                else:
                    self.close()
            else:
                self.close()
        elif asciify(event.text()) in COMPLETER_CHARS and not event.modifiers():
            alreadyTyped, start, end = self.editor.currentWord(
                direction="left", search=False)
            if end - start >= self.editor.wordLengthToComplete or event.key() == QtCore.Qt.Key_Period:
                self.setCompletionPrefix(alreadyTyped)
                self.complete(self.editor.cursorRect())
    
    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        self.model().insertCompletion(sIndex)
        self.close()

    def setCurrentRow(self, index):
        successful = QtGui.QCompleter.setCurrentRow(self, index)
        if successful:
            self.popup().setCurrentIndex(self.completionModel().index(index, 0))
        return successful

    def addModel(self, completionModel):
        self.completionModels.append(completionModel)

    def nextModel(self):
        currentModel = self.model() or self.completionModels[-1]
        index = self.completionModels.index(currentModel)
        while True:
            index = (index + 1) % len(self.completionModels)
            model = self.completionModels[index]
            if not model.isReady():
                model.fill()
            self.setModel(model)
            if self.setCurrentRow(0) and (self.completionCount() > 1 or self.completionPrefix() != self.currentCompletion()):
                return True
            elif model == currentModel:
                return False

    def complete(self, rect, explicit = None):
        self.explicitRunning = explicit is not None and explicit or self.explicitRunning
        if self.model() or self.nextModel():
            self.fixPopupView()
            self.startCursorPosition = self.editor.textCursor().position() - len(self.completionPrefix())
            return QtGui.QCompleter.complete(self, rect)
