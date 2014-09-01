#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorComplitionMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorComplitionMode, self).__init__(**kwargs)
        self.completer = None
        self.setObjectName("CodeEditorComplitionMode")
    
    def name(self):
        return "Complition"
        
    def initialize(self, **kwargs):
        super(CodeEditorComplitionMode, self).initialize(**kwargs)
        self.completer = self.editor.completer
        self.editor.installEventFilter(self)

    def eventFilter(self, obj, event):
        if self.isActive() and event.type() == QtCore.QEvent.KeyPress:
            self.pre_key_press_event(event)
            
        return False
        
    def pre_key_press_event(self, event):
        if self.isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab):
                event.ignore()
                return True
            elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
                #Proximo modelo
                if self.trySetNextModel():
                    self.complete(self.editor.cursorRect())
                    self.explicit_launch = True
                    return not self.explicit_launch
                else:
                    self.hide()
            elif event.key() in (QtCore.Qt.Key_Space, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
                self.hide()
        elif event.key() == QtCore.Qt.Key_Space and event.modifiers() == QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.explicit_launch = True
            self.setCompletionPrefix(alreadyTyped)
            self.runCompleter(self.editor.cursorRect())
        return False
    
    def post_key_press_event(self, event):
        if self.isVisible():
            current_prefix = self.completionPrefix()
            maxPosition = self.startCursorPosition + len(current_prefix) + 1
            cursor = self.editor.textCursor()
            
            if not (self.startCursorPosition <= cursor.position() <= maxPosition):
                self.hide()
                return
            cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
            new_prefix = cursor.selectedText()
            if new_prefix == current_prefix:
                return
            self.setCompletionPrefix(new_prefix)
            if not self.setCurrentRow(0) and not self.trySetNextModel():
                self.hide()
                return
            self.complete(self.editor.cursorRect())
        elif text.asciify(event.text()) in COMPLETER_CHARS:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            if end - start >= self.editor.wordLengthToComplete:
                self.explicit_launch = False
                self.setCompletionPrefix(alreadyTyped)
                self.runCompleter(self.editor.cursorRect())