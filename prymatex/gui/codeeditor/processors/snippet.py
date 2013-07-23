#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
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
        self.indentation = "" if self.disableIndent else self.editor.blockUserData(self.snippetCursorWrapper.block()).indent
        
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
        self.__startPosition = self.caretPosition()

    def endRender(self):
        self.__endPosition = self.caretPosition()
        self.editor.updatePlainText(self.output, self.snippetCursorWrapper)

    def environmentVariables(self):
        return self.__env
    
    def configure(self, settings):
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})

    def caretPosition(self):
        return self.snippetCursorWrapper.selectionStart() + len(self.output)

    def insertText(self, text):
        if self.captures:
            self.captures[-1] = self.captures[-1] + text
        else:
            # Replace new lines and tabs
            text = text.replace('\n', '\n' + self.indentation)
            self.output += text.replace('\t', self.tabreplacement)
    
    def selectHolder(self):
        start, end = self.snippet.currentPosition()
        self.editor.setTextCursor(self.editor.newCursorAtPosition(start, end))
        #if hasattr(holder, 'options'):
        #    self.editor.showFlatPopupMenu(
        #        holder.options, 
        #        lambda index, holder = holder: self.setSnippetHolderOption(holder, index), 
        #        cursorPosition = True)

    def setSnippetHolderOption(self, holder, index):
        if index >= 0:
            holder.setOptionIndex(index)
            # Wrap snippet
            wrapCursor = self.editor.newCursorAtPosition(
                self.startPosition(), self.endPosition())
            #Insert snippet
            self.render(wrapCursor)
            holder = self.nextHolder(holder)
            if holder is not None:
                self.selectHolder(holder)
    
    def nextHolder(self, holder):
        self.snippet.setCurrentHolder(holder)
        return self.snippet.nextHolder()

    def previousHolder(self, holder):
        self.snippet.setCurrentHolder(holder)
        return self.snippet.previousHolder()

    def endPosition(self):
        return self.__endPosition

    def startPosition(self):
        return self.__startPosition

    def render(self, cursor):
        self.snippetCursorWrapper = cursor
        self.snippet.render(self)
