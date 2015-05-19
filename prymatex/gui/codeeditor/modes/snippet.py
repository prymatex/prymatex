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

    def activate(self):
        self.editor.keyPressed.connect(self.on_editor_keyPressed)
        super().activate()
        
    def deactivate(self):
        self.editor.keyPressed.disconnect(self.on_editor_keyPressed)
        super().deactivate()

    def on_editor_keyPressed(self, event):
        if not event.text():
            return
        command, args, _ = self.editor.commandHistory(0, True)
        if not self.processor.setHolder(args['position'], args['position']):
            self.processor.stop()
            return
        holder_start, holder_end = self.processor.currentPosition()
        if command == 'insert':
            holder_position = args['position'] - holder_start + len(args['characters'])
            cursor = self.editor.newCursorAtPosition(holder_start, holder_end + len(args['characters']))
        elif command == 'delete':
            holder_position = args['position'] - holder_start
            cursor = self.editor.newCursorAtPosition(holder_start, holder_end - len(args['characters']))
        elif command == 'replace':
            holder_position = args['position'] - holder_start + len(args['by'])
            cursor = self.editor.newCursorAtPosition(holder_start, holder_end - (len(args['characters']) - len(args['by'])))

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
