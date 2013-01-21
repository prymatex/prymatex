#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        self.editor = editor
        self.snippetCursorWrapper = self.snippet = None
        self.tabreplacement = "\t"
        self.indentation = ""
        self.__env = {}

    def startSnippet(self, snippet):
        """Inicia el snippet"""
        self.snippet = snippet
        self.editor.modeChanged.emit()
        
        self.snippetCursorWrapper = self.editor.textCursor()
        if self.tabTriggered:
            self.snippetCursorWrapper.setPosition(self.snippetCursorWrapper.position() - len(snippet.tabTrigger), QtGui.QTextCursor.KeepAnchor)
        
        self.tabreplacement = self.editor.tabKeyBehavior()
        self.indentation = "" if self.disableIndent else self.snippetCursorWrapper.block().userData().indent
        
        self.__env = snippet.environmentVariables()
        self.__env.update(self.editor.mainWindow.environmentVariables())
        self.__env.update(self.editor.environmentVariables())
        self.__env.update(self.baseEnvironment)


    def endSnippet(self, snippet):
        """Termina el snippet"""
        self.snippetCursorWrapper = self.snippet = None
        self.output = ""
        self.editor.modeChanged.emit()


    def startRender(self):
        self.output = ""
        self.captures = []


    def endRender(self):
        self.editor.updatePlainText(self.output, self.snippetCursorWrapper)


    def environmentVariables(self):
        return self.__env

    
    def configure(self, settings):
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})

        
    def startTransformation(self, transformation):
        self.captures.append("")


    def endTransformation(self, transformation):
        captured = self.captures.pop()
        self.insertText(transformation.transform(captured, self))


    def caretPosition(self):
        return self.snippetCursorWrapper.selectionStart() + len(self.output)


    def insertText(self, text):
        if self.captures:
            self.captures[-1] = self.captures[-1] + text
        else:
            self.output += text

    
    def selectHolder(self, holder):
        self.editor.setTextCursor(self.editor.newCursorAtPosition(holder.start, holder.end))


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


    def render(self, cursor):
        self.snippetCursorWrapper = cursor
        self.snippet.render(self)
