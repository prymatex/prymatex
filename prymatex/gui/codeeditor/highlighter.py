#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from prymatex.utils import asyncio
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

class HighlighterThread(QtCore.QThread):
    def start(self, *args, **kwargs):
        self.running = True
        super(HighlighterThread, self).start(*args, **kwargs)
     
    def stop(self):
        self.running = False
   
    def run(self):
        while self.running:
            self.msleep(100)

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
        self.editor.aboutToClose.connect(self.stop)
        self.thread = HighlighterThread(self)
        # Setup visible area
        block = editor.firstVisibleBlock()
        self.visible_area = block.blockNumber() 
        line_height = self.editor.blockBoundingGeometry(block).height()
        screen_height = QtWidgets.QDesktopWidget().screenGeometry().height()
        self.visible_area = (self.visible_area, self.visible_area + int(screen_height / line_height))

    def on_task_finished(self, *args):
        self.highlightBlock = self.syncHighlightFunction
        self.highlight_task = None
        self.thread.stop()
        self.highlightChanged.emit()

    def isRunning(self):
        return self.thread.isRunning()

    def stop(self):
        self.thread.stop()
        return
        if self.running():
            self.highlight_task.cancel()
        self.highlightBlock = lambda text: None

    def start(self, callback=None):
        self.thread.start()
        return
        if self.syntaxProcessor.ready() and self.themeProcessor.ready():
            self.aboutToHighlightChange.emit()
            # Setup visible area
            line_height = self.editor.blockBoundingGeometry(self.document().begin()).height()
            screen_height = QtWidgets.QDesktopWidget().screenGeometry().height()
            lines = int(screen_height / line_height)
            # Create tasks
            tasks = [ asyncio.async(highlight_function(self, 
                        self.document().findBlockByNumber(n), n + lines)) for n in 
                        range(0, self.document().lineCount(), lines) ]
            self.highlight_task = asyncio.async(asyncio.wait(tasks))
            self.highlight_task.add_done_callback(self.on_task_finished)
            if callable(callback):
                self.highlight_task.add_done_callback(callback)
            self.thread.start()

    def highlightBlock(self, text):
        block = self.currentBlock()
        if self.visible_area[0] <= block.blockNumber() <= self.visible_area[1]:
            userData = self.syntaxProcessor.blockUserData(self.currentBlock())
            for token in userData.tokens():
                self.setFormat(token.start, token.end - token.start,
                    self.themeProcessor.textCharFormat(token.scope))
