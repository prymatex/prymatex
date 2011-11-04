#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

class PMXBaseEditorHelper(PMXObject):
    KEY = None
    def accept(self, event, cursor, scope):
        return event.key() == self.KEY
    
    def execute(self, editor, event):
        editor.keyPressEvent(event)

class KeyEquivalentHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Any
    def accept(self, event, cursor, scope):
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
    def accept(self, event, cursor, scope):
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
    def accept(self, event, cursor, scope):
        preferences = self.application.supportManager.getPreferenceSettings(scope)
        if not cursor.atBlockEnd(): return False
        pairs = filter(lambda pair: event.text() == pair[0], preferences.smartTypingPairs)
        self.pair = pairs[0] if len(pairs) == 1 else []
        return bool(self.pair)
            
    def execute(self, editor, event):
        cursor = editor.textCursor()
        if cursor.hasSelection():
            position = cursor.selectionStart()
            text = self.pair[0] + cursor.selectedText() + self.pair[1]
            cursor.insertText(text)
            cursor.setPosition(position)
            cursor.setPosition(position + len(text), QtGui.QTextCursor.KeepAnchor)
            editor.setTextCursor(cursor)
        else:
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            editor.setTextCursor(cursor)

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
            editor.textCursor().insertText(self.tabKeyBehavior)
        else:
            editor.textCursor().insertText(self.tabKeyBehavior)

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
            if counter > 0:
                cursor.beginEditBlock()
                position = block.position() if block.position() <= cursor.position() <= block.position() + self.tabStopSize else cursor.position() - counter
                cursor.setPosition(block.position()) 
                for _ in range(counter):
                    cursor.deleteChar()
                cursor.setPosition(position)
                self.setTextCursor(cursor)
                cursor.endEditBlock()

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
        super(PMXCodeEditor, self).keyPressEvent(event)
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

class SmartSyntaxHelper(PMXBaseEditorHelper):
    KEY = QtCore.Qt.Key_Return
    def accept(self, event, cursor, scope):
        if cursor.document().blockCount() == 1:
            self.syntax = self.application.supportManager.findSyntaxByFirstLine(cursor.block().text())
            return bool(self.syntax)
        return False
        
    def execute(self, editor, event):
        editor.setSyntax(self.syntax)
        QtGui.QPlainTextEdit.keyPressEvent(editor, event)