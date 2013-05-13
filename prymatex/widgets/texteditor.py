#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re
import difflib

from prymatex.utils import text

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import textcursor2tuple
from functools import reduce

class TextEditWidget(QtGui.QPlainTextEdit):
    #------ Signals
    extraSelectionChanged = QtCore.pyqtSignal()
    fontChanged = QtCore.pyqtSignal()
    
    #------ Regular expresions
    RE_WORD = re.compile(r"([A-Za-z_]\w+\b)", re.UNICODE)
    
    def __init__(self, parent = None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        
        # TODO: Buscar sobre este atributo en la documnetación
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.__scopedExtraSelections = {}
        self.__updateExtraSelectionsOrder = []
        self.__textCharFormatBuilders = {}

    #------ Overrides
    def setFont(self, font):
        QtGui.QPlainTextEdit.setFont(self, font)
        self.fontChanged.emit()

    #------ Retrieve text
    def wordUnderCursor(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return cursor.selectedText(), cursor.selectionStart(), cursor.selectionEnd()

    def currentWord(self, direction = "both", search = True):
        return self.word(cursor = self.textCursor(), direction = direction, search = search)
        
    def word(self, cursor = None, pattern = RE_WORD, direction = "both", search = True):
        cursor = cursor or self.textCursor()
        line = cursor.block().text()
        position = cursor.position()
        columnNumber = cursor.columnNumber()
        #Get text before and after the cursor position.
        first_part, last_part = line[:columnNumber][::-1], line[columnNumber:]
        
        #Try left word
        lword = rword = ""
        m = pattern.match(first_part)
        if m and direction in ("left", "both"):
            lword = m.group(0)[::-1]
        #Try right word
        m = pattern.match(last_part)
        if m and direction in ("right", "both"):
            rword = m.group(0)
        
        if lword or rword:
            return lword + rword, position - len(lword), position + len(rword)
        
        if not search: 
            return "", position, position

        lword = rword = ""
        #Search left word
        for i in range(len(first_part)):
            lword += first_part[i]
            m = pattern.search(first_part[i + 1:])
            if m and m.group(0):
                lword += m.group(0)
                break
        lword = lword[::-1]
        #Search right word
        for i in range(len(last_part)):
            rword += last_part[i]
            m = pattern.search(last_part[i:])
            if m and m.group(0):
                rword += m.group(0)
                break
        lword = lword.lstrip()
        rword = rword.rstrip()
        return lword + rword, position - len(lword), position + len(rword)

    #------ Retrieve cursors and blocks
    def newCursorAtPosition(self, position, anchor = None):
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(position)
        if anchor is not None:
            cursor.setPosition(anchor, QtGui.QTextCursor.KeepAnchor)
        return cursor

    def selectionBlockStartEnd(self, cursor = None):
        cursor = cursor or self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start > end:
            return self.document().findBlock(end), self.document().findBlock(start)
        else:
            return self.document().findBlock(start), self.document().findBlock(end)

    #------ Find and Replace
    def findTypingPair(self, b1, b2, cursor, backward = False):
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
    def registerTextCharFormatBuilder(self, scope, formatBuilder):
        # TODO Un poco mejor esto para soportar subscopes con puntos
        self.__updateExtraSelectionsOrder.append(scope)
        self.__textCharFormatBuilders[scope] = formatBuilder
    
    def defaultTextCharFormatBuilder(self, scope):
        return QtGui.QTextCharFormat()

    def extendExtraSelectionCursors(self, scope, cursors):
        self.__scopedExtraSelections.setdefault(scope, []).extend(self.__build_extra_selections(scope, cursors))

    def setExtraSelectionCursors(self, scope, cursors):
        self.__scopedExtraSelections[scope] = self.__build_extra_selections(scope, cursors)
    
    def updateExtraSelectionCursors(self, cursorsDict):
        list(map(lambda scope_cursors: self.setExtraSelectionCursors(scope_cursors[0], scope_cursors[1]), iter(cursorsDict.items())))
    
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
            selection = QtGui.QTextEdit.ExtraSelection()
            if scope in self.__textCharFormatBuilders:
                # TODO: un FORMAT_CACHE
                selection.format = self.__textCharFormatBuilders[scope]()
            else:
                selection.format = self.defaultTextCharFormatBuilder(scope)
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
        otherBlock = next(cursor.block()) if moveType == QtGui.QTextCursor.Down else cursor.block().previous()
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
    def selectWordUnder(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
        
    def selectWordCurrent(self, cursor = None):
        cursor = cursor or self.textCursor()
        _, start, end = self.word(cursor = cursor)
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
        tupleCursor = textcursor2tuple(cursor)
        cursor.beginEditBlock()
        if not cursor.hasSelection():
            word, start, end = self.word(cursor = cursor)
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
    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
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
