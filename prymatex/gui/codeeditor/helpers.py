#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax
from prymatex import resources
from prymatex.gui.codeeditor.editor import PMXEditorMode

class PMXCursorsHelper(PMXEditorMode):
    def __init__(self, editor):
        PMXEditorMode.__init__(self, editor)
        self.cursors = []
        self.scursor = self.dragPoint = self.startPoint = None
    
    def isActive(self):
        return bool(self.cursors)
    
    def setActive(self, active):
        if not active:
            self.cursors = []

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
            #Se termino la joda
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
    
    def __iter__(self):
        return iter(self.cursors)
        
class PMXCompleterHelper(QtGui.QCompleter, PMXEditorMode):
    def __init__(self, editor):
        QtGui.QCompleter.__init__(self, editor)
        PMXEditorMode.__init__(self, editor)
        self.setWidget(self.editor)
        self.popupView = QtGui.QListView()
        self.popupView.setAlternatingRowColors(True)
        self.popupView.setWordWrap(False)
        self.setPopup(self.popupView)
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.activated[str].connect(self.insertCompletion)
    
    def isActive(self):
        return self.popup().isVisible()
        
    def setActive(self, active):
        pass

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
            event.ignore()
        else:
            self.editor.keyPressEvent(event)
    
    def insertCompletion(self, insert):
        self.editor.textCursor().insertText(insert[len(self.completionPrefix()):])

    def complete(self, rect):
        self.popup().setCurrentIndex(self.completionModel().index(0, 0))
        rect.setWidth(self.popup().sizeHintForColumn(0) + self.popup().verticalScrollBar().sizeHint().width() + 20)
        QtGui.QCompleter.complete(self, rect)

class PMXFoldingHelper(object):
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.editor.foldingChanged.connect(self.on_foldingChanged)
        self.editor.textBlocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []
        self.folding = []

    def on_foldingChanged(self, block):
        if block in self.blocks:
            userData = block.userData()
            if userData.foldingMark == PMXSyntax.FOLDING_NONE:
                self.blocks.remove(block)
        else:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)
        if self.indentSensitive:
            self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
    
    def on_textBlocksRemoved(self):
        remove = filter(lambda block: block.userData() is None, self.blocks)
        if remove:
            sIndex = self.blocks.index(remove[0])
            eIndex = self.blocks.index(remove[-1])
            self.blocks = self.blocks[:sIndex] + self.blocks[eIndex + 1:]
        if self.indentSensitive:
            self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
        
    def updateFoldingBlocks(self):
        self.folding = []
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)

    def updateIndentFoldingBlocks(self):
        self.folding = []
        nest = 0
        lastOpenIndent = currentIndent = ""
        for block in self.blocks:
            userData = block.userData()
            if userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                #Esta cerrando, es blank?
                if block.text().strip() == "":
                    continue
            elif userData.foldingMark >= PMXSyntax.FOLDING_START:
                #Esta abriendo, esta menos indentado?
                if userData.indent <= currentIndent and len(self.folding) > 0:
                    #Hay que cerrar algo antes
                    closeBlock = self.findPreviousMoreIndentBlock(block)
                    lenIndent = len(userData.indent)
                    if lenIndent:
                        closeBlock.userData().foldingMark = - (len(currentIndent) / lenIndent)
                    else:
                        closeBlock.userData().foldingMark = -nest
                    self.folding.append(closeBlock)
                    nest += closeBlock.userData().foldingMark
                else:
                    #Store last valid indent
                    lastOpenIndent = currentIndent
            nest += userData.foldingMark
            currentIndent = userData.indent if userData.foldingMark >= PMXSyntax.FOLDING_START else lastOpenIndent
            if nest >= 0:
                self.folding.append(block)
        if nest > 0:
            #Tengo que cerrar el ultimo
            closeBlock = self.editor.document().lastBlock()
            userData = closeBlock.userData()
            if userData is not None:
                closeBlock.userData().foldingMark = -nest
                self.folding.append(closeBlock)

    def findPreviousMoreIndentBlock(self, block):
        """ Return previous block if text in block is not bank """
        indent = block.userData().indent
        while block.isValid():
            block = block.previous()
            if indent < block.userData().indent:
                break
        return block
    
    def getFoldingMark(self, block):
        if block in self.folding:
            userData = block.userData()
            return userData.foldingMark
        return PMXSyntax.FOLDING_NONE
    
    def findBlockFoldClose(self, block):
        nest = 0
        assert block in self.folding, "The block is not in folding"
        index = self.folding.index(block)
        for block in self.folding[index:]:
            userData = block.userData()
            if userData.foldingMark >= PMXSyntax.FOLDING_START or userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                nest += userData.foldingMark
            if nest <= 0:
                break
        #return the founded block or the last valid block
        return block if block.isValid() else block.previous()
    
    def findBlockFoldOpen(self, block):
        nest = 0
        assert block in self.folding, "The block is not in folding"
        index = self.folding.index(block)
        folding = self.folding[:index + 1]
        folding.reverse()
        for block in folding:
            userData = block.userData()
            if userData.foldingMark >= PMXSyntax.FOLDING_START or userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                nest += userData.foldingMark
            if nest >= 0:
                break

        #return the founded block or the first valid block
        return block if block.isValid() else block.next()
    
    def getNestedLevel(self, index):
        return reduce(lambda x, y: x + y, map(lambda block: block.userData().foldingMark, self.folding[:index]), 0)
        
    def isStart(self, mark):
        return mark >= PMXSyntax.FOLDING_START

    def isStop(self, mark):
        return mark <= PMXSyntax.FOLDING_STOP
        
    def isFoldingMark(self, block):
        return block in self.folding