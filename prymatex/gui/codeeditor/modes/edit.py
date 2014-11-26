#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorEditMode(CodeEditorBaseMode):
    def name(self):
        return self.editor.overwriteMode() and "OVERWRITE" or "EDIT"

    def initialize(self, **kwargs):
        super(CodeEditorEditMode, self).initialize(**kwargs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_key_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_typing_pairs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__first_line_syntax)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__insert_new_line)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__insert_tab_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Home, self.__move_cursor_to_line_start)
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
    
    def __insert_new_line(self, event):
        self.editor.insertNewLine(self.editor.textCursor())
        return True
    
    def __insert_key_bundle_item(self, event):
        keyseq = int(event.modifiers()) + event.key()
        # Try key equivalent
        if keyseq in self.application().supportManager.getAllKeyEquivalentCodes():
            leftScope, rightScope = self.editor.scope(self.editor.textCursor())
            items = self.application().supportManager.getKeyEquivalentItem(
                keyseq, leftScope, rightScope)
            self.editor.insertBundleItem(items)
            return bool(items)
    
    def __insert_tab_bundle_item(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            trigger = self.application().supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.positionInBlock())
            if trigger:
                triggerCursor = self.editor.newCursorAtPosition(
                    cursor.position(), cursor.position() - len(trigger))
                leftScope, rightScope = self.editor.scope(triggerCursor)
                items = self.application().supportManager.getTabTriggerItem(
                    trigger, leftScope, rightScope)
                print(trigger, str(leftScope), str(rightScope))
                self.editor.insertBundleItem(items, textCursor = triggerCursor)
                return bool(items)

    def __move_cursor_to_line_start(self, event):
        cursor = self.editor.textCursor()
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        newPosition = block.position() + len(self.editor.blockIndentation(block))
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True
        
    def __unindent_backward_tab_behavior(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            lineText = cursor.block().text()
            if lineText[:cursor.positionInBlock()].endswith(self.editor.tabKeyBehavior()):
                self.editor.unindent()
                return True
        
    def __remove_backward_braces(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor1, _, cursor2, _ = self.editor._smart_typing_pairs(cursor)
            if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
                cursor.beginEditBlock()
                cursor1.removeSelectedText()
                cursor2.removeSelectedText()
                cursor.endEditBlock()
                return True

    def __unindent_forward_tab_behavior(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            tab_behavior = self.editor.tabKeyBehavior()
            cursor = self.editor.newCursorAtPosition(cursor.position(), cursor.position() + len(tab_behavior))
            if cursor.selectedText() == tab_behavior:
                cursor.removeSelectedText()
                return True
        
    def __remove_forward_braces(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            _, cursor1, _, cursor2 = self.editor._smart_typing_pairs(cursor)
            if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
                cursor.beginEditBlock()
                cursor1.removeSelectedText()
                cursor2.removeSelectedText()
                cursor.endEditBlock()
                return True
        
    def __insert_typing_pairs(self, event):
        cursor = self.editor.textCursor()
        settings = self.editor.preferenceSettings(cursor)
        character = event.text()
        pairs = [pair for pair in settings.smartTypingPairs if character in pair]
        
        # No pairs
        if not pairs: return False
        lc1, rc1, lc2, rc2 = self.editor._smart_typing_pairs(cursor)
        
        pair = pairs[0]
        
        isOpen = character == pair[0]
        isClose = character == pair[1]
        isSame = pair[0] == pair[1]
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose and not cursor.hasSelection() \
            and rc1 and rc2 and character == rc1.selectedText():
            # Skip
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            self.editor.setTextCursor(cursor)
            return True
        elif control_down and isOpen:
            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if any([selectedText == pair[0] for pair in settings.smartTypingPairs]):
                    # Replace
                    if lc1 is not None and lc2 is not None:
                        lc1.insertText(pair[0])
                        lc2.insertText(pair[1])
                    elif rc1 is not None and rc2 is not None:
                        rc1.insertText(pair[0])
                        rc2.insertText(pair[1])
                else:
                    # Wrap
                    cursor.insertText("%s%s%s" % (pair[0],selectedText,pair[1]))
                return True
            else:
                if lc1 and lc2:
                    if cursor.position() == lc1.selectionStart():
                        lc1.setPosition(lc1.selectionStart())
                        rc2.setPosition(lc2.selectionEnd())
                    else:
                        lc1.setPosition(lc1.selectionEnd())
                        rc2.setPosition(lc2.selectionStart())
                    cursor.beginEditBlock()
                    lc1.insertText(pair[0])
                    lc2.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                elif rc1 and rc2:
                    if cursor.position() == rc1.selectionStart():
                        rc1.setPosition(rc1.selectionStart())
                        rc2.setPosition(rc2.selectionEnd())
                    else:
                        rc1.setPosition(rc1.selectionEnd())
                        rc2.setPosition(rc2.selectionStart())
                    cursor.beginEditBlock()
                    rc1.insertText(pair[0])
                    rc2.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                    
        word, wordStart, wordEnd = self.editor.currentWord()
        if isOpen and not isSame and not (wordStart <= cursor.position() < wordEnd):
            position = cursor.position()
            cursor.insertText("%s%s" % (pair[0], pair[1]))
            cursor.setPosition(position + 1)
            self.editor.setTextCursor(cursor)
            return True

    def __toggle_overwrite(self, event):
        self.editor.setOverwriteMode(not self.editor.overwriteMode())
