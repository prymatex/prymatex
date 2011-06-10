#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        super(PMXSnippetProcessor, self).__init__()
        self.editor = editor
        self.snippet = None
        self.transformation = None
        self.tabreplacement = "\t"
        self.indentation = ""
        self.tabTrigger = True
        self.disableIndent = False

    @property
    def hasSnippet(self):
        return self.snippet is not None
    
    @property
    def environment(self, format = None):
        return self.__env
    
    def configure(self, tabTrigger, disableIndent):
        self.tabTrigger = tabTrigger
        self.disableIndent = disableIndent
        
    def startSnippet(self, snippet):
        '''
            Inicia el snippet
        '''
        self.snippet = snippet
        
        cursor = self.editor.textCursor()
        if self.tabTrigger:
            #Remove Trigger
            for _ in range(len(snippet.tabTrigger)):
                cursor.deletePreviousChar()
        
        self.tabreplacement = self.editor.tabKeyBehavior
        self.indentation = "" if self.disableIndent else cursor.block().userData().indent
        
        env = snippet.buildEnvironment()
        env.update(self.editor.buildEnvironment())
        self.__env = env

    def startTransformation(self, transformation):
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
                return False
            if key == Qt.Key_Tab:
                holder = self.snippet.next()
            else:
                holder = self.snippet.previous()
            if holder == None:
                self.setCursorPosition(self.snippet.ends)
            else:
                self.selectHolder(holder)
            return True
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            if cursor.hasSelection():
                holder = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None:
                    self.endSnippet()
                    return False
                holder.setContent("")
                self.selectSlice(self.snippet.start, self.snippet.end)
                self.snippet.render(self)
                self.setCursorPosition(holder.start)
            else:
                if key == Qt.Key_Delete:
                    holder = self.snippet.setDefaultHolder(cursor.position() + 1)
                else:
                    holder = self.snippet.setDefaultHolder(cursor.position())
                if holder == None:
                    self.endSnippet()
                    return False
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                position = cursor.position()
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.end - 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(unicode(cursor.selectedText()))
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end - 1)
                self.snippet.render(self)
                if holder.start <= position <= holder.end:
                    self.setCursorPosition(position)
                else:
                    self.setCursorPosition(holder.start)
            return True
        elif event.text(): #Para latin poner otra cosa
            if cursor.hasSelection():
                holder = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None or holder.last:
                    self.endSnippet()
                    return False
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Posicion relativa al holder
                position = cursor.position()
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.start + 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(unicode(cursor.selectedText()))
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end - len(holder) + 1)
                self.snippet.render(self)
                self.setCursorPosition(position)
            else:
                holder = self.snippet.setDefaultHolder(cursor.position())
                if holder == None or holder.last:
                    self.endSnippet()
                    return False
                QtGui.QPlainTextEdit.keyPressEvent(self.editor, event)
                #Posicion relativa al holder
                position = cursor.position() - holder.start
                #Capture Text
                cursor.setPosition(holder.start)
                cursor.setPosition(holder.end + 1, QtGui.QTextCursor.KeepAnchor)
                holder.setContent(unicode(cursor.selectedText()))
                #Prepare replace
                self.selectSlice(self.snippet.start, self.snippet.end + 1)
                self.snippet.render(self)
                self.setCursorPosition(holder.start + position)
            return True