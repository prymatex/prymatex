#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from prymatex.support import PMXMacroProcessor
from prymatex.support.command import PMXCommand

class PMXMacroProcessor(PMXMacroProcessor):
    def __init__(self, editor):
        super(PMXMacroProcessor, self).__init__()
        self.editor = editor

    def startMacro(self, macro):
        """docstring for startMacro"""
        self.macro = macro
    
    def endMacro(self, macro):
        pass

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
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        
    def deleteBackward(self):
        self.editor.textCursor().deletePreviousChar()

    def insertText(self, text):
        cursor = self.editor.textCursor()
        cursor.insertText(text)

    def executeCommandWithOptions(self, options):
        uuid = self.macro.manager.uuidgen(options.get('uuid', None))
        command = PMXCommand(uuid, "internal", hash = options)
        command.bundle = self.macro.bundle
        self.editor.insertBundleItem(command)