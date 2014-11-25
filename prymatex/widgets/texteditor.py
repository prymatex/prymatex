#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
import os
import difflib

from prymatex.qt import API
from prymatex.utils import text

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import textcursor_to_tuple
from prymatex.core import config
from functools import reduce

class TextEditWidget(QtWidgets.QPlainTextEdit):
    #------ Signals
    extraSelectionChanged = QtCore.Signal()

    #------ Editor constants
    EOL_CHARS = [ item[0] for item in text.EOLS ]
    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
    CHARACTER = "#"
    
    def __init__(self, **kwargs):
        super(TextEditWidget, self).__init__(**kwargs)

        # TODO: Buscar sobre este atributo en la documnetación
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.__scopedExtraSelections = {}
        self.__updateExtraSelectionsOrder = []
        self.__textCharFormat = {}
        # Defaults
        self.eol_chars = os.linesep
        self.soft_tabs = False
        self.tab_size = 2

    #------ EOL characters
    def setEolChars(self, eol_chars):
        """Set widget end-of-line (EOL) characters from chars_or_text"""
        
        if eol_chars in self.EOL_CHARS and self.eol_chars != eol_chars:
            self.eol_chars = eol_chars
            self.setModified(True)
        self.textChanged.emit()

    def eolChars(self):
        return self.eol_chars

    #------ Soft Tabs
    def setSoftTabs(self, soft):
        self.soft_tabs = soft
    
    def softTabs(self):
        return self.soft_tabs
        
    #------ Tab Size
    def setTabSize(self, size):
        self.tab_size = size
        self.setTabStopWidth(self.tab_size * self.characterWidth())
    
    def tabSize(self):
        return self.tab_size

    def tabKeyBehavior(self):
        return ' ' * self.tabSize() if self.softTab() else '\t'

    #--------- Indentation
    def indentation(self, cursor = None, direction = "left"):
        cursor =  cursor or self.textCursor()
        sourceText = cursor.block().text()
        if direction == "left":
            sourceText = sourceText[:cursor.columnNumber()]
        elif direction == "right":
            sourceText = sourceText[cursor.columnNumber():]
        return text.white_space(sourceText)

    def indent(self, cursor = None):
        """Indents text, block selections."""
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        block = start
        while True:
            cursor = self.newCursorAtPosition(block.position())
            cursor.insertText(self.tabKeyBehavior())
            if block == end:
                break
            block = block.next()
        cursor.endEditBlock()

    def unindent(self, cursor = None):
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        tab_behavior = self.tabKeyBehavior()
        indent_len = len(self.tabKeyBehavior())
        block = start
        while True:
            cursor = self.newCursorAtPosition(block.position(), block.position() + indent_len)
            if cursor.selectedText() == tab_behavior:
                cursor.removeSelectedText()
            if block == end:
                break
            block = block.next()
        cursor.endEditBlock()

    # OVERRIDE: QPlainTextEdit.keyPressEvent()
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            self.indent()
        elif event.key() == QtCore.Qt.Key_Backtab:
            self.unindent()
        else:
            super(TextEditWidget, self).keyPressEvent(event)

    # OVERRIDE: QPlainTextEdit.wheelEvent()
    def wheelEvent(self, event):
        if API == "pyqt5":
            delta = event.angleDelta().y()
        else:
            delta = event.delta()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if delta > 0:
                self.zoomIn()
            elif delta < 0:
                self.zoomOut()
            event.ignore()
        else:
            super(TextEditWidget, self).wheelEvent(event)

    #------ Retrieve text
    def currentWord(self):
        return self.wordUnderCursor(self.textCursor(), search = True)
        
    def currentText(self):
        return self.textUnderCursor(self.textCursor(), search = True)

    def wordUnderCursor(self, cursor = None, pattern = config.RE_WORD,
        direction = "both", search = False):
        #Como cambio el cursor hago una copia
        cursor = cursor or self.textCursor()
        selectCursor = QtGui.QTextCursor(cursor)
        character = self.document().characterAt(selectCursor.position() - 1)
        if search and pattern.match(character) is not None:
            selectCursor.movePosition(QtGui.QTextCursor.Left)
        selectCursor.select(QtGui.QTextCursor.WordUnderCursor)
        if selectCursor.hasSelection() and pattern.match(selectCursor.selectedText()):
            wordUnderCursor, start, end = selectCursor.selectedText(), selectCursor.selectionStart(), selectCursor.selectionEnd()
            if direction == "both":
                return wordUnderCursor, start, end
            elif direction == "left":
                index = cursor.position() - start
                return wordUnderCursor[:index], start, start + index
            elif direction == "right":
                index = end - cursor.position()
                return wordUnderCursor[len(wordUnderCursor) - index:], end - index, end
        return None, cursor.position(), cursor.position()
            
    def textUnderCursor(self, cursor = None, pattern = config.RE_WORD,
        direction = "both", search = False):
        cursor = cursor or self.textCursor()
        wordUnderCursor, start, end = self.wordUnderCursor(cursor = cursor,
            pattern = pattern, direction = direction, search = search)

        if wordUnderCursor:
            return wordUnderCursor, start, end
        elif search:
            columnNumber = cursor.columnNumber()
            line = cursor.block().text()
            blockPosition = cursor.block().position()
            first_part, last_part = line[:columnNumber][::-1], line[columnNumber:]
            rmatch = lmatch = None
            start = end = cursor.position()

            if direction in ("left", "both"):
                #Search left word
                lend = start
                lmatch = pattern.search(first_part)
                if lmatch is not None:
                    start = blockPosition + len(first_part[lmatch.end():])
                    lend = blockPosition + len(first_part[lmatch.start():])
                    if direction == "left":
                        return first_part[:lmatch.end()][::-1], start, lend

            if direction in ("right", "both"):
                #Search right word
                rstart = end
                rmatch = pattern.search(last_part)
                if rmatch is not None:
                    rstart = blockPosition + len(first_part)
                    end = blockPosition + len(first_part) + len(last_part[:rmatch.end()])
                    if direction == "right":
                        return last_part[:rmatch.start()], rstart, end

            # Si estamos aca es porque es both
            if lmatch is not None:
                return line[start - blockPosition : end - blockPosition], start, end
        return None, cursor.position(), cursor.position()

    #------ Retrieve cursors and blocks
    def newCursorAtPosition(self, position, anchor = None):
        cursor = QtGui.QTextCursor(self.document())
        if isinstance(position, QtCore.QPoint):
            position = self.cursorForPosition(position).position()
        if anchor and isinstance(anchor, QtCore.QPoint):
            anchor = self.cursorForPosition(anchor).position()
        cursor.setPosition(position)
        if anchor is not None:
            cursor.setPosition(anchor, QtGui.QTextCursor.KeepAnchor)
        return cursor

    def selectionBlockStartEnd(self, cursor = None):
        cursor = cursor or self.textCursor()
        return ( self.document().findBlock(cursor.selectionStart()),
            self.document().findBlock(cursor.selectionEnd()))

    #------ Retrieve and set cursor position
    def setCursorPosition(self, position):
        if isinstance(position, (tuple, list)):
            position = self.document().findBlockByNumber(position[0]).position() + position[1]
        self.setTextCursor(self.newCursorAtPosition(position))
        
    def cursorPosition(self):
        return self.textCursor().position()

    #------ Find and Replace
    def findPair(self, b1, b2, cursor, backward = False):
        """
        Busca b2 asumiendo que b1 es su antitesis de ese modo controla el balanceo.
        b1 antitesis de b2
        b2 texto a buscar
        cursor representando la posicion a partir de la cual se busca
        backward buscar para atras
        Si b1 es igual a b2 no se controla el balanceo y se retorna la primera ocurrencia que se encuentre dentro del bloque actual
        """
        flags = QtGui.QTextDocument.FindFlags()
        if backward:
            flags |= QtGui.QTextDocument.FindBackward
        if cursor.hasSelection():
            if b1 == b2:
                startPosition = cursor.selectionStart() if backward else cursor.selectionEnd()
            else:
                startPosition = cursor.selectionEnd() if backward else cursor.selectionStart()
        else:
            startPosition = cursor.position()
        c1 = self.document().find(b1, startPosition, flags)
        c2 = self.document().find(b2, startPosition, flags)
        if b1 != b2:
            #Balanceo para cuando son distintos
            if backward:
                while c1 > c2:
                    c1 = self.document().find(b1, c1.selectionStart(), flags)
                    if c1 > c2:
                        c2 = self.document().find(b2, c2.selectionStart(), flags)
            else:
                while not c1.isNull() and c1.position() != -1 and c1 < c2:
                    c1 = self.document().find(b1, c1.selectionEnd(), flags)
                    if c1.isNull():
                        break
                    if c1 < c2:
                        c2 = self.document().find(b2, c2.selectionEnd(), flags)
            if not c2.isNull():
                return c2
        else:
            #Cuando son iguales por ahora balanceo solo para el mismo bloque
            if not c2.isNull() and c2.block() == cursor.block():
                #Balanceamos usando el texto del block
                block = cursor.block()
                text = block.text()
                positionStart = cursor.selectionEnd() if backward else cursor.selectionStart()
                positionStart -= block.position()
                positionEnd = c2.selectionEnd() if c2 > cursor else c2.selectionStart()
                positionEnd -= block.position()
                if text[:positionStart].count(b2) % 2 == 0 and text[positionEnd:].count(b2) % 2 == 0:
                    return c2

    def findMatchCursor(self, match, flags, findNext = False, cursor = None, cyclicFind = False):
        """Busca la ocurrencia de match a partir de un cursor o el cursor actual
        si cyclicFind = True intenta desde el principio al llegar al final del texto"""
        cursor = cursor or self.textCursor()
        if cursor.hasSelection():
            cursor.setPosition(findNext and cursor.selectionEnd() or cursor.selectionStart())
        cursor = self.document().find(match, cursor, flags)
        if cursor.isNull() and cyclicFind:
            cursor = self.textCursor()
            if flags & QtGui.QTextDocument.FindBackward:
                cursor.movePosition(QtGui.QTextCursor.End)
            else:
                cursor.movePosition(QtGui.QTextCursor.Start)
            cursor = self.document().find(match, cursor, flags)
        if not cursor.isNull():
            return cursor

    def findMatch(self, match, flags, findNext = False, cyclicFind = False):
        cursor = self.findMatchCursor(match, flags, findNext = findNext, cyclicFind = cyclicFind)
        if cursor is not None:
            self.setTextCursor(cursor)
            return True
        return False

    def findAll(self, match, flags):
        cursors = []
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor = self.findMatchCursor(match, flags, cursor = cursor)
        while cursor is not None:
            cursors.append(QtGui.QTextCursor(cursor))
            cursor = self.findMatchCursor(match, flags, findNext = True, cursor = cursor)
        return cursors

    def replaceMatch(self, match, text, flags, allText = False):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        replaced = 0
        findCursor = cursor
        if allText:
            findCursor.movePosition(QtGui.QTextCursor.Start)
        while True:
            findCursor = self.findMatchCursor(match, flags, cursor = findCursor)
            if not findCursor: break
            if isinstance(match, QtCore.QRegExp):
                findCursor.insertText(re.sub(match.pattern(), text, cursor.selectedText()))
            else:
                findCursor.insertText(text)
            replaced += 1
            if not allText: break
        cursor.endEditBlock()
        return replaced

    #------ Extra selections
    def registerTextCharFormat(self, scope, frmt):
        # TODO Un poco mejor esto para soportar subscopes con puntos
        self.__updateExtraSelectionsOrder.append(scope)
        self.__textCharFormat[scope] = frmt

    def textCharFormat(self, scope):
        if scope in self.__textCharFormat:
            return self.__textCharFormat[scope]
        return super(TextEditWidget, self).currentCharFormat()

    def extendExtraSelectionCursors(self, scope, cursors):
        self.__scopedExtraSelections.setdefault(scope, []).extend(self.__build_extra_selections(scope, cursors))

    def setExtraSelectionCursors(self, scope, cursors):
        self.__scopedExtraSelections[scope] = self.__build_extra_selections(scope, cursors)

    def updateExtraSelectionCursors(self, cursorsDict):
        for scope, cursors in cursorsDict.items():
            self.setExtraSelectionCursors(scope, cursors)

    def updateExtraSelections(self):
        extraSelections = []
        for scope in self.__updateExtraSelectionsOrder:
            if scope in self.__scopedExtraSelections:
                extraSelections.extend(self.__scopedExtraSelections[scope])
        self.setExtraSelections(extraSelections)
        self.extraSelectionChanged.emit()

    def searchExtraSelections(self, scope):
        # TODO: Mejorar esta forma de obtener los cursores en un scope
        filterCursors = [scopedCursors[1] for scopedCursors in iter(self.__scopedExtraSelections.items()) if scopedCursors[0].startswith(scope)]
        return reduce(lambda allCursors, cursors: allCursors + cursors, filterCursors, [])

    def clearExtraSelectionCursors(self, scope):
        if scope in self.__scopedExtraSelections:
            del self.__scopedExtraSelections[scope]

    def clearExtraSelections(self):
        self.__scopedExtraSelections.clear()
        self.updateExtraSelections()

    def __build_extra_selections(self, scope, cursors):
        extraSelections = []
        for cursor in cursors:
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.format = self.textCharFormat(scope)
            selection.cursor = cursor
            extraSelections.append(selection)
        return extraSelections

    #------ Move text
    def __move_line(self, cursor, moveType):
        cursor.beginEditBlock()
        column = cursor.columnNumber()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text1 = cursor.selectedText()
        cursor2 = QtGui.QTextCursor(cursor)
        otherBlock = cursor.block().next() if moveType == QtGui.QTextCursor.Down else cursor.block().previous()
        cursor2 = self.newCursorAtPosition(otherBlock.position())
        cursor2.select(QtGui.QTextCursor.LineUnderCursor)
        text2 = cursor2.selectedText()
        cursor.insertText(text2)
        cursor2.insertText(text1)
        cursor.setPosition(otherBlock.position() + column)
        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def __move_text(self, cursor, moveType):
        cursor.beginEditBlock()
        openRight = cursor.position() == cursor.selectionEnd()
        text = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.movePosition(moveType)
        start = cursor.position()
        cursor.insertText(text)
        end = cursor.position()
        cursor = self.newCursorAtPosition(start, end) if openRight else self.newCursorAtPosition(end, start)
        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def moveUp(self, cursor = None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection():
            self.__move_text(cursor, QtGui.QTextCursor.Up)
        elif cursor.block() != self.document().firstBlock():
            self.__move_line(cursor, QtGui.QTextCursor.Up)

    def moveDown(self, cursor = None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection():
            self.__move_text(cursor, QtGui.QTextCursor.Down)
        elif cursor.block() != self.document().lastBlock():
            self.__move_line(cursor, QtGui.QTextCursor.Down)

    def moveLeft(self, cursor = None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection() and cursor.selectionStart() != 0:
            self.__move_text(cursor, QtGui.QTextCursor.Left)

    def moveRight(self, cursor = None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection() and cursor.selectionEnd() != self.document().characterCount():
            self.__move_text(cursor, QtGui.QTextCursor.Right)

    #------ Select Text
    def selectText(self, cursor = None):
        cursor = cursor or self.textCursor()
        text, start, end = self.textUnderCursor(cursor, search = True)
        if text:
            self.setTextCursor(self.newCursorAtPosition(start, end))

    def selectWord(self, cursor = None):
        cursor = cursor or self.textCursor()
        word, start, end = self.wordUnderCursor(cursor, search = True)
        if word:
            self.setTextCursor(self.newCursorAtPosition(start, end))

    def selectLine(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(cursor)

    def selectParagraph(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.BlockUnderCursor)
        self.setTextCursor(cursor)

    def selectDocument(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)

    #------ Convert Text
    def __convert_text(self, cursor = None, convertFunction = lambda x: x):
        cursor = cursor or self.textCursor()
        tupleCursor = textcursor_to_tuple(cursor)
        cursor.beginEditBlock()
        if not cursor.hasSelection():
            word, start, end = self.wordUnderCursor(cursor = cursor, search = True)
            self.newCursorAtPosition(start, end).insertText(convertFunction(word))
        else:
            cursor.insertText(convertFunction(cursor.selectedText()))
        cursor.endEditBlock()
        self.setTextCursor(self.newCursorAtPosition(*tupleCursor))

    def convertToUppercase(self, cursor = None):
        self.__convert_text(cursor, text.upper_case)

    def convertToLowercase(self, cursor = None):
        self.__convert_text(cursor, text.lower_case)

    def convertToTitlecase(self, cursor = None):
        self.__convert_text(cursor, text.title_case)

    def convertToOppositeCase(self, cursor = None):
        self.__convert_text(cursor, text.opposite_case)

    def convertSpacesToTabs(self, cursor = None):
        self.__convert_text(cursor, text.spaces_to_tabs)

    def convertTabsToSpaces(self, cursor = None):
        self.__convert_text(cursor, text.tabs_to_spaces)

    def convertTranspose(self, cursor = None):
        self.__convert_text(cursor, text.transpose)

    #------ Set and Get Text
    def setPlainText(self, plainText):
        """Set the text of the editor"""
        QtWidgets.QPlainTextEdit.setPlainText(self, plainText)
        self.eol_chars = text.get_eol_chars(plainText)

    def toPlainTextWithEol(self):
        """Same as 'toPlainText', replace '\n' by correct end-of-line characters"""
        plainText = QtWidgets.QPlainTextEdit.toPlainText(self)
        return plainText.replace("\n", self.eolChars())

    def selectedTextWithEol(self, cursor = None):
        """
        Return text selected text cursor
        Replace the unicode line separator character \u2029 by
        the line separator characters returned by eolChars
        """
        cursor = cursor or self.textCursor()
        return cursor.selectedText().replace("\u2029", self.eolChars())

    def selectedText(self, cursor = None):
        """
        Return text selected text cursor
        Replace the unicode line separator character \u2029 by \n
        """
        cursor = cursor or self.textCursor()
        return cursor.selectedText().replace("\u2029", '\n')

    #------ Update Text
    def updatePlainText(self, text, cursor = None):
        if cursor:
            sourceText = cursor.selectedText()
            sourceOffset = cursor.selectionStart()
        else:
            sourceText = self.toPlainText()
            sourceOffset = 0

        def perform_action(code, cursor, text=""):
            def _nop():
                pass
            def _action():
                cursor.insertText(text)
            return _action if code in ["insert", "replace", "delete"] else _nop

        sequenceMatcher = difflib.SequenceMatcher(None, sourceText, text)
        opcodes = sequenceMatcher.get_opcodes()

        actions = [perform_action(
                code[0],
                self.newCursorAtPosition(code[1] + sourceOffset, code[2] + sourceOffset), text[code[3]:code[4]]
            ) for code in opcodes]

        cursor = self.textCursor()

        cursor.beginEditBlock()
        list(map(lambda action: action(), actions))
        cursor.endEditBlock()

        self.ensureCursorVisible()

    #------ Text Zoom
    def zoomIn(self):
        font = self.font()
        size = font.pointSize()
        if size >= self.FONT_MAX_SIZE:
            return
        size += 1
        font.setPointSize(size)
        self.setFont(font)

    def zoomOut(self):
        font = self.font()
        size = font.pointSize()
        if size <= self.FONT_MIN_SIZE:
            return
        size -= 1
        font.setPointSize(size)
        self.setFont(font)

    #------ Character width
    def characterWidth(self):
        return self.fontMetrics().width(self.CHARACTER)

    def characterHeight(self):
        return self.fontMetrics().height()
