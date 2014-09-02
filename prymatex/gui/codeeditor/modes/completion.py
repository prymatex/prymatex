#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string

from prymatex.qt import QtCore, QtGui
from prymatex.utils import text

from .base import CodeEditorBaseMode

COMPLETER_CHARS = list(string.ascii_letters)

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
        self.editor.registerPreKeyPressHandler(
            QtGui.QKeySequence.fromString("Ctrl+Space"),
            self.__run_completer
        )
        self.completer.popup().installEventFilter(self)
        self.editor.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.editor and event.type() == QtCore.QEvent.KeyRelease and \
        text.asciify(event.text()) in COMPLETER_CHARS:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            if end - start >= self.editor.wordLengthToComplete:
                self.completer.setCompletionPrefix(alreadyTyped)
                self.completer.runCompleter(self.editor.cursorRect())
        elif event.type() == QtCore.QEvent.KeyRelease and self.isActive():
            prefix, start, end = self.completer.completionPrefixRange()
            cursor = self.editor.textCursor()
            if start <= cursor.position() <= end:
                cursor.setPosition(self.completer.startPosition(), QtGui.QTextCursor.KeepAnchor)
                new_prefix = cursor.selectedText()
                if new_prefix != prefix:
                    self.completer.setCompletionPrefix(new_prefix)
                    if self.completer.setCurrentRow(0) or self.completer.trySetNextModel():
                        self.completer.complete(self.editor.cursorRect())
            else: 
                self.completer.hide()
        elif event.type() == QtCore.QEvent.Show and obj == self.completer.popup():
            self.activate()
        elif event.type() == QtCore.QEvent.Hide and obj == self.completer.popup():
            self.deactivate()
        return False

    def __run_completer(self, event):
        if self.isActive() and self.completer.trySetNextModel():
            self.completer.complete(self.editor.cursorRect())
            return True
        elif self.isActive():
            self.completer.hide()
        else:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.completer.setCompletionPrefix(alreadyTyped)
            self.completer.runCompleter(self.editor.cursorRect())
        return False
