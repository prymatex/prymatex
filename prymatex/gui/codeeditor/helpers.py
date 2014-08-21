#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# https://github.com/textmate/textmate/blob/master/Applications/TextMate/about/Changes.md
from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexEditorKeyHelper, Key_Any
from prymatex.qt.helpers import debug_key

class CodeEditorKeyHelper(PrymatexEditorKeyHelper, QtCore.QObject):
    def setPalette(self, palette):
        pass
        
    def setFont(self, font):
        pass

class KeyEquivalentHelper(CodeEditorKeyHelper):
    def accept(self, event = None, cursor = None, **kwargs):
        keyseq = int(event.modifiers()) + event.key()
        if keyseq not in self.application().supportManager.getAllKeyEquivalentCodes():
            return False
    
        leftScope, rightScope = self.editor.scope(cursor)
        self.items = self.application().supportManager.getKeyEquivalentItem(
            keyseq, leftScope, rightScope)
        return bool(self.items)

    def execute(self, event = None, cursor = None, **kwargs):
        self.editor.insertBundleItem(self.items)

class TabTriggerHelper(CodeEditorKeyHelper):
    """When expanding tab triggers, the left scope is the scope to the left of
    the start of the potential tab trigger and the right scope is likewise
    that to the right of the potential tab trigger.
    """
    KEY = QtCore.Qt.Key_Tab
    def accept(self, event = None, cursor = None, **kwargs):
        if cursor.hasSelection(): return False

        trigger = self.application().supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        if not trigger: return False
        
        self.triggerCursor = self.editor.newCursorAtPosition(cursor.position(), cursor.position() - len(trigger))
        leftScope, rightScope = self.editor.scope(self.triggerCursor)
        self.items = self.application().supportManager.getTabTriggerItem(
            trigger, leftScope, rightScope)
        return bool(self.items)

    def execute(self, event = None, cursor = None, **kwargs):
        #Inserto los items
        self.editor.insertBundleItem(self.items, textCursor = self.triggerCursor)

class SmartTypingPairsHelper(CodeEditorKeyHelper):
    def accept(self, event = None, cursor = None, **kwargs):
        settings = self.editor.preferenceSettings(cursor)
        character = event.text()
        pairs = [pair for pair in settings.smartTypingPairs if character in pair]
        
        # No pairs
        if not pairs: return False

        self.pair = pairs[0]
        
        self.insert = self.replace = self.wrap = self.skip = False
        self.cursor1 = self.cursor2 = None
        
        isClose = character == self.pair[1]
        isOpen = character == self.pair[0]
        meta_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose:
            cursor1, cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
            self.skip = cursor1 and cursor2 and \
                character == cursor2.selectedText() and \
                self.pair[0] != self.pair[1]
        elif meta_down and isOpen:
            if cursor.hasSelection():
                self.wrap = True
                selectedText = cursor.selectedText()
                self.replace = any([selectedText == pair[0] for pair in settings.smartTypingPairs])
                if self.replace:
                    self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor)
            else:
                self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor)
                if self.cursor1 is not None and self.cursor2 is not None:
                    self.insert = True
                    if cursor.position() == self.cursor1.selectionStart():
                        self.cursor1.setPosition(self.cursor1.selectionStart())
                        self.cursor2.setPosition(self.cursor2.selectionEnd())
                    else:
                        self.cursor1.setPosition(self.cursor1.selectionEnd())
                        self.cursor2.setPosition(self.cursor2.selectionStart())

        word, wordStart, wordEnd = self.editor.currentWord()
        return not (wordStart <= cursor.position() < wordEnd) and (self.wrap or self.skip or self.insert)
        
    def execute(self, event = None, cursor = None, **kwargs):
        cursor.beginEditBlock()
        if self.skip:
            # Skip
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            self.editor.setTextCursor(cursor)
        elif self.wrap:
            if self.replace:
                self.cursor1.insertText(self.pair[0])
                self.cursor2.insertText(self.pair[1])
            else:
                position = cursor.position()
                cursorBegin = cursor.selectionStart() == position
                text = self.pair[0] + cursor.selectedText() + self.pair[1]
                cursor.insertText(text)
                if cursorBegin:
                    cursor.setPosition(position + len(text))
                    cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
                else:
                    cursor.setPosition(position - len(text) + 2)
                    cursor.setPosition(position + 2, QtGui.QTextCursor.KeepAnchor)
                self.editor.setTextCursor(cursor)
        elif self.insert:
            # Surround
            self.cursor1.insertText(self.pair[0])
            self.cursor2.insertText(self.pair[1])
        else:
            # Peer
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            self.editor.setTextCursor(cursor)
        cursor.endEditBlock()

class MoveCursorToHomeHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Home
    def accept(self, event = None, cursor = None, **kwargs):
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        self.newPosition = block.position() + len(self.editor.blockIndentation(block))
        return self.newPosition != cursor.position()
        
    def execute(self, event = None, cursor = None, **kwargs):
        #Lo muevo al final de la indentacion
        cursor = self.editor.textCursor()
        cursor.setPosition(self.newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
        self.editor.setTextCursor(cursor)

class OverwriteHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Insert
    def execute(self, event = None, cursor = None, **kwargs):
        self.editor.setOverwriteMode(not self.editor.overwriteMode())
        self.editor.modeChanged.emit()
        
class TabIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def execute(self, event = None, cursor = None, **kwargs):
        start, end = self.editor.selectionBlockStartEnd()
        if start != end:
            #Tiene seleccion en distintos bloques, es un indentar
            self.editor.indentBlocks()
        else:
            cursor.insertText(self.editor.tabKeyBehavior())

class BacktabUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backtab
    #Siempre se come esta pulsacion solo que no unindenta si la linea ya esta al borde
    def execute(self, event = None, cursor = None, **kwargs):
        self.editor.unindentBlocks()

class BackspaceUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, event = None, cursor = None, **kwargs):
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        return lineText[:cursor.columnNumber()].endswith(self.editor.tabKeyBehavior())
        
    def execute(self, event = None, cursor = None, **kwargs):
        counter = cursor.columnNumber() % self.editor.tabWidth or self.editor.tabWidth
        self.editor.newCursorAtPosition(cursor.position(), cursor.position() - counter).removeSelectedText()

class BackspaceRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, event = None, cursor = None, **kwargs):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor, direction = "left")
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())

    def execute(self, event = None, cursor = None, **kwargs):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()
        
class DeleteUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def accept(self, event = None, cursor = None, **kwargs):
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        return lineText[cursor.columnNumber():].startswith(self.editor.tabKeyBehavior())
        
    def execute(self, event = None, cursor = None, **kwargs):
        counter = cursor.columnNumber() % self.editor.tabWidth or self.editor.tabWidth
        self.editor.newCursorAtPosition(cursor.position(), cursor.position() + counter).removeSelectedText()

class DeleteRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def accept(self, event = None, cursor = None, **kwargs):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())
        
    def execute(self, event = None, cursor = None, **kwargs):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()
        
class SmartIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Return
    def execute(self, event = None, cursor = None, **kwargs):
        if cursor.blockNumber() == 0:
            text = cursor.block().text()[:cursor.columnNumber()]
            syntax = self.application().supportManager.findSyntaxByFirstLine(text)
            if syntax is not None:
                self.editor.insertBundleItem(syntax)
        self.editor.insertNewLine(cursor)

class PrintEditorStatusHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_D
    def accept(self, event = None, cursor = None, **kwargs):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return control_down and control_down
        
    def execute(self, event = None, cursor = None, **kwargs):
        #Aca lo que queramos hacer
        userData = self.editor.blockUserData(cursor.block())
        print(userData.tokens())
        print(self.editor.scope())
        print("wordUnderCursor", self.editor.wordUnderCursor(), cursor.position())
        print("currentWord", self.editor.currentWord(), cursor.position())
        print("wordUnderCursor, left", self.editor.wordUnderCursor(direction = "left"), cursor.position())
        print("wordUnderCursor, right", self.editor.wordUnderCursor(direction = "right"), cursor.position())
        print("textUnderCursor, left", self.editor.textUnderCursor(direction = "left"), cursor.position())
        print("textUnderCursor, right", self.editor.textUnderCursor(direction = "right"), cursor.position())
        print(self.editor.word(), cursor.position())
        print(self.editor.word(direction = "left", search=True), cursor.position())
        print(self.editor.word(direction = "right", search=True), cursor.position())
        print(self.editor.word(search=True), cursor.position())
