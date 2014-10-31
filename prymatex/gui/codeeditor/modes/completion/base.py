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
    
    def name(self):
        return "COMPLITION"

    def initialize(self, **kwargs):
        super(CodeEditorComplitionMode, self).initialize(**kwargs)
        # To default editor mode
        self.editor.defaultMode().registerKeyPressHandler(
            QtCore.Qt.Key_Space,
            self.__default_space_pressed
        )
        self.editor.defaultMode().registerKeyPressHandler(
            QtCore.Qt.Key_Any,
            self.__default_after_any_pressed,
            after = True
        )
        # To this mode
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Any,
            self.__after_any_pressed,
            after = True
        )
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Any,
            self.__any_pressed
        )
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Space,
            self.__next_model
        )
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Return,
            self.__insert_completion
        )
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Enter,
            self.__insert_completion
        )
        self.registerKeyPressHandler(
            QtCore.Qt.Key_Tab,
            self.__insert_completion
        )
        self.completer.popup().installEventFilter(self)

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
        if self.completer.trySetModel(self.suggestionsCompletionModel):
            self.completer.complete(self.editor.cursorRect())

    # ------ Mode handlers
    def __any_pressed(self, event):
        if event.text() and text.asciify(event.text()) not in COMPLETER_CHARS:
            self.completer.hide()

    def __after_any_pressed(self, event):
        alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
        self.completer.setCompletionPrefix(alreadyTyped)
        if self.completer.setCurrentRow(0) or self.completer.trySetNextModel():
            self.completer.complete(self.editor.cursorRect())

    def __next_model(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier and self.completer.trySetNextModel():
            self.completer.complete(self.editor.cursorRect())
            return True
        else:
            self.completer.hide()

    def __insert_completion(self, event):
        event.ignore()
        return True

    # ------ Default mode handlers
    def __default_space_pressed(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.completer.setCompletionPrefix(alreadyTyped)
            self.completer.runCompleter(self.editor.cursorRect())
            return True

    def __default_after_any_pressed(self, event):
        if not (event.modifiers() & QtCore.Qt.ControlModifier) and (text.asciify(event.text()) in COMPLETER_CHARS):
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            if end - start >= self.editor.wordLengthToComplete:
                self.completer.setCompletionPrefix(alreadyTyped)
                self.completer.runCompleter(self.editor.cursorRect())
