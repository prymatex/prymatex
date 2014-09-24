#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import asyncio

import re

from prymatex.qt import QtCore, QtGui, QtWidgets

@asyncio.coroutine
def highlight_function(highlighter, block, stop):
    position = block.position()
    length = 0 
    while block.isValid() and block.blockNumber() <= stop:
        userData = highlighter.syntaxProcessor.blockUserData(block)
        formats = highlighter.themeProcessor.textCharFormats(userData)
        block.layout().setAdditionalFormats(formats)
        length += block.length()
        block = block.next()
        yield
    highlighter.document().markContentsDirty(position, length)

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
        self.editor.aboutToClose.connect(self.stop)
        self.highlightBlock = lambda text: None

    def on_task_finished(self, *args):
        self.highlightBlock = self.syncHighlightFunction
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
            # Setup visible area
            line_height = self.editor.blockBoundingGeometry(self.document().begin()).height()
            screen_height = QtWidgets.QDesktopWidget().screenGeometry().height()
            lines = int(screen_height / line_height)
            # Create tasks
            loop = self.editor.application().loop()
            self.highlight_tasks = [ asyncio.async(highlight_function(self, 
                        self.document().findBlockByNumber(n), n + lines), loop=loop) for n in 
                        range(0, self.document().lineCount(), lines) ]
            self.highlight_task = asyncio.async(asyncio.wait(self.highlight_tasks, loop=loop), loop=loop)
            self.highlight_task.add_done_callback(self.on_task_finished)
            if callable(callback):
                self.highlight_task.add_done_callback(callback)

    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.syntaxProcessor.blockUserData(self.currentBlock())
        for token in userData.tokens():
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
