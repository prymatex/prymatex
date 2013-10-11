#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditorAddon

from prymatex.qt.helpers.keyevents import KEY_NUMBERS
from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor import helpers
from prymatex.models.support import BundleItemTreeNode

class CodeEditorBaseMode(PMXBaseEditorAddon):
    def __init__(self, editor):
        self.editor = editor

    def active(self, event, scope):
        pass
    
    def isActive(self):
        return False

    def inactive(self):
        pass
    
    # ------------ Mouse Events
    def mousePressEvent(self, event):
        return self.editor.mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        return self.editor.mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        return self.editor.mouseReleaseEvent(event)
        
    # ------------ Key Events
    def keyPressEvent(self, event):
        return self.editor.keyPressEvent(event)
        
    def keyReleaseEvent(self, event):
        return self.editor.keyReleaseEvent(event)

class PMXSnippetEditorMode(CodeEditorBaseMode):
    def __init__(self, editor):
        CodeEditorBaseMode.__init__(self, editor)
        self.logger = editor.application.getLogger('.'.join([self.__class__.__module__, self.__class__.__name__]))

    @property
    def snippet(self):
        return self.editor.snippetProcessor.snippet

    def isActive(self):
        return self.snippet is not None

    def inactive(self):
        self.endSnippet()

    def keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Escape:
            self.logger.debug("Se termina el modo snippet")
            return self.endSnippet(event)
        elif event.key() in [ QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab ]:
            self.logger.debug("Camino entre los holders")
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.endSnippet(event)

            if event.key() == QtCore.Qt.Key_Tab:
                ok = self.snippet.nextHolder()
            else:
                ok = self.snippet.previousHolder()
            if not ok:
                self.editor.showMessage("Snippet end")
                self.editor.snippetProcessor.selectHolder()
                self.endSnippet()
            else:
                self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (self.snippet.name, self.snippet.holderNumber(), len(self.snippet)))
                self.editor.snippetProcessor.selectHolder()
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.endSnippet(event)
            
            holderStart, holderEnd = self.snippet.currentPosition()
            #Cuidado con los extremos del holder
            if not cursor.hasSelection():
                if event.key() == QtCore.Qt.Key_Backspace and cursor.position() == holderStart:
                    return self.endSnippet(event)

                if event.key() == QtCore.Qt.Key_Delete and cursor.position() == holderEnd:
                    return self.endSnippet(event)

            holderPosition = cursor.selectionStart() - holderStart
            positionBefore = cursor.selectionStart()
            charactersBefore = cursor.document().characterCount()
            
            #Insert Text
            cursor.beginEditBlock()
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = charactersBefore - charactersAfter 
            
            #Capture Text
            cursor.setPosition(holderStart)
            cursor.setPosition(holderEnd - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = self.editor.selectedTextWithEol(cursor)

            self.snippet.setContent(selectedText)
            
            # Wrap snippet
            wrapCursor = self.editor.newCursorAtPosition(
                self.editor.snippetProcessor.startPosition(), self.editor.snippetProcessor.endPosition() - length
            )
            
            #Insert snippet
            self.editor.snippetProcessor.render(wrapCursor)
            
            #if selectedText:
            newHolderStart, _ = self.snippet.currentPosition()
            self.editor.setTextCursor(
                self.editor.newCursorAtPosition(
                    newHolderStart + holderPosition + (positionAfter - positionBefore)
                )
            )
            #elif self.snippet.nextHolder():
                # The holder is killed
            #    self.editor.snippetProcessor.selectHolder()
            if selectedText and self.snippet.lastHolder():
                # Put text on last holder, force snippet ends
                self.endSnippet()
            cursor.endEditBlock()
        else:
            self.logger.debug("Con cualquier otra tecla sin texto")
            return QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            
    def endSnippet(self, event = None):
        self.editor.snippetProcessor.endSnippet(self.editor.snippetProcessor.snippet)
        if event is not None:
            return self.editor.keyPressEvent(event)

class PMXMultiCursorEditorMode(CodeEditorBaseMode):
    def __init__(self, editor):
        CodeEditorBaseMode.__init__(self, editor)
        # TODO: Buscar una forma mejor de obtener o trabajar con este helper en el modo, quiza filtarndo por clase en el evento
        self.helper = helpers.MultiCursorHelper()
        self.helper.initialize(editor)
        self.cursors = []
        self.selectedCursors = []
        self.scursor = self.dragPoint = self.startPoint = self.doublePoint = None
    
    def isActive(self):
        return bool(self.cursors) or self.startPoint != None
    
    def inactive(self):
        self.cursors = []
        self.selectedCursors = []
        self.editor.application.restoreOverrideCursor()
        self.editor.modeChanged.emit()

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

    @property
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
            self.editor.modeChanged.emit()
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
        QtGui.QPlainTextEdit.keyReleaseEvent(self.editor, event)
