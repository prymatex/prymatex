#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    blockReady = QtCore.Signal(int, str, int, int)
    def __init__(self, parent):
        super(HighlighterThread, self).__init__(parent)
        self.pending_work = []
    
    def flush(self):
        self.pending_work = []

    def run(self):
        while True:
            if self.pending_work:
                number, text, revision = self.pending_work.pop(0)
                block = self.parent().document().findBlockByNumber(number)
                user_data = self.parent().editor.blockUserData(block)
                user_data, state = self.parent().syntaxProcessor.parseBlock(block, text, user_data)
                self.blockReady.emit(number, text, revision, state)
            else:
                self.msleep(300)

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()

    def __init__(self, editor):
        super(CodeEditorSyntaxHighlighter, self).__init__(editor)
        self.setDocument(editor.document())
        self.editor = editor
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.themeProcessor.begin.connect(self.on_processors_ready)
        self.themeProcessor.end.connect(self.on_processors_ready)
        self.syntaxProcessor.begin.connect(self.on_processors_ready)
        self.syntaxProcessor.end.connect(self.on_processors_ready)
        self.highlight_task = None
        self.editor.aboutToClose.connect(self.stop)
        self.thread = HighlighterThread(self)
        self.thread.blockReady.connect(self.on_thread_blockReady)
    
    def on_processors_ready(self):
        if self.syntaxProcessor.ready() and self.themeProcessor.ready():
            self.highlightBlock = self._highlight_block
        else:
            self.highlightBlock = self._nop

    def on_thread_blockReady(self, number, text, revision, state):
        block = self.document().findBlockByNumber(number)
        user_data = self.editor.blockUserData(block)
        self.editor.processBlockUserData(text, block, user_data)
        block.setUserState(state)
        block.setRevision(revision)
        self.rehighlightBlock(block)

    def on_task_finished(self, *args):
        self.highlightBlock = self.syncHighlightFunction
        self.highlight_task = None
        self.highlightChanged.emit()

    def isRunning(self):
        return self.thread.isRunning()

    def stop(self):
        self.thread.flush()
        self.thread.terminate()
        self.thread.wait()

    def start(self, callback=None):
        self.thread.callback = callback
        self.thread.start()

    def _nop(self, text):
        pass

    def _user_data_factory(self, text):
        self.editor.blockUserData(self.currentBlock())
        
    def _highlight_block(self, text):
        block = self.currentBlock()
        revision = helpers.qt_int(hash("%s:%s:%d" % (
            self.syntaxProcessor.scopeName(), text, 
            block.previous().userState()
        )))
        print(block.revision(), revision)
        if block.revision() != revision:
            self.thread.pending_work.append((block.blockNumber(), text, revision))
        else:
            user_data = self.editor.blockUserData(block)
            for token in user_data.tokens():
                self.setFormat(token.start, token.end - token.start,
                    self.themeProcessor.textCharFormat(token.scope))
