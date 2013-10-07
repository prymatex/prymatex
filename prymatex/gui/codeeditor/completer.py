#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.models.support import BundleItemTreeNode

# Models
class AlreadyTypedWordsModel(QtCore.QAbstractTableModel): 
    def __init__(self, editor): 
        QtCore.QAbstractTableModel.__init__(self, editor)
        self.editor = editor
        self.editor.registerBlockUserDataHandler(self)

        self.suggestions = []
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

    def buildSuggestions(self):
        self.suggestions = list(set(self.words))

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent = None):
        return len(self.suggestions)
    
    def columnCount(self, parent = None):
        return 1

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return suggestion
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon("scope-root-none")

    def getSuggestion(self, index):
        return self.suggestions[index.row()]

# Completer
class CodeEditorCompleter(QtGui.QCompleter):
    def __init__(self, editor):
        QtGui.QCompleter.__init__(self, editor)
        self.editor = editor

        # Popup table view
        self.setPopup(QtGui.QTableView())
        # Models
        self.alreadyTypedWordsModel = AlreadyTypedWordsModel(self.editor)
        
        # Config popup table view
        self.popup().setAlternatingRowColors(True)
        self.popup().setWordWrap(False)
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
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)
        
        self.setWidget(self.editor)
        
    def fixPopupViewSize(self):
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
                self.popup().hide()
                return True
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.popup().hide()
        return False
        
    def post_key_event(self, event):
        if self.popup().isVisible():
            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()
            
            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                prefix = cursor.selectedText()
                if (event.text() and prefix == self.currentCompletion()) or self.completionCount() == 0:
                    self.popup().hide()
                else:
                    self.setCompletionPrefix(prefix)
            else:
                self.popup().hide()
        elif event.text():
            currentAlreadyTyped, start, end = self.editor.currentWord(direction="left", search=False)
            if (end - start >= self.editor.wordLengthToComplete and event.modifiers() != QtCore.Qt.ControlModifier) or \
            event.key() == QtCore.Qt.Key_Period or \
            (event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier):
                self.complete(self.editor.cursorRect(), currentAlreadyTyped)

    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        suggestion = self.model().getSuggestion(sIndex)
        _, start, end = self.editor.currentWord(search = False)
        cursor = self.editor.newCursorAtPosition(start, end)
        if isinstance(suggestion, tuple):
            cursor.insertText(suggestion[1])
        elif isinstance(suggestion, dict):
            if 'display' in suggestion:
                cursor.insertText(suggestion['display'])
            elif 'title' in suggestion:
                cursor.insertText(suggestion['title'])
        elif isinstance(suggestion, BundleItemTreeNode):
            cursor.removeSelectedText()
            self.editor.insertBundleItem(suggestion)
        else:
            cursor.insertText(suggestion)
    
    def setCompletionPrefix(self, prefix):
        QtGui.QCompleter.setCompletionPrefix(self, prefix)
        self.fixPopupViewSize()
        self.popup().setCurrentIndex(self.completionModel().index(0, 0))

    def setModel(self, model):
        model.buildSuggestions()
        QtGui.QCompleter.setModel(self, model)

    def complete(self, rect, currentAlreadyTyped):
        self.setModel(self.alreadyTypedWordsModel)
        self.startCursorPosition = self.editor.textCursor().position() - len(currentAlreadyTyped)
        self.setCompletionPrefix(currentAlreadyTyped)
        if currentAlreadyTyped != self.currentCompletion() and self.completionCount():
            QtGui.QCompleter.complete(self, rect)
