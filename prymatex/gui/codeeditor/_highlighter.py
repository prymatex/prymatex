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
        self._indexes = set()
        self._running_indexes = set()
        self._texts = {}
        self._running_texts = {}
        self._states = {}
        self._running_states = {}
        self._processor = editor.findProcessor("syntax")
        self._stopped = False
        self._scheduled = False

    def isRunning(self):
        return self._scheduled or super(HighlighterThread, self).isRunning()
        
    def addLine(self, index, text, previous_state, previous_revision):
        if index not in self._running_states:
            self._indexes.add(index)
            self._texts[index] = text
            self._states[index] = (previous_state, previous_revision)
        if not self.isRunning() and self._indexes:
            self._scheduled = True
            time = previous_revision == -1 and 100 or 0
            print(time)
            QtCore.QTimer.singleShot(time, self.start)

    def start(self):
        self._stopped = False
        super(HighlighterThread, self).start()
        self._scheduled = False
        
    def stop(self):
        self._stopped = True
        self._indexes = set()
        self._texts = {}
        self._states = {}
        self.wait()
        
    def run(self):
        while not self._stopped and self._indexes:
            self._running_indexes = sorted(self._indexes)
            self._running_states = self._states.copy()
            self._running_texts = self._texts.copy()
            self._indexes = set()
            self._texts = {}
            self._states = {}
            for index in self._running_indexes:
                text = self._running_texts[index]
                previous_state, previous_revision = self._running_states[index]
                user_data = self._processor.textUserData(
                    text, previous_state, previous_revision
                )
                self._running_states[index + 1] = (user_data.state, user_data.revision)
                self.ready.emit(index, user_data)
            self.changed.emit(self._running_indexes)
            self._running_indexes = set()
            self._running_states = {}
            self._running_texts = {}

class CodeEditorSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    changed = QtCore.Signal(list)        # On the highlight changed allways triggered
    aboutToChange = QtCore.Signal()  
    def __init__(self, editor):
        self._stopped = True
        self.editor = editor
        super(CodeEditorSyntaxHighlighter, self).__init__(editor.document())
        self.syntaxProcessor = editor.findProcessor("syntax")
        self.themeProcessor = editor.findProcessor("theme")
        self.editor.aboutToClose.connect(self.stop)
        self.thread = HighlighterThread(editor)
        self.thread.ready.connect(self.on_thread_ready)
        self.thread.changed.connect(self.on_thread_changed)
        self.thread.changed.connect(self.changed.emit)

    def on_thread_changed(self, changes):
        print(changes[0], changes[-1], len(changes), changes[-1] - changes[0], self.syntaxProcessor.scope_name)
        
    def on_thread_ready(self, index, user_data):
        block = self.document().findBlockByNumber(index)
        block.setUserData(user_data)
        self.rehighlightBlock(block)
    
    def stop(self):
        if self.thread.isRunning():
            self.thread.stop()
        self._stopped = True

    def start(self, callback=None):
        self._stopped = False
        self.aboutToChange.emit()
        self.rehighlight()

    def highlightBlock(self, text):
        if not self._stopped:
            text = text + '\n'
            block = self.currentBlock()
            user_data = self.currentBlockUserData()
            if user_data is None:
                self.thread.addLine(block.blockNumber(), text, -1, -1)
                user_data = self.syntaxProcessor.emptyUserData()
            elif user_data.revision == self.syntaxProcessor.textRevision(text, self.previousBlockState()):
                self.setCurrentBlockState(user_data.state)
            elif user_data.blockText() != text:
                # tengo que agregar el block pero tambien tengo que mentir un poco con el formato
                previous_block = block.previous()
                previous_user_data = previous_block.userData()
                self.thread.addLine(block.blockNumber(), text, self.previousBlockState(), previous_user_data and previous_user_data.revision or -1)
            elif user_data.state != self.previousBlockState():
                # tegno que agregar el block y apurar el tramite de los proximos agregados
                previous_block = block.previous()
                previous_user_data = previous_block.userData()
                self.thread.addLine(block.blockNumber(), text, self.previousBlockState(), previous_user_data and previous_user_data.revision or -1)
            
            # ------ Formats
            for token in user_data.tokens:
                self.setFormat(token.start, token.end - token.start,
                    self.themeProcessor.textCharFormat(token.scope))
