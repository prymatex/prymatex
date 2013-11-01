#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorSnippetMode(CodeEditorBaseMode):
    @property
    def snippet(self):
        return self.editor.snippetProcessor.snippet

    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)
        editor.installEventFilter(self)
    
    def isActive(self):
        return self.snippet is not None

    def inactive(self, handled):
        self.editor.snippetProcessor.endSnippet(self.snippet)
        return handled

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and self.isActive():
            return self.keyPressEvent(event)
        return False

    def keyPressEvent(self, event):
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Escape:
            self.logger.debug("Se termina el modo snippet")
            return self.inactive(False)
        elif event.key() in [ QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab ]:
            self.logger.debug("Camino entre los holders")
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.inactive(False)

            if event.key() == QtCore.Qt.Key_Tab:
                ok = self.snippet.nextHolder()
            else:
                ok = self.snippet.previousHolder()
            if not ok:
                self.editor.showMessage("Snippet end")
                self.editor.snippetProcessor.selectHolder()
                self.inactive()
            else:
                self.editor.showMessage("<i>&laquo;%s&raquo;</i> %s of %s" % (self.snippet.name, self.snippet.holderNumber(), len(self.snippet)))
                self.editor.snippetProcessor.selectHolder()
            return True
        elif event.text():
            self.logger.debug("Con texto %s" % event.text())
            if not self.snippet.setHolder(cursor.selectionStart(), cursor.selectionEnd()):
                return self.inactive(False)
            
            if self.snippet.lastHolder() and not self.snippet.hasHolderContent():
                # Put text on last empty holder, force snippet ends
                return self.inactive(False)
            
            holderStart, holderEnd = self.snippet.currentPosition()
            #Cuidado con los extremos del holder
            if not cursor.hasSelection():
                if (event.key() == QtCore.Qt.Key_Backspace and cursor.position() == holderStart) or \
                (event.key() == QtCore.Qt.Key_Delete and cursor.position() == holderEnd):
                    return self.inactive(False)

            holderPosition = cursor.selectionStart() - holderStart
            positionBefore = cursor.selectionStart()
            charactersBefore = cursor.document().characterCount()
            
            #Insert Text
            cursor.beginEditBlock()
            self.editor.keyPressEvent(event)
            positionAfter = cursor.position()
            charactersAfter = cursor.document().characterCount()
            length = charactersBefore - charactersAfter 
            
            #Capture Text
            cursor.setPosition(holderStart)
            cursor.setPosition(holderEnd - length, QtGui.QTextCursor.KeepAnchor)
            selectedText = self.editor.selectedTextWithEol(cursor)

            self.snippet.setHolderContent(selectedText)
            
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

            cursor.endEditBlock()
            return True
        return False
