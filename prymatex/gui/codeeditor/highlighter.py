#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from prymatex.qt import QtGui, QtCore

def _highlight_function(document, processor):
    try:
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
                    position = block.position()
                    length = 0
                length += block.length()
            elif position is not None:
                document.markContentsDirty(position, length)
                position = None
            else:
                start, end, theme = (yield)
            block = block.next()
    finally:
        print("Se termino")

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.editor = editor
        self.processor = editor.findProcessor("syntax")
	#self.theme = editor.defaultTheme()
        self.theme = None

        self.editor.updateRequest.connect(self.on_editor_updateRequest)
        self.editor.themeChanged.connect(self.on_editor_themeChanged)
        
        # The task
        self.highlightWorker = self.editor.application.schedulerManager.worker(
            _highlight_function,
            self.editor.document(), self.processor)
        self.highlightWorker.started.connect(self.on_worker_started)
        self.highlightWorker.finished.connect(self.on_worker_finished)
        self.editor.aboutToClose.connect(self.stop)

    def on_editor_updateRequest(self, rect, dy):
        if dy:
            self.highlightWorker.send(self._worker_data())

    def on_editor_themeChanged(self, theme):
	self.theme = theme
        self.highlightWorker.send(self._worker_data())

    def on_worker_started(self):
        self.aboutToHighlightChange.emit()
        self.highlightBlock = lambda text: None

    def on_worker_finished(self):
        self.highlightChanged.emit()
        self.highlightBlock = self.syncHighlightFunction

    def stop(self):
        self.highlightWorker.stop()

    def start(self, callback = None):
        if self.highlightWorker.running():
            self.highlightWorker.stop()
        self.highlightWorker.start(callback = callback,
            sendval = self._worker_data())

    def _worker_data(self):
        # Visible area
        start = self.editor.firstVisibleBlock().blockNumber()
        return start, start + 50, self.theme
    
    def syncHighlightFunction(self, text):
        block = self.currentBlock()
        userData = self.processor.blockUserData(self.currentBlock())
        
        self.applyFormat(userData)

    def applyFormat(self, userData):
        for token in userData.tokens():
            frmt = self.theme.textCharFormat(token.scope)
            if frmt is not None:
                self.setFormat(token.start, token.end - token.start, frmt)
