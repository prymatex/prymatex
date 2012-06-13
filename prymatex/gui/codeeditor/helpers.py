#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin.editor import PMXBaseEditorKeyHelper

class CodeEditorKeyHelper(PMXBaseEditorKeyHelper):
    def accept(self, editor, event, cursor, scope):
        return PMXBaseEditorKeyHelper.accept(self, editor, event)
    
    def execute(self, editor, event, cursor, scope):
        PMXBaseEditorKeyHelper.accept(self, editor, event)

class KeyEquivalentHelper(CodeEditorKeyHelper):
    def accept(self, editor, event, cursor = None, scope = None):
        keyseq = int(event.modifiers()) + event.key()
        self.items = self.application.supportManager.getKeyEquivalentItem(keyseq, scope)
        return bool(self.items)

    def execute(self, editor, event, cursor = None, scope = None):
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0])
        else:
            editor.selectBundleItem(self.items)

class TabTriggerHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, editor, event, cursor = None, scope = None):
        trigger = self.application.supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        self.items = self.application.supportManager.getTabTriggerItem(trigger, scope) if trigger is not None else []
        return bool(self.items)

    def execute(self, editor, event, cursor = None, scope = None):
        #Inserto los items
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0], tabTriggered = True)
        else:
            editor.selectBundleItem(self.items, tabTriggered = True)

class CompleterHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Space
    def accept(self, editor, event, cursor = None, scope = None):
        """Accept the completer event"""
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.completions, self.alreadyTyped = editor.completionSuggestions(cursor, scope)
            return bool(self.completions)
        return False

    def execute(self, editor, event, cursor = None, scope = None):
        editor.showCompleter(self.completions, self.alreadyTyped)

class SmartTypingPairsHelper(CodeEditorKeyHelper):
    #TODO: Mas amor para la inteligencia de los cursores balanceados
    def accept(self, editor, event, cursor = None, scope = None):
        settings = editor.preferenceSettings(scope)
        character = event.text()
        pairs = filter(lambda pair: character in pair, settings.smartTypingPairs)
        
        #Si no tengo nada retorno
        if not pairs: return False
        self.pair = pairs[0]
        
        self.skip = False
        self.cursor1 = self.cursor2 = None
        
        isOpen = character == self.pair[0]
        if isOpen and cursor.hasSelection():
            #El cursor tiene seleccion, veamos si es un brace de apertura y tiene seleccionado un brace de apertura 
            selectedText = cursor.selectedText()
            if any(map(lambda pair: selectedText == pair[0], settings.smartTypingPairs)):
                self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor)
            return True
        
        isClose = character == self.pair[1] and self.pair[0] != self.pair[1]
        if isClose:
            #Es un caracter de cierre, veamos si tengo que saltarme algo hacia la derecha
            cursor1, cursor2 = editor.currentBracesPairs(cursor, direction = "right")
            self.skip = cursor1 is not None and cursor2 is not None and character == cursor2.selectedText()
            return self.skip

        ctrl_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isOpen and ctrl_down:
            self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor, direction = "left")
            if self.cursor1 is not None and self.cursor2 is not None:
                self.cursor1.setPosition(self.cursor1.selectionEnd())
                self.cursor2.setPosition(self.cursor2.selectionStart())
        return True
        
        """
        nearBalancedCursors = self.cursor1 is not None and self.cursor2 is not None
        ctrl_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)

        if not ctrl_down and nearBalancedCursors and \
        (self.pair[0], self.pair[1]) == (self.cursor1.selectedText(), character) and \
        (cursor.position() == self.cursor2.selectionStart()) and not cursor.hasSelection():
            self.skip = True
            self.cursor1 = self.cursor2 = None
        elif ctrl_down and character == self.pair[0]:
            #Ya se que son pares, vamos a intentar inferir donde esta el cierre o la apertura del brace

            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if selectedText in openTyping + closeTyping:
                    self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor)
                return True
            elif editor.besideBrace(cursor) and character in openTyping + closeTyping:
                self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor)
                if self.cursor2 is not None and self.cursor1 is not None and \
                (self.cursor1.selectionEnd() == self.cursor2.selectionStart()):
                    #Estan pegados
                    self.cursor1 = self.cursor2 = None
                elif nearBalancedCursors:
                    if (cursor.position() == self.cursor1.selectionEnd() and character in openTyping) or \
                    (cursor.position() == self.cursor2.selectionStart() and character in closeTyping):
                        self.cursor1.setPosition(self.cursor1.selectionEnd())
                        self.cursor2.setPosition(self.cursor2.selectionStart())
                    #elif (cursor.position() == self.cursor2.selectionStart() and character in closeTyping):
                    #    self.cursor1.setPosition(self.cursor1.position() < self.cursor2.position() and self.cursor1.selectionEnd() or self.cursor1.selectionStart())
                    #    self.cursor2.setPosition(self.cursor1.position() < self.cursor2.position() and self.cursor2.selectionStart() or self.cursor2.selectionEnd())
                    else:
                        self.cursor1 = self.cursor2 = None
            else:
                currentWord, currentWordStart, currentWordEnd = editor.currentWord()
                if currentWord and currentWordEnd != cursor.position():
                    return False
        else:
            self.cursor1 = self.cursor2 = None
        return True
        """

    def execute(self, editor, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        if self.skip:
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            editor.setTextCursor(cursor)
        elif cursor.hasSelection():
            if self.cursor2 is not None and self.cursor1 is not None:
                self.cursor1.insertText(self.pair[0])
                self.cursor2.insertText(self.pair[1])
            else:
                position = cursor.selectionStart()
                text = self.pair[0] + cursor.selectedText() + self.pair[1]
                cursor.insertText(text)
                cursor.setPosition(position)
                cursor.setPosition(position + len(text), QtGui.QTextCursor.KeepAnchor)
                editor.setTextCursor(cursor)
        elif self.cursor1 is not None and self.cursor2 is not None:
            self.cursor1.insertText(self.pair[0])
            self.cursor2.insertText(self.pair[1])
        else:
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            editor.setTextCursor(cursor)
        cursor.endEditBlock()

class MoveCursorToHomeHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Home
    def accept(self, editor, event, cursor = None, scope = None):
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        self.newPosition = block.position() + len(block.userData().indent)
        return self.newPosition != cursor.position()
        
    def execute(self, editor, event, cursor = None, scope = None):
        #Lo muevo al final de la indentacion
        cursor = editor.textCursor()
        cursor.setPosition(self.newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
        editor.setTextCursor(cursor)

class OverwriteHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Insert
    def execute(self, editor, event, cursor = None, scope = None):
        editor.setOverwriteMode(not editor.overwriteMode())
        editor.modeChanged.emit()
        
class TabIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, editor, event, cursor = None, scope = None):
        #Solo si el cursor tiene seleccion o usa soft Tab
        return cursor.hasSelection() or editor.tabStopSoft
        
    def execute(self, editor, event, cursor = None, scope = None):
        start, end = editor.getSelectionBlockStartEnd()
        if start != end:
            #Tiene seleccion en distintos bloques, es un indentar
            editor.indentBlocks()
        else:
            #Insertar un numero multiplo de espacios a la posicion del cursor
            spaces = editor.tabStopSize - (cursor.columnNumber() % editor.tabStopSize)
            cursor.insertText(spaces * ' ')

class BacktabUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backtab
    #Siempre se come esta pulsacion solo que no unindenta si la linea ya esta al borde
    def execute(self, editor, event, cursor = None, scope = None):
        editor.unindentBlocks()

class BackspaceUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, editor, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        return lineText[:cursor.columnNumber()].endswith(editor.tabKeyBehavior)
        
    def execute(self, editor, event, cursor = None, scope = None):
        counter = cursor.columnNumber() % editor.tabStopSize or editor.tabStopSize
        for _ in range(counter):
            cursor.deletePreviousChar()

class BackspaceRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, editor, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor)
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())
        
    def execute(self, editor, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()

class SmartIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Return
    def execute(self, editor, event, cursor = None, scope = None):
        if editor.document().blockCount() == 1:
            syntax = self.application.supportManager.findSyntaxByFirstLine(cursor.block().text()[:cursor.columnNumber()])
            if syntax is not None:
                editor.setSyntax(syntax)
        editor.insertNewLine(cursor)

class MultiCursorHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_M
    def accept(self, editor, event, cursor = None, scope = None):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return event.key() == self.KEY and control_down and meta_down

    def execute(self, editor, event, cursor = None, scope = None):
        cursor = cursor or editor.textCursor()
        flags = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
        if not cursor.hasSelection():
            text, start, end = editor.getCurrentWord()
            newCursor = QtGui.QTextCursor(cursor)
            newCursor.setPosition(start)
            newCursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            editor.multiCursorMode.addMergeCursor(newCursor)
        else:
            text = cursor.selectedText()
            editor.multiCursorMode.addMergeCursor(cursor)
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                flags |= QtGui.QTextDocument.FindBackward
            newCursor = editor.document().find(text, cursor, flags)
            if not newCursor.isNull():
                editor.multiCursorMode.addMergeCursor(newCursor)
                editor.centerCursor(newCursor)

class DeleteRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def accept(self, editor, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = editor.currentBracesPairs(cursor, direction = "right")
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())
        
    def execute(self, editor, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()

class PrintEditorStatusHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_P
    def accept(self, editor, event, cursor = None, scope = None):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return control_down and control_down
        
    def execute(self, editor, event, cursor = None, scope = None):
        #Aca lo que queramos hacer
        for group in [ "comment", "constant", "entity", "invalid", "keyword", "markup", "meta", "storage", "string", "support", "variable" ]:
            print "%s: %s" % (group, cursor.block().userData().wordsByGroup(group))
        print "sin comentarios, sin cadenas", cursor.block().userData().wordsByGroup("-string -comment")