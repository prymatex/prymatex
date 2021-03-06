#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import time
from bisect import bisect

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.qt import QtCore, QtGui, QtWidgets, helpers

class HighlighterThread(QtCore.QThread):
    ready = QtCore.Signal(int, CodeEditorBlockUserData)
    changed = QtCore.Signal(list)
    def __init__(self, editor):
        super(HighlighterThread, self).__init__(editor)
        self._processor = editor.findProcessor("syntax")
        self._indexes = set()
        self._doing_indexes = set()
        self._texts = {}
        self._states = {}
        self._stopped = True
 
    def __del__(self):
        self.wait()

    def addLine(self, index, text, previous_state, previous_revision):
        if index not in self._doing_indexes:
            self._indexes.add(index)
            self._texts[index] = text
            self._states[index] = (previous_state, previous_revision)
    
    def start(self):
        self._stopped = False
        super(HighlighterThread, self).start()

    def stop(self):
        self._stopped = True
        self.wait()

    def run(self):
        while not self._stopped:
            if self._indexes:
                self._doing_indexes, self._indexes = sorted(self._indexes), set()
                states = self._states.copy()
                for index in self._doing_indexes:
                    previous_state, previous_revision = states[index]
                    user_data = self._processor.textUserData(
                        self._texts[index], previous_state, previous_revision
                    )
                    self._states[index + 1] = states[index + 1] = (user_data.state, user_data.revision)
                    self.ready.emit(index, user_data)
                self.changed.emit(list(self._doing_indexes))
                self._doing_indexes = set()
            self.msleep(1)

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    blockHighlightChanged = QtCore.Signal(QtGui.QTextBlock)        # On the highlight changed allways triggered
    def __init__(self, editor):
        self.editor = editor
        super(CodeEditorSyntaxHighlighter, self).__init__(editor.document())
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.editor.aboutToClose.connect(self.stop)
        self.thread = HighlighterThread(editor)
        self.thread.ready.connect(self.on_thread_ready)
        self.thread.changed.connect(self.on_thread_changed)
        self.editor.activated.connect(self.start)
        self.editor.deactivated.connect(self.stop)
        
    def on_thread_changed(self, indexes):
        for index in indexes:
            self.blockHighlightChanged.emit(
                self.document().findBlockByNumber(index)
            )

    def on_thread_ready(self, index, user_data):
        block = self.document().findBlockByNumber(index)
        if block.isValid():
            block.layout().setAdditionalFormats(
                self.themeProcessor.textCharFormats(user_data)
            )
            block.setUserData(user_data)
            renext = block.userState() not in (-1, user_data.state)
            block.setUserState(user_data.state)
            self.document().markContentsDirty(block.position(), block.length())
            if renext:
                self.rehighlightBlock(block.next())
    
    def stop(self):
        QtCore.QTimer.singleShot(0, self.thread.stop)

    def start(self):
        QtCore.QTimer.singleShot(0, self.thread.start)

    def _highlightBlock(self, text):
        block = self.currentBlock()
        previous_user_data = block.previous().userData() or self.syntaxProcessor.emptyUserData() 
        user_data = self.syntaxProcessor.textUserData(
            text + '\n', self.previousBlockState(), previous_user_data.revision
        )
        self.setCurrentBlockUserData(user_data)
        self.setCurrentBlockState(user_data.state)
        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))

    def highlightBlock(self, text):
        text = text + '\n'
        user_data = self.currentBlockUserData() or self.syntaxProcessor.emptyUserData() 
        previous_state = self.previousBlockState()
        if user_data.revision == self.syntaxProcessor.textRevision(text, previous_state):
            self.setCurrentBlockState(user_data.state)
        else:
            block = self.currentBlock()
            if user_data.blockText() != text:
                # Mentir un poco con el formato
                pass
            elif not user_data.blank and previous_state != self.currentBlockState():
                # Apurar el tramite de los proximos agregados
                self.setCurrentBlockState(-1)
            previous_user_data = block.previous().userData() or self.syntaxProcessor.emptyUserData()
            self.thread.addLine(
                block.blockNumber(),
                text,
                previous_state,
                previous_user_data.revision
            )

        # ------ Formats
        for token in user_data.tokens:
            self.setFormat(token.start, token.end - token.start,
                self.themeProcessor.textCharFormat(token.scope))
