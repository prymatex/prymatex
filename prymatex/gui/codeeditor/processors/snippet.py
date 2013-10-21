#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        self.editor = editor
        self.cursorWrapper = self.snippet = None
        self.tabreplacement = "\t"
        self.indentation = ""
        self.__env = None

    def environmentVariables(self):
        if self.__env is None:
            # TODO No es mejor que tambien el editor saque de la mainwindow para 
            # preservar la composision?
            self.__env = {}
            envs = [ self.snippet.environmentVariables(),
                self.editor.mainWindow.environmentVariables(),
                self.editor.environmentVariables(),
                self.baseEnvironment ]
            for env in envs:
                self.__env.update(env)
        return self.__env

    def shellVariables(self):
        leftSettings, rightSettings = self.editor.settings(self.cursorWrapper)
        return rightSettings.shellVariables

    def startSnippet(self, snippet):
        """Inicia el snippet"""
        self.snippet = snippet
        
        self.tabreplacement = self.editor.tabKeyBehavior()
        self.indentation = "" if self.disableIndent else self.editor.blockUserData(self.cursorWrapper.block()).indent
        
        self.__env = None
        self.editor.modeChanged.emit("snippet")

    def endSnippet(self, snippet):
        """Termina el snippet"""
        self.cursorWrapper = self.snippet = None
        self.output = ""
        self.editor.modeChanged.emit("")

    def startRender(self):
        self.output = ""
        self.__startPosition = self.caretPosition()

    def endRender(self):
        self.__endPosition = self.caretPosition()
        self.editor.updatePlainText(self.output, self.cursorWrapper)

    def configure(self, settings):
        self.cursorWrapper = settings.get("cursorWrapper", self.editor.textCursor())
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})

    def caretPosition(self):
        return self.cursorWrapper.selectionStart() + len(self.output)

    def insertText(self, text):
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
    
    def runShellScript(self, script):
        context = self.editor.application.supportManager.runSystemCommand(
            shellCommand = script,
            environment = self.environmentVariables(),
            shellVariables = self.shellVariables()
        )
        return context.outputValue.strip()
    
    def endPosition(self):
        return self.__endPosition

    def startPosition(self):
        return self.__startPosition

    def render(self, cursor):
        self.cursorWrapper = cursor
        self.snippet.render(self)
