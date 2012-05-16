#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui import utils
from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor import helpers
from prymatex.gui.support.models import PMXBundleTreeNode

class PMXBaseEditorMode(object):
    def __init__(self, editor):
        self.editor = editor
    
    def active(self, event, scope):
        pass
    
    def isActive(self):
        return False

    def inactive(self):
        pass

    def keyPressEvent(self, event):
        pass

class PMXSnippetEditorMode(PMXBaseEditorMode):
    def __init__(self, editor):
        PMXBaseEditorMode.__init__(self, editor)
        self.logger = editor.application.getLogger('.'.join([self.__class__.__module__, self.__class__.__name__]))

    def isActive(self):
        return self.editor.snippetProcessor.snippet is not None

    def inactive(self):
        self.editor.snippetProcessor.endSnippet()

    def keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Escape:
            self.logger.debug("Se termina el modo snippet")
            return self.endSnippet(event)
        elif event.key() in [ QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab ]:
            self.logger.debug("Camino entre los holders")
            holder = self.editor.snippetProcessor.getHolder(cursor.selectionStart(), cursor.selectionEnd())
            if holder is None:
                return self.endSnippet(event)

            if event.key() == QtCore.Qt.Key_Tab:
                holder = self.editor.snippetProcessor.nextHolder(holder)
            else:
                holder = self.editor.snippetProcessor.previousHolder(holder)
            if holder == None:
                self.editor.showMessage("Last Holder")
                self.setCursorPosition(self.editor.snippetProcessor.endPosition())
                self.endSnippet()
            else:
                snippet = self.editor.snippetProcessor.snippet 
                self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (snippet.name, snippet.index + 1, len(snippet) -1))
                self.editor.snippetProcessor.selectHolder(holder)
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            currentHolder = self.editor.snippetProcessor.getHolder(cursor.selectionStart(), cursor.selectionEnd())
            if currentHolder is None:
                return self.endSnippet(event)
            
            #Cuidado con los extremos del holder
            if not cursor.hasSelection():
                if event.key() == QtCore.Qt.Key_Backspace and cursor.position() == currentHolder.start:
                    return self.endSnippet(event)
                
                if event.key() == QtCore.Qt.Key_Delete and cursor.position() == currentHolder.end:
                    return self.endSnippet(event)
                
            holderPosition = cursor.selectionStart() - currentHolder.start
            positionBefore = cursor.selectionStart()
            charactersBefore = cursor.document().characterCount()
            
            #Insert Text
            self.editor.textCursor().beginEditBlock()
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = charactersBefore - charactersAfter 
            
            #Capture Text
            cursor.setPosition(currentHolder.start)
            cursor.setPosition(currentHolder.end - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = utils.replaceLineBreaks(cursor.selectedText())
            currentHolder.setContent(selectedText)
            
            #Remove text
            self.selectSlice(self.editor.snippetProcessor.startPosition(), self.editor.snippetProcessor.endPosition() - length)
            self.editor.textCursor().removeSelectedText()
            #TODO: Hacer esto de purgar de una mejor forma
            self.editor.symbolListModel._purge_blocks()
            self.editor.folding._purge_blocks()
            self.editor.alreadyTypedWords._purge_blocks()
            
            #Insert snippet
            self.editor.snippetProcessor.render()
            self.setCursorPosition(currentHolder.start + holderPosition + (positionAfter - positionBefore))
            self.editor.textCursor().endEditBlock()
        else:
            self.logger.debug("Con cualquier otra tecla sin texto")
            holder = self.editor.snippetProcessor.getHolder(cursor.selectionStart(), cursor.selectionEnd())
            if (holder is None or holder.last) and event.key() in [ QtCore.Qt.Key_Return ]:
                return self.endSnippet(event)
            else:
                return QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            
    def endSnippet(self, event = None):
        self.editor.snippetProcessor.endSnippet()
        if event is not None:
            return self.editor.keyPressEvent(event)

    def setCursorPosition(self, position):
        cursor = self.editor.textCursor()
        cursor.setPosition(position)
        self.editor.setTextCursor(cursor)
        
    def selectSlice(self, start, end):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)

class PMXMultiCursorEditorMode(PMXBaseEditorMode):
    def __init__(self, editor):
        PMXBaseEditorMode.__init__(self, editor)
        self.helper = helpers.MultiCursorHelper()
        self.cursors = []
        self.scursor = self.dragPoint = self.startPoint = self.doublePoint = None
    
    def isActive(self):
        return bool(self.cursors) or self.startPoint != None
    
    def inactive(self):
        self.cursors = []
        self.editor.modeChanged.emit()

    def highlightCurrentLines(self):
        extraSelections = self.editor.extraSelections()
        for cursor in self.cursors:
            selection = QtGui.QTextEdit.ExtraSelection()
            selection.format.setBackground(self.editor.colours['lineHighlight'])
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = QtGui.QTextCursor(cursor)
            selection.cursor.clearSelection()
            extraSelections.append(selection)
            if cursor.hasSelection():
                selection = QtGui.QTextEdit.ExtraSelection()
                selection.format.setBackground(self.editor.colours['selection'])
                selection.cursor = cursor
                extraSelections.append(selection)
        self.editor.setExtraSelections(extraSelections)

    @property
    def isDragCursor(self):
        return self.startPoint != None and self.dragPoint != None

    def getDragCursorRect(self):
        """Retorna un rectangulo que representa la zona del drag cursor"""
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
        emit = points and not self.isActive()
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
                        multicursorAction(cursor)
            else: # Derecha a izquierda
                start, end = tupla
                cursor = self.editor.cursorForPosition(QtCore.QPoint(*start))
                rect = self.editor.cursorRect(cursor)
                if rect.right() - width / 2 <= start[0] <= rect.right() + width / 2 and rect.top() <= start[1] <= rect.bottom():
                    ecursor = self.editor.cursorForPosition(QtCore.QPoint(*end))
                    rect = self.editor.cursorRect(ecursor)
                    if (rect.right() <= end[0] or rect.right() - width / 2 <= end[0] <= rect.right() + width / 2) and rect.top() <= end[1] <= rect.bottom():
                        ecursor.setPosition(cursor.position(), QtGui.QTextCursor.KeepAnchor)
                        multicursorAction(ecursor)
        
        if emit:
            #Arranco modo multicursor
            self.editor.modeChanged.emit()
        #Clean last acction
        self.scursor = self.dragPoint = self.startPoint = self.doublePoint = None

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
        """
        Only can add new cursors, if the cursor has selection then try to merge with others
        """
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
                position = bisect_key(self.cursors, cursor, lambda cursor: cursor.position())
                self.cursors.insert(position, cursor)
        else:
            for c in self.cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if begin <= cursor.position() <= end:
                    return
            position = bisect_key(self.cursors, cursor, lambda cursor: cursor.position())
            self.cursors.insert(position, cursor)
        self.editor.highlightCurrent()

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
                elif (c_begin <= new_begin <= c_end) or (c_begin <= new_end <= c_end):
                    #Recortar
                    if c_begin <= new_begin <= c_end:
                        #Recorta por detras, quitar el actual y agregar uno con la seleccion mas chica
                        newCursor = QtGui.QTextCursor(self.editor.document())
                        if c.position() > new_begin:
                            newCursor.setPosition(c_begin)
                            newCursor.setPosition(new_begin, QtGui.QTextCursor.KeepAnchor)
                        else:
                            newCursor.setPosition(new_begin)
                            newCursor.setPosition(c.position(), QtGui.QTextCursor.KeepAnchor)
                        newCursors.append(newCursor)
                    if c_begin <= new_end <= c_end:
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
            for newCursor in newCursors:
                self.addMergeCursor(newCursor)
        else:
            #Solo puedo quitar cursores que no tengan seleccion osea que sean un clic :)
            for c in self.cursors:
                begin, end = c.selectionStart(), c.selectionEnd()
                if not c.hasSelection() and c.position() == cursor.position():
                    self.cursors.remove(c)
                    break
        self.editor.highlightCurrent()

    def canMoveRight(self):
        return all(map(lambda c: not c.atEnd(), self.cursors))
    
    def canMoveLeft(self):
        return all(map(lambda c: not c.atStart(), self.cursors))
    
    def keyPressEvent(self, event):
        if self.helper.accept(self.editor, event):
            cursor = self.cursors[0] if event.modifiers() & QtCore.Qt.ShiftModifier else self.cursors[-1]
            self.helper.execute(self.editor, event, cursor)
        elif event.key() == QtCore.Qt.Key_Escape:
            #Deprecated usar una lista de cursores ordenados para tomar de [0] y [-1]
            scursor = min(self.cursors, key = lambda cursor: cursor.position())
            ecursor = max(self.cursors, key = lambda cursor: cursor.position())
            self.editor.document().markContentsDirty(scursor.position(), ecursor.position())
            if ecursor.hasSelection():
                ecursor.clearSelection()
            self.editor.setTextCursor(ecursor)
            self.inactive()
            self.editor.highlightCurrent()
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
    
class PMXCompleterEditorMode(QtGui.QCompleter, PMXBaseEditorMode):
    def __init__(self, editor):
        QtGui.QCompleter.__init__(self, editor)
        PMXBaseEditorMode.__init__(self, editor)
        self.setWidget(self.editor)
        self.currentContentWidth = 0

        #Table view
        self.popupView = QtGui.QTableView()
        self.popupView.setAlternatingRowColors(True)
        self.popupView.setWordWrap(False)
        self.popupView.verticalHeader().setVisible(False)
        self.popupView.horizontalHeader().setVisible(False)
        self.popupView.setShowGrid(False)
        self.popupView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popupView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popupView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #Table view size
        spacing = self.popupView.verticalHeader().fontMetrics().lineSpacing()
        self.popupView.verticalHeader().setDefaultSectionSize(spacing + 3);
        self.popupView.horizontalHeader().setStretchLastSection(True)
        self.popupView.setMinimumWidth(spacing * 18)
        #self.popupView.setMinimumHeight(spacing * 12)
        
        self.setPopup(self.popupView)

        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

    def setModel(self, completerTableModel):
        QtGui.QCompleter.setModel(self, completerTableModel)
        #Tenemos Modelo
        #Acomodamos al contenido
        self.popupView.resizeColumnsToContents()
        #self.popupView.resizeRowsToContents()
        #Tomamos ancho de los datos del modelo
        self.currentContentWidth = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.completionModel().sourceModel().columnCount()):
            self.currentContentWidth += self.popup().sizeHintForColumn(columnIndex)

    def isActive(self):
        return self.popup().isVisible()
        
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
            event.ignore()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            
            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()
            
            #TODO: Se puede hacer mejor, para controlar que si esta en la mitad de la palabro o algo de eso
            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                newPrefix = cursor.selectedText()
                if not self.completionModel().hasIndex(1, 0):
                    #Me queda solo una sugerencia, veamos si no es lo que ya esta tipeado y en modo texto :)
                    sIndex = self.completionModel().mapToSource(self.completionModel().index(0, 0))
                    suggestion = self.completionModel().sourceModel().getSuggestion(sIndex)
                    if isinstance(suggestion, basestring) and suggestion == newPrefix:
                        #Se termino
                        self.popup().setVisible(False)
                        return
                self.setCompletionPrefix(newPrefix)
                self.complete(self.editor.cursorRect())
            else:
                self.popup().setVisible(False)
                
    def setStartCursorPosition(self, position):
        self.startCursorPosition = position
        
    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        suggestion = self.completionModel().sourceModel().getSuggestion(sIndex)
        cursor = self.editor.textCursor()
        cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
        if isinstance(suggestion, dict):
            if 'display' in suggestion:
                cursor.insertText(suggestion['display'])
            elif 'title' in suggestion:
                cursor.insertText(suggestion['title'])
        elif isinstance(suggestion, PMXBundleTreeNode):
            cursor.removeSelectedText()
            self.editor.insertBundleItem(suggestion)
        else:
            cursor.insertText(suggestion)

    def complete(self, rect):
        self.popup().setCurrentIndex(self.completionModel().index(0, 0))
        rect.setWidth(self.currentContentWidth)
        #TODO: height
        QtGui.QCompleter.complete(self, rect)
