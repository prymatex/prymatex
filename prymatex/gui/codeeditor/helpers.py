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

class SmartTypingHelper(PMXBaseEditorHelper):
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
        
class IndentHelper(PMXBaseEditorHelper):
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
            if position <= blockPosition + len(indent):
                delta = len(indent) % editor.tabStopSize
                cursor.insertText(editor.tabStopSoft and u' ' * delta or u'\t' * delta)
            else:
                
            position - blockPosition
            
            self.tabKeyBehavior
        else:
            editor.textCursor().insertText(self.tabKeyBehavior)
