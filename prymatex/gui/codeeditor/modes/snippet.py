#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorSnippetMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorSnippetMode, self).__init__(**kwargs)
        self.processor = None
        self.enableCompletion = None
        self.setObjectName("CodeEditorSnippetMode")

    def initialize(self, **kwargs):
        super(CodeEditorSnippetMode, self).initialize(**kwargs)
        self.processor = self.editor.findProcessor("snippet")
        self.processor.begin.connect(self.activate)
        self.processor.end.connect(self.deactivate)
        self.editor.installEventFilter(self)

    def eventFilter(self, obj, event):
        if self.isActive() and event.type() == QtCore.QEvent.KeyPress:
            return self.keyPressEvent(event)
        return False

    def keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Escape:
            self.logger.debug("Se termina el modo snippet")
            self.processor.stop()
            return False
        elif event.key() in [ QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab ]:
            self.logger.debug("Camino entre los holders")
            if not self.processor.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                self.processor.stop()
                return False

            if event.key() == QtCore.Qt.Key_Tab:
                ok = self.processor.nextHolder()
            else:
                ok = self.processor.previousHolder()
            if not ok:
                self.editor.showMessage("Snippet end")
                self.processor.stop()
            else:
                # TODO Esto mandarlo al processor para eso esta
                #self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (self.snippet.name, self.snippet.holderNumber(), len(self.snippet)))
                self.processor.selectHolder()
            return True
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            if not self.processor.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                self.processor.stop()
                return False

            if self.processor.lastHolder() and not self.processor.hasHolderContent():
                # Put text on last empty holder
                self.processor.stop()
                return False
            
            holderStart, holderEnd = self.processor.currentPosition()
            #Cuidado con los extremos del holder
            if not cursor.hasSelection():
                if (event.key() == QtCore.Qt.Key_Backspace and cursor.position() == holderStart) or \
                (event.key() == QtCore.Qt.Key_Delete and cursor.position() == holderEnd):
                    self.processor.stop()
                    return False

            holderPosition = cursor.selectionStart() - holderStart
            positionBefore = cursor.selectionStart()
            charactersBefore = cursor.document().characterCount()
            
            #Insert Text
            cursor.beginEditBlock()
            print("snippet keyPressEvent")
            self.editor.keyPressEvent(event)
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = charactersBefore - charactersAfter 
            
            #Capture Text
            cursor.setPosition(holderStart)
            cursor.setPosition(holderEnd - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = self.editor.selectedTextWithEol(cursor)

            self.processor.setHolderContent(selectedText)
            
            # Render
            self.processor.render()
            
            if selectedText:
                newHolderStart, _ = self.processor.currentPosition()
                self.editor.setTextCursor(
                    self.editor.newCursorAtPosition(
                        newHolderStart + holderPosition + (positionAfter - positionBefore)
                    )
                )
            # TODO Esto mejor no, asi se queda igual en el holder aunque no tenga nada
            elif self.processor.nextHolder():
                # The holder is killed
                self.processor.selectHolder()

            cursor.endEditBlock()
            return True
        return False
