#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseAddon
from prymatex.support import PMXPreferenceSettings

class CompleterAddon(QtCore.QObject, PMXBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        self.editor = editor
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def finalize(self):
        pass
        
    def on_editor_keyPressEvent(self, event):
        currentWord, start, end = self.editor.getCurrentWord()
        if event.text() and end - start >= 2:
            scope = self.editor.currentScope()
            settings = self.application.supportManager.getPreferenceSettings(scope)
            disableDefaultCompletion = settings.disableDefaultCompletion
            
            #An array of additional candidates when cycling through completion candidates from the current document.
            completions = settings.completions[:]
    
            #A shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
            completionCommand = settings.completionCommand
            
            #A tab tigger completion
            completionTabTriggers = self.application.supportManager.getAllTabTiggerItemsByScope(scope)
            
            #print completions, completionCommand, disableDefaultCompletion, completionTabTriggers
            completions += completionTabTriggers
            if bool(completions):
                self.editor.showCompleter(completions, currentWord)
                
class SmartUnindentAddon(QtCore.QObject, PMXBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        self.editor = editor
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def finalize(self):
        pass
        
    def on_editor_keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        currentBlock = cursor.block()
        previousBlock = currentBlock.previous()
        settings = self.editor.preferenceSettings(self.editor.currentScope())
        indentMarks = settings.indent(currentBlock.text())
        if PMXPreferenceSettings.INDENT_DECREASE in indentMarks and previousBlock.isValid() and currentBlock.userData().indent >= previousBlock.userData().indent:
            self.editor.unindentBlocks(cursor)