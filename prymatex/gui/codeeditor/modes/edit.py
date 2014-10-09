#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorEditMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorEditMode, self).__init__(**kwargs)
        self.editor.setDefaultCodeEditorMode(self)

    def name(self):
        return self.editor.overwriteMode() and "OVERWRITE" or "EDIT"

    def initialize(self, **kwargs):
        super(CodeEditorEditMode, self).initialize(**kwargs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_key_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_typing_pairs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__first_line_syntax)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__insert_new_line)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__insert_tab_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__indent_tab_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Home, self.__move_cursor_to_line_start)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backtab, self.__unindent)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__unindent_backward_tab_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__remove_backward_braces)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__unindent_forward_tab_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__remove_forward_braces)
        self.registerKeyPressHandler(QtCore.Qt.Key_Insert, self.__toggle_overwrite)

    # ------------ Key press handlers
    def __first_line_syntax(self, event):
        cursor = self.editor.textCursor()
        if cursor.blockNumber() == 0:
            self.editor.trySyntaxByText(cursor)
        return False
    
    def __insert_new_line(self, event):
        self.editor.insertNewLine(self.editor.textCursor())
        return True
    
    def __insert_key_bundle_item(self, event):
        keyseq = int(event.modifiers()) + event.key()
        # Try key equivalent
        if keyseq in self.application().supportManager.getAllKeyEquivalentCodes():
            leftScope, rightScope = self.editor.scope()
            items = self.application().supportManager.getKeyEquivalentItem(
                keyseq, leftScope, rightScope)
            self.editor.insertBundleItem(items)
            return bool(items)
        return False
    
    def __insert_tab_bundle_item(self, event):
        cursor = self.editor.textCursor()
        if cursor.hasSelection(): return False

        trigger = self.application().supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        if not trigger: return False

        triggerCursor = self.editor.newCursorAtPosition(
            cursor.position(), cursor.position() - len(trigger))
        leftScope, rightScope = self.editor.scope(triggerCursor)
        items = self.application().supportManager.getTabTriggerItem(
            trigger, leftScope, rightScope)
        self.editor.insertBundleItem(items, textCursor = triggerCursor)
        return bool(items)

    def __indent_tab_behavior(self, event):
        start, end = self.editor.selectionBlockStartEnd()
        if start != end:
            self.editor.indentBlocks()
        else:
            self.editor.textCursor().insertText(self.editor.tabKeyBehavior())
        return True
    
    def __move_cursor_to_line_start(self, event):
        cursor = self.editor.textCursor()
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        newPosition = block.position() + len(self.editor.blockIndentation(block))
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True
        return False

    def __unindent(self, event):
        self.editor.unindentBlocks()
       
    def __unindent_backward_tab_behavior(self, event):
        cursor = self.editor.textCursor()
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        if lineText[:cursor.columnNumber()].endswith(self.editor.tabKeyBehavior()):
            counter = cursor.columnNumber() % self.editor.tabWidth or self.editor.tabWidth
            self.editor.newCursorAtPosition(cursor.position(), cursor.position() - counter).removeSelectedText()
            return True
        return False
        
    def __remove_backward_braces(self, event):
        cursor = self.editor.textCursor()
        if cursor.hasSelection(): return False
        cursor1, cursor2 = self.editor.currentBracesPairs(cursor, direction = "left")
        if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
            cursor.beginEditBlock()
            cursor1.removeSelectedText()
            cursor2.removeSelectedText()
            cursor.endEditBlock()
            return True
        return False

    def __unindent_forward_tab_behavior(self, event):
        cursor = self.editor.textCursor()
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        if lineText[cursor.columnNumber():].startswith(self.editor.tabKeyBehavior()):
            counter = cursor.columnNumber() % self.editor.tabWidth or self.editor.tabWidth
            self.editor.newCursorAtPosition(cursor.position(), cursor.position() + counter).removeSelectedText()
            return True
        return False
        
    def __remove_forward_braces(self, event):
        cursor = self.editor.textCursor()
        if cursor.hasSelection(): return False
        cursor1, cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
        if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
            cursor.beginEditBlock()
            cursor1.removeSelectedText()
            cursor2.removeSelectedText()
            cursor.endEditBlock()
            return True
        return False
        
    def __insert_typing_pairs(self, event):
        cursor = self.editor.textCursor()
        settings = self.editor.preferenceSettings(cursor)
        character = event.text()
        pairs = [pair for pair in settings.smartTypingPairs if character in pair]
        
        # No pairs
        if not pairs: return False

        pair = pairs[0]
        
        insert = replace = wrap = skip = False

        isOpen = character == pair[0]
        isClose = character == pair[1]
        meta_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose:
            cursor1, cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
            if cursor1 and cursor2 and \
                character == cursor2.selectedText():
                cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                self.editor.setTextCursor(cursor)
                return True
            elif pair[0] != pair[1]:
                return False
        elif meta_down and isOpen:
            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if any([selectedText == pair[0] for pair in settings.smartTypingPairs]):
                    cursor1, cursor2 = self.currentBracesPairs(cursor)
                    cursor1.insertText(pair[0])
                    cursor2.insertText(pair[1])
                    return True
            else:
                cursor1, cursor2 = self.editor.currentBracesPairs(cursor)
                if cursor1 and cursor2:
                    if cursor.position() == cursor1.selectionStart():
                        cursor1.setPosition(cursor1.selectionStart())
                        cursor2.setPosition(cursor2.selectionEnd())
                    else:
                        cursor1.setPosition(cursor1.selectionEnd())
                        cursor2.setPosition(cursor2.selectionStart())
                    cursor.beginEditBlock()
                    cursor1.insertText(pair[0])
                    cursor2.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                    
        word, wordStart, wordEnd = self.editor.currentWord()
        if not (wordStart <= cursor.position() < wordEnd):
            position = cursor.position()
            cursor.insertText("%s%s" % (pair[0], pair[1]))
            cursor.setPosition(position + 1)
            self.editor.setTextCursor(cursor)
            return True
        return False

    def __toggle_overwrite(self, event):
        overwrite = not self.editor.overwriteMode()
        self.editor.setOverwriteMode(overwrite)
        return False