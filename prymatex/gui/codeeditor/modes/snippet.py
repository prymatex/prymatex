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

    # OVERRIDE: CodeEditorBaseMode.keyPress_handlers()
    def keyPress_handlers(self, event):
        for handler in super().keyPress_handlers(event):
            yield handler

        # Text event
        if event.text():
            yield self.__keyPressed

    # -------------- Tools
    def _update_and_render(self, content, position):
        # Update holder
        self.processor.setHolderContent(content)

        # Render
        self.processor.render()
        
        new_holder_start, _ = self.processor.currentPosition()
        self.editor.setTextCursor(
            self.editor.newCursorAtPosition(
                new_holder_start + position
            )
        )
    
    # -------------- Editor text keyPressed handler
    def __keyPressed(self, event):
        cursor = self.editor.textCursor()
        holder_start, holder_end = self.processor.translateToHolderPosition(
            cursor.selectionStart(), cursor.selectionEnd()
        )
        if not holder_start or (self.processor.isLastHolder() and holder_start == holder_end):
            self.processor.stop()
            return False
        holder_position = cursor.selectionStart() - holder_start
        add = len(event.text())
        remove = len(cursor.selectedText()) if cursor.hasSelection() else 0
        cursor.beginEditBlock()
        cursor.insertText(event.text())
        content = self.editor.toPlainTextWithEol()[holder_start:holder_end - remove + add]
        self._update_and_render(content, holder_position + add)
        cursor.endEditBlock()
        return True

    # -------------- Editor key handlers
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
        holder_start, holder_end = self.processor.translateToHolderPosition(
            cursor.selectionStart(), cursor.selectionEnd()
        )
        if not holder_start:
            self.processor.stop()
            return False
        holder_position = cursor.selectionStart() - holder_start
        remove = len(cursor.selectedText())
        if not cursor.hasSelection():
            remove = 1
            holder_position -= 1
        if not(holder_start <= cursor.position() - remove <= holder_end):
            self.processor.stop()
            return False
        cursor.beginEditBlock()
        cursor.deletePreviousChar()
        content = self.editor.toPlainTextWithEol()[holder_start:holder_end - remove]
        self._update_and_render(content, holder_position)
        cursor.endEditBlock()
        return True
    
    def __snippet_delete(self, event):
        cursor = self.editor.textCursor()
        holder_start, holder_end = self.processor.translateToHolderPosition(
            cursor.selectionStart(), cursor.selectionEnd()
        )
        if not holder_start:
            self.processor.stop()
            return False
        holder_position = cursor.selectionStart() - holder_start
        remove = len(cursor.selectedText()) if cursor.hasSelection() else 1
        if not(holder_start <= cursor.position() - remove <= holder_end):
            self.processor.stop()
            return False
        cursor.beginEditBlock()
        cursor.deleteChar()
        content = self.editor.toPlainTextWithEol()[holder_start:holder_end - remove]
        self._update_and_render(content, holder_position)
        cursor.endEditBlock()
        return True

    def __snippet_return(self, event):
        if self.processor.isLastHolder():
            self.processor.stop()
