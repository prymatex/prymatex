#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    highlightingReady = QtCore.Signal(object)
    def run(self):
        block = self.parent().document().begin()
        highlighted = []
        while block.isValid():
            data = self.parent().syntaxProcessor.parseBlock(block)
            user_data = CodeEditorBlockUserData(*data)
            highlighted.append((
                block.blockNumber(),
                user_data)
            )
            block = block.next()
            self.usleep(300)
        self.highlightingReady.emit(highlighted)

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
        self.thread = HighlighterThread(self)
        self.thread.highlightingReady.connect(self.on_thread_highlightingReady)

    def on_thread_highlightingReady(self, highlighted):
        for number, user_data in highlighted:
            block = self.document().findBlockByNumber(number)
            self._process(block, user_data)
            self.rehighlightBlock(block)
        self.highlightBlock = self._highlight
        self.highlightChanged.emit()

    def stop(self):
        self.highlightBlock = self._nop
        self.thread.terminate()
        self.thread.wait()

    def start(self, callback=None):
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
