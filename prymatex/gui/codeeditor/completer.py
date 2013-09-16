#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

# Models
class AlreadyTypedWordsModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent): 
        QtCore.QAbstractListModel.__init__(self, parent) 
        self.suggestions = []
        self.typedWords = set()
        self.suggestions = []
        
    def removeWords(self, words):
        self.typedWords.difference_update(words)
        
    def addWords(self, words):
        self.typedWords.update(words)

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
            return suggestion[1]
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon("scope-root-%s" % ( suggestion[0] or "none"))

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
        self.alreadyTypedWordsModel = AlreadyTypedWordsModel(self)
        self.setModel(self.alreadyTypedWordsModel)
        
        # Config popup table view
        self.popup().setAlternatingRowColors(True)
        self.popup().setWordWrap(False)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #QCompleter::PopupCompletion	0	Current completions are displayed in a popup window.
        #QCompleter::InlineCompletion	2	Completions appear inline (as selected text).
        #QCompleter::UnfilteredPopupCompletion	1	All possible completions are displayed in a popup window with the most likely suggestion indicated as current.
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

        self.currentSource = None
        self.activeSources = []
        self.completerSuggestions = {}
    
        self.editor.registerBlockUserDataHandler(self)
        self.setWidget(self.editor)

    # -------------------- Process User Data
    def contributeToBlockUserData(self, userData):
        userData.words = set()

    def processBlockUserData(self, text, block, userData):
        words = set()
        
        for token in userData.tokens()[::-1]:
            words.update([(token.group, word) for word in self.editor.RE_WORD.findall(token.chunk) ])
        
        if userData.words != words:
            #Quitar las palabras anteriores
            self.alreadyTypedWordsModel.removeWords(userData.words.difference(words))
            
            #Agregar las palabras nuevas
            self.alreadyTypedWordsModel.addWords(words)
            userData.words = words
    
    def fixPopupViewSize(self):
        self.popup().setMinimumHeight(200)
        self.popup().resizeColumnsToContents()
        width = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.completionModel().sourceModel().columnCount()):
            width += self.popup().sizeHintForColumn(columnIndex)
        self.popup().setMinimumWidth(width)
      
    def hasSource(self, source):
        return source in self.activeSources
        
    def switch(self):
        if len(self.activeSources) > 1:
            index = self.activeSources.index(self.currentSource)
            index = (index + 1) % len(self.activeSources)
            self.currentSource = self.activeSources[index]
            self.model().setSuggestions(self.completerSuggestions[self.currentSource])
            self.fixPopupViewSize()

    def setSource(self, source):
        # TODO Esto esta muy feo y es lento
        self.activeSources.append(source)
        self.currentSource = source
        self.model().setSuggestions(self.completerSuggestions[source])
        self.fixPopupViewSize()

    def setSuggestions(self, suggestions, source):
        # TODO Esto esta muy feo y es lento
        self.completerSuggestions[source] = suggestions
        self.activeSources.append(source)
        self.currentSource = source
        self.model().setSuggestions(suggestions)
        self.fixPopupViewSize()
    
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
            event.ignore()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space:
            self.editor.switchCompleter()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)

            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()

            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                self.complete(self.editor.cursorRect())

    def onlyOneSameSuggestion(self):
        cursor = self.editor.textCursor()
        if not self.completionModel().hasIndex(1, 0):
            sIndex = self.completionModel().mapToSource(self.completionModel().index(0, 0))
            suggestion = self.model().data(sIndex)
            return suggestion == self.completionPrefix()
        return False

    def setStartCursorPosition(self, position):
        self.setCompletionPrefix("")
        self.activeSources = []
        self.startCursorPosition = position

    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        suggestion = self.completionModel().sourceModel().getSuggestion(sIndex)
        _, start, end = self.editor.currentWord(search = False)
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        if isinstance(suggestion, dict):
            if 'display' in suggestion:
                cursor.insertText(suggestion['display'])
            elif 'title' in suggestion:
                cursor.insertText(suggestion['title'])
        elif isinstance(suggestion, BundleItemTreeNode):
            cursor.removeSelectedText()
            self.editor.insertBundleItem(suggestion)
        else:
            cursor.insertText(suggestion)

    def complete(self, rect):
        self.popup().setCurrentIndex(self.completionModel().index(0, 0))
        QtGui.QCompleter.complete(self, rect)
