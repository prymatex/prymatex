#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class PMXCursorsHelper(object):
    def __init__(self, editor):
        self.editor = editor
        self.cursors = []
    
    @property
    def hasCursors(self):
        return bool(self.cursors)

    @property
    def isDragCursor(self):
        return self.dp != None
    
    def getDragCursorRect(self):
        """Retorna un rectangulo que representa la zona del drag cursor"""
        return QRect(self.sp, self.dp)
    
    def startPoint(self, start):
        self.sp = start
        self.scursor = self.editor.cursorForPosition(self.sp)

    def dragPoint(self, pos):
        self.dp = pos
        dcursor = self.cursorForPosition(self.dp)
        self.document().markContentsDirty(self.scursor.position(), dcursor.position())

    def endPoint(self, end):
        scursor = self.scursor
        ecursor = self.editor.cursorForPosition(end)
        if scursor.position() == ecursor.position():
            self.addCursor(scursor)
            self.editor.document().markContentsDirty(scursor.position(), scursor.position())
        elif scursor.block() == ecursor.block():
            #Estan en el mismo block
            if scursor.position() > ecursor.position():
                ecursor.setPosition(scursor.position(), QtGui.QTextCursor.KeepAnchor)
                self.addCursor(ecursor)
                self.editor.document().markContentsDirty(ecursor.position(), scursor.position())
            else:
                scursor.setPosition(ecursor.position(), QtGui.QTextCursor.KeepAnchor)
                self.addCursor(scursor)
                self.editor.document().markContentsDirty(scursor.position(), ecursor.position())
        else:
            #Estan en distintos block
            if scursor.position() > ecursor.position():
                startx, starty = ecursor.columnNumber(), ecursor.block().blockNumber()
                endx, endy = scursor.columnNumber(), scursor.block().blockNumber()
                self.editor.document().markContentsDirty(ecursor.position(), scursor.position())
            else:
                startx, starty = scursor.columnNumber(), scursor.block().blockNumber()
                endx, endy = ecursor.columnNumber(), ecursor.block().blockNumber()
                self.editor.document().markContentsDirty(scursor.position(), ecursor.position())
            for i in xrange(starty, endy + 1):
                start = self.editor.document().findBlockByNumber(i).position()
                cursor = QtGui.QTextCursor(scursor)
                #Para que lado fue la apertura del recuadro
                if startx == endx:
                    cursor.setPosition(start + startx)
                elif startx > endx:
                    cursor.setPosition(start + startx)
                    cursor.setPosition(start + endx, QtGui.QTextCursor.KeepAnchor)
                else:
                    cursor.setPosition(start + endx)
                    cursor.setPosition(start + startx, QtGui.QTextCursor.KeepAnchor)
                self.addCursor(cursor)
        #Clean last acction
        self.scursor = self.dp = self.sp = None
        
    def addCursor(self, cursor):
        self.editor.setTextCursor(cursor)
        self.cursors.append(cursor)
    
    def removeAll(self):
        self.cursors = []
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            scursor = min(self.cursors, key = lambda cursor: cursor.position())
            ecursor = max(self.cursors, key = lambda cursor: cursor.position())
            self.editor.document().markContentsDirty(scursor.position(), ecursor.position())
            self.editor.setTextCursor(ecursor)
            self.removeAll()
            return False
        elif event.modifiers() & QtCore.Qt.ControlModifier:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
        elif event.key() == QtCore.Qt.Key_Right or event.key() == QtCore.Qt.Key_Left:
            #Mouse Move
            value = 1 if event.key() == QtCore.Qt.Key_Right else -1
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() + value)
                    cursor.setPosition(cursor.position() + value, QtGui.QTextCursor.KeepAnchor)
            else:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() + value)
                    cursor.setPosition(cursor.position() + value)
            self.editor.setTextCursor(cursor)
        elif event.key() in [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]:
            #Desactivados por ahora
            pass
        else:
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            for cursor in self.cursors:
                self.editor.setTextCursor(cursor)
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            cursor.endEditBlock()
        return True
    
    def __iter__(self):
        return iter(self.cursors)

class PMXFoldingHelper(object):
    def __init__(self, editor):
        self.editor = editor
        self.start = []
        self.stop = []
    
    def fill(self, index):
        if len(self.start) <= index:
            self.start[len(self.start):index] = [0 for _ in xrange(index - len(self.start))]
            self.start.append(0)
        if len(self.stop) <= index:
            self.stop[len(self.stop):index] = [0 for _ in xrange(index - len(self.stop))]
            self.stop.append(0)
            
    def setStart(self, index):
        self.fill(index)
        self.start[index] = 1
        
    def setStop(self, index):
        self.fill(index)
        self.stop[index] = -1
    
    def setNone(self, index):
        self.fill(index)
        self.start[index] = self.stop[index] = 0
    
    def insert(self, index):
        self.start.insert(index, 0)
        self.stop.insert(index, 0)
    
    def getNestedLevel(self, index):
        start = self.start[:index]
        stop = self.stop[:index]
        print index
        print start
        print stop
        return reduce(lambda x, y: x + y, start, 0) + reduce(lambda x, y: x + y, stop, 0)