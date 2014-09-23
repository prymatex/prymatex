#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import asyncio

import re

from prymatex.qt import QtGui, QtCore

@asyncio.coroutine
def highlight_function(highlighter):
    block = highlighter.document().begin()
    position = None
    length = 0
    while block.isValid():
        userData = highlighter.syntaxProcessor.blockUserData(block)
        
        def formats(themeProcessor):
            for token in userData.tokens():
                frange = QtGui.QTextLayout.FormatRange()
                frange.start = token.start
                frange.length = token.end - token.start
                frange.format = themeProcessor.textCharFormat(token.scope)
                yield frange

        block.layout().setAdditionalFormats(list(formats(highlighter.themeProcessor)))
        if highlighter.visible_area[0] <= block.blockNumber() <= highlighter.visible_area[1]:
            if position is None:
                position = block.position()
                length = 0
            length += block.length()
        elif position is not None:
            highlighter.document().markContentsDirty(position, length)
            position = None
        else:
            visible_range = yield
        block = block.next()
    highlighter.document().markContentsDirty(0, document.characterCount())
    
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
        self.visible_area = self.editor.firstVisibleBlock().blockNumber()
        self.visible_area = (self.visible_area, self.visible_area + 50)
        self.editor.updateRequest.connect(self.on_editor_updateRequest)
        self.editor.aboutToClose.connect(self.stop)

    def on_editor_updateRequest(self, rect, dy):
        if dy:
            self.visible_area = self.editor.firstVisibleBlock().blockNumber()
            self.visible_area = (self.visible_area, self.visible_area + 50)
    
    def on_task_finished(self, *args):
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
            loop = self.editor.application().loop()
            self.highlight_task = asyncio.async(highlight_function(self), loop=loop)
            self.highlight_task.add_done_callback(self.on_task_finished)
            if callable(callback):
                self.highlight_task.add_done_callback(callback)

    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.syntaxProcessor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.themeProcessor.textCharFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)
