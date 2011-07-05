#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class PMXCursorsHelper(object):
    def __init__(self, editor):
        self.editor = editor
        self.cursors = []
        self.scursor = self.dp = self.sp = None
    
    @property
    def hasCursors(self):
        return bool(self.cursors)

    @property
    def isDragCursor(self):
        return self.dp != None
    
    def getDragCursorRect(self):
        """Retorna un rectangulo que representa la zona del drag cursor"""
        return QtCore.QRect(self.sp, self.dp)
    
    def startPoint(self, start):
        self.sp = start

    def dragPoint(self, pos):
        self.dp = pos
        scursor = self.editor.cursorForPosition(self.sp)
        dcursor = self.editor.cursorForPosition(self.dp)
        self.editor.document().markContentsDirty(scursor.position(), dcursor.position())

    def getPoints(self, start, end):
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
        
    def endPoint(self, endPoint):
        _, width, points = self.getPoints(self.sp, endPoint)
        
        for tupla in points:
            if tupla[0] == tupla[1]:
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*tupla[0]))
                self.addCursor(cursor)
                self.editor.document().markContentsDirty(cursor.position(), cursor.position())
                continue
            #Sentido en el que queda el cursor
            if self.sp.x() < endPoint.x():  #izquierda a derecha
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        cursor.setPosition(ecursor.position(), QtGui.QTextCursor.KeepAnchor)
                        self.addCursor(cursor)
                    self.editor.document().markContentsDirty(cursor.position(), ecursor.position())
            else: # Derecha a izquierda
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        ecursor.setPosition(cursor.position(), QtGui.QTextCursor.KeepAnchor)
                        self.addCursor(ecursor)
                    self.editor.document().markContentsDirty(cursor.position(), ecursor.position())
        
        #Clean last acction
        self.scursor = self.dp = self.sp = None
        
    def addCursor(self, cursor):
        '''
            Solo se pueden incorporar cursores nuevos.
        '''
        new_begin, new_end = (cursor.selectionStart(), cursor.selectionEnd()) if cursor.hasSelection() else (cursor.position(), cursor.position())
        for c in self.cursors:
            c_begin, c_end = (c.selectionStart(), c.selectionEnd()) if c.hasSelection() else (c.position(), c.position())
            if c_begin <= new_begin <= new_end <= c_end:
                #Esta contenido
                return
        self.editor.setTextCursor(cursor)
        self.cursors.append(cursor)
    
    def removeAll(self):
        self.cursors = []
    
    def canMoveRight(self):
        return all(map(lambda c: not c.atBlockStart(), self.cursors))
    
    def canMoveLeft(self):
        return all(map(lambda c: not c.atBlockEnd(), self.cursors))
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            #Deprecated usar una lista de cursores ordenados para tomar de [0] y [-1]
            scursor = min(self.cursors, key = lambda cursor: cursor.position())
            ecursor = max(self.cursors, key = lambda cursor: cursor.position())
            self.editor.document().markContentsDirty(scursor.position(), ecursor.position())
            if ecursor.hasSelection():
                ecursor.clearSelection()
            self.editor.setTextCursor(ecursor)
            self.removeAll()
            self.editor.highlightCurrentLine()
            return False
        elif event.modifiers() & QtCore.Qt.ControlModifier:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
        elif event.key() == QtCore.Qt.Key_Right and self.canMoveRight():
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() + 1)
                    cursor.setPosition(cursor.position() + 1, QtGui.QTextCursor.KeepAnchor)
            else:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() + 1)
                    cursor.setPosition(cursor.position() + 1)
            self.editor.setTextCursor(cursor) 
        elif event.key() == QtCore.Qt.Key_Left and self.canMoveLeft():
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() - 1)
                    cursor.setPosition(cursor.position() - 1, QtGui.QTextCursor.KeepAnchor)
            else:
                for cursor in self.cursors:
                    self.editor.document().markContentsDirty(cursor.position(), cursor.position() - 1)
                    cursor.setPosition(cursor.position() - 1)
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

class PMXCompleterHelper(QtGui.QCompleter):
    def __init__(self, editor):
        super(PMXCompleterHelper, self).__init__()
        self.editor = editor
        self.setWidget(self.editor)
        self.popupView = QtGui.QListWidget()
        self.popupView.setAlternatingRowColors(True)
        self.popupView.setWordWrap(False)
        self.setPopup(self.popupView)
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.activated[str].connect(self.insertCompletion)

    def insertCompletion(self, insert):
        extra = insert.length() - self.completionPrefix().length()
        self.editor.textCursor().insertText(insert.right(extra))

    def complete(self, cr):
        try:
            model = self.obtainModelItems()
            self.setModel(model)
            self.popup().setCurrentIndex(model.index(0, 0))
            cr.setWidth(self.popup().sizeHintForColumn(0) \
                + self.popup().verticalScrollBar().sizeHint().width() + 10)
            self.popupView.updateGeometries()
            super(PMXCompleterHelper, self).complete(cr)
        except:
            return

    def obtainModelItems(self):
        for name in ['uno', 'dos', 'tres']:
            self.popupView.addItem(QtGui.QListWidgetItem(name))
        return self.popupView.model()

class PMXFoldingHelper(QtCore.QThread):
    def __init__(self, editor):
        super(PMXFoldingHelper, self).__init__(editor)
        self.editor = editor
        self.open = []
        self.close = []
    
    def run(self):
        while True:
            QtCore.QThread.sleep(2)
            print "valores"
            print self.open
            print self.close
            
    def setOpen(self, index):
        self.open[index] = 1
        
    def setClose(self, index):
        self.close[index] = -1
    
    def setNone(self, index):
        self.open[index] = self.close[index] = 0
    
    def insert(self, index):
        self.open.insert(index, 0)
        self.close.insert(index, 0)
    
    def getNestedLevel(self, index):
        start = self.open[:index]
        stop = self.close[:index]
        print index
        print start
        print stop
        return reduce(lambda x, y: x + y, start, 0) + reduce(lambda x, y: x + y, stop, 0)
