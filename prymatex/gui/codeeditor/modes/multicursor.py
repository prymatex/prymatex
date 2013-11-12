#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources

from .base import CodeEditorBaseMode

from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor.helpers import CodeEditorKeyHelper

WIDTH_CHARACTER = '#'

class CodeEditorMultiCursorMode(CodeEditorBaseMode):
    def __init__(self, parent = None):
        CodeEditorBaseMode.__init__(self, parent)
        self.cursors = []
        self.draggedCursors = []
        self.scursor = self.startPoint = self.doublePoint = None

    # ------- Overrides
    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)
        self.editor.installEventFilter(self)
        self.editor.viewport().installEventFilter(self)
        # Formater
        editor.registerTextCharFormatBuilder("dragged", self.textCharFormat_dragged_builder)
    
    def isActive(self):
        return bool(self.cursors) or self.startPoint != None

    def inactive(self, handled):
        self.cursors = []
        self.editor.modeChanged.emit("")
        self.highlightEditor()
        return handled
    
    # ------- Text char format builder
    def textCharFormat_dragged_builder(self):
        textCharFormat = self.editor.textCharFormat_selection_builder()
        textCharFormat.setBackground(self.editor.colours['lineHighlight'])
        return textCharFormat
        
    # ------- Handle events
    def eventFilter(self, obj, event):
        if self.isActive() and event.type() == QtCore.QEvent.KeyPress:
            return self.keyPressEvent(event)
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
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            #Deprecated usar una lista de cursores ordenados para tomar de [0] y [-1]
            firstCursor = self.cursors[0]
            lastCursor = self.cursors[-1]
            self.editor.document().markContentsDirty(firstCursor.position(), lastCursor.position())
            if lastCursor.hasSelection():
                lastCursor.clearSelection()
            self.editor.setTextCursor(lastCursor)
            return self.inactive(True)
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
                return True
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
                return True
        elif event.key() in [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_End, QtCore.Qt.Key_Home]:
            #Desactivados por ahora
            pass
        elif event.text():
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            for cursor in self.activeCursors():
                self.editor.setTextCursor(cursor)
                self.editor.keyPressEvent(event)
            cursor.endEditBlock()
            return True
        return False

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

    def activeCursors(self):
        return self.cursors

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
                    if c.position() < new_begin:
                        newCursors.append(
                            self.editor.newCursorAtPosition(new_begin, c_begin))
                        newCursors.append(
                            self.editor.newCursorAtPosition(c_end, new_end))    
                    else:
                        newCursors.append(
                            self.editor.newCursorAtPosition(c_begin, new_begin))
                        newCursors.append(
                            self.editor.newCursorAtPosition(new_end, c_end))
                    removeCursor = c
                    break
                elif c_begin <= new_begin <= c_end:
                    #Recorta por detras, quitar el actual y agregar uno con la seleccion mas chica
                    if c.position() > new_begin:
                        newCursors.append(
                            self.editor.newCursorAtPosition(c_begin, new_begin))
                    else:
                        newCursors.append(
                            self.editor.newCursorAtPosition(new_begin, c.position()))
                    removeCursor = c
                    break
                elif c_begin <= new_end <= c_end:
                    #Recorta por el frente, quitra el actual y agregar uno con la seleccion mas chica
                    if c.position() < new_end:
                        newCursors.append(
                            self.editor.newCursorAtPosition(c_end, new_end))
                    else:
                        newCursors.append(
                            self.editor.newCursorAtPosition(new_end, c.position()))
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

    def findCursor(self, backward = False):
        if not self.isActive():
            cursor = self.editor.textCursor()
        else:
            cursor = self.cursors[0] if backward else self.cursors[-1]
        if not cursor.hasSelection():
            text, start, end = self.editor.currentWord()
            newCursor = self.editor.newCursorAtPosition(start, end)
            self.addMergeCursor(newCursor)
        else:
            text = cursor.selectedText()
            flags = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
            if backward:
                flags |= QtGui.QTextDocument.FindBackward
            newCursor = self.editor.document().find(text, cursor, flags)
            if not newCursor.isNull():
                self.addMergeCursor(newCursor)
                self.editor.centerCursor(newCursor)
    
    def contributeToShortcuts(self):
        return [{
            "sequence": resources.get_sequence("Multiedit", "FindForwardCursor", "Ctrl+Meta+M"),
            "activated": lambda : self.findCursor()
        }, {
            "sequence": resources.get_sequence("Multiedit", "FindBackwardCursor", "Ctrl+Meta+Shift+M"),
            "activated": lambda : self.findCursor(True)
        }]