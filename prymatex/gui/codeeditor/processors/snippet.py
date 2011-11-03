#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        self.editor = editor
        self.snippet = None
        self.transformation = None
        self.tabreplacement = "\t"
        self.indentation = ""

    @property
    def environment(self, format = None):
        return self.__env
    
    def configure(self, settings):
        self.tabTriggered = settings.get("tabTriggered", True)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})
        
    def startSnippet(self, snippet):
        '''
            Inicia el snippet
        '''
        self.snippet = snippet
        
        cursor = self.editor.textCursor()
        if self.tabTriggered:
            #Remove Trigger
            for _ in range(len(snippet.tabTrigger)):
                cursor.deletePreviousChar()
        
        self.tabreplacement = self.editor.tabKeyBehavior
        self.indentation = "" if self.disableIndent else cursor.block().userData().indent
        
        self.__env = self.editor.buildEnvironment(snippet.buildEnvironment())

    def startTransformation(self, transformation):
        #TODO: que pasa si tiene transformaciones anidadas, creo que es mejor una lista
        self.transformation = True
        self.capture = ""
        
    def endTransformation(self, transformation):
        self.transformation = False
        self.insertText(transformation.transform(self.capture, self))
        
    def cursorPosition(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            return cursor.selectionStart()
        else:
            return cursor.position()
    
    def setCursorPosition(self, position):
        cursor = self.editor.textCursor()
        cursor.setPosition(position)
        self.editor.setTextCursor(cursor)
    
    def selectSlice(self, start, end):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        
    def selectHolder(self, holder):
        self.selectSlice(holder.start, holder.end)
    
    def insertText(self, text):
        if self.transformation:
            self.capture += text
        else:
            self.editor.textCursor().insertText(text)
    
    def endSnippet(self):
        self.snippet = None
        
    def keyPressEvent(self, event):
        key = event.key()
        cursor = self.editor.textCursor()
        
        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            if cursor.hasSelection():
                holder = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
            else:
                holder = self.snippet.setDefaultHolder(cursor.position())
            if holder == None:
                self.endSnippet()
            if key == Qt.Key_Tab:
                holder = self.snippet.next()
            else:
                holder = self.snippet.previous()
            if holder == None:
                self.setCursorPosition(self.snippet.end)
            else:
                self.selectHolder(holder)
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            if cursor.hasSelection():
                holder = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None:
                    self.endSnippet()
                #Posicion relativa al holder
                position = cursor.selectionStart() - holder.start
                leng = cursor.selectionEnd() - cursor.selectionStart()
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.end - leng, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(cursor.selectedText())
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end - leng)
                self.snippet.render(self)
                self.setCursorPosition(holder.start + position)
            else:
                if key == Qt.Key_Delete:
                    holder = self.snippet.setDefaultHolder(cursor.position() + 1)
                else:
                    holder = self.snippet.setDefaultHolder(cursor.position() - 1)
                if holder == None:
                    self.endSnippet()
                #Posicion relativa al holder
                position = cursor.position() - holder.start
                leng = cursor.selectionEnd() - cursor.selectionStart()
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.end - 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(cursor.selectedText())
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end - 1)
                self.snippet.render(self)
                if key == Qt.Key_Delete:
                    self.setCursorPosition(holder.start + position)
                else:
                    self.setCursorPosition(holder.start + position - 1)
        elif event.text():
            if cursor.hasSelection():
                holder = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None or holder.last:
                    self.endSnippet()
                #Posicion relativa al holder
                position = cursor.selectionStart() - holder.start
                leng = cursor.selectionEnd() - cursor.selectionStart()
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.start + (holder.end - holder.start - leng) + 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(cursor.selectedText())
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end - leng + 1)
                self.snippet.render(self)
                self.setCursorPosition(holder.start + position + 1)
            else:
                holder = self.snippet.setDefaultHolder(cursor.position())
                if holder == None or holder.last:
                    self.endSnippet()
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Posicion relativa al holder
                position = cursor.position() - holder.start
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.end + 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(cursor.selectedText())
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end + 1)
                self.snippet.render(self)
                self.setCursorPosition(holder.start + position)
