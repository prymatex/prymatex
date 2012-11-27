#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re

from prymatex.qt import QtGui, QtCore

class TextEditWidget(QtGui.QPlainTextEdit):
    RE_MAGIC_FORMAT_BUILDER = re.compile(r"textCharFormat_([A-Za-z]+)_builder", re.UNICODE)
    #------ Signals
    extraSelectionChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        
        # TODO: Buscar sobre este atributo en la documnetación
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.scopedExtraSelections = {}
        self.textCharFormatBuilders = {}
        self.registerTextCharFormatBuildersByName()

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

    #------ Cursors
    def newCursorAtPosition(self, position, anchor = None):
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(position)
        if anchor is not None:
            cursor.setPosition(anchor, QtGui.QTextCursor.KeepAnchor)
        return cursor
        
    #------ Extra selections
    def registerTextCharFormatBuildersByName(self):
        for method in dir(self):
            match = self.RE_MAGIC_FORMAT_BUILDER.match(method)
            if match:
                self.registerTextCharFormatBuilder("%s" % match.group(1), getattr(self, method))

    def registerTextCharFormatBuilder(self, scope, formatBuilder):
        self.textCharFormatBuilders[scope] = formatBuilder
    
    def defaultTextCharFormatBuilder(self, scope):
        return QtGui.QTextCharFormat()

    def extendExtraSelectionCursors(self, scope, cursors):
        self.scopedExtraSelections.setdefault(scope, []).extend(self.__build_extra_selections(scope, cursors))

    def setExtraSelectionCursors(self, scope, cursors):
        self.scopedExtraSelections[scope] = self.__build_extra_selections(scope, cursors)
    
    def updateExtraSelectionCursors(self, cursorsDict):
        map(lambda (scope, cursors): self.setExtraSelectionCursors(scope, cursors), cursorsDict.iteritems())
    
    def updateExtraSelections(self, order = []):
        extraSelections = []
        for scope in order:
            extraSelections.extend(self.scopedExtraSelections[scope])
        for scope, extra in self.scopedExtraSelections.iteritems():
            if scope not in order:
                extraSelections.extend(extra)
        self.setExtraSelections(extraSelections)
        self.extraSelectionChanged.emit()
        
    def searchExtraSelections(self, scope):
        cursors = filter(lambda (s, _): s.startswith(scope), self.scopedExtraSelections.iteritems())
        return reduce(lambda c1, (_, c2): c1 + c2, cursors, [])    
    
    def clearExtraSelectionCursors(self, scope):
        del self.scopedExtraSelections[scope]
        
    def clearExtraSelections(self):
        self.scopedExtraSelections.clear()
        self.updateExtraSelections()
        
    def __build_extra_selections(self, scope, cursors):
        extraSelections = []
        for cursor in cursors:
            selection = QtGui.QTextEdit.ExtraSelection()
            if scope in self.textCharFormatBuilders:
                # TODO: un FORMAT_CACHE
                selection.format = self.textCharFormatBuilders[scope]()
            else:
                selection.format = self.defaultTextCharFormatBuilder(scope)
            selection.cursor = cursor
            extraSelections.append(selection)
        return extraSelections
