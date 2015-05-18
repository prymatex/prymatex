#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core import config

from .base import CodeEditorBaseMode

class CodeEditorEditMode(CodeEditorBaseMode):
    def name(self):
        return self.editor.overwriteMode() and "OVERWRITE" or "EDIT"

    def initialize(self, **kwargs):
        super(CodeEditorEditMode, self).initialize(**kwargs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_key_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Any, self.__insert_typing_pairs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__insert_new_line)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__insert_tab_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Home, self.__move_cursor_to_home)
        self.registerKeyPressHandler(QtCore.Qt.Key_End, self.__move_cursor_to_end)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__backspace_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__delete_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Insert, self.__toggle_overwrite)
        self.registerKeyPressHandler("Ctrl+Space", self.__run_completer)

    # ------------ Key press handlers
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
                self.editor.insertBundleItem(items, textCursor = triggerCursor)
                return bool(items)

    def __move_cursor_to_home(self, event):
        cursor = self.editor.textCursor()
        block = cursor.block()
        newPosition = block.position() + len(self.editor.blockIndentation(block))
        # Solo si el cursor no esta al final de la indentacion
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True
        
    def __move_cursor_to_end(self, event):
        cursor = self.editor.textCursor()
        block = cursor.block()
        newPosition = block.position() + len(block.text().rstrip())
        # Solo si el cursor no esta al final del texto
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True

    def __backspace_behavior(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            # ----------- Remove Braces
            cl, cr, clo, cro = self.editor._smart_typing_pairs(cursor)
            if cl and clo  and (cl.selectionStart() == clo.selectionEnd() or cl.selectionEnd() == clo.selectionStart()):
                cursor.beginEditBlock()
                cl.removeSelectedText()
                clo.removeSelectedText()
                cursor.endEditBlock()
                return True
            # ----------- Remove Tab_behavior
            tab_behavior = self.editor.tabKeyBehavior()
            cursor = self.editor.newCursorAtPosition(cursor.position(), cursor.position() - len(tab_behavior))
            if cursor.selectedText() == tab_behavior:
                cursor.removeSelectedText()
                return True

    def __delete_behavior(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            # ----------- Remove Braces
            cl, cr, clo, cro = self.editor._smart_typing_pairs(cursor)
            if cr and cro  and (cr.selectionStart() == cro.selectionEnd() or cr.selectionEnd() == cro.selectionStart()):
                cursor.beginEditBlock()
                cr.removeSelectedText()
                cro.removeSelectedText()
                cursor.endEditBlock()
                return True
            # ----------- Remove Tab_behavior
            tab_behavior = self.editor.tabKeyBehavior()
            cursor = self.editor.newCursorAtPosition(cursor.position(), cursor.position() + len(tab_behavior))
            if cursor.selectedText() == tab_behavior:
                cursor.removeSelectedText()
                return True
        
    def __insert_typing_pairs(self, event):
        cursor = self.editor.textCursor()
        settings = self.editor.preferenceSettings(cursor)
        character = event.text()
        pairs = [pair for pair in settings.smartTypingPairs if character in pair]
        
        # No pairs
        if not pairs: return False
        cl, cr, clo, cro = self.editor._smart_typing_pairs(cursor)
        
        pair = pairs[0]
        
        isOpen = character == pair[0]
        isClose = character == pair[1]
        isSame = pair[0] == pair[1]
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose and not cursor.hasSelection() \
            and cr and cro and character == cr.selectedText():
            # Skip
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            self.editor.setTextCursor(cursor)
            return True
        elif control_down and isOpen:
            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if any([selectedText == pair[0] for pair in settings.smartTypingPairs]):
                    # Replace
                    if cl is not None and clo is not None:
                        cl.insertText(pair[0])
                        clo.insertText(pair[1])
                    elif cr is not None and cro is not None:
                        cr.insertText(pair[0])
                        cro.insertText(pair[1])
                else:
                    # Wrap
                    cursor.insertText("%s%s%s" % (pair[0],selectedText,pair[1]))
                return True
            else:
                if cl and clo:
                    if cursor.position() == cl.selectionStart():
                        cl.setPosition(cl.selectionStart())
                        clo.setPosition(clo.selectionEnd())
                    else:
                        cl.setPosition(cl.selectionEnd())
                        clo.setPosition(clo.selectionStart())
                    cursor.beginEditBlock()
                    cl.insertText(pair[0])
                    clo.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                elif cr and cro:
                    if cursor.position() == cr.selectionStart():
                        cr.setPosition(cr.selectionStart())
                        cro.setPosition(cro.selectionEnd())
                    else:
                        cr.setPosition(cr.selectionEnd())
                        cro.setPosition(cro.selectionStart())
                    cursor.beginEditBlock()
                    cr.insertText(pair[0])
                    cro.insertText(pair[1])
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

    def __run_completer(self, event):
        alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
        suggestions = set()
        block = self.editor.document().begin()
        # TODO: No usar la linea actual, quiza algo de niveles de anidamiento
        while block.isValid():
            user_data = self.editor.blockUserData(block)
            all_words = map(lambda token: config.RE_WORD.findall(token.chunk),
                user_data.tokens[::-1])
            for words in all_words:
                suggestions.update(words)
            block = block.next()

        suggestions.update(self.editor.preferenceSettings().completions)
        suggestions.discard(alreadyTyped)
        suggestions = sorted(list(suggestions))
        self.editor.completer.complete(suggestions, completion_prefix=alreadyTyped)
        return True
