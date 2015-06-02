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
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__snippet_remove)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__snippet_remove)

    def activate(self):
        self.editor.keyPressed.connect(self.on_editor_keyPressed)
        super().activate()
        
    def deactivate(self):
        self.editor.keyPressed.disconnect(self.on_editor_keyPressed)
        super().deactivate()

    def on_editor_keyPressed(self, event):
        if not event.text():
            return
        position = self.editor.textCursor().position() - len(event.text())
        if not self.processor.setHolder(position, position):
            self.processor.stop()
            return
        holder_start, holder_end = self.processor.currentPosition()
        holder_position = position - holder_start + len(event.text())
        cursor = self.editor.newCursorAtPosition(holder_start, holder_end + len(event.text()))
            
        cursor.joinPreviousEditBlock()        
        selected_text = self.editor.selectedTextWithEol(cursor)
        # Update holder
        self.processor.setHolderContent(selected_text)

        # Render
        self.processor.render()
        
        new_holder_start, _ = self.processor.currentPosition()
        self.editor.setTextCursor(
            self.editor.newCursorAtPosition(
                new_holder_start + holder_position
            )
        )
        cursor.endEditBlock()

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

    def __snippet_remove(self, event):
        cursor = self.editor.textCursor()
        holder_start, holder_end = self.processor.translateToHolderPosition(
            cursor.selectionStart(), cursor.selectionEnd()
        )
        if not holder_start:
            return False
        position = cursor.selectionStart() - holder_start
        remove = len(cursor.selectedText()) or 1
        if event.key() == QtCore.Qt.Key_Backspace:
            cursor.deletePreviousChar()
        else:
            cursor.deleteChar()
        content = self.editor.toPlainTextWithEol()[holder_start:holder_end - remove]
        # Update holder
        self.processor.setHolderContent(content)

        # Render
        self.processor.render()
        
        new_holder_start, _ = self.processor.currentPosition()
        self.editor.setTextCursor(
            self.editor.newCursorAtPosition(
                new_holder_start + position - remove
            )
        )
        return True

    def __snippet_return(self, event):
        if self.processor.isLastHolder():
            self.processor.stop()
