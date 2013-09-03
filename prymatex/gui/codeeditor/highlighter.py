#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

from prymatex.gui.codeeditor.processors import CodeEditorSyntaxProcessor

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
        self.__format_cache = None
        
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
        self.__format_cache = PMXSyntaxHighlighter.FORMAT_CACHE.setdefault(theme.uuidAsText(), {})
        self.theme = theme

    def asyncHighlightFunction(self):
        block = self.document().begin()
        scopeName = self.syntax.scopeName
        
        self.processor.startParsing(scopeName)
        stack = [( self.syntax.grammar, None )]
        blockState = -1
        while block.isValid():
            text = block.text() + "\n"
            userData = self.editor.blockUserData(block)
            
            if not userData.testStateHash(self.__build_userData_hash(scopeName, text, blockState)):
                self.syntax.parseLine(stack, text, self.processor)

                self.setupBlockUserData(text, block, userData)
                userData.setStateHash(self.__build_userData_hash(scopeName, text, blockState))

                # Store stack and state
                blockState = len(stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE
                if blockState == self.MULTI_LINE:
                    userData.setProcessorState((stack[:], self.processor.scopes()[:])) #Store copy
                block.setUserState(blockState)
            else:
                blockState = block.userState()

            formats = []
            for token in userData.tokens():
                frange = QtGui.QTextLayout.FormatRange()
                frange.start = token.start
                frange.length = token.end - token.start
                frange.format = self.highlightFormat(self.editor.scope(
                    scopeHash = token.scopeHash).path)
                formats.append(frange)

            block.layout().setAdditionalFormats(formats)
            block = block.next()
            yield
        self.document().markContentsDirty(0, self.document().characterCount())
        self.processor.endParsing(self.syntax.scopeName)
    
    @staticmethod
    def __build_userData_hash(scope, text, state):
        return hash("%s:%s:%s" % (scope, text, state))

    def setupBlockUserData(self, text, block, userData):
        userData.setTokens(self.processor.tokens())
        userData.setBlank(text.strip() == "")
        # Process by handlers
        self.editor.processBlockUserData(text, block, userData)
    
    def syncHighlightFunction(self, text):
        text += "\n"
        block = self.currentBlock()
        userData = self.editor.blockUserData(block)
        if userData.testStateHash(self.__build_userData_hash(self.syntax.scopeName, text, self.previousBlockState())):
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
            userData.setStateHash(self.__build_userData_hash(self.syntax.scopeName, text, self.previousBlockState()))
            
            # Store stack and state
            blockState = len(stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE
            if blockState == self.MULTI_LINE:
                userData.setProcessorState((stack[:], self.processor.scopes()[:])) #Store copy
            self.setCurrentBlockState(blockState)

            self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.highlightFormat(self.editor.scope(scopeHash = token.scopeHash).path)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)

    def highlightFormat(self, scopePath):
        if scopePath not in self.__format_cache:
            frmt = QtGui.QTextCharFormat()
            settings = self.theme.getStyle(scopePath)
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
            self.__format_cache[scopePath] = frmt 
        return self.__format_cache[scopePath]