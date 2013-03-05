#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditorAddon

from prymatex.utils.lists import bisect_key
from prymatex.support import PMXPreferenceSettings

class CodeEditorAddon(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        PMXBaseEditorAddon.initialize(self, editor)

    def contributeToContextMenu(self, cursor):
        return PMXBaseEditorAddon.contributeToContextMenu(self)

class CompleterAddon(CodeEditorAddon):
    def initialize(self, editor):
        CodeEditorAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        if event.text() and event.modifiers() == 0 and self.editor.currentWord(direction = "left", search = False)[0]:
            self.editor.showCachedCompleter()
        
class SmartUnindentAddon(CodeEditorAddon):
    def initialize(self, editor):
        CodeEditorAddon.initialize(self, editor)
        # TODO No usar esta señal porque el user data no esta listo
        #self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        #Solo si tiene texto
        if event.text():
            cursor = self.editor.textCursor()
            userData = cursor.userData()
            positionInBlock = cursor.positionInBlock()
            block = cursor.block()
            settings = self.editor.scope(cursor = cursor, attribute='settings')
            indentMarks = settings.indent(block.text()[:positionInBlock])
            indentGuide = self.editor.findPreviousNoBlankBlock(block)
            if PMXPreferenceSettings.INDENT_DECREASE in indentMarks and indentGuide is not None:
                previousBlock = self.editor.findPreviousLessIndentBlock(indentGuide)
                if previousBlock is not None and block.userData().indent > previousBlock.userData().indent:
                    self.editor.unindentBlocks(cursor)

class SpellCheckerAddon(CodeEditorAddon):
    def __init__(self, parent):
        CodeEditorAddon.__init__(self, parent)
        self.spellingOnType = False
        self.wordCursors = []
        self.currentSpellTask = None
        self.setupSpellChecker()
        
    def setupSpellChecker(self):
        try:
            import enchant
            # TODO: Use custom word list with DictWithPWL class
            self.dictionary = enchant.Dict()
        except Exception as e:
            self.dictionary = None
            
    def initialize(self, editor):
        CodeEditorAddon.initialize(self, editor)
        if self.dictionary is not None:
            self.editor.registerTextCharFormatBuilder("spell", self.textCharFormat_spell_builder)
            #self.editor.syntaxReady.connect(self.on_editor_syntaxReady)
            # TODO No usar esta señal porque el user data no esta listo
            #self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionSpellingOnType_toggled(editor, checked):
            instance = editor.findChild(cls, "Nombre")
            #instance.spellingOnType = checked

        def on_actionSpellingOnType_testChecked(editor):
            instance = editor.findChild(cls, "Nombre")
            return False
            #return instance.spellingOnType

        menuEntry = {
                'name': 'spelling',
                'text': 'Spelling',
                'items': [
                    {'text': 'Show Spelling'},
                    {'text': 'Check Spelling'},
                    {'text': 'Check Spelling as You Type',
                      'callback': on_actionSpellingOnType_toggled,
                      'checkable': True,
                      'testChecked': on_actionSpellingOnType_testChecked
                    }
                ]}
        return { 'edit': menuEntry }

    def contributeToContextMenu(self, cursor):
        items = []
        cursors = filter(lambda c: c.selectionStart() <= cursor.selectionStart() <= cursor.selectionEnd() <= c.selectionEnd(), self.wordCursors)
        if cursors:
            cursor = cursors[0]
            for word in self.dictionary.suggest(cursor.selectedText()):
                items.append({'text': word,
                'callback': lambda word = word, cursor = cursor: cursor.insertText(word) })
        return items

    def textCharFormat_spell_builder(self):
        format = QtGui.QTextCharFormat()
        format.setFontUnderline(True)
        format.setUnderlineColor(QtCore.Qt.red) 
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        format.setBackground(QtCore.Qt.transparent)
        return format

    def spellWordsForBlock(self, block):
        spellRange = self.editor.scopes(attribute = 'settings', scope_filter = lambda attr: attr.spellChecking)
        for ran, _ in spellRange:
            wordRangeList = block.userData().wordsRanges(ran[0], ran[1])
            for (start, end), word, _ in wordRangeList:
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
        
    def on_editor_syntaxReady(self):
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
        
class HighlightCurrentSelectionAddon(CodeEditorAddon):
    def initialize(self, editor):
        CodeEditorAddon.initialize(self, editor)
        editor.registerTextCharFormatBuilder("selection.extra", self.textCharFormat_extraSelection_builder)
        editor.selectionChanged.connect(self.findHighlightCursors)
        editor.cursorPositionChanged.connect(self.findHighlightCursors)

    def textCharFormat_extraSelection_builder(self):
        format = QtGui.QTextCharFormat()
        color = QtGui.QColor(self.editor.colours['selection'])
        color.setAlpha(128)
        format.setBackground(color)
        return format
    
    def findHighlightCursors(self):
        cursor = self.editor.textCursor()
        cursors = self.editor.findAll(
                cursor.selectedText(), 
                QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
            ) if cursor.hasSelection() and cursor.selectedText().strip() != '' else []
        self.editor.setExtraSelectionCursors("selection.extra", cursors)
        self.editor.updateExtraSelections()
        