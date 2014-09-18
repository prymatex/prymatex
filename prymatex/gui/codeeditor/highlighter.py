#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import asyncio

import re

from prymatex.qt import QtGui, QtCore

@asyncio.coroutine
def highlight_function(document, visible_range, syntaxProcessor, themeProcessor):
    block = document.begin()
    position = None
    length = 0
    while block.isValid():
        userData = syntaxProcessor.blockUserData(block)
        
        formats = []
        for token in userData.tokens():
            frange = QtGui.QTextLayout.FormatRange()
            frange.start = token.start
            frange.length = token.end - token.start
            frange.format = themeProcessor.textCharFormat(token.scope)
            formats.append(frange)

        block.layout().setAdditionalFormats(formats)
        if visible_range and visible_range[0] <= block.blockNumber() <= visible_range[1]:
            if position is None:
                position = block.position()
                length = 0
            length += block.length()
        elif position is not None:
            document.markContentsDirty(position, length)
            position = None
        else:
            visible_range = yield
        block = block.next()
    document.markContentsDirty(0, document.characterCount())
    
class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.setDocument(editor.document())
        self.editor = editor
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.highlight_task = None
        self.editor.updateRequest.connect(self.on_editor_updateRequest)
        self.editor.aboutToClose.connect(self.stop)

    def on_editor_updateRequest(self, rect, dy):
        if dy and self.running():
            self.highlight_coroutine.send(self.visible_range())
    
    def _on_task_finished(self, *args):
        self.highlightBlock = self.syncHighlightFunction
        self.highlightChanged.emit()

    def running(self):
        return self.highlight_task and not self.highlight_task.done()

    def stop(self):
        if self.running():
            self.highlight_task.cancel()
        self.highlightBlock = lambda text: None

    def start(self, callback=None):
        if self.syntaxProcessor.ready() and self.themeProcessor.ready():
            self.aboutToHighlightChange.emit()
            visible_range = self.visible_range()
            loop = self.editor.application().loop()
            self.highlight_coroutine = highlight_function(self.document(), 
                visible_range, self.syntaxProcessor, self.themeProcessor)
            self.highlight_task = asyncio.async(self.highlight_coroutine, loop=loop)
            self.highlight_task.add_done_callback(self._on_task_finished)
            if callable(callback):
                self.highlight_task.add_done_callback(callback)

    def visible_range(self):
        # Visible area
        start = self.editor.firstVisibleBlock().blockNumber()
        return start, start + 50
    
    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.syntaxProcessor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.themeProcessor.textCharFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)
