#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import time
from bisect import bisect

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    userDataReady = QtCore.Signal(int, CodeEditorBlockUserData)
    def __init__(self, processor):
        super(HighlighterThread, self).__init__()
        self._lines = {}
        self._order = []
        self._processor = processor
        self._stopped = False

    def setLine(self, index, text, previous_state, previous_revision):
        self._lines[index] = (index, text, previous_state, previous_revision)
        if index not in self._order:
            self._order.insert(bisect(self._order, index), index)

    def start(self):
        self._stopped = False
        super(HighlighterThread, self).start()
        
    def stop(self):
        self._stopped = True
        self._lines = {}
        self._order = []
        self.wait()

    def run(self):
        index = next_index = -1
        user_data = None
        self.first = self.last = self._order and self._order[0] or 0
        while not self._stopped and self._lines:
            self.last = self._order.pop(0)
            if self.last < self.first:
                self.first = self.last
            index, text, previous_state, previous_revision = self._lines.pop(self.last)
            if user_data is not None and index == next_index:
                previous_revision = user_data.revision
                prevouse_state = user_data.state
            user_data = self._processor.textUserData(
                text, previous_state, previous_revision
            )
            next_index = index + 1
            self.userDataReady.emit(index, user_data)
            self.usleep(1)

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
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
        self.thread.finished.connect(self.print_number)

    def print_number(self):
        print(self.thread.first, self.thread.last, self.syntaxProcessor.scope_name)
        
    def on_thread_userDataReady(self, index, user_data):
        block = self.document().findBlockByNumber(index)
        block.setUserData(user_data)
        self.rehighlightBlock(block)
    
    def stop(self):
        self.setDocument(None)
        if self.thread.isRunning():
            self.thread.stop()

    def start(self, callback=None):
        self.setDocument(self.editor.document())

    def highlightBlock(self, text):
        block = self.currentBlock()

        # ------ No changes
        if self.syntaxProcessor.testRevision(block):
            user_data = block.userData()
            self.setCurrentBlockState(user_data.state)
        else:
            user_data = block.previous().userData()
            self.thread.setLine(block.blockNumber(), text + '\n', self.previousBlockState(), user_data and user_data.revision or -1)
            if not self.thread.isRunning():
                QtCore.QTimer.singleShot(0, self.thread.start)
            user_data = block.userData() or self.syntaxProcessor.emptyUserData()

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
