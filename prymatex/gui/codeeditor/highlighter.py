#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import time
from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    highlightReady = QtCore.Signal()
    highlightBlockReady = QtCore.Signal(int, object, list)
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
        self.msleep(100)
        block = self.parent().document().begin()
        syntaxProcessor = self.parent().syntaxProcessor
        themeProcessor = self.parent().themeProcessor
        while block.isValid() and self._running:
            self.usleep(1)
            user_data = syntaxProcessor.blockUserData(block)
            formats = themeProcessor.textCharFormats(user_data)
            self.highlightBlockReady.emit(block.blockNumber(), user_data, formats)
            block = block.next()
        print("listo, aviso al resto")
        self.highlightReady.emit()

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.highlightBlock = self._nop
        self.setDocument(editor.document())
        self.editor = editor
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.editor.aboutToClose.connect(self.stop)
        self.thread = None

    def on_thread_highlightingReady(self):
        self.highlightBlock = self._highlight
        self.document().markContentsDirty(0, self.document().characterCount())

    def on_thread_highlightBlockReady(self, block_number, user_data, formats):
        block = self.document().findBlockByNumber(block_number)
        self._process(block, user_data)
        block.layout().setAdditionalFormats(formats)

    def stop(self):
        #return
        self.highlightBlock = self._nop
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

    def start(self, callback=None):
        #self.rehighlight()
        #return
        self.thread = HighlighterThread(self)
        self.thread.highlightReady.connect(self.on_thread_highlightingReady)
        self.thread.highlightBlockReady.connect(self.on_thread_highlightBlockReady)
        self.thread.highlightReady.connect(self.editor.highlightReady.emit)
        self.thread.started.connect(self.editor.aboutToHighlightChange.emit)
        self.thread.finished.connect(self.editor.highlightChanged.emit)
        self.thread.start()

    def _process(self, block, user_data):
        block.setUserData(user_data)
        block.setUserState(user_data.state)

    def _nop(self, text):
        pass

    def _highlight(self, text):
        block = self.currentBlock()

        # ------ Syntax
        if not self.syntaxProcessor.testRevision(block):
            user_data = self.syntaxProcessor.blockUserData(block)
            self._process(block, user_data)
        else:
            user_data = block.userData()

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
