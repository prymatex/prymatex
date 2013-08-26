#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

from prymatex.models.support import BundleItemTreeNode
from prymatex.gui.codeeditor.models import PMXCompleterTableModel

class CodeEditorCompleterMode(QtGui.QCompleter, CodeEditorBaseMode):
    def __init__(self, parent = None):
        QtGui.QCompleter.__init__(self, parent)

        #Table view
        self.popupView = QtGui.QTableView()
        self.popupView.setAlternatingRowColors(True)
        self.popupView.setWordWrap(False)
        self.popupView.verticalHeader().setVisible(False)
        self.popupView.horizontalHeader().setVisible(False)
        self.popupView.setShowGrid(False)
        self.popupView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popupView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popupView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #Table view size
        spacing = self.popupView.verticalHeader().fontMetrics().lineSpacing()
        self.popupView.verticalHeader().setDefaultSectionSize(spacing + 3);
        self.popupView.horizontalHeader().setStretchLastSection(True)
        self.popupView.setMinimumWidth(spacing * 18)
        #self.popupView.setMinimumHeight(spacing * 12)
        
        self.setPopup(self.popupView)

        #QCompleter::PopupCompletion	0	Current completions are displayed in a popup window.
        #QCompleter::InlineCompletion	2	Completions appear inline (as selected text).
        #QCompleter::UnfilteredPopupCompletion	1	All possible completions are displayed in a popup window with the most likely suggestion indicated as current.
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

        self.setModel(PMXCompleterTableModel(self))
        
        self.currentSource = None
        self.activeSources = []
        self.completerSuggestions = {}
        self.activatedCallback = None

    def initialize(self, editor):
        self.setWidget(self.editor)
        
    def fixPopupViewSize(self):
        self.popup().setMinimumHeight(200)
        self.popup().resizeColumnsToContents()
        width = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.completionModel().sourceModel().columnCount()):
            width += self.popup().sizeHintForColumn(columnIndex)
        self.popupView.setMinimumWidth(width)
      
    def hasSource(self, source):
        return source in self.activeSources
        
    def switch(self):
        if len(self.activeSources) > 1:
            index = self.activeSources.index(self.currentSource)
            index = (index + 1) % len(self.activeSources)
            self.currentSource = self.activeSources[index]
            self.completionModel().sourceModel().setSuggestions(self.completerSuggestions[self.currentSource])
            self.fixPopupViewSize()

    def setActivatedCallback(self, callback):
        self.activatedCallback = callback

    def setSource(self, source):
        self.activeSources.append(source)
        self.currentSource = source
        self.completionModel().sourceModel().setSuggestions(self.completerSuggestions[source])
        self.fixPopupViewSize()

    def setSuggestions(self, suggestions, source):
        self.completerSuggestions[source] = suggestions
        self.activeSources.append(source)
        self.currentSource = source
        self.completionModel().sourceModel().setSuggestions(suggestions)
        self.fixPopupViewSize()
        
    def isActive(self):
        return self.popup().isVisible()
        
    def inactive(self):
        self.popup().setVisible(False)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
            event.ignore()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space:
            self.editor.switchCompleter()
        elif self.editor.runKeyHelper(event):
            self.inactive()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)

            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()

            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                self.complete(self.editor.cursorRect())
            else:
                self.inactive()

    def onlyOneSameSuggestion(self):
        cursor = self.editor.textCursor()
        if not self.completionModel().hasIndex(1, 0):
            sIndex = self.completionModel().mapToSource(self.completionModel().index(0, 0))
            suggestion = self.completionModel().sourceModel().data(sIndex)
            return suggestion == self.completionPrefix()
        return False

    def setStartCursorPosition(self, position):
        self.setCompletionPrefix("")
        self.activeSources = []
        self.startCursorPosition = position

    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        suggestion = self.completionModel().sourceModel().getSuggestion(sIndex)
        if self.activatedCallback is not None:
            self.activatedCallback(suggestion)
        else:
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
        if not self.onlyOneSameSuggestion():
            self.popup().setCurrentIndex(self.completionModel().index(0, 0))
            QtGui.QCompleter.complete(self, rect)
        else:
            self.inactive()
