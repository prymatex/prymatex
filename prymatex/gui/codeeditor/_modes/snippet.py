#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorSnippetMode(CodeEditorBaseMode):
    @property
    def snippet(self):
        return self.editor.snippetProcessor.snippet

    def isActive(self):
        return self.snippet is not None

    def inactive(self):
        self.endSnippet()

    def keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Escape:
            self.logger.debug("Se termina el modo snippet")
            return self.endSnippet(event)
        elif event.key() in [ QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab ]:
            self.logger.debug("Camino entre los holders")
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.endSnippet(event)

            if event.key() == QtCore.Qt.Key_Tab:
                ok = self.snippet.nextHolder()
            else:
                ok = self.snippet.previousHolder()
            if not ok:
                self.editor.showMessage("Snippet end")
                self.editor.snippetProcessor.selectHolder()
                self.endSnippet()
            else:
                self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (self.snippet.name, self.snippet.holderNumber(), len(self.snippet)))
                self.editor.snippetProcessor.selectHolder()
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.endSnippet(event)
            
            holderStart, holderEnd = self.snippet.currentPosition()
            #Cuidado con los extremos del holder
            if not cursor.hasSelection():
                if event.key() == QtCore.Qt.Key_Backspace and cursor.position() == holderStart:
                    return self.endSnippet(event)

                if event.key() == QtCore.Qt.Key_Delete and cursor.position() == holderEnd:
                    return self.endSnippet(event)

            holderPosition = cursor.selectionStart() - holderStart
            positionBefore = cursor.selectionStart()
            charactersBefore = cursor.document().characterCount()
            
            #Insert Text
            cursor.beginEditBlock()
            QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = charactersBefore - charactersAfter 
            
            #Capture Text
            cursor.setPosition(holderStart)
            cursor.setPosition(holderEnd - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = self.editor.selectedTextWithEol(cursor)

            self.snippet.setContent(selectedText)
            
            # Wrap snippet
            wrapCursor = self.editor.newCursorAtPosition(
                self.editor.snippetProcessor.startPosition(), self.editor.snippetProcessor.endPosition() - length
            )
            
            #Insert snippet
            self.editor.snippetProcessor.render(wrapCursor)
            
            if selectedText:
                newHolderStart, _ = self.snippet.currentPosition()
                self.editor.setTextCursor(
                    self.editor.newCursorAtPosition(
                        newHolderStart + holderPosition + (positionAfter - positionBefore)
                    )
                )
            elif self.snippet.nextHolder():
                # The holder is killed
                self.editor.snippetProcessor.selectHolder()
            if selectedText and self.snippet.lastHolder():
                # Put text on last holder, force snippet ends
                self.endSnippet()
            cursor.endEditBlock()
        else:
            self.logger.debug("Con cualquier otra tecla sin texto")
            return QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
            
    def endSnippet(self, event = None):
        self.editor.snippetProcessor.endSnippet(self.editor.snippetProcessor.snippet)
        if event is not None:
            return self.editor.keyPressEvent(event)