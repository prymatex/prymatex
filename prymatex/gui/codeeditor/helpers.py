#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# https://github.com/textmate/textmate/blob/master/Applications/TextMate/about/Changes.md
from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexEditorKeyHelper, Key_Any
from prymatex.qt.helpers import debug_key

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
