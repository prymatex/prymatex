#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re

from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexEditorAddon

from prymatex.utils.lists import bisect_key
from prymatex.support import PreferenceSettings

class CodeEditorAddon(PrymatexEditorAddon, QtCore.QObject):
    def setPalette(self, palette):
        pass
        
    def setFont(self, font):
        pass

class SmartUnindentAddon(CodeEditorAddon):
    def initialize(self, **kwargs):
        super(SmartUnindentAddon, self).initialize(**kwargs)
        # TODO No usar esta señal porque el user data no esta listo
        #self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        #Solo si tiene texto
        if event.text():
            cursor = self.editor.textCursor()
            userData = cursor.userData()
            positionInBlock = cursor.positionInBlock()
            block = cursor.block()
            _, settings = self.editor.preferenceSettings(cursor)
            indentMarks = settings.indent(block.text()[:positionInBlock])
            indentGuide = self.editor.findPreviousNoBlankBlock(block)
            if PreferenceSettings.INDENT_DECREASE in indentMarks and indentGuide is not None:
                previousBlock = self.editor.findPreviousLessIndentBlock(indentGuide)
                if previousBlock is not None and block.userData().indent > previousBlock.userData().indent:
                    self.editor.unindentBlocks(cursor)

class SpellCheckerAddon(CodeEditorAddon):
    def __init__(self, **kwargs):
        super(SpellCheckerAddon, self).__init__(**kwargs)
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

    def initialize(self, **kwargs):
        super(SpellCheckerAddon, self).initialize(**kwargs)
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
                      'toggled': on_actionSpellingOnType_toggled,
                      'testChecked': on_actionSpellingOnType_testChecked
                    }
                ]}
        return { 'edit': menuEntry }

    def contributeToContextMenu(self, cursor = None):
        items = []
        cursors = [c for c in self.wordCursors if c.selectionStart() <= cursor.selectionStart() <= cursor.selectionEnd() <= c.selectionEnd()]
        if cursors:
            cursor = cursors[0]
            for word in self.dictionary.suggest(cursor.selectedText()):
                items.append({'text': word,
                'triggered': lambda word = word, cursor = cursor: cursor.insertText(word) })
        return items

    def textCharFormat_spell_builder(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontUnderline(True)
        fmt.setUnderlineColor(QtCore.Qt.red) 
        fmt.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        fmt.setBackground(QtCore.Qt.transparent)
        return fmt

    def spellWordsForBlock(self, block):
        userData = self.editor.blockUserData(block)
        for token in userData.tokens():
            if token.settings.spellChecking:
                wordRangeList = userData.wordsRanges(ran[0], ran[1])
                for (start, end), word, _ in wordRangeList:
                    yield (start, end), word

    def cleanCursorsForBlock(self, block):
        self.wordCursors = [cursor for cursor in self.wordCursors if cursor.block() != block]

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
        print(cursor.selectedText())
        
    def on_editor_syntaxReady(self):
        self.currentSpellTask = self.application.scheduler.task(self.spellCheckAllDocument())
        def on_spellReady():
            self.currentSpellTask = None
        self.currentSpellTask.done.connect(on_spellReady)

    def on_editor_keyPressEvent(self, event):
        '''Dynamically connect dependant on pyenchant import'''
        assert self.dictionary is not None
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ] and self.currentSpellTask is None:
            cursor = self.editor.textCursor()
            block = cursor.block()
            self.cleanCursorsForBlock(block)
            for (start, end), word in self.spellWordsForBlock(block):
                self.spellCheckWord(word, block, start, end)
        self.editor.highlightEditor()
        
class HighlightCurrentSelectionAddon(CodeEditorAddon):
    def initialize(self, **kwargs):
        super(HighlightCurrentSelectionAddon, self).initialize(**kwargs)
        self.editor.selectionChanged.connect(self.findHighlightCursors)
        self.editor.cursorPositionChanged.connect(self.findHighlightCursors)

    def setPalette(self, palette):
        textCharFormat = QtGui.QTextCharFormat()
        color = palette.highlight().color()
        color.setAlpha(128)
        textCharFormat.setBackground(color)
        self.editor.registerTextCharFormat("dyn.selection.extra", textCharFormat)
    
    def findHighlightCursors(self):
        cursor = self.editor.textCursor()
        cursors = self.editor.findAll(
                cursor.selectedText(), 
                QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
            ) if cursor.hasSelection() and cursor.selectedText().strip() != '' else []
        self.editor.setExtraSelectionCursors("dyn.selection.extra", cursors)
        self.editor.updateExtraSelections()
        
