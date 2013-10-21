#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

from prymatex.qt.helpers.keyevents import KEY_NUMBERS
from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor import helpers

class CodeEditorMultiCursorMode(CodeEditorBaseMode):
    def __init__(self, parent = None):
        CodeEditorBaseMode.__init__(self, parent)
        self.cursors = []
        self.selectedCursors = []
        self.scursor = self.dragPoint = self.startPoint = self.doublePoint = None
    
    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)
        # TODO: Buscar una forma mejor de obtener o trabajar con este helper en el modo, quiza filtarndo por clase en el evento
        helperInstances = editor.keyHelpersByClass(helpers.MultiCursorHelper)
        if helperInstances:
            self.helper = helperInstances[0]
        editor.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if self.isActive():
            if event.type() == QtCore.QEvent.KeyPress:
                self.keyPressEvent(event)
                return True
            elif event.type() == QtCore.QEvent.KeyRelease:
                self.keyReleaseEvent(event)
                return True
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.mousePressPoint(event.pos())
                return True
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.mouseReleasePoint(event.pos(), event.modifiers() & QtCore.Qt.MetaModifier)
                self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
                return True
            elif event.type() == QtCore.QEvent.MouseMove:
                self.mouseMovePoint(event.pos())
                self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
                return True
        elif event.type() == QtCore.QEvent.MouseButtonPress and bool(event.modifiers() & QtCore.Qt.ControlModifier):
            self.mousePressPoint(event.pos())
            return True
        elif event.type() == QtCore.QEvent.MouseMove and bool(event.modifiers() & QtCore.Qt.ControlModifier):
            self.mouseMovePoint(event.pos())
            self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
            return True
        if event.type() == QtCore.QEvent.Paint and (self.isActive() or self.isDragCursor()):
            self.paintEvent(event)
            return True
        return False

    def isActive(self):
        return bool(self.cursors) or self.startPoint != None
    
    def inactive(self):
        self.cursors = []
        self.selectedCursors = []
        self.editor.application.restoreOverrideCursor()
        self.editor.modeChanged.emit("")

    def paintEvent(self, event):
        self.editor.paintEvent(event)
        painter = QtGui.QPainter(self.editor.viewport())
        font_metrics = self.editor.fontMetrics()
        ctrl_down = bool(self.application.keyboardModifiers() & QtCore.Qt.ControlModifier)
        
        for index, cursor in enumerate(self.cursors, 1):
            rec = self.editor.cursorRect(cursor)
            fakeCursor = QtCore.QLine(rec.x(), rec.y(), rec.x(), rec.y() + font_metrics.ascent() + font_metrics.descent())
            colour = self.editor.colours['caret']
            painter.setPen(QtGui.QPen(colour))
            if ctrl_down:
                painter.drawText(rec.x() + 2, rec.y() + font_metrics.ascent(), str(index))
            if (self.hasSelection() and not self.isSelected(cursor)) or \
            (ctrl_down and not self.hasSelection()):
                 colour = self.editor.colours['selection']
            painter.setPen(QtGui.QPen(colour))
            painter.drawLine(fakeCursor)
        
        if self.isDragCursor():
            pen = QtGui.QPen(self.editor.colours['caret'])
            pen.setWidth(2)
            painter.setPen(pen)
            color = QtGui.QColor(self.editor.colours['selection'])
            color.setAlpha(128)
            painter.setBrush(QtGui.QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(self.getDragCursorRect())
        painter.end()
                            
    def highlightEditor(self):
        cursors = {}
        self.editor.setExtraSelectionCursors("selection", [c for c in [QtGui.QTextCursor(c) for c in self.cursors] if c.hasSelection()])
        cursorLines = []
        for cursorLine in [QtGui.QTextCursor(c) for c in self.cursors]:
            if all([c.block() != cursorLine.block() for c in cursorLines]):
                cursorLine.clearSelection()
                cursorLines.append(cursorLine)
        self.editor.setExtraSelectionCursors("line", cursorLines)
        self.editor.updateExtraSelections()

    def isDragCursor(self):
        return self.startPoint != None and self.dragPoint != None

    def isSelected(self, cursor):
        return cursor in self.selectedCursors
    
    def hasSelection(self):
        return bool(self.selectedCursors)
        
    def activeCursors(self):
        if self.selectedCursors:
            return self.selectedCursors
        return self.cursors
        
    def getDragCursorRect(self):
        """Retorna un rectángulo que representa la zona del drag cursor"""
        return QtCore.QRect(self.startPoint, self.dragPoint)
    
    def mousePressPoint(self, point):
        self.startPoint = point

    def mouseDoubleClickPoint(self, point):
        self.doublePoint = point
        
    def mouseMovePoint(self, point):
        self.dragPoint = point

    def mouseReleasePoint(self, endPoint, remove = False):
        _, width, points = self.getPoints(self.startPoint, endPoint)
        
        multicursorAction = self.addMergeCursor if not remove else self.removeBreakCursor
        lastCursor = None
        for tupla in points:
            if tupla[0] == tupla[1]:
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*tupla[0]))
                multicursorAction(cursor)
                continue
            #Sentido en el que queda el cursor
            if self.startPoint.x() < endPoint.x():  #izquierda a derecha
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        cursor.setPosition(ecursor.position(), QtGui.QTextCursor.KeepAnchor)
                        if lastCursor is None or (lastCursor.position() != cursor.position()):
                            multicursorAction(cursor)
                            lastCursor = cursor
            else: # Derecha a izquierda
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        ecursor.setPosition(cursor.position(), QtGui.QTextCursor.KeepAnchor)
                        if lastCursor is None or (lastCursor.position() != ecursor.position()):
                            multicursorAction(ecursor)
                            lastCursor = ecursor
        
        #Clean last acction
        self.scursor = self.dragPoint = self.startPoint = self.doublePoint = None

    def getPoints(self, start, end):
        #TODO: Ver de mejorar las medidas porque esta salteando lineas de seleccion
        metrics = QtGui.QFontMetrics(self.editor.document().defaultFont())
        hight = metrics.lineSpacing()
        width = metrics.width("x")
        sx, ex = (start.x(), end.x()) if start.x() <= end.x() else (end.x(), start.x())
        sy, ey = (start.y(), end.y()) if start.y() <= end.y() else (end.y(), start.y())
        puntos = [ ( (sx, sy), (ex, sy) ) ]
        p = sy + hight
        e = ey - hight
        while p <= e:
            puntos.append( ( (sx, p), (ex, p) ) )
            p += hight
        puntos.append( ( (sx, ey), (ex, ey) ) )
        return hight, width, puntos
        
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
            self.editor.application.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
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
        if self.helper.accept(event):
            cursor = self.cursors[0] if event.modifiers() & QtCore.Qt.ShiftModifier else self.cursors[-1]
            self.helper.execute(event, cursor)
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
    
    def keyReleaseEvent(self, event):
        self.editor.viewport().repaint(self.editor.viewport().visibleRegion())
        return False