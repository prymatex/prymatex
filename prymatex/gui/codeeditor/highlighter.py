#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

def _highlight_function(document, processor, theme):
    block = document.begin()
    start, end = (yield)
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
                position = block.position()
                length = 0
            length += block.length()
        elif position is not None:
            document.markContentsDirty(position, length)
            position = None
        else:
            start, end = (yield)
        block = block.next()
    document.markContentsDirty(0, document.characterCount())
            
class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.setDocument(editor.document())
        self.editor = editor
        self.processor = editor.findProcessor("syntax")
        self.theme = None
        self.highlightTask = None
        self.editor.updateRequest.connect(self.on_editor_updateRequest)
        self.editor.aboutToClose.connect(self.stop)

    def on_editor_updateRequest(self, rect, dy):
        if dy and self.running():
            self.highlightTask.sendval = self._task_data()
    
    def _on_worker_finished(self):
        self.highlightBlock = self.syncHighlightFunction
        self.highlightChanged.emit()

    def setTheme(self, theme):
        self.theme = theme

    def running(self):
        return self.highlightTask and self.highlightTask.running()

    def stop(self):
        if self.running():
            self.highlightTask.cancel()
        self.highlightBlock = lambda text: None

    def start(self, callback = None):
        # The task
        self.aboutToHighlightChange.emit()
        self.highlightTask = self.editor.application().schedulerManager.task(
            _highlight_function(self.document(), self.processor, self.theme),
            sendval = self._task_data())
        self.highlightTask.finished.connect(self._on_worker_finished)
        if callback:
            self.highlightTask.done.connect(callback)

    def _task_data(self):
        # Visible area
        start = self.editor.firstVisibleBlock().blockNumber()
        return start, start + 50
    
    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.processor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.theme.textCharFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)
