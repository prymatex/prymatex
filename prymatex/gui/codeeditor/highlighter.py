#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    highlightingReady = QtCore.Signal(object)
    def run(self):
        highlighting = {}
        block = self.parent().document().begin()
	while block.isValid():
            block = block.next()

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
        self.highlightBlock = self._nop
        self.editor.aboutToClose.connect(self.stop)
        self.thread = HighlighterThread(self)
        self.thread.finished.connect(self.on_trhead_finished)
        self.thread.highlightingReady.connect(self.on_thread_highlightingReady)
    
    def on_processors_ready(self):
        if self.syntaxProcessor.ready() and self.themeProcessor.ready():
            self.highlightBlock = self.realtime_highlight
        else:
            self.highlightBlock = self._nop

    def on_trhead_finished(self):
        self.highlightBlock = self.realtime_highlight

    def on_thread_highlightingReady(self, data):
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
        self.thread.terminate()
        self.thread.wait()

    def start(self, callback=None):
        self.thread.start()

    def _nop(self, text):
        pass
        
    def threaded_highlight(self, text):
        pass

    def realtime_highlight(self, text):
        block = self.currentBlock()
        user_data = self.syntaxProcessor.blockUserData(block)
        block.setUserData(user_data)
        block.setUserState(user_data.state)
        block.setRevision(user_data.revision)
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))

    def _highlight_block(self, text):
        block = self.currentBlock()
        revision = helpers.qt_int(hash("%s:%s:%d" % (
            self.syntaxProcessor.scopeName(), text, 
            block.previous().userState()
        )))
        if block.revision() != revision:
            self.thread.pending_work.append((block.blockNumber(), text, revision))
        else:
            user_data = self.editor.blockUserData(block)
            for token in user_data.tokens():
                self.setFormat(token.start, token.end - token.start,
                    self.themeProcessor.textCharFormat(token.scope))
