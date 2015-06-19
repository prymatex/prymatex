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
        holder_text = self.editor.newCursorAtPosition(holder_start, holder_end).selectedText()
        holder_content = holder_text[holder_start - holder_start:cursor.selectionStart() - holder_start] + \
            event.text() + \
            holder_text[cursor.selectionEnd() - holder_start:holder_end - holder_start]
        self._update_and_render(holder_content, holder_position + len(event.text()))
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
        holder_text = self.editor.newCursorAtPosition(holder_start, holder_end).selectedText()
        holder_content = holder_text[holder_start - holder_start:cursor.selectionStart() - holder_start - 1] + \
            holder_text[cursor.selectionEnd() - holder_start:holder_end - holder_start]
        self._update_and_render(holder_content, holder_position - 1)
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
        holder_text = self.editor.newCursorAtPosition(holder_start, holder_end).selectedText()
        holder_content = holder_text[holder_start - holder_start:cursor.selectionStart() - holder_start] + \
            holder_text[cursor.selectionEnd() - holder_start + 1:holder_end - holder_start]
        self._update_and_render(holder_content, holder_position)
        return True

    def __snippet_return(self, event):
        if self.processor.isLastHolder():
            self.processor.stop()
