#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support import PMXMacroProcessor

class PMXMacroProcessor(PMXMacroProcessor):
    def __init__(self, editor):
        super(PMXMacroProcessor, self).__init__()
        self.editor = editor
    
    # Move
    def moveRight(self):
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.position() + 1)
        self.editor.setTextCursor(cursor)
   
    def moveLeft(self):
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.position() - 1)
        self.editor.setTextCursor(cursor)
        
    def selectHardLine(self):
        cursor = self.editor.textCursor()
        block = cursor.block()
        start = block.position()
        next = block.next()
        end = next.position() if next.isValid() else start + block.length() - 1
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        
    def deleteBackward(self):
        self.editor.textCursor().deletePreviousChar()