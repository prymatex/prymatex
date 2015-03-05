#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import time
from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class _HighlighterThread(QtCore.QThread):
    ready = QtCore.Signal(dict)
    def __init__(self, document, processor):
        super(HighlighterThread, self).__init__(document)
        self._document = document
        self._processor = processor
        self._stopped = False

    def stop(self):
        self._stopped = True
        self.wait()
        self.deleteLater()

    def run(self):
        self.msleep(300)
        block = self._document.begin()
        user_datas = {}
        user_data = None
        while block.isValid() and not self._stopped:
            user_data = self._processor.blockUserData(block, user_data)
            user_datas[block.blockNumber()] = user_data
            block = block.next()
        if not self._stopped:
            self.ready.emit(user_datas)

class HighlighterThread(QtCore.QThread):
    ready = QtCore.Signal()
    userDataReady = QtCore.Signal(int, CodeEditorBlockUserData)
    def __init__(self, processor):
        super(HighlighterThread, self).__init__()
        self._lines = []
        self._processor = processor
        self._stopped = False

    def addLine(self, index, text, previous_state, previous_revision):
        self._lines.append((index, text, previous_state, previous_revision))

    def start(self):
        self._stopped = False
        super(HighlighterThread, self).start()
        
    def stop(self):
        self._stopped = True
        self._lines = []
        self.wait()
        #self.deleteLater()

    def run(self):
        self.msleep(100)
        next_index = revision = state = -1
        while not self._stopped and self._lines:
            index, text, previous_state, previous_revision = self._lines.pop(0)
            if index == next_index:
                previous_revision = revision
                prevouse_state = state
            user_data = self._processor.textUserData(
                text, previous_state, previous_revision
            )
            state = user_data.state
            revision = user_data.revision
            next_index = index + 1
            self.userDataReady.emit(index, user_data)
        if not self._stopped:
            self.ready.emit()

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
        self.thread = HighlighterThread(
                self.syntaxProcessor
            )
        self.thread.userDataReady.connect(self.on_thread_userDataReady)
        self.thread.ready.connect(self.ready.emit)
        self.thread.started.connect(self.aboutToChange.emit)
        self.thread.finished.connect(self.changed.emit)

    def on_thread_userDataReady(self, index, user_data):
        block = self.document().findBlockByNumber(index)
        block.setUserData(user_data)
        block.setUserState(user_data.state)
        self.rehighlightBlock(block)

    def stop(self):
        if self.thread.isRunning():
            self.thread.stop()
        self.setDocument(None)

    def start(self, callback=None):
        self.setDocument(self.editor.document())

    def highlightBlock(self, text):
        block = self.currentBlock()

        # ------ No changes
        if self.syntaxProcessor.testRevision(block):
            user_data = block.userData()
        else:
            user_data = block.previous().userData()
            self.thread.addLine(block.blockNumber(), text + '\n', self.previousBlockState(), user_data and user_data.revision or -1)
            if not self.thread.isRunning():
                self.thread.start()
            user_data = block.userData() or self.syntaxProcessor.emptyUserData()

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))