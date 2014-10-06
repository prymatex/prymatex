#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import time
from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    highlightingReady = QtCore.Signal()
    def __init__(self, highlighter):
        super(HighlighterThread, self).__init__(highlighter)
        self._highlighter = highlighter
        self._running = True
    
    def stop(self):
        self._running = False
        self.terminate()
        self.wait()
        self.deleteLater()

    def run(self):
        self.msleep(300)
        block = self.parent().document().begin()
        while block.isValid() and self._running:
            user_data = self.parent().syntaxProcessor.blockUserData(block)
            self.parent()._process(block, user_data)
            formats = self.parent().themeProcessor.textCharFormats(user_data)
            block.layout().setAdditionalFormats(formats)
            block = block.next()
        self.highlightingReady.emit()

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.setDocument(editor.document())
        self.editor = editor
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.editor.aboutToClose.connect(self.stop)
        self.thread = None

    def on_thread_highlightingReady(self):
        self.highlightBlock = self._highlight
        self.document().markContentsDirty(0, self.document().characterCount())
        self.highlightChanged.emit()

    def stop(self):
        self.highlightBlock = self._nop
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

    def start(self, callback=None):
        self.aboutToHighlightChange.emit()
        self.thread = HighlighterThread(self)
        self.thread.highlightingReady.connect(self.on_thread_highlightingReady)
        self.thread.start()

    def _process(self, block, user_data):
        block.setUserData(user_data)
        block.setUserState(user_data.state)
        block.setRevision(user_data.revision)

    def _nop(self, text):
        pass

    def _highlight(self, text):
        block = self.currentBlock()
        # ------ Syntax
        revision = self.syntaxProcessor.buildRevision(block)
        if block.revision() != revision:
            user_data = self.syntaxProcessor.blockUserData(block)
            self._process(block, user_data)
        else:
            user_data = block.userData()

        # ------ Formats
        if user_data is not None:
            for token in user_data.tokens:
                self.setFormat(token.start, token.end - token.start,
                    self.themeProcessor.textCharFormat(token.scope))
