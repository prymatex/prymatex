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
        self.editor.registerKeyPressHandler(
            QtCore.Qt.Key_Space,
            self.__run_completer
        )
        self.editor.registerKeyPressHandler(
            QtCore.Qt.Key_Any,
            self.__autorun_completer,
            after = True
        )
        self.completer.popup().installEventFilter(self)

    def activate(self):
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)
        super(CodeEditorComplitionMode, self).activate()
    
    def deactivate(self):
        self.editor.textChanged.disconnect(self.on_editor_textChanged)
        self.editor.cursorPositionChanged.disconnect(self.on_editor_cursorPositionChanged)
        super(CodeEditorComplitionMode, self).deactivate()
    
    def on_editor_textChanged(self):
        alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
        self.completer.setCompletionPrefix(alreadyTyped)
        if self.completer.setCurrentRow(0) or self.completer.trySetNextModel():
            self.completer.complete(self.editor.cursorRect())
        else:
            self.completer.hide()

    def on_editor_cursorPositionChanged(self):
        prefix, start, end = self.completer.completionPrefixRange()
        cursor = self.editor.textCursor()
        if not (start <= cursor.position() <= end):
            self.completer.hide()
                        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Show:
            self.activate()
        elif event.type() == QtCore.QEvent.Hide:
            self.deactivate()
        return False

    def __run_completer(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
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

    def __autorun_completer(self, event):
        if not self.isActive() and not event.modifiers() and \
            text.asciify(event.text()) in COMPLETER_CHARS:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            if end - start >= self.editor.wordLengthToComplete:
                self.completer.setCompletionPrefix(alreadyTyped)
                self.completer.runCompleter(self.editor.cursorRect())
