#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

from prymatex.utils.lists import bisect_key

def build_point_matrix(start, end, hight):
    offset = hight / 2
    sx, ex = start.x(), end.x()
    sy, ey = start.y() + offset, end.y() + offset
    yield ( (sx, sy), (ex, sy) )
    p = sy + hight
    while p <= ey:
        yield ( (sx, p), (ex, p) ) 
        p += hight
    
class CodeEditorMultiCursorMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorMultiCursorMode, self).__init__(**kwargs)
        self.draggedCursors = []
        self.startPoint = self.doublePoint = None
        self.standardCursor = None

    def name(self):
        return "MULTICURSOR"

    # ------- Overrides
    def initialize(self, **kwargs):
        super(CodeEditorMultiCursorMode, self).initialize(**kwargs)
        self.editor.installEventFilter(self)
        self.editor.viewport().installEventFilter(self)
        self.standardCursor = self.editor.viewport().cursor()

        # ------------ Handlers
        self.registerKeyPressHandler(QtCore.Qt.Key_Escape, self.__multicursor_end)
        self.registerKeyPressHandler(QtCore.Qt.Key_Right, self.__move_cursors)
        self.registerKeyPressHandler(QtCore.Qt.Key_Left, self.__move_cursors)

    def activate(self):
        CodeEditorBaseMode.activate(self)
        self.editor.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

    def deactivate(self):
        self.draggedCursors = []
        self.editor.setExtraCursors([])
        self.editor.viewport().setCursor(self.standardCursor)
        CodeEditorBaseMode.deactivate(self)

    # OVERRIDE: CodeEditorAddon.setPalette()
    def setPalette(self, palette):
        # Dragged Cursor
        draggedTextCharFormat = QtGui.QTextCharFormat()
        draggedTextCharFormat.setBackground(palette.alternateBase().color())
        self.editor.registerTextCharFormat("dyn.caret.mixed.dragged", draggedTextCharFormat)
        
        # Multi cursor
        multicursorTextCharFormat = QtGui.QTextCharFormat()
        multicursorTextCharFormat.setBackground(palette.highlightedText().color())
        multicursorTextCharFormat.setForeground(palette.base().color())
        self.editor.registerTextCharFormat("dyn.caret.mixed", multicursorTextCharFormat)
        
    # ------------ Key press handlers
    def __multicursor_end(self, event):
        firstCursor = self.cursors()[0]
        lastCursor = self.cursors()[-1]
        self.editor.document().markContentsDirty(firstCursor.position(), lastCursor.position())
        if lastCursor.hasSelection():
            lastCursor.clearSelection()
        self.editor.setTextCursor(lastCursor)
        self.deactivate()
        return True

    def __move_cursors(self, event):
        if self.canMove(event.key()):
            mode = QtGui.QTextCursor.KeepAnchor if bool(event.modifiers() & QtCore.Qt.ShiftModifier) else QtGui.QTextCursor.MoveAnchor
            if event.key() == QtCore.Qt.Key_Right:
                position = QtGui.QTextCursor.NextWord if bool(event.modifiers() & QtCore.Qt.ControlModifier) else QtGui.QTextCursor.NextCharacter
            elif event.key() == QtCore.Qt.Key_Left:
                position = QtGui.QTextCursor.PreviousWord if bool(event.modifiers() & QtCore.Qt.ControlModifier) else QtGui.QTextCursor.PreviousCharacter
            for cursor in self.cursors():
                cursor.movePosition(position, mode)
            return True

    # ------- Handle events
    def eventFilter(self, obj, event):
        if self.isActive() and event.type() == QtCore.QEvent.KeyPress:
            return self.keyPressEvent(event)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and \
            (self.isActive() or event.modifiers() & QtCore.Qt.ControlModifier):
            self.mouseReleasePoint(event.pos(), 
                event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonPress and \
            (self.isActive() or event.modifiers() & QtCore.Qt.ControlModifier):
            self.mousePressPoint(event.pos(), 
                event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        elif event.type() == QtCore.QEvent.MouseMove and \
            (self.isActive() or event.modifiers() & QtCore.Qt.ControlModifier):
            self.mouseMovePoint(event.pos(), 
                event.modifiers() & QtCore.Qt.MetaModifier)
            return True
        return False

    def mousePressPoint(self, point, remove = False):
        self.startPoint = point

    def mouseMovePoint(self, dragPoint, remove = False):
        self.draggedCursors = []
        
        startPoint = self.startPoint
        endPoint = dragPoint
        anchor = 'right'
        if self.startPoint.x() > dragPoint.x():
            anchor = 'left'
            startPoint, endPoint = endPoint, startPoint
            
        hight = self.editor.characterHeight()
        topLeft = self.editor.cursorRect(
            self.editor.cursorForPosition(startPoint)).topLeft()
        bottomRight = self.editor.cursorRect(
            self.editor.cursorForPosition(endPoint)).bottomRight()
        
        for start, end in build_point_matrix(topLeft, bottomRight, hight):
            #Sentido en el que queda el cursor
            if anchor == 'left':
                cursor = self.editor.newCursorAtPosition(
                    QtCore.QPoint(*end), QtCore.QPoint(*start)
                )
            else:
                cursor = self.editor.newCursorAtPosition(
                    QtCore.QPoint(*start),
                    QtCore.QPoint(*end)
                )
            self.draggedCursors.append(cursor)

        # Muestro los dragged cursors
        self.highlightEditor()
    
    def mouseReleasePoint(self, endPoint, remove = False):
        multicursorAction = self.addMergeCursor if not remove else self.removeBreakCursor
        if self.draggedCursors:
            for cursor in self.draggedCursors:
                multicursorAction(cursor)
        elif self.startPoint is not None:
            multicursorAction(self.editor.newCursorAtPosition(self.startPoint))

        if self.editor.extraCursors() and not self.isActive():
            self.activate()
        elif not self.editor.extraCursors() and self.isActive():
            self.deactivate()

        #Clean last acction
        self.draggedCursors = []
        self.startPoint = self.doublePoint = None
        self.application().restoreOverrideCursor()
        
        # Muestro los nuevos cursores
        self.highlightEditor()

    def keyPressEvent(self, event):
        handled = False
        if event.key() in [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_End, QtCore.Qt.Key_Home]:
            #Desactivados por ahora
            pass
        elif event.text() and not event.modifiers():
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            for cursor in self.cursors():
                self.editor.setTextCursor(cursor)
                self.editor.keyPressEvent(event)
            cursor.endEditBlock()
            handled = True
        if handled:
            self.highlightEditor()
        return handled

    def highlightEditor(self):
        # Dragged
        dragged = (c for c in (QtGui.QTextCursor(c) for c in self.draggedCursors) if c.hasSelection())
        self.editor.setExtraSelectionCursors("dyn.caret.mixed.dragged", [c for c in [QtGui.QTextCursor(c) for c in self.draggedCursors] if c.hasSelection()])
        
        self.editor.updateExtraSelections()

    def cursors(self):
        return self.editor.extraCursors()
        
    def setCursors(self, cursors):
        self.editor.setExtraCursors(cursors)

    def addMergeCursor(self, cursor):
        """Only can add new cursors, if the cursor has selection then try to merge with others"""
        cursors = self.cursors()
        if cursor.hasSelection():
            newCursor = None
            removeCursor = None
            new_begin, new_end = cursor.selectionStart(), cursor.selectionEnd()
            for c in cursors:
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
                cursors.remove(removeCursor)
                self.addMergeCursor(newCursor)
            else:
                position = bisect_key(cursors, cursor, lambda cursor: cursor.position())
                cursors.insert(position, cursor)
        else:
            for c in cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if begin <= cursor.position() <= end:
                    return
            position = bisect_key(cursors, cursor, lambda cursor: cursor.position())
            cursors.insert(position, cursor)
    
        self.setCursors(cursors)        

    def removeBreakCursor(self, cursor):
        cursors = self.cursors()
        #TODO: Hay cosas que se pueden simplificar pero hoy no me da el cerebro
        if cursor.hasSelection():
            newCursors = []
            removeCursor = None
            new_begin, new_end = cursor.selectionStart(), cursor.selectionEnd()
            for c in cursors:
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
                cursors.remove(removeCursor)
            for cursors in newCursors:
                position = bisect_key(cursors, cursors, lambda cursor: cursor.position())
                cursors.insert(position, cursors)
        else:
            #Solo puedo quitar cursores que no tengan seleccion osea que sean un clic :)
            for c in cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if not c.hasSelection() and c.position() == cursor.position():
                    cursors.remove(c)
                    break

        self.setCursors(cursors)

    def canMove(self, key):
        return (key == QtCore.Qt.Key_Right and not self.cursors()[-1].atEnd()) or \
            (key == QtCore.Qt.Key_Left and not self.cursors()[0].atStart())

    def findCursor(self, backward = False):
        # Get leader cursor
        if not self.isActive():
            cursor = self.editor.textCursor()
        else:
            cursor = self.cursors()[0] if backward else self.cursors()[-1]
            
        # Build new cursor
        if cursor.hasSelection():
            text = cursor.selectedText()
            flags = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
            if backward:
                flags |= QtGui.QTextDocument.FindBackward
            new_cursor = self.editor.document().find(text, cursor, flags)
        else:
            text, start, end = self.editor.currentWord()
            new_cursor = self.editor.newCursorAtPosition(start, end)
        
        if not self.isActive() and cursor.hasSelection():
            # The first time also add the leader cursor if has selection
            self.addMergeCursor(cursor)
        if not new_cursor.isNull():
            self.addMergeCursor(new_cursor)
            self.editor.centerCursor(new_cursor)

        if self.editor.extraCursors() and not self.isActive():
            self.activate()
        self.highlightEditor()

    def switchToColumnSelection(self):
        cursor = self.editor.textCursor()
        cursor_start = self.editor.newCursorAtPosition(cursor.selectionStart()) 
        cursor_end = self.editor.newCursorAtPosition(cursor.selectionEnd())
        delta = cursor_end.columnNumber() - cursor_start.columnNumber()
        if delta >= 0:
            block = cursor_start.block()
            while block.isValid():
                start = block.position() + cursor_start.columnNumber()
                end = start + delta
                block_position_end = block.position() + block.length()
                if end > block_position_end:
                    end = block_position_end
                cursor = self.editor.newCursorAtPosition(start, end)
                self.addMergeCursor(cursor)
                if block == cursor_end.block():
                    break
                block = block.next()
        if self.editor.extraCursors() and not self.isActive():
            self.activate()
        self.highlightEditor()

    def contributeToShortcuts(self):
        return [{
            "sequence": ("Multiedit", "SwitchToColumnSelection", "Ctrl+Shift+M"),
            "activated": lambda : self.switchToColumnSelection()
        }, {
            "sequence": ("Multiedit", "FindForwardCursor", "Ctrl+Meta+M"),
            "activated": lambda : self.findCursor()
        }, {
            "sequence": ("Multiedit", "FindBackwardCursor", "Ctrl+Meta+Shift+M"),
            "activated": lambda : self.findCursor(backward=True)
        }]
