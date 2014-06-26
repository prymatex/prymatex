#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

def _highlight_function(document, processor):
    block = document.begin()
    start, end, theme = (yield)
    position = None
    length = 0
    while block.isValid():
        userData = processor.blockUserData(block)
        
        formats = []
        for token in userData.tokens():
            frange = QtGui.QTextLayout.FormatRange()
            frange.start = token.start
            frange.length = token.end - token.start
            frange.format = theme.textCharFormat(token.scope)
            formats.append(frange)

        block.layout().setAdditionalFormats(formats)
        if start <= block.blockNumber() <= end:
            if position is None:
                positon = block.position()
                length = 0
            length += block.length()
        elif position is not None:
            document.markContentsDirty(position, length)
            position = None
        else:
            start, end, theme = (yield)
        block = block.next()

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    FORMAT_CACHE = {}
    
    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.editor = editor
        self.processor = editor.findProcessor("syntax")
        self.theme = None
        self.__format_cache = None
        
        # Visible area
        self.visible_start = self.editor.firstVisibleBlock().blockNumber()
        self.visible_end = self.visible_start + 50
        self.editor.updateRequest.connect(self.on_editor_updateRequest)
        
        # The task
        self.editor.aboutToClose.connect(self.stop)        
        self.highlightTask = self.editor.application.schedulerManager.idleTask()

    def on_editor_updateRequest(self, rect, dy):
        if dy:
            self.visible_start = self.editor.firstVisibleBlock().blockNumber()
            self.visible_end = self.visible_start + 50

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
        while block.isValid():
            userData = self.processor.blockUserData(block)
            
            formats = []
            for token in userData.tokens():
                frange = QtGui.QTextLayout.FormatRange()
                frange.start = token.start
                frange.length = token.end - token.start
                frange.format = self.theme.textCharFormat(token.scope)
                formats.append(frange)

            block.layout().setAdditionalFormats(formats)
            block = block.next()
            if self.visible_start <= block.blockNumber() <= self.visible_end:
                self.document().markContentsDirty(block.position(), block.length())
            yield

    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.processor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.theme.textCharFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)
