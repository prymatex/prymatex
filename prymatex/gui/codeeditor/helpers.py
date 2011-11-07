#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.support import PMXPreferenceSettings

class PMXBaseEditorHelper(PMXObject):
    KEY = None
    def accept(self, editor, event, cursor, scope):
        return event.key() == self.KEY
    
    def execute(self, editor, event):
        pass

class KeyEquivalentHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Any
    def accept(self, editor, event, cursor, scope):
        keyseq = int(event.modifiers()) + event.key()
        self.items = self.application.supportManager.getKeyEquivalentItem(keyseq, scope)
        return bool(self.items)

    def execute(self, editor, event):
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0])
        else:
            editor.selectBundleItem(self.items)

class TabTriggerHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, editor, event, cursor, scope):
        trigger = self.application.supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        self.items = self.application.supportManager.getTabTriggerItem(trigger, scope) if trigger is not None else []
        return bool(self.items)

    def execute(self, editor, event):
        #Inserto los items
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0], tabTriggered = True)
        else:
            editor.selectBundleItem(self.items, tabTriggered = True)    

class SmartTypingPairsHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Any
    
    def accept(self, editor, event, cursor, scope):
        settings = self.application.supportManager.getPreferenceSettings(scope)
        character = event.text()
        pairs = filter(lambda pair: character in pair, settings.smartTypingPairs)
        self.pair = pairs[0] if len(pairs) == 1 else []
        
        #Si no tengo nada termino
        if not bool(self.pair): return False

        #Vamos a intentar algo radical
        openBraces = map(lambda pair: pair[0], settings.smartTypingPairs)
        closeBraces = map(lambda pair: pair[1], settings.smartTypingPairs)
        self.cursorOpen = self.cursorClose = None
        if cursor.hasSelection():
            current = cursor.selectedText()
            if character in openBraces:
                #Es un caracter especial de apertura
                self.cursorOpen = cursor
                index = openBraces.index(character)
                self.cursorClose = editor.findTypingPair(character, closeBraces[index], cursor)
            elif character in closeBraces:
                #Es un caracter especial de cierre
                self.cursorClose = cursor
                index = closeBraces.index(character)
                self.cursorOpen = editor.findTypingPair(character, openBraces[index], cursor, True)
            return True
        elif character in openBraces:
            leftChar = cursor.document().characterAt(cursor.position() - 1)
            rightChar = cursor.document().characterAt(cursor.position())
            #Buscar de izquierda a derecha por dentro
            pairs = filter(lambda pair: leftChar == pair[0] and rightChar != pair[1], settings.smartTypingPairs)
            if pairs:
                pair = pairs[0]
                self.cursorOpen = cursor
                cursor = QtGui.QTextCursor(self.cursorOpen)
                cursor.setPosition(cursor.position() - 1)
                self.cursorClose = editor.findTypingPair(pair[0], pair[1], cursor)
                self.cursorClose.setPosition(self.cursorClose.selectionStart())
                return bool(self.pair)
            #Buscar de izquierda a derecha por fuera
            pairs = filter(lambda pair: rightChar == pair[0], settings.smartTypingPairs)
            if pairs:
                pair = pairs[0]
                self.cursorOpen = cursor
                self.cursorClose = editor.findTypingPair(pair[0], pair[1], self.cursorOpen)
                self.cursorClose.setPosition(self.cursorClose.selectionEnd())
                return bool(self.pair)
        elif character in closeBraces and character not in openBraces:
            rightChar = cursor.document().characterAt(cursor.position())
            leftChar = cursor.document().characterAt(cursor.position() - 1)
            #Buscar de derecha a izquierda por dentro
            pairs = filter(lambda pair: rightChar == pair[1] and leftChar != pair[0], settings.smartTypingPairs)
            if pairs:
                pair = pairs[0]
                self.cursorClose = cursor
                cursor = QtGui.QTextCursor(self.cursorClose)
                cursor.setPosition(cursor.position() + 1)
                self.cursorOpen = editor.findTypingPair(pair[1], pair[0], cursor, True)
                self.cursorOpen.setPosition(self.cursorOpen.selectionEnd())
                return bool(self.pair)
            #Buscar de derecha a izquierda por fuera
            pairs = filter(lambda pair: leftChar == pair[1], settings.smartTypingPairs)
            if pairs:
                pair = pairs[0]
                self.cursorClose = cursor
                self.cursorOpen = editor.findTypingPair(pair[1], pair[0], cursor, True)
                self.cursorOpen.setPosition(self.cursorOpen.selectionStart())
                return bool(self.pair)
        return bool(self.pair)
            #438833 421870 saraniti dito para el miercoles 23 (cancelar)
            # olmos 16 ecografia obstetrica

    def execute(self, editor, event):
        cursor = editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            if self.cursorClose is not None and self.cursorOpen is not None:
                self.cursorOpen.insertText(self.pair[0])
                self.cursorClose.insertText(self.pair[1])
            else:
                position = cursor.selectionStart()
                text = self.pair[0] + cursor.selectedText() + self.pair[1]
                cursor.insertText(text)
                cursor.setPosition(position)
                cursor.setPosition(position + len(text), QtGui.QTextCursor.KeepAnchor)
                editor.setTextCursor(cursor)
        elif self.cursorOpen is None:
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            editor.setTextCursor(cursor)
        else:
            self.cursorOpen.insertText(self.pair[0])
            self.cursorClose.insertText(self.pair[1])
        cursor.endEditBlock()

class MoveCursorToHomeHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Home
    def execute(self, editor, event):
        cursor = editor.textCursor()
        block = cursor.block()
        newPosition = block.position() + len(block.userData().indent)
        cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
        editor.setTextCursor(cursor)

class OverwriteHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Insert
    def execute(self, editor, event):
        editor.setOverwriteMode(not editor.overwriteMode())
        editor.modeChanged.emit()
        
class TabIndentHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Tab
    def execute(self, editor, event):
        start, end = editor.getSelectionBlockStartEnd()
        if start != end:
            editor.indentBlocks()
        elif editor.getSyntax().indentSensitive:
            #Smart indent
            cursor = editor.textCursor()
            position = cursor.position()
            blockPosition = cursor.block().position()
            indent = cursor.block().userData().indent
            editor.textCursor().insertText(editor.tabKeyBehavior)
        else:
            editor.textCursor().insertText(editor.tabKeyBehavior)

class BacktabUnindentHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Backtab
    def execute(self, editor, event):
        start, end = editor.getSelectionBlockStartEnd()
        if start != end:
            editor.unindentBlocks()
        else:
            cursor = editor.textCursor()
            block = cursor.block()
            userData = cursor.block().userData()
            counter = editor.tabStopSize if len(userData.indent) > editor.tabStopSize else len(userData.indent)
            for _ in range(counter):
                cursor.deletePreviousChar()

class SmartIndentHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Return
    def execute(self, editor, event):
        cursor = editor.textCursor()
        block = cursor.block()
        prev = cursor.block().previous()
        line = block.text()
        if editor.document().blockCount() == 1:
            syntax = self.application.supportManager.findSyntaxByFirstLine(line)
            if syntax is not None:
                editor.setSyntax(syntax)
        preference = editor.getPreference(block.userData().getLastScope())
        indentMark = preference.indent(line)
        QtGui.QPlainTextEdit.keyPressEvent(editor, event)
        if indentMark == PMXPreferenceSettings.INDENT_INCREASE:
            self.debug("Increase indent")
            cursor.insertText(block.userData().indent + editor.tabKeyBehavior)
        elif indentMark == PMXPreferenceSettings.INDENT_NEXTLINE:
            self.debug("Increase next line indent")
        elif indentMark == PMXPreferenceSettings.UNINDENT:
            self.debug("Unindent")
        elif indentMark == PMXPreferenceSettings.INDENT_DECREASE:
            self.debug("Decrease indent")
            cursor.insertText(prev.userData().indent[:len(editor.tabKeyBehavior)])
        else:
            self.debug("Preserve indent")
            cursor.insertText(block.userData().indent)
