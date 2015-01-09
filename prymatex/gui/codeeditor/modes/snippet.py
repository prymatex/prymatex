#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorSnippetMode(CodeEditorBaseMode):
    def name(self):
        return "SNIPPET"
    
    def initialize(self, **kwargs):
        super(CodeEditorSnippetMode, self).initialize(**kwargs)
        self.setAllowDefaultHandlers(False)
        self.processor = self.editor.findProcessor("snippet")
        self.processor.begin.connect(self.activate)
        self.processor.end.connect(self.deactivate)
        self.registerKeyPressHandler(QtCore.Qt.Key_Escape, self.__snippet_end)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__snippet_navigation)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backtab, self.__snippet_navigation)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__snippet_backspace)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__snippet_delete)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__snippet_update_holder)
    
    def activate(self):
        super(CodeEditorSnippetMode, self).activate()
        cursor = self.editor.textCursor()
        holderStart, holderEnd = self.processor.currentPosition()
        self.holderPositionBefore = cursor.selectionStart() - holderStart
        self.positionBefore = cursor.selectionStart()
        self.charactersBefore = cursor.document().characterCount()

    def on_editor_keyPressed(self, event):
        if event.text():
            cursor = self.editor.textCursor()
            holderStart, holderEnd = self.processor.currentPosition()
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = self.charactersBefore - charactersAfter 
            
            # Capture Text
            cursor.setPosition(holderStart)
            cursor.setPosition(holderEnd - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = self.editor.selectedTextWithEol(cursor)
            cursor.removeSelectedText()
            
            # Update holder
            self.processor.setHolderContent(selectedText)
    
            # Render
            self.processor.render()
            
            if selectedText:
                newHolderStart, _ = self.processor.currentPosition()
                self.editor.setTextCursor(
                    self.editor.newCursorAtPosition(
                        newHolderStart + self.holderPositionBefore + (positionAfter - self.positionBefore)
                    )
                )

    # ------------ Key press handlers
    def __snippet_update_holder(self, event):
        cursor = self.editor.textCursor()
        if self.processor.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
            holderStart, holderEnd = self.processor.currentPosition()

            self.holderPositionBefore = cursor.selectionStart() - holderStart
            self.positionBefore = cursor.selectionStart()
            self.charactersBefore = cursor.document().characterCount()
        else:
            self.processor.stop()
    
    def __snippet_end(self, event):
        self.processor.stop()
        return True

    def __snippet_navigation(self, event):
        cursor = self.editor.textCursor()
        if self.processor.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
            if event.key() == QtCore.Qt.Key_Tab:
                self.processor.nextHolder()
            else:
                self.processor.previousHolder()
            return True
        self.processor.stop()

    def __snippet_backspace(self, event):
        cursor = self.editor.textCursor()
        if self.processor.isReady():
            holderStart, holderEnd = self.processor.currentPosition()
            if not cursor.hasSelection() and cursor.position() == holderStart:
                self.processor.stop()

    def __snippet_delete(self, event):
        cursor = self.editor.textCursor()
        if self.processor.isReady():
            holderStart, holderEnd = self.processor.currentPosition()
            if not cursor.hasSelection() and cursor.position() == holderEnd:
                self.processor.stop()
