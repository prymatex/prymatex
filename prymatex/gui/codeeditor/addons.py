#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseAddon
from prymatex.support import PMXPreferenceSettings

class CompleterAddon(QtCore.QObject, PMXBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.charCounter = 0

    def initialize(self, editor):
        self.editor = editor
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def finalize(self):
        pass
        
    def on_editor_keyPressEvent(self, event):
        if not event.modifiers() and event.text() and event.key() not in [ QtCore.Qt.Key_Space, QtCore.Qt.Key_Backspace ]:
            self.charCounter += 1
        else:
            self.charCounter = 0
        if self.charCounter == 3:
            completions, alreadyTyped = self.editor.completionSuggestions()
            if bool(completions):
                self.editor.showCompleter(completions, alreadyTyped)
                
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