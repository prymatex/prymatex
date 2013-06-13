#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

from prymatex.gui.codeeditor.processors import CodeEditorSyntaxProcessor
from prymatex.support.syntax import PMXSyntax
from prymatex.utils.decorators.helpers import printtime

class PMXSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    NO_STATE = -1
    SINGLE_LINE = 1
    MULTI_LINE = 2
    FORMAT_CACHE = {}
    
    def __init__(self, editor, syntax = None, theme = None):
        QtGui.QSyntaxHighlighter.__init__(self, editor)
        self.editor = editor
        self.processor = CodeEditorSyntaxProcessor(editor)
        self.syntax = syntax
        self.theme = theme
        
        self.highlightTask = self.editor.application.schedulerManager.idleTask()

    def stop(self):
        self.stopAsyncHighlight()
        self.stopSyncHighlight()

    def stopSyncHighlight(self):
        self.highlightBlock = lambda text: None
    
    def startSyncHighlight(self):
        self.highlightBlock = self.syncHighlightFunction
        
    def stopAsyncHighlight(self):
        if self.highlightTask.isRunning():
            self.highlightTask.cancel()
        
    def runAsyncHighlight(self, callback):
        #Cuidado si estoy corriendo la tarea no correrla nuevamente
        if not self.highlightTask.isRunning():
            self.stopSyncHighlight()
            self.highlightTask = self.editor.application.schedulerManager.newTask(self.asyncHighlightFunction())
            def on_highlightReady():
                self.startSyncHighlight()
                callback()
            self.highlightTask.done.connect(on_highlightReady)

    def setSyntax(self, syntax):
        self.syntax = syntax
        
    def setTheme(self, theme):
        PMXSyntaxHighlighter.FORMAT_CACHE = {}
        self.theme = theme
            
    def asyncHighlightFunction(self):
        block = self.document().begin()
        lastBlock = self.document().lastBlock()
        
        self.processor.startParsing(self.syntax.scopeName)
        stack = [[ self.syntax.grammar, None ]]
        length = 0
        while block.isValid():
            #text = block != lastBlock and block.text() + "\n" or block.text()
            text = block.text() + "\n"

            self.syntax.parseLine(stack, text, self.processor)
            userData = self.editor.blockUserData(block)
            
            self.setupBlockUserData(text, block, userData)
            
            # Store stack and state
            blockState = len(stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE
            if blockState == self.MULTI_LINE:
                userData.setProcessorState((stack[:], self.processor.scopes()[:])) #Store copy
            userData.textHash = hash(text) + hash(self.syntax.scopeName) + blockState
            block.setUserState(blockState)
            
            length += block.length()
            
            formats = []
            for (start, end), scope in userData.scopeRanges():
                frange = QtGui.QTextLayout.FormatRange()
                frange.start = start
                frange.length = end - start
                frange.format = self.highlightFormat(self.editor.scope(scopeHash = scope).name)
                formats.append(frange)

            block.layout().setAdditionalFormats(formats)
            block = block.next()
            yield
        self.document().markContentsDirty(0, length)
        self.processor.endParsing(self.syntax.scopeName)
        
    def setupBlockUserData(self, text, block, userData):
        userData.setTokens(self.processor.tokens())
        userData.setBlank(text.strip() == "")
        # Process by handlers
        self.editor.processBlockUserData(text, block, userData)
    
    def syncHighlightFunction(self, text):
        #if self.currentBlock() != self.document().lastBlock():
        #    text += "\n"
        text += "\n"
        block = self.currentBlock()
        userData = self.editor.blockUserData(block)
        if userData.textHash == hash(text) + hash(self.syntax.scopeName) + self.previousBlockState():
            self.applyFormat(userData)
        else:
            self.processor.startParsing(self.syntax.scopeName)
            if self.previousBlockState() == self.MULTI_LINE:
                #Recupero una copia del stack y los scopes del user data
                stack, scopes = self.editor.blockUserData(block.previous()).processorState()
                #Parche hasta que se solucione lo del puto UserData
                if not stack:
                    stack = [[ self.syntax.grammar, None ]]
                else:
                    #Set copy, not original
                    stack = stack[:]
                    self.processor.setScopes(scopes[:])
            else:
                #Creo un stack y scopes nuevos
                stack = [[ self.syntax.grammar, None ]]

            # A parserar mi amor, vamos a parsear mi amor
            self.syntax.parseLine(stack, text, self.processor)
            self.processor.endParsing(self.syntax.scopeName)
            
            self.setupBlockUserData(text, block, userData)

            # Store stack and state
            blockState = len(stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE
            if blockState == self.MULTI_LINE:
                userData.setProcessorState((stack[:], self.processor.scopes()[:])) #Store copy
            userData.textHash = hash(text) + hash(self.syntax.scopeName) + blockState
            self.setCurrentBlockState(blockState)
            
            self.applyFormat(userData)

    def applyFormat(self, userData):
        for (start, end), scope in userData.scopeRanges():
            frmt = self.highlightFormat(self.editor.scope(scopeHash = scope).name)
            if frmt is not None:
                self.setFormat(start, end - start, frmt)

    def highlightFormat(self, scope):
        if scope not in PMXSyntaxHighlighter.FORMAT_CACHE:
            frmt = QtGui.QTextCharFormat()
            settings = self.theme.getStyle(scope)
            if 'foreground' in settings:
                frmt.setForeground(settings['foreground'])
            if 'background' in settings:
                frmt.setBackground(settings['background'])
            if 'fontStyle' in settings:
                if 'bold' in settings['fontStyle']:
                    frmt.setFontWeight(QtGui.QFont.Bold)
                if 'underline' in settings['fontStyle']:
                    frmt.setFontUnderline(True)
                if 'italic' in settings['fontStyle']:
                    frmt.setFontItalic(True)
            PMXSyntaxHighlighter.FORMAT_CACHE[scope] = frmt 
        return PMXSyntaxHighlighter.FORMAT_CACHE[scope]