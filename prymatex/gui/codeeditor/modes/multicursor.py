#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

def _build_points(start, end, hight):
    offset = (hight / 2) + start.y()
    while offset <= end.y():
        yield ( QtCore.QPoint(start.x(), offset), QtCore.QPoint(end.x(), offset) )
        offset += hight

def _build_set(cursors):
    s = set()
    for c in cursors:
        s.update(list(range(c.selectionStart(), c.selectionEnd() + 1))) 
    return s

def _build_cursors(editor, s):
    cursors = []
    ranges = sorted(s)
    if ranges:
        end = start = ranges[0]
        for index in ranges[1:]:
            if index != (end + 1):
                cursors.append(editor.newCursorAtPosition(start, end))
                end = start = index
            else:
                end = index
        cursors.append(editor.newCursorAtPosition(start, end))
    return cursors
    
class CodeEditorMultiCursorMode(CodeEditorBaseMode):
    MOVE_CHARACTERS = { 
        QtCore.Qt.Key_Up: QtGui.QTextCursor.Up,
        QtCore.Qt.Key_Down: QtGui.QTextCursor.Down,
        QtCore.Qt.Key_Right: QtGui.QTextCursor.Right,
        QtCore.Qt.Key_Left: QtGui.QTextCursor.Left
    }
    MOVE_WORDS = { 
        QtCore.Qt.Key_Right: QtGui.QTextCursor.WordRight,
        QtCore.Qt.Key_Left: QtGui.QTextCursor.WordLeft
    }
    def __init__(self, **kwargs):
        super(CodeEditorMultiCursorMode, self).__init__(**kwargs)
        self.draggedCursors = self.startPoint = None
        self.standardCursor = None
        self._hash = None

    def name(self):
        return "MULTICURSOR"

    # ------- Overrides
    def initialize(self, **kwargs):
        super(CodeEditorMultiCursorMode, self).initialize(**kwargs)
        self.editor.viewport().installEventFilter(self)
        self.editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)

        self.standardCursor = self.editor.viewport().cursor()

        # ------------ Handlers
        self.registerKeyPressHandler("esc", self.__multicursor_end)
        self.registerKeyPressHandler([
            "Up", "Down", "Right", "Left",
            "Shift+Up", "Shift+Down", "Shift+Right", "Shift+Left"
            ],
            self.__cursors_move_by_character
        )
        self.registerKeyPressHandler([
            "Ctrl+Right", "Ctrl+Left",
            "Ctrl+Shift+Right", "Ctrl+Shift+Left"
            ],
            self.__cursors_move_by_word
        )

    def activate(self):
        self.editor.commandAdded.connect(self.on_editor_commandAdded)
        self.editor.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        super().activate()

    def deactivate(self):
        self.editor.commandAdded.disconnect(self.on_editor_commandAdded)
        self.editor.viewport().setCursor(self.standardCursor)
        super().deactivate()

    def on_editor_commandAdded(self):
        command, args, _ = self.editor.commandHistory(0, True)
        print(command, args)
        if command in ("insert", "replace"):
            text = args[command == "insert" and "characters" or "by"]
            cursors = self.editor.textCursors()
            cursors[0].joinPreviousEditBlock() 
            new_cursors = [ cursors[0] ]
            for cursor in cursors[1:]:
                cursor.insertText(text)
                new_cursors.append(cursor)
            new_cursors[0].endEditBlock()
            new_cursors = _build_cursors(self.editor, _build_set(new_cursors))
            self.editor.setTextCursors(new_cursors)
        elif command == 'remove':
            prev_command, prev_args, _ = self.editor.commandHistory(-1, True)
            print(prev_args)
            print("quita texto")
            
    def on_editor_cursorPositionChanged(self):
        # Test and switch state
        cursors = self.editor.textCursors()
        if len(cursors) > 1 and not self.isActive():
            self.activate()
        elif len(cursors) == 1 and self.isActive():
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
        self.editor.clearExtraCursors()
        return True
    
    def __cursors_move(self, move, event):
        mode = event.modifiers() & QtCore.Qt.ShiftModifier and \
            QtGui.QTextCursor.KeepAnchor or \
            QtGui.QTextCursor.MoveAnchor
        cursors = self.editor.textCursors()
        new_cursors = [ ]
        for cursor in cursors:
            cursor.movePosition(move, mode)
            new_cursors.append(cursor)
        new_cursors = _build_cursors(self.editor, _build_set(new_cursors))
        self.editor.setTextCursors(new_cursors)
        return True

    def __cursors_move_by_character(self, event):
        return self.__cursors_move(self.MOVE_CHARACTERS[event.key()], event)
    
    def __cursors_move_by_word(self, event):
        return self.__cursors_move(self.MOVE_WORDS[event.key()], event)

    # ------- Handle Mouse events
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease and \
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
        if not self.startPoint:
            self.startPoint = dragPoint
            return

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
            [self.editor.newCursorAtPosition(endPoint)]
        )

        #Clean last acction
        self.draggedCursors = self.startPoint = None
        self.application().restoreOverrideCursor()
        
        # Muestro los nuevos cursores
        self.highlightEditor()

    def highlightEditor(self):
        # Dragged
        dragged = []
        if self.draggedCursors:
            dragged = [c for c in [QtGui.QTextCursor(c) for c in self.draggedCursors] if c.hasSelection()]
        self.editor.setExtraSelectionCursors("dyn.caret.mixed.dragged", dragged)
        self.editor.updateExtraSelections()

    def addMergeCursor(self, cursors):
        set1 = _build_set(self.cursors())
        set2 = _build_set(cursors)
        self.editor.setTextCursors(
            _build_cursors(self.editor, set1.union(set2))
        )

    def removeBreakCursor(self, cursors):
        set1 = _build_set(self.cursors())
        set2 = _build_set(cursors)
        self.editor.setTextCursors(
            _build_cursors(self.editor, set1.difference(set2))
        )
