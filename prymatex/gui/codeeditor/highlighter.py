#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from copy import copy

from prymatex.qt import QtGui, QtCore

from prymatex.gui.codeeditor.processors import PMXSyntaxProcessor, CodeEditorSyntaxProcessor
from prymatex.support.syntax import PMXSyntax
from prymatex.utils.decorators.helpers import printtime

class PMXSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    NO_STATE = -1
    SINGLE_LINE = 1
    FORMAT_CACHE = {}
    
    def __init__(self, editor, syntax = None, theme = None):
        QtGui.QSyntaxHighlighter.__init__(self, editor.document())
        self.editor = editor
        self.processor = CodeEditorSyntaxProcessor(editor)
        self.syntax = syntax
        self.theme = theme
        self.__running = True
        
        #Highlight Function
        self.highlight_function = self.realtime_highlight
        self.highlightTask = self.editor.application.scheduler.idleTask()

    def stop(self):
        self.__running = False
        if self.highlightTask.isRunning():
            self.highlightTask.cancel()
        
    def runAsyncHighlight(self, callback):
        #Cuidado si estoy corriendo la tarea no correrla nuevamente
        if not self.highlightTask.isRunning():
            self.highlight_function = self.async_highlight
            self.__running = True
            self.highlightTask = self.editor.application.scheduler.newTask(self.highlightAllDocument())
            def on_highlightReady():
                #Restore realitme function
                self.highlight_function = self.realtime_highlight
                callback()
            self.highlightTask.done.connect(on_highlightReady)

    def ready(self):
        return self.__running and self.theme is not None and self.syntax is not None

    def setSyntax(self, syntax):
        self.syntax = syntax
        self.rehighlight()
        
    def setTheme(self, theme):
        PMXSyntaxHighlighter.FORMAT_CACHE = {}
        self.theme = theme
        self.rehighlight()
            
    def highlightAllDocument(self):
        block = self.document().begin()
        self.processor.startParsing(self.syntax.scopeName)
        stack = [[self.syntax.grammar, None]]
        while block.isValid():
            text = block.text()
            self.syntax.parseLine(stack, text, self.processor)
            userData = block.userData()
            if userData is None:
                userData = self.editor.blockUserDataFactory(block)
                block.setUserData(userData)
            
            self.setupBlockUserData(text, block, userData)
            
            blockState = len(stack)
            if blockState != self.SINGLE_LINE:
                userData.setProcessorState((copy(stack), copy(self.processor.scopes())))
            userData.textHash = hash(text) + hash(self.syntax.scopeName) + blockState
            block.setUserState(blockState)
            
            self.rehighlightBlock(block)
            block = block.next()
            yield
        self.processor.endParsing(self.syntax.scopeName)
        
    def setupBlockUserData(self, text, block, userData):
        userData.setScopeRanges(self.processor.scopeRanges())
        userData.setLineChunks(self.processor.lineChunks())
        userData.setBlank(text.strip() == "")
        
        self.editor.processBlockUserData(text, block, userData)
        
    
    def highlightBlock(self, text):
        if self.ready():
            self.highlight_function(text)
        
    def async_highlight(self, text):
        userData = self.currentBlock().userData()
        if userData:
            self.applyFormat(userData)
    
    def realtime_highlight(self, text):
        userData = self.currentBlock().userData()
        if userData is not None and userData.textHash == hash(text) + hash(self.syntax.scopeName) + self.previousBlockState():
            self.applyFormat(userData)
        else:
            self.processor.startParsing(self.syntax.scopeName)
            if self.previousBlockState() not in [self.SINGLE_LINE, self.NO_STATE]:
                #Recupero una copia del stack y los scopes del user data
                stack, scopes = self.currentBlock().previous().userData().processorState()
                #Set copy, not original
                stack = stack[:]
                self.processor.setScopes(scopes[:])
            else:
                #Creo un stack y scopes nuevos
                stack = [[self.syntax.grammar, None]]

            # A parserar mi amor, vamos a parsear mi amor
            self.syntax.parseLine(stack, text, self.processor)
            self.processor.endParsing(self.syntax.scopeName)

            if userData is None:
                userData = self.editor.blockUserDataFactory(self.currentBlock())
                self.setCurrentBlockUserData(userData)

            self.setupBlockUserData(text, self.currentBlock(), userData)

            blockState = len(stack)
            
            if blockState != self.SINGLE_LINE:
                userData.setProcessorState((copy(stack), copy(self.processor.scopes())))
            userData.textHash = hash(text) + hash(self.syntax.scopeName) + blockState
            
            self.setCurrentBlockState(blockState)
            self.applyFormat(userData)

    def applyFormat(self, userData):
        for (start, end), scope in userData.scopeRanges():
            format = self.highlightFormat(self.editor.scope(scopeHash = scope, attribute = 'name'))
            if format is not None:
                self.setFormat(start, end - start, format)

    def highlightFormat(self, scope):
        if scope not in PMXSyntaxHighlighter.FORMAT_CACHE:
            format = QtGui.QTextCharFormat()
            settings = self.theme.getStyle(scope)
            if 'foreground' in settings:
                format.setForeground(settings['foreground'])
            if 'background' in settings:
                format.setBackground(settings['background'])
            if 'fontStyle' in settings:
                if 'bold' in settings['fontStyle']:
                    format.setFontWeight(QtGui.QFont.Bold)
                if 'underline' in settings['fontStyle']:
                    format.setFontUnderline(True)
                if 'italic' in settings['fontStyle']:
                    format.setFontItalic(True)
            PMXSyntaxHighlighter.FORMAT_CACHE[scope] = format 
        return PMXSyntaxHighlighter.FORMAT_CACHE[scope]