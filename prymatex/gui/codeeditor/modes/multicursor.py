#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

from prymatex.qt.helpers.keyevents import KEY_NUMBERS
from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor.helpers import CodeEditorKeyHelper

WIDTH_CHARACTER = '#'

# ==================================
# Helper for MultiCursor
# ==================================
class MultiCursorHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_M
    def __init__(self, multiCursorMode):
        CodeEditorKeyHelper.__init__(self, multiCursorMode)
        self.multiCursorMode = multiCursorMode

    def accept(self, event, cursor = None):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return event.key() == self.KEY and control_down and meta_down

    def execute(self, event, cursor = None):
        cursor = cursor or self.editor.textCursor()
        flags = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
        if not cursor.hasSelection():
            text, start, end = self.editor.currentWord()
            newCursor = QtGui.QTextCursor(cursor)
            newCursor.setPosition(start)
            newCursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            self.multiCursorMode.addMergeCursor(newCursor)
        else:
            text = cursor.selectedText()
            self.multiCursorMode.addMergeCursor(cursor)
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                flags |= QtGui.QTextDocument.FindBackward
            newCursor = self.editor.document().find(text, cursor, flags)
            if not newCursor.isNull():
                self.multiCursorMode.addMergeCursor(newCursor)
                self.editor.centerCursor(newCursor)

class CodeEditorMultiCursorMode(CodeEditorBaseMode):
    def __init__(self, parent = None):
        CodeEditorBaseMode.__init__(self, parent)
        self.keyHelper = MultiCursorHelper(self)
        self.cursors = []
        self.selectedCursors = []
        self.draggedCursors = []
        self.scursor = self.startPoint = self.doublePoint = None

    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)
        self.editor.installEventFilter(self)
        self.editor.viewport().installEventFilter(self)
        # Helper
        self.keyHelper.initialize(editor)
        self.editor.addKeyHelper(self.keyHelper)
        # Formater
        editor.registerTextCharFormatBuilder("dragged", self.textCharFormat_dragged_builder)
        
    def eventFilter(self, obj, event):
        if self.isActive() and event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        elif self.isActive() and event.type() == QtCore.QEvent.MouseButtonRelease and event.modifiers() & QtCore.Qt.ControlModifier:
            self.mouseReleasePoint(event.pos(), event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.modifiers() & QtCore.Qt.ControlModifier:
            self.mousePressPoint(event.pos(), event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        elif event.type() == QtCore.QEvent.MouseMove and bool(event.modifiers() & QtCore.Qt.ControlModifier):
            self.mouseMovePoint(event.pos(), event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        return False

    def textCharFormat_dragged_builder(self):
        textCharFormat = self.editor.textCharFormat_selection_builder()
        textCharFormat.setBackground(self.editor.colours['lineHighlight'])
        return textCharFormat
        
    def isActive(self):
        return bool(self.cursors) or self.startPoint != None

    def inactive(self):
        self.cursors = []
        self.selectedCursors = []
        self.editor.modeChanged.emit("")

    def highlightEditor(self):
        cursors = {}
        self.editor.setExtraSelectionCursors("dragged", [c for c in [QtGui.QTextCursor(c) for c in self.draggedCursors] if c.hasSelection()])
        self.editor.setExtraSelectionCursors("selection", [c for c in [QtGui.QTextCursor(c) for c in self.cursors] if c.hasSelection()])
        cursorLines = []
        for cursorLine in [QtGui.QTextCursor(c) for c in self.cursors]:
            if all([c.block() != cursorLine.block() for c in cursorLines]):
                cursorLine.clearSelection()
                cursorLines.append(cursorLine)
        self.editor.setExtraSelectionCursors("line", cursorLines)
        self.editor.updateExtraSelections()

    def isSelected(self, cursor):
        return cursor in self.selectedCursors

    def hasSelection(self):
        return bool(self.selectedCursors)

    def activeCursors(self):
        if self.selectedCursors:
            return self.selectedCursors
        return self.cursors

    def mousePressPoint(self, point, remove = False):
        self.startPoint = point
        self.application.setOverrideCursor(QtGui.QCursor(remove and QtCore.Qt.CrossCursor or QtCore.Qt.ArrowCursor))

    def mouseMovePoint(self, dragPoint, remove = False):
        self.draggedCursors = []
        
        metrics = self.editor.fontMetrics()
        hight = metrics.lineSpacing()
        width = metrics.width(WIDTH_CHARACTER)

        lastCursor = None
        for start, end in self.getPoints(self.startPoint, dragPoint, hight):
            #Sentido en el que queda el cursor
            if self.startPoint.x() > dragPoint.x():  #derecha a izquierda
                start, end = end, start
            cursor = self.editor.newCursorAtPosition(QtCore.QPoint(*start),
                QtCore.QPoint(*end))
            if lastCursor is None or (lastCursor.position() != cursor.position()):
                self.draggedCursors.append(cursor)
                lastCursor = cursor
        self.highlightEditor()
    
    def mouseReleasePoint(self, endPoint, remove = False):
        multicursorAction = self.addMergeCursor if not remove else self.removeBreakCursor
        for cursor in self.draggedCursors:
            multicursorAction(cursor)

        #Clean last acction
        self.draggedCursors = []
        self.scursor = self.startPoint = self.doublePoint = None
        self.application.restoreOverrideCursor()
        self.highlightEditor()

    def getPoints(self, start, end, hight):
        sx, ex = (start.x(), end.x()) if start.x() <= end.x() else (end.x(), start.x())
        sy, ey = (start.y(), end.y()) if start.y() <= end.y() else (end.y(), start.y())
        yield ( (sx, sy), (ex, sy) )
        p = sy + hight
        e = ey - hight
        while p <= e:
            yield ( (sx, p), (ex, p) ) 
            p += hight
        yield ( (sx, ey), (ex, ey) )

    def addMergeCursor(self, cursor):
        """Only can add new cursors, if the cursor has selection then try to merge with others"""
        firstCursor = not bool(self.cursors)
        if cursor.hasSelection():
            newCursor = None
            removeCursor = None
            new_begin, new_end = cursor.selectionStart(), cursor.selectionEnd()
            for c in self.cursors:
                c_begin, c_end = c.selectionStart(), c.selectionEnd()
                if c_begin <= new_begin <= new_end <= c_end:
                    return
                elif c_begin <= new_begin <= c_end:
                    # Extiende por detras
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    if c.position() > new_begin:
                        newCursor.setPosition(c_begin)
                        newCursor.setPosition(new_end, QtGui.QTextCursor.KeepAnchor)
                    else:
                        newCursor.setPosition(new_end)
                        newCursor.setPosition(c.position(), QtGui.QTextCursor.KeepAnchor)
                    removeCursor = c
                    break
                elif c_begin <= new_end <= c_end:
                    #Extiende por el frente
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    if c.position() < new_end:
                        newCursor.setPosition(c_end)
                        newCursor.setPosition(new_begin, QtGui.QTextCursor.KeepAnchor)
                    else:
                        newCursor.setPosition(new_begin)
                        newCursor.setPosition(c.position(), QtGui.QTextCursor.KeepAnchor)
                    removeCursor = c
                    break
                elif new_begin <= c_begin <= c_end <= new_end:
                    #Contiene al cursor
                    newCursor = cursor
                    removeCursor = c
                    break
            if newCursor is not None:
                self.cursors.remove(removeCursor)
                self.addMergeCursor(newCursor)
            else:
                position = bisect_key(self.cursors, cursor, lambda cursor: cursor.position())
                self.cursors.insert(position, cursor)
        else:
            for c in self.cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if begin <= cursor.position() <= end:
                    return
            position = bisect_key(self.cursors, cursor, lambda cursor: cursor.position())
            self.cursors.insert(position, cursor)
        if firstCursor:
            #Ponemos el ultimo cursor agregado sin seleccion para que no moleste
            lastCursor = QtGui.QTextCursor(self.cursors[-1])
            lastCursor.clearSelection()
            self.editor.setTextCursor(lastCursor)
            self.editor.modeChanged.emit("multicursor")
        self.highlightEditor()

    def removeBreakCursor(self, cursor):
        #TODO: Hay cosas que se pueden simplificar pero hoy no me da el cerebro
        if cursor.hasSelection():
            newCursors = []
            removeCursor = None
            new_begin, new_end = cursor.selectionStart(), cursor.selectionEnd()
            for c in self.cursors:
                c_begin, c_end = c.selectionStart(), c.selectionEnd()
                if new_begin <= c_begin <= c_end <= new_end:
                    #Contiene al cursor, hay que quitarlo
                    removeCursor = c
                    break
                elif (c_begin < new_begin < new_end < c_end):
                    #Recortar
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    if c.position() < new_begin:
                        newCursor.setPosition(new_begin)
                        newCursor.setPosition(c_begin, QtGui.QTextCursor.KeepAnchor)
                        newCursors.append(newCursor)
                        newCursor = QtGui.QTextCursor(self.editor.document())
                        newCursor.setPosition(c_end)
                        newCursor.setPosition(new_end, QtGui.QTextCursor.KeepAnchor)
                        newCursors.append(newCursor)
                    else:
                        newCursor.setPosition(c_begin)
                        newCursor.setPosition(new_begin, QtGui.QTextCursor.KeepAnchor)
                        newCursors.append(newCursor)
                        newCursor = QtGui.QTextCursor(self.editor.document())
                        newCursor.setPosition(new_end)
                        newCursor.setPosition(c_end, QtGui.QTextCursor.KeepAnchor)
                        newCursors.append(newCursor)
                    removeCursor = c
                    break
                elif c_begin <= new_begin <= c_end:
                    #Recorta por detras, quitar el actual y agregar uno con la seleccion mas chica
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    if c.position() > new_begin:
                        newCursor.setPosition(c_begin)
                        newCursor.setPosition(new_begin, QtGui.QTextCursor.KeepAnchor)
                    else:
                        newCursor.setPosition(new_begin)
                        newCursor.setPosition(c.position(), QtGui.QTextCursor.KeepAnchor)
                    newCursors.append(newCursor)
                    removeCursor = c
                    break
                elif c_begin <= new_end <= c_end:
                    #Recorta por el frente, quitra el actual y agregar uno con la seleccion mas chica
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    if c.position() < new_end:
                        newCursor.setPosition(c_end)
                        newCursor.setPosition(new_end, QtGui.QTextCursor.KeepAnchor)
                    else:
                        newCursor.setPosition(new_end)
                        newCursor.setPosition(c.position(), QtGui.QTextCursor.KeepAnchor)
                    newCursors.append(newCursor)
                    removeCursor = c
                    break
            if removeCursor is not None:
                self.cursors.remove(removeCursor)
            for cursors in newCursors:
                position = bisect_key(self.cursors, cursors, lambda cursor: cursor.position())
                self.cursors.insert(position, cursors)
        else:
            #Solo puedo quitar cursores que no tengan seleccion osea que sean un clic :)
            for c in self.cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if not c.hasSelection() and c.position() == cursor.position():
                    self.cursors.remove(c)
                    break
        self.highlightEditor()

    def canMoveRight(self):
        return not self.cursors[-1].atEnd()

    def canMoveLeft(self):
        return not self.cursors[0].atStart()

    def keyPressEvent(self, event):
        if bool(event.modifiers() & QtCore.Qt.ControlModifier):
            self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
        if self.keyHelper.accept(event):
            cursor = self.cursors[0] if event.modifiers() & QtCore.Qt.ShiftModifier else self.cursors[-1]
            self.keyHelper.execute(event, cursor)
        elif event.key() == QtCore.Qt.Key_Escape:
            #Deprecated usar una lista de cursores ordenados para tomar de [0] y [-1]
            firstCursor = self.cursors[0]
            lastCursor = self.cursors[-1]
            self.editor.document().markContentsDirty(firstCursor.position(), lastCursor.position())
            if lastCursor.hasSelection():
                lastCursor.clearSelection()
            self.editor.setTextCursor(lastCursor)
            self.inactive()
            self.highlightEditor()
            #Se termino la joda
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() in [ QtCore.Qt.Key_Z]:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
        elif bool(event.modifiers() & QtCore.Qt.ControlModifier) and event.key() in KEY_NUMBERS:
            #Seleccionamos cursores de la multiseleccion
            index = KEY_NUMBERS.index(event.key())
            if index == 0:
                if bool(event.modifiers() & QtCore.Qt.MetaModifier) and self.selectedCursors:
                    #Toggle
                    self.selectedCursors = list(set(self.cursors).difference(self.selectedCursors))
                else:
                    #Remove
                    self.selectedCursors = []
            elif index <= len(self.cursors):
                index = index - 1
                cursor = self.cursors[index]
                if bool(event.modifiers() & QtCore.Qt.MetaModifier):
                    self.selectedCursors = [cursor]
                elif cursor in self.selectedCursors:
                    self.selectedCursors.remove(cursor)
                else:
                    self.selectedCursors.append(cursor)
            self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
        elif event.key() == QtCore.Qt.Key_Right:
            if self.canMoveRight():
                mode = QtGui.QTextCursor.KeepAnchor if bool(event.modifiers() & QtCore.Qt.ShiftModifier) else QtGui.QTextCursor.MoveAnchor
                for cursor in self.activeCursors():
                    if event.modifiers() & QtCore.Qt.ControlModifier:
                        cursor.movePosition(QtGui.QTextCursor.NextWord, mode)
                    else:
                        cursor.movePosition(QtGui.QTextCursor.NextCharacter, mode)
                self.editor.setTextCursor(self.editor.newCursorAtPosition(cursor.position()))
                self.highlightEditor()
        elif event.key() == QtCore.Qt.Key_Left:
            if self.canMoveLeft():
                mode = QtGui.QTextCursor.KeepAnchor if bool(event.modifiers() & QtCore.Qt.ShiftModifier) else QtGui.QTextCursor.MoveAnchor
                for cursor in self.activeCursors():
                    if event.modifiers() & QtCore.Qt.ControlModifier:
                        cursor.movePosition(QtGui.QTextCursor.PreviousWord, mode)
                    else:
                        cursor.movePosition(QtGui.QTextCursor.PreviousCharacter, mode)
                self.editor.setTextCursor(self.editor.newCursorAtPosition(cursor.position()))
                self.highlightEditor()
        elif event.key() in [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_End, QtCore.Qt.Key_Home]:
            #Desactivados por ahora
            pass
        elif event.key() in [QtCore.Qt.Key_Insert]:
            self.editor.setOverwriteMode(not self.editor.overwriteMode())
        elif event.text():
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            for cursor in self.activeCursors():
                self.editor.setTextCursor(cursor)
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            cursor.endEditBlock()
