#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXCursorsHelper(object):
    def __init__(self, editor):
        self.editor = editor
        self.cursors = []
        self.scursor = self.dragPoint = self.startPoint = None
    
    @property
    def hasCursors(self):
        return bool(self.cursors)

    @property
    def isDragCursor(self):
        return self.dragPoint != None
    
    def getDragCursorRect(self):
        """Retorna un rectangulo que representa la zona del drag cursor"""
        return QtCore.QRect(self.startPoint, self.dragPoint)
    
    def mousePressPoint(self, point):
        self.startPoint = point

    def mouseDoubleClickPoint(self, point):
        self.startPoint = point
        
    def mouseMovePoint(self, point):
        self.dragPoint = point
        self.editor.viewport().repaint(self.editor.viewport().visibleRegion())

    def mouseReleasePoint(self, endPoint):
        _, width, points = self.getPoints(self.startPoint, endPoint)
        
        for tupla in points:
            if tupla[0] == tupla[1]:
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*tupla[0]))
                cursor = self.addMergeCursor(cursor)
                #self.editor.document().markContentsDirty(cursor.position(), cursor.position())
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
                        cursor = self.addMergeCursor(cursor)
                    #self.editor.document().markContentsDirty(cursor.position(), ecursor.position())
            else: # Derecha a izquierda
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        ecursor.setPosition(cursor.position(), QtGui.QTextCursor.KeepAnchor)
                        ecursor = self.addMergeCursor(ecursor)
                    #self.editor.document().markContentsDirty(cursor.position(), ecursor.position())

        #Clean last acction
        self.scursor = self.dragPoint = self.startPoint = None
        self.editor.viewport().repaint(self.editor.viewport().visibleRegion())

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
        
    def addMergeCursor(self, cursor):
        '''
            Only can add new cursors, if the cursor has selection then try to merge with others
        '''
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
                    newCursor = QtGui.QTextCursor(self.editor.document())
                    removeCursor = c
                    break
            if newCursor is not None:
                self.cursors.remove(removeCursor)
                self.addMergeCursor(newCursor)
            else:
                self.editor.setTextCursor(cursor)
                self.cursors.append(cursor)
        else:
            for c in self.cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if begin <= cursor.position() <= end:
                    return
            self.editor.setTextCursor(cursor)
            self.cursors.append(cursor)

    def removeAll(self):
        self.cursors = []
    
    def canMoveRight(self):
        return all(map(lambda c: not c.atEnd(), self.cursors))
    
    def canMoveLeft(self):
        return all(map(lambda c: not c.atStart(), self.cursors))
    
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
        elif event.modifiers() & QtCore.Qt.ControlModifier and event.key() in [ QtCore.Qt.Key_Z]:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
        elif event.key() == QtCore.Qt.Key_Right:
            if self.canMoveRight():
                if event.modifiers() & QtCore.Qt.ShiftModifier:
                    for cursor in self.cursors:
                        self.editor.document().markContentsDirty(cursor.position(), cursor.position() + 1)
                        cursor.setPosition(cursor.position() + 1, QtGui.QTextCursor.KeepAnchor)
                else:
                    for cursor in self.cursors:
                        self.editor.document().markContentsDirty(cursor.position(), cursor.position() + 1)
                        cursor.setPosition(cursor.position() + 1)
                self.editor.setTextCursor(cursor)
        elif event.key() == QtCore.Qt.Key_Left:
            if self.canMoveLeft():
                if event.modifiers() & QtCore.Qt.ShiftModifier:
                    for cursor in self.cursors:
                        self.editor.document().markContentsDirty(cursor.position(), cursor.position() - 1)
                        cursor.setPosition(cursor.position() - 1, QtGui.QTextCursor.KeepAnchor)
                else:
                    for cursor in self.cursors:
                        self.editor.document().markContentsDirty(cursor.position(), cursor.position() - 1)
                        cursor.setPosition(cursor.position() - 1)
                self.editor.setTextCursor(cursor)
        elif event.key() in [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_End, QtCore.Qt.Key_Home]:
            #Desactivados por ahora
            pass
        elif event.key() in [QtCore.Qt.Key_Insert]:
            self.editor.setOverwriteMode(not self.editor.overwriteMode())
        elif event.text():
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
        #TODO: Mi propio modelo para autocompletado
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

    def complete(self, rect, suggestions = None):
        try:
            if suggestions is not None:
                self.popupView.clear()
                model = self.buildModelItems(suggestions)
                self.setModel(model)
                self.popup().setCurrentIndex(model.index(0, 0))
            rect.setWidth(self.popup().sizeHintForColumn(0) + self.popup().verticalScrollBar().sizeHint().width() + 10)
            self.popupView.updateGeometries()
            super(PMXCompleterHelper, self).complete(rect)
        except:
            return

    def buildModelItems(self, suggestions):
        for suggestion in suggestions:
            if 'display' in suggestion:
                item = QtGui.QListWidgetItem(suggestion['display'])
                if 'insert' in suggestion:
                    print "no, por ahora"
                if 'image' in suggestion:
                    item.setIcon(QtGui.QIcon(suggestion['image']))
                if 'match' in suggestion:
                    print "no, por ahora"
            elif 'title' in suggestion:
                item = QtGui.QListWidgetItem(suggestion['title'])
            else:
                continue
            self.popupView.addItem(item)
        return self.popupView.model()

class PMXFoldingHelper(object):
    FOLDING_NONE = PMXSyntax.FOLDING_NONE              #Cuidado esto tiene que ser 0
    FOLDING_START = PMXSyntax.FOLDING_START            #Cuidado esto tiene que ser +1
    FOLDING_STOP = PMXSyntax.FOLDING_STOP              #Cuidado esto tiene que ser -1
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.folding = []
    
    def findPreviousNotBlankBlock(self, block):
        """ Return previous block if text in block is not "" """
        while block.isValid():
            block = block.previous()
            if block.text().strip() != "":
                break
        return block
    
    def findPreviousMoreNestedBlock(self, block):
        """ Return previous block if text in block is not "" """
        indent = block.userData().indent
        block = self.findPreviousNotBlankBlock(block)
        while block.isValid():
            if block.userData().indent > indent:
                break
            block = self.findPreviousNotBlankBlock(block)
        return block
    
    def closePreviousBlock(self, block):
        #Le pongo un "corcho" al anterior
        factor = 1
        userData = block.userData()
        startBlock = previousBlock = self.findPreviousMoreNestedBlock(block)
        while startBlock.isValid():
            #Busco uno que abre al mismo nivel
            if startBlock.userData().foldingMark == self.FOLDING_START and startBlock.userData().indent == userData.indent:
                self.folding[previousBlock.blockNumber()] = -1 * factor
                break
            elif startBlock.userData().indent <= userData.indent:
                break
            #Update factor
            factor = factor + 1 if self.folding[previousBlock.blockNumber()] > 0 else factor - 1 if self.folding[previousBlock.blockNumber()] < 0 else factor
            startBlock = self.findPreviousNotBlankBlock(startBlock)
        return factor
    
    def updateIndentFoldingMarks(self, lastBlock):
        index = len(self.folding)
        block = self.editor.document().findBlockByNumber(index)
        nest = reduce(lambda x, y: x + y, self.folding, 0)
        #Find Start
        last = self.findPreviousNotBlankBlock(block)
        lastIndent = last.userData().indent if last.isValid() else ""
        while block.isValid():
            userData = block.userData()
            mark = userData.foldingMark
            if mark == self.FOLDING_START or (mark == self.FOLDING_STOP and nest > 0 and block.text().strip() != ""):
                if mark == self.FOLDING_START and nest > 0:
                    nest -= self.closePreviousBlock(block)
                self.folding.append(mark)
                nest += mark
            elif lastIndent > userData.indent and block.text().strip() != "" and nest > 0:
                nest -= self.closePreviousBlock(block)
                lastIndent = userData.indent
                self.folding.append(self.FOLDING_NONE)
            else:
                self.folding.append(self.FOLDING_NONE)
            if block >= lastBlock:
                break
            block = block.next()
    
    def updateFoldingMarks(self, lastBlock):
        index = len(self.folding)
        block = self.editor.document().findBlockByNumber(index)
        nest = reduce(lambda x, y: x + y, self.folding, 0)
        while block.isValid():
            userData = block.userData()
            mark = userData.foldingMark
            if mark != self.FOLDING_STOP or (mark == self.FOLDING_STOP and nest > 0):
                self.folding.append(mark)
                nest += mark
            elif mark == self.FOLDING_STOP:
                self.folding.append(self.FOLDING_NONE)
            if block >= lastBlock and nest <= 0:
                break
            block = block.next()

    def deprecateFolding(self, index):
        self.folding = self.folding[:index]
    
    def getFoldingMark(self, block):
        #FIXME: hacer el folding para que defo se quede tranquilo
        if self.indentSensitive:
            if block.blockNumber() >= len(self.folding):
                self.updateIndentFoldingMarks(block)
            if self.folding[block.blockNumber()] < 0:
                return self.FOLDING_STOP
            elif self.folding[block.blockNumber()] > 0:
                return self.FOLDING_START
            else:
                return self.FOLDING_NONE
        else:
            if block.blockNumber() >= len(self.folding):
                self.updateFoldingMarks(block)
            return self.folding[block.blockNumber()]
    
    def findBlockFoldClose(self, block):
        nest = 0
        #DEBUG
        index = block.blockNumber()
        print self.folding[index]
        
        while block.isValid():
            index = block.blockNumber()
            nest += self.folding[index]
            if nest <= 0:
                break
            block = block.next()
        #return the founded block or the last valid block
        return block if block.isValid() else block.previous()
    
    def findBlockFoldOpen(self, block):
        nest = 0
        #DEBUG
        index = block.blockNumber()
        print self.folding[index]
        
        while block.isValid():
            index = block.blockNumber()
            nest += self.folding[index]
            if nest >= 0:
                break
            block = block.previous()
        #return the founded block or the first valid block
        return block if block.isValid() else block.next()
    
    def getNestedLevel(self, index):
        return reduce(lambda x, y: x + y, self.folding[:index], 0)
