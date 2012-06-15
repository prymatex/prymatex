#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin.editor import PMXBaseEditorAddon
from prymatex.support import PMXPreferenceSettings

class CodeEditorObjectAddon(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        PMXBaseEditorAddon.initialize(self, editor)

    def extraSelections(self):
        return []
        
class CompleterAddon(CodeEditorObjectAddon):
    def __init__(self, parent):
        CodeEditorObjectAddon.__init__(self, parent)
        self.charCounter = 0

    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        if event.text() and event.key() not in [ QtCore.Qt.Key_Space, QtCore.Qt.Key_Backspace ]:
            self.charCounter += 1
        else:
            self.charCounter = 0
        if self.charCounter == 3:
            completions, alreadyTyped = self.editor.completionSuggestions()
            if bool(completions):
                self.editor.showCompleter(completions, alreadyTyped)
                
class SmartUnindentAddon(CodeEditorObjectAddon):
    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
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

class SpellCheckerAddon(CodeEditorObjectAddon):
    def __init__(self, parent):
        CodeEditorObjectAddon.__init__(self, parent)
        self.wordCursors = []

    def initialize(self, editor):
        print editor
        CodeEditorObjectAddon.initialize(self, editor)
        editor.registerTextCharFormatBuilder("#spell", self.textCharFormat_spell_builder)
        
        try:
            import enchant
            # TODO: Use custom word list with DictWithPWL class
            self.dict = enchant.Dict()
            self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
        except Exception as e:
            # TODO: Configure this some way...
            print "No spellcheck due to ", e
            self.dict = None
        
    def textCharFormat_spell_builder(self):
        format = QtGui.QTextCharFormat()
        format.setFontUnderline(True)
        format.setUnderlineColor(QtCore.Qt.red) 
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        format.setBackground(QtCore.Qt.transparent)
        return format
        
    def extraSelections(self):
        return self.editor.buildExtraSelections("#spell", self.wordCursors)
        
    def on_editor_keyPressEvent(self, event):
        '''Dynamically connect dependant on pyenchant import'''
        assert self.dict is not None
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ]:
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            spellRange = filter(lambda ((start, end), p): p.spellChecking,  currentBlock.userData().preferences)
            for ran, p in spellRange:
                wordRangeList = currentBlock.userData().wordsRanges(ran[0], ran[1])
                for (start, end), word in wordRangeList:
                    if not self.dict.check(word):
                        cursor = self.editor.textCursor()
                        cursor.setPosition(currentBlock.position() + start)
                        cursor.setPosition(currentBlock.position() + end, QtGui.QTextCursor.KeepAnchor)
                        self.wordCursors.append(cursor)

class HighlightCurrentWordAddon(CodeEditorObjectAddon):
    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)
    
    def on_editor_cursorPositionChanged(self):
        pass
