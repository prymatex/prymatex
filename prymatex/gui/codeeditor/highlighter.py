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
        self._ready_indexes = set()
        self._texts = {}
        self._states = {}
        self._processor = editor.findProcessor("syntax")
        self._stopped = False
        self._scheduled = False
    
    def isRunning(self):
        return self._scheduled or super(HighlighterThread, self).isRunning()
        
    def addLine(self, index, text, previous_state, previous_revision):
        if index not in self._ready_indexes:
            self._indexes.add(index)
            self._texts[index] = text
            self._states[index] = (previous_state, previous_revision)
            if not self.isRunning() and self._indexes:
                self._scheduled = True
                QtCore.QTimer.singleShot(0, self.start)

    def start(self):
        self._stopped = False
        super(HighlighterThread, self).start()
        self._scheduled = False
        
    def stop(self):
        self._indexes = set()
        self._texts = {}
        self._states = {}
        self._stopped = True
        self.wait()
        
    def run(self):
        while not self._stopped and self._indexes:
            self._ready_indexes, self._indexes = sorted(self._indexes), set()
            states, self._states = self._states.copy(), {}
            texts, self._texts = self._texts.copy(), {}
            for index in self._ready_indexes:
                previous_state, previous_revision = states[index]
                user_data = self._processor.textUserData(
                    texts[index], previous_state, previous_revision
                )
                states[index + 1] = (user_data.state, user_data.revision)
                self.ready.emit(index, user_data)
            self.changed.emit(self._ready_indexes)
        self._ready_indexes = set()

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
        #self.thread.changed.connect(self.on_thread_changed)
        self.thread.changed.connect(self.changed.emit)

    def on_thread_changed(self, changes):
        print(changes[0], changes[-1], len(changes), changes[-1] - changes[0], self.syntaxProcessor.scope_name)
        
    def on_thread_ready(self, index, user_data):
        block = self.document().findBlockByNumber(index)
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
        if self.thread.isRunning():
            self.thread.stop()
        self._stopped = True

    def start(self):
        self._stopped = False
        self.aboutToChange.emit()
        self.rehighlight()
    
    def highlightBlock(self, text):
        if not self._stopped:
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
                elif previous_state != self.currentBlockState():
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
