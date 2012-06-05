#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseAddon
from prymatex.support import PMXPreferenceSettings

class CodeEditorBaseAddon(PMXBaseAddon):
    pass

class SideBarWidgetAddon(PMXBaseAddon):
    pass
    
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
        if event.text() and event.key() not in [ QtCore.Qt.Key_Space, QtCore.Qt.Key_Backspace ]:
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
        #Solo si metio texto, sino lo hace cuando me muevo entre caracteres
        if event.text():
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            previousBlock = currentBlock.previous()
            settings = self.editor.preferenceSettings(self.editor.currentScope())
            indentMarks = settings.indent(currentBlock.text())
            if PMXPreferenceSettings.INDENT_DECREASE in indentMarks and previousBlock.isValid() and currentBlock.userData().indent >= previousBlock.userData().indent:
                self.editor.unindentBlocks(cursor)
            
class SpellCheckerAddon(QtCore.QObject, PMXBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        self.editor = editor
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def finalize(self):
        pass
        
    def on_editor_keyPressEvent(self, event):
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ]:
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            spellRange = filter(lambda ((start, end), p): p.spellChecking,  currentBlock.userData().preferences)
            print spellRange

class SpellCheckerAddon(QtCore.QObject, PMXBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        self.editor = editor
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def finalize(self):
        pass
        
    def on_editor_keyPressEvent(self, event):
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ]:
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            spellRange = filter(lambda ((start, end), p): p.spellChecking,  currentBlock.userData().preferences)
            print spellRange
        
class ExtraSelectionSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

    def initialize(self, editor):
        self.editor = editor
        
    def finalize(self):
        pass
        
    def sizeHint(self):
        return QtCore.QSize(30, 30)

    def paintEvent(self, event):
        print "pintando"
        painter = QtGui.QPainter(self)
        painter.setPen(self.editor.colours['foreground'])
        painter.fillRect(self.rect(), self.editor.colours['foreground'])
        painter.end()
        QtGui.QWidget.paintEvent(self, event)
