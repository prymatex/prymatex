#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.support import PMXMacroProcessor
from prymatex.support.command import PMXCommand

class PMXMacroProcessor(PMXMacroProcessor):
    def __init__(self, editor):
        super(PMXMacroProcessor, self).__init__()
        self.editor = editor

    @property
    def environment(self):
        return self.__env
        
    def configure(self, settings):
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})

    def startMacro(self, macro):
        """docstring for startMacro"""
        self.macro = macro
        self.__env = self.editor.buildEnvironment(macro.buildEnvironment())
        self.__env.update(self.baseEnvironment)
        
    def endMacro(self, macro):
        pass

    # Move
    # QTextCursor::NoMove 0 Keep the cursor where it is 
    # QTextCursor::Start 1 Move to the start of the document. 
    # QTextCursor::StartOfLine 3 Move to the start of the current line. 
    # QTextCursor::StartOfBlock 4 Move to the start of the current block. 
    # QTextCursor::StartOfWord 5 Move to the start of the current word. 
    # QTextCursor::PreviousBlock 6 Move to the start of the previous block. 
    # QTextCursor::PreviousCharacter 7 Move to the previous character. 
    # QTextCursor::PreviousWord 8 Move to the beginning of the previous word. 
    # QTextCursor::WordLeft 10 Move left one word. 
    # QTextCursor::End 11 Move to the end of the document. 
    # QTextCursor::EndOfWord 14 Move to the end of the current word. 
    # QTextCursor::EndOfBlock 15 Move to the end of the current block. 
    # QTextCursor::NextBlock 16 Move to the beginning of the next block. 
    # QTextCursor::NextCharacter 17 Move to the next character. 
    # QTextCursor::NextWord 18 Move to the next word. 
    # QTextCursor::WordRight 20 Move right one word. 
    # QTextCursor::NextCell 21 Move to the beginning of the next table cell inside the current table. If the current cell is the last cell in the row, the cursor will move to the first cell in the next row. 
    # QTextCursor::PreviousCell 22 Move to the beginning of the previous table cell inside the current table. If the current cell is the first cell in the row, the cursor will move to the last cell in the previous row. 
    # QTextCursor::NextRow 23 Move to the first new cell of the next row in the current table. 
    # QTextCursor::PreviousRow 24 Move to the last cell of the previous row in the current table. 

    def moveRight(self):
        #QTextCursor::Right 19 Move right one character. 
        self.editor.moveCursor(QtGui.QTextCursor.Right)

    def moveLeft(self):
        #QTextCursor::Left 9 Move left one character.
        self.editor.moveCursor(QtGui.QTextCursor.Left)

    def moveUp(self):
        #QTextCursor::Up 2 Move up one line.
        self.editor.moveCursor(QtGui.QTextCursor.Up)
    
    def moveDown(self):
        #QTextCursor::Down 12 Move down one line. 
        self.editor.moveCursor(QtGui.QTextCursor.Down)
    
    def moveToEndOfLine(self):
        #QTextCursor::EndOfLine 13 Move to the end of the current line.
        self.editor.moveCursor(QtGui.QTextCursor.EndOfLine)
        
    def moveToEndOfParagraph(self):
        self.editor.moveCursor(QtGui.QTextCursor.EndOfBlock)
        
    def moveToBeginningOfLine(self):
        pass
        
    def moveToEndOfDocumentAndModifySelection(self):
        pass
    
    def moveToBeginningOfDocumentAndModifySelection(self):
        pass
    
    def moveRightAndModifySelection(self):
        pass
    
    def selectLine(self):
        self.editor.select(self.editor.SelectLine)
    
    def selectHardLine(self):
        self.editor.select(self.editor.SelectParagraph)

    def deleteBackward(self):
        self.editor.textCursor().deletePreviousChar()

    def insertNewline(self):
        self.editor.insertNewLine()

    def insertText(self, text):
        self.editor.insertPlainText(text)

    def executeCommandWithOptions(self, commandHash):
        command = PMXCommand(self.editor.application.supportManager.uuidgen(), dataHash = commandHash)
        command.setBundle(self.macro.bundle)
        command.setManager(self.macro.manager)
        self.editor.insertBundleItem(command, asynchronous = False)
