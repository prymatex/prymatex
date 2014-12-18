#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

from prymatex.utils.lists import bisect_key

def _build_points(start, end, hight):
    offset = (hight / 2) + start.y()
    while offset <= end.y():
        yield ( QtCore.QPoint(start.x(), offset), QtCore.QPoint(end.x(), offset) )
        offset += hight

def _build_set(cursors):
    s = set()
    for c in cursors:
        s.update(list(range(c.selectionStart(), c.selectionEnd()))) 
    return s

def _build_cursors(editor, s):
    cursors = []
    ranges = sorted(s)
    if ranges:
        end = start = ranges[0]
        for index in ranges[1:]:
            if index != (end + 1):
                cursors.append(editor.newCursorAtPosition(start, end + 1))
                end = start = index
            else:
                end = index
        cursors.append(editor.newCursorAtPosition(start, end + 1))
    return cursors
    
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
        self.editor.setTextCursors([])
        self.editor.viewport().setCursor(self.standardCursor)
        CodeEditorBaseMode.deactivate(self)

    def switch(self):
        # Test and switch state
        if len(self.cursors()) > 1 and not self.isActive():
            self.activate()
        elif len(self.cursors()) == 1 and self.isActive():
            self.deactivate()

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
        
        if self.startPoint.x() <= dragPoint.x():
            anchor = 'right'
            startRect = self.editor.cursorRect(
                self.editor.cursorForPosition(self.startPoint))
            endRect = self.editor.cursorRect(
                self.editor.cursorForPosition(dragPoint))
            point1, point2 = startRect.topLeft(), endRect.bottomRight()
        else:
            anchor = 'left'
            startRect = self.editor.cursorRect(
                self.editor.cursorForPosition(dragPoint))
            endRect = self.editor.cursorRect(
                self.editor.cursorForPosition(self.startPoint))
            point1, point2 = endRect.topRight(), startRect.bottomLeft()
            point1, point2 = QtCore.QPoint(point2.x(), point1.y()), QtCore.QPoint(point1.x(), point2.y()) 

        hight = self.editor.characterHeight()
        for start, end in _build_points(point1, point2, hight):
            #Sentido en el que queda el cursor
            if anchor == 'left':
                cursor = self.editor.newCursorAtPosition(end, start)
            else:
                cursor = self.editor.newCursorAtPosition(start, end)
            self.draggedCursors.append(cursor)

        # Muestro los dragged cursors
        self.highlightEditor()
    
    def mouseReleasePoint(self, endPoint, remove = False):
        multicursorAction = self.addMergeCursor if not remove else self.removeBreakCursor
        multicursorAction(self.draggedCursors or \
            [self.editor.newCursorAtPosition(self.startPoint)]
        )

        self.switch()

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
            cursors = self.cursors()
            cursors[0].beginEditBlock()
            for cursor in cursors:
                self.editor.setTextCursor(cursor)
                self.editor.keyPressEvent(event)
            cursors[0].endEditBlock()
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
        return self.editor.textCursors()
        
    def setCursors(self, cursors):
        self.editor.setTextCursors(cursors)

    def addMergeCursor(self, cursors):
        set1 = _build_set(self.cursors())
        set2 = _build_set(cursors)
        self.setCursors(_build_cursors(self.editor, set1.union(set2)))

    def removeBreakCursor(self, cursors):
        set1 = _build_set(self.cursors())
        set2 = _build_set(cursors)
        self.setCursors(_build_cursors(self.editor, set1.difference(set2)))

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
            self.addMergeCursor([ cursor ])
        if not new_cursor.isNull():
            self.addMergeCursor([ new_cursor ])
            self.editor.centerCursor(new_cursor)

        self.switch()
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
                self.addMergeCursor([ cursor ])
                if block == cursor_end.block():
                    break
                block = block.next()
        self.switch()
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
