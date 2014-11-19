#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import time
from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    ready = QtCore.Signal(dict)
    def __init__(self, document, processor):
        super(HighlighterThread, self).__init__(document)
        self._document = document
        self._processor = processor
        self._running = True

    def stop(self):
        self._running = False
        self.terminate()
        self.wait()
        self.deleteLater()

    def run(self):
        self.msleep(100)
        block = self._document.begin()
        user_datas = {}
        while block.isValid() and self._running:
            self.usleep(1)
            user_datas[block.blockNumber()] = self._processor.blockUserData(block)
            block = block.next()
        self.ready.emit(user_datas)

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToChange = QtCore.Signal()  # When the highlight go to change allways triggered
    ready = QtCore.Signal()       # When the highlight is ready not allways triggered
    changed = QtCore.Signal()        # On the highlight changed allways triggered

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.editor = editor
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.editor.aboutToClose.connect(self.stop)
        self.thread = None
        self._user_datas = {}

    def on_thread_ready(self, user_datas):
        self._user_datas = user_datas
        self.setDocument(self.editor.document())
        self.ready.emit()

    def stop(self):
        self.setDocument(None)
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

    def start(self, callback=None):
        self.thread = HighlighterThread(self.editor.document(), self.syntaxProcessor)
        self.thread.ready.connect(self.on_thread_ready)
        self.thread.started.connect(self.aboutToChange.emit)
        self.thread.finished.connect(self.changed.emit)
        self.thread.start()

    def _process(self, block, user_data):
        block.setUserData(user_data)
        block.setUserState(user_data.state)

    def highlightBlock(self, text):
        block = self.currentBlock()

        # ------ Cache
        if block.blockNumber() in self._user_datas:
            user_data = self._user_datas.pop(block.blockNumber())
            self._process(block, user_data)
        # ------ No changes
        elif self.syntaxProcessor.testRevision(block):
            user_data = block.userData()
        # ------ Build
        else:
            user_data = self.syntaxProcessor.blockUserData(block)
            self._process(block, user_data)

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
