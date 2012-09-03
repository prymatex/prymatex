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
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})
        
    def startSnippet(self, snippet):
        """Inicia el snippet"""
        self.snippet = snippet
        self.editor.modeChanged.emit()
        
        cursor = self.editor.textCursor()
        if self.tabTriggered:
            #Remove Trigger
            for _ in range(len(snippet.tabTrigger)):
                cursor.deletePreviousChar()
        
        self.tabreplacement = self.editor.tabKeyBehavior()
        self.indentation = "" if self.disableIndent else cursor.block().userData().indent
        
        self.__env = snippet.buildEnvironment()
        self.__env.update(self.editor.buildEnvironment())
        self.__env.update(self.baseEnvironment)
    
    def endSnippet(self):
        """Termina el snippet"""
        self.snippet = None
        self.editor.modeChanged.emit()

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
    
    def insertText(self, text):
        if self.transformation:
            self.capture += text
        else:
            self.editor.textCursor().insertText(text)
    
    def selectHolder(self, holder):
        cursor = self.editor.textCursor()
        cursor.setPosition(holder.start)
        cursor.setPosition(holder.end, QtGui.QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
    
    def getHolder(self, start, end = None):
        return self.snippet.getHolder(start, end)
    
    def currentHolder(self, start, end):
        #Get the current holder
        holder = self.getHolder(start, end)
        if holder == None: return holder
        self.snippet.setCurrentHolder(holder)
        return holder

    def nextHolder(self, holder):
        self.snippet.setCurrentHolder(holder)
        return self.snippet.next()
    
    def previousHolder(self, holder):
        self.snippet.setCurrentHolder(holder)
        return self.snippet.previous()
    
    def endPosition(self):
        return self.snippet.end
        
    def startPosition(self):
        return self.snippet.start

    def render(self):
        self.snippet.render(self)
