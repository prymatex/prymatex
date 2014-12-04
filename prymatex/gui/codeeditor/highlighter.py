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
        self._stopped = False
        print(self._document)

    def stop(self):
        self._stopped = True
        self.wait()
        self.deleteLater()

    def run(self):
        self.msleep(100)
        block = self._document.begin()
        user_datas = {}
        user_data = None
        while block.isValid() and self._stopped:
            user_data = self._processor.blockUserData(block, user_data)
            user_datas[block.blockNumber()] = user_data
            block = block.next()
        if not self._stopped:
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
        print("ready bitch")

    def stop(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.setDocument(None)
            print("stop bitch")

    def start(self, callback=None):
        if self.syntaxProcessor.isReady():
            print("run bitch", self.themeProcessor.isReady())
            self.thread = HighlighterThread(self.editor.document(), self.syntaxProcessor)
            self.thread.ready.connect(self.on_thread_ready)
            self.thread.started.connect(self.aboutToChange.emit)
            self.thread.finished.connect(self.changed.emit)
            self.thread.start()

    def highlightBlock(self, text):
        block = self.currentBlock()

        # ------ No changes
        if self.syntaxProcessor.testRevision(block):
            user_data = block.userData()
        else:
            # ------ Cache or build
            block_number = block.blockNumber()
            user_data = self._user_datas.pop(block_number) \
                if block_number in self._user_datas \
                else self.syntaxProcessor.blockUserData(block)
            self.setCurrentBlockUserData(user_data)
            self.setCurrentBlockState(user_data.state)

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
