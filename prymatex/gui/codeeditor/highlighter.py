#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    FORMAT_CACHE = {}
    
    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.editor = editor
        self.theme = None
        self.__format_cache = None
        
        self.editor.aboutToClose.connect(self.stop)        
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
    
    def setTheme(self, theme):
        self.__format_cache = self.FORMAT_CACHE.setdefault(theme.uuidAsText(), {})
        self.theme = theme

    def asyncHighlightFunction(self):
        block = self.document().begin()
        processor = self.editor.findProcessor("syntax")
        while block.isValid():
            userData = processor.blockUserData(block)
            
            formats = []
            for token in userData.tokens():
                frange = QtGui.QTextLayout.FormatRange()
                frange.start = token.start
                frange.length = token.end - token.start
                frange.format = self.highlightFormat(token.scope)
                formats.append(frange)

            block.layout().setAdditionalFormats(formats)
            block = block.next()
            yield
        self.document().markContentsDirty(0, self.document().characterCount())

    def syncHighlightFunction(self, text):
        # TODO: Obtener el processor en el init del editor
        processor = self.editor.findProcessor("syntax")
        block = self.currentBlock()
        userData = processor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.highlightFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)

    def highlightFormat(self, scope):
        if scope not in self.__format_cache:
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
            self.__format_cache[scope] = frmt
        return self.__format_cache[scope]
