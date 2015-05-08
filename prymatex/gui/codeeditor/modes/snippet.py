#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorSnippetMode(CodeEditorBaseMode):
    def name(self):
        return "SNIPPET"

    def initialize(self, **kwargs):
        super(CodeEditorSnippetMode, self).initialize(**kwargs)
        self.processor = self.editor.findProcessor("snippet")
        self.processor.begin.connect(self.activate)
        self.processor.end.connect(self.deactivate)
        self.registerKeyPressHandler(QtCore.Qt.Key_Escape, self.__snippet_end)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__snippet_return)
        self.registerKeyPressHandler(QtCore.Qt.Key_Enter, self.__snippet_return)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__snippet_navigation)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backtab, self.__snippet_navigation)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__snippet_backspace)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__snippet_delete)
        #self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__snippet_update)

    def activate(self):
        cursor = self.editor.textCursor()
        self.cursor_position_before = cursor.selectionStart()
        self.document_characters_before = cursor.document().characterCount()
        self.editor.textChanged.connect(self.on_editor_textChanged)
        super().activate()
        
    def deactivate(self):
        self.editor.textChanged.disconnect(self.on_editor_textChanged)
        super().deactivate()

    def on_editor_textChanged(self):
        if self.processor.isRendering():
            return 
        command, args, _ = self.editor.commandHistory(0)
        if not self.processor.setHolder(args['position'], args['position']):
            self.processor.stop()
        elif command == 'insert':
            holderStart, holderEnd = self.processor.currentPosition()
            holder_position = args['position'] - holderStart + len(args['characters'])
            cursor = self.editor.newCursorAtPosition(holderStart, holderEnd + len(args['characters']))
            selectedText = self.editor.selectedTextWithEol(cursor)
            # Update holder
            self.processor.setHolderContent(selectedText)
    
            # Render
            self.processor.render()
            
            newHolderStart, _ = self.processor.currentPosition()
            self.editor.setTextCursor(
                self.editor.newCursorAtPosition(
                    newHolderStart + holder_position
                )
            )

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

    def __snippet_return(self, event):
        print(self.processor.isLastHolder())
        if self.processor.isLastHolder():
            self.processor.stop()
