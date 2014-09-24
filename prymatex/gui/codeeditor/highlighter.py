#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import asyncio

import re

from prymatex.qt import QtGui, QtCore

@asyncio.coroutine
def highlight_function(highlighter, block):
    position = None
    length = 0
    while block.isValid():
        userData, uchanged = highlighter.syntaxProcessor.blockUserData(block)
        formats, tchanged = highlighter.themeProcessor.textCharFormats(userData)
        if (not uchanged and not tchanged):
            return
        block.layout().setAdditionalFormats(formats)
        if highlighter.visible_area[0] <= block.blockNumber() <= highlighter.visible_area[1]:
            if position is None:
                position = block.position()
                length = 0
            length += block.length()
        elif position is not None:
            highlighter.document().markContentsDirty(position, length)
            position = None
        else:
            yield
        block = block.next()

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
        self.highlight_tasks = []
        self.editor.updateRequest.connect(self.update_visible_area)
        self.editor.aboutToClose.connect(self.stop)
        self.highlightBlock = lambda text: None

    def update_visible_area(self, *args):
        block = self.editor.firstVisibleBlock()
        start = block.blockNumber()
        offset = int(self.editor.viewport().height() / self.editor.blockBoundingGeometry(block).height())
        self.visible_area = (start, start + offset)

    def on_task_finished(self, *args):
        self.highlightBlock = self.syncHighlightFunction
        self.document().markContentsDirty(0, self.document().characterCount())
        self.highlight_task = None
        self.highlightChanged.emit()

    def running(self):
        return self.highlight_task and not self.highlight_task.done()

    def stop(self):
        if self.running():
            self.highlight_task.cancel()
            [ task.cancel() for task in self.highlight_tasks ]
        self.highlightBlock = lambda text: None

    def start(self, callback=None):
        if self.syntaxProcessor.ready() and self.themeProcessor.ready():
            self.aboutToHighlightChange.emit()
            loop = self.editor.application().loop()
            self.highlight_tasks = [ asyncio.async(highlight_function(self, 
                        self.document().findBlockByNumber(n)), loop=loop) for n in 
                        range(0, self.document().lineCount(), 20) ]
            self.highlight_task = asyncio.async(asyncio.wait(self.highlight_tasks, loop=loop), loop=loop)
            self.highlight_task.add_done_callback(self.on_task_finished)
            if callable(callback):
                self.highlight_task.add_done_callback(callback)

    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData, changed = self.syntaxProcessor.blockUserData(self.currentBlock())
        for token in userData.tokens():
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
