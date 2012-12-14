#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.qt.helpers.keyevents import KEY_NUMBERS
from prymatex.utils.lists import bisect_key
from prymatex.gui.codeeditor import helpers
from prymatex.models.support import BundleItemTreeNode
from prymatex.gui.codeeditor.models import PMXCompleterTableModel

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
        QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
        
    def keyReleaseEvent(self, event):
        QtGui.QPlainTextEdit.keyReleaseEvent(self.editor, event)

class PMXSnippetEditorMode(PMXBaseEditorMode):
    def __init__(self, editor):
        PMXBaseEditorMode.__init__(self, editor)
        self.logger = editor.application.getLogger('.'.join([self.__class__.__module__, self.__class__.__name__]))

    def isActive(self):
        return self.editor.snippetProcessor.snippet is not None

    def inactive(self):
        self.editor.endSnippet()

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
                self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (snippet.name, snippet.index + 1, len(snippet)))
                self.editor.snippetProcessor.selectHolder(holder)
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            currentHolder = self.editor.snippetProcessor.getHolder(cursor.selectionStart(), cursor.selectionEnd())
            if currentHolder is None or currentHolder.last:
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
            selectedText = cursor.selectedText().replace(u"\u2029", '\n').replace(u"\u2028", '\n')
            currentHolder.setContent(selectedText)
            
            #Remove text
            self.selectSlice(self.editor.snippetProcessor.startPosition(), self.editor.snippetProcessor.endPosition() - length)
            self.editor.textCursor().removeSelectedText()
            #TODO: Hacer esto de purgar de una mejor forma
            #self.editor.symbolListModel._purge_blocks()
            #self.editor.folding._purge_blocks()
            #self.editor.alreadyTypedWords._purge_blocks()
            
            #Insert snippet
            self.editor.snippetProcessor.render()
            self.setCursorPosition(currentHolder.start + holderPosition + (positionAfter - positionBefore))
            self.editor.textCursor().endEditBlock()
        else:
            self.logger.debug("Con cualquier otra tecla sin texto")
            return QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            
    def endSnippet(self, event = None):
        self.editor.snippetProcessor.endSnippet(self.editor.snippetProcessor.snippet)
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
        # TODO: Buscar una forma mejor de obtener o trabajar con este helper en el modo, quiza filtarndo por clase en el evento
        self.helper = helpers.MultiCursorHelper(editor)
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
        self.editor.setExtraSelectionCursors("selection", filter(lambda c: c.hasSelection(), map(lambda c: QtGui.QTextCursor(c), self.cursors)))
        cursorLines = []
        for cursorLine in map(lambda c: QtGui.QTextCursor(c), self.cursors):
            if all(map(lambda c: c.block() != cursorLine.block(), cursorLines)):
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

class PMXCompleterEditorMode(QtGui.QCompleter, PMXBaseEditorMode):
    def __init__(self, editor):
        QtGui.QCompleter.__init__(self, editor)
        PMXBaseEditorMode.__init__(self, editor)
        self.setWidget(self.editor)

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

        #QCompleter::PopupCompletion	0	Current completions are displayed in a popup window.
        #QCompleter::InlineCompletion	2	Completions appear inline (as selected text).
        #QCompleter::UnfilteredPopupCompletion	1	All possible completions are displayed in a popup window with the most likely suggestion indicated as current.
        self.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.connect(self, QtCore.SIGNAL('activated(QModelIndex)'), self.insertCompletion)

        self.setModel(PMXCompleterTableModel(self))
        
        self.currentSource = None
        self.activeSources = []
        self.completerSuggestions = {}
        self.activatedCallback = None
    
    def fixPopupViewSize(self):
        self.popup().setMinimumHeight(200)
        self.popup().resizeColumnsToContents()
        width = self.popup().verticalScrollBar().sizeHint().width()
        for columnIndex in range(self.completionModel().sourceModel().columnCount()):
            width += self.popup().sizeHintForColumn(columnIndex)
        self.popupView.setMinimumWidth(width)
      
    def hasSource(self, source):
        return source in self.activeSources
        
    def switch(self):
        if len(self.activeSources) > 1:
            index = self.activeSources.index(self.currentSource)
            index = (index + 1) % len(self.activeSources)
            self.currentSource = self.activeSources[index]
            self.completionModel().sourceModel().setSuggestions(self.completerSuggestions[self.currentSource])
            self.fixPopupViewSize()

    def setActivatedCallback(self, callback):
        self.activatedCallback = callback

    def setSource(self, source):
        self.activeSources.append(source)
        self.currentSource = source
        self.completionModel().sourceModel().setSuggestions(self.completerSuggestions[source])
        self.fixPopupViewSize()

    def setSuggestions(self, suggestions, source):
        self.completerSuggestions[source] = suggestions
        self.activeSources.append(source)
        self.currentSource = source
        self.completionModel().sourceModel().setSuggestions(suggestions)
        self.fixPopupViewSize()
        
    def isActive(self):
        return self.popup().isVisible()
        
    def inactive(self):
        self.popup().setVisible(False)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Backtab):
            event.ignore()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space:
            self.editor.switchCompleter()
        elif self.editor.runKeyHelper(event):
            self.inactive()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)

            maxPosition = self.startCursorPosition + len(self.completionPrefix()) + 1
            cursor = self.editor.textCursor()

            if self.startCursorPosition <= cursor.position() <= maxPosition:
                cursor.setPosition(self.startCursorPosition, QtGui.QTextCursor.KeepAnchor)
                self.setCompletionPrefix(cursor.selectedText())
                self.complete(self.editor.cursorRect())
            else:
                self.inactive()

    def onlyOneSameSuggestion(self):
        cursor = self.editor.textCursor()
        if not self.completionModel().hasIndex(1, 0):
            sIndex = self.completionModel().mapToSource(self.completionModel().index(0, 0))
            suggestion = self.completionModel().sourceModel().data(sIndex)
            return suggestion == self.completionPrefix()
        return False

    def setStartCursorPosition(self, position):
        self.setCompletionPrefix("")
        self.activeSources = []
        self.startCursorPosition = position
        
    def insertCompletion(self, index):
        sIndex = self.completionModel().mapToSource(index)
        suggestion = self.completionModel().sourceModel().getSuggestion(sIndex)
        if self.activatedCallback is not None:
            self.activatedCallback(suggestion)
        else:
            _, start, end = self.editor.currentWord(search = False)
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            if isinstance(suggestion, dict):
                if 'display' in suggestion:
                    cursor.insertText(suggestion['display'])
                elif 'title' in suggestion:
                    cursor.insertText(suggestion['title'])
            elif isinstance(suggestion, BundleItemTreeNode):
                cursor.removeSelectedText()
                self.editor.insertBundleItem(suggestion)
            else:
                cursor.insertText(suggestion)
        
    def complete(self, rect):
        if not self.onlyOneSameSuggestion():
            self.popup().setCurrentIndex(self.completionModel().index(0, 0))
            QtGui.QCompleter.complete(self, rect)
        else:
            self.inactive()
