#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re

from PyQt4 import QtCore, QtGui

from prymatex.utils.lists import bisect_key
from prymatex.core.plugin.editor import PMXBaseEditorAddon
from prymatex.support import PMXPreferenceSettings

RE_CHAR = re.compile(r"(\w)", re.UNICODE)

class CodeEditorObjectAddon(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        PMXBaseEditorAddon.initialize(self, editor)

    def extraSelections(self):
        return []
        
    def contributeToContextMenu(self, cursor):
        return PMXBaseEditorAddon.contributeToContextMenu(self)
        
class CompleterAddon(CodeEditorObjectAddon):
    def __init__(self, parent):
        CodeEditorObjectAddon.__init__(self, parent)

    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        if event.text() and self.editor.currentWord(direction = "left", search = False)[0]:
            self.editor.showCachedCompleter()
        
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
        self.currentSpellTask = None
        self.setupSpellChecker()
        
    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        if self.dictionary is not None:
            editor.registerTextCharFormatBuilder("#spell", self.textCharFormat_spell_builder)
            editor.afterOpened.connect(self.on_editor_afterOpened)
            self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)

    def contributeToContextMenu(self, cursor):
        items = []
        cursors = filter(lambda c: c.selectionStart() <= cursor.selectionStart() <= cursor.selectionEnd() <= c.selectionEnd(), self.wordCursors)
        if cursors:
            cursor = cursors[0]
            for word in self.dictionary.suggest(cursor.selectedText()):
                items.append({'title': word,
                'callback': lambda word = word, cursor = cursor: cursor.insertText(word) })
        return items

    def extraSelections(self):
        return self.editor.buildExtraSelections("#spell", self.wordCursors)
        
    def setupSpellChecker(self):
        try:
            import enchant
            # TODO: Use custom word list with DictWithPWL class
            self.dictionary = enchant.Dict()
        except Exception as e:
            self.dictionary = None

    def textCharFormat_spell_builder(self):
        format = QtGui.QTextCharFormat()
        format.setFontUnderline(True)
        format.setUnderlineColor(QtCore.Qt.red) 
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        format.setBackground(QtCore.Qt.transparent)
        return format

    def spellWordsForBlock(self, block):
        spellRange = filter(lambda ((start, end), p): p.spellChecking,  block.userData().preferences)
        for ran, p in spellRange:
            wordRangeList = block.userData().wordsRanges(ran[0], ran[1])
            for (start, end), word, group in wordRangeList:
                yield (start, end), word

    def cleanCursorsForBlock(self, block):
        self.wordCursors = filter(lambda cursor: cursor.block() != block, self.wordCursors)

    def spellCheckWord(self, word, block, start, end):
        if not self.dictionary.check(word):
            cursor = self.editor.textCursor()
            cursor.setPosition(block.position() + start)
            cursor.setPosition(block.position() + end, QtGui.QTextCursor.KeepAnchor)
            self.wordCursors.append(cursor)

    def spellCheckAllDocument(self):
        block = self.editor.document().firstBlock()
        while block.isValid():
            for (start, end), word in self.spellWordsForBlock(block):
                self.spellCheckWord(word, block, start, end)
            block = block.next()
            yield
        self.editor.highlightEditor()
    
    def on_actionSpell_toggled(self, cursor):
        print cursor.selectedText()
        
    def on_editor_afterOpened(self):
        self.currentSpellTask = self.application.scheduler.newTask(self.spellCheckAllDocument())
        def on_spellReady():
            self.currentSpellTask = None
        self.currentSpellTask.done.connect(on_spellReady)
        
    def on_editor_keyPressEvent(self, event):
        '''Dynamically connect dependant on pyenchant import'''
        assert self.dictionary is not None
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ] and self.currentSpellTask == None:
            cursor = self.editor.textCursor()
            block = cursor.block()
            self.cleanCursorsForBlock(block)
            for (start, end), word in self.spellWordsForBlock(block):
                self.spellCheckWord(word, block, start, end)
        self.editor.highlightEditor()
        
class HighlightCurrentSelectionAddon(CodeEditorObjectAddon):
    def __init__(self, parent):
        CodeEditorObjectAddon.__init__(self, parent)
        self.highlightCursors = []

    def initialize(self, editor):
        CodeEditorObjectAddon.initialize(self, editor)
        editor.registerTextCharFormatBuilder("#currentSelection", self.textCharFormat_currentSelection_builder)
        editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)

    def textCharFormat_currentSelection_builder(self):
        format = QtGui.QTextCharFormat()
        color = QtGui.QColor(self.editor.colours['selection'])
        color.setAlpha(128)
        format.setBackground(color)
        return format

    def extraSelections(self):
        return self.editor.buildExtraSelections("#currentSelection", self.highlightCursors)

    def on_editor_cursorPositionChanged(self):
        cursor = self.editor.textCursor()
        self.highlightCursors = self.editor.findAll(cursor.selectedText(), QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords) if cursor.hasSelection() and cursor.selectedText().strip() != '' else []