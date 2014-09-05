#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string

from prymatex.qt import QtCore, QtGui
from prymatex.utils import text

from ..base import CodeEditorBaseMode

from .completer import CodeEditorCompleter
from .models import (WordsCompletionModel, TabTriggerItemsCompletionModel, SuggestionsCompletionModel)

COMPLETER_CHARS = list(string.ascii_letters)

class CodeEditorComplitionMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorComplitionMode, self).__init__(**kwargs)
        
        self.completer = CodeEditorCompleter(self.editor)
        self.completer.registerModel(WordsCompletionModel(parent = self.editor))
        self.completer.registerModel(TabTriggerItemsCompletionModel(parent = self.editor))
        self.suggestionsCompletionModel = SuggestionsCompletionModel(parent = self.editor)
        self.completer.registerModel(self.suggestionsCompletionModel)

        # Install method
        self.editor.runCompleter = self.__editor_run_completer
        self.setObjectName("CodeEditorComplitionMode")

    def name(self):
        return "Complition"

    def initialize(self, **kwargs):
        super(CodeEditorComplitionMode, self).initialize(**kwargs)
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

    def __editor_run_completer(self, suggestions, already_typed=None, callback = None, 
        case_insensitive=True, disable_auto_insert = True, api_completions_only = True,
        next_completion_if_showing = False, auto_complete_commit_on_tab = True):
        self.suggestionsCompletionModel.setSuggestions(suggestions)
        self.suggestionsCompletionModel.setCompletionCallback(callback or
            self.defaultCompletionCallback)
        self.completer.setCaseSensitivity(case_insensitive and QtCore.Qt.CaseInsensitive or QtCore.Qt.CaseSensitive)
        #self.completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        if not self.completer.isVisible():
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.completer.setCompletionPrefix(already_typed or alreadyTyped or "")
        self.completer.runCompleter(self.editor.cursorRect(), model = self.suggestionsCompletionModel)

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
