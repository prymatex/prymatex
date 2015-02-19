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
        self.registerModel(TabTriggerItemsCompletionModel(parent = self.editor))
        self.registerModel(WordsCompletionModel(parent = self.editor))
        self.suggestionsCompletionModel = SuggestionsCompletionModel(parent = self.editor)
        self.registerModel(self.suggestionsCompletionModel)

        # Add new command to editor
        self.editor.addCommand('auto_complete', self.__auto_complete)
        self.editor.addCommand('hide_auto_complete', self.__hide_auto_complete)
    
    # Command
    def __auto_complete(self, args):
        print(args)
        self.completer.runCompleter()
        return
        #self.suggestionsCompletionModel.setSuggestions(suggestions)
        #self.suggestionsCompletionModel.setCompletionCallback(callback or
        #    self.defaultCompletionCallback)
        self.completer.setCaseSensitivity(case_insensitive and QtCore.Qt.CaseInsensitive or QtCore.Qt.CaseSensitive)
        #self.completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        if not self.completer.isVisible():
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.completer.setCompletionPrefix(already_typed or alreadyTyped or "")
        if self.completer.trySetModel(self.suggestionsCompletionModel):
            self.completer.complete(self.editor.cursorRect())

    def __hide_auto_complete(self, args):
        self.completer.hide()

    def name(self):
        return "COMPLITION"
    
    def registerModel(self, model):
        self.completer.registerModel(model)
        
    def initialize(self, **kwargs):
        super(CodeEditorComplitionMode, self).initialize(**kwargs)
        # To default editor mode
        self.editor.defaultMode().registerKeyPressHandler(
            QtCore.Qt.Key_Space,
            self.__default_space_pressed
        )
        self.editor.keyPressed.connect(self.on_editor_keyPressed)
        
        # To this mode
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

    def defaultCompletionCallback(self, suggestion):
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end) \
            if currentWord is not None else self.editor.textCursor()
        snippet = suggestion.get('insert') or suggestion.get('display') or suggestion.get('title')
        self.editor.insertSnippet(snippet, textCursor = cursor)

    def on_editor_keyPressed(self, event):
        alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
        self.completer.setCompletionPrefix(alreadyTyped)
        if self.isActive() and not (self.completer.setCurrentRow(0) or self.completer.trySetNextModel()):
            self.completer.hide()
        elif not self.isActive() and not (event.modifiers() & QtCore.Qt.ControlModifier) and (text.asciify(event.text()) in COMPLETER_CHARS) and end - start >= self.editor.wordLengthToComplete:
            self.completer.runCompleter()
        elif self.isActive():
            self.completer.complete(self.editor.cursorRect())

    # ------ Mode handlers
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
            self.completer.runCompleter()
            return True
