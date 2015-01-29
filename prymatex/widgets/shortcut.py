#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import keyevent_to_keysequence

class ShortcutEdit(QtWidgets.QLineEdit):
    def setKeySequence(self, sequence):
        self.setText(sequence.toString())
        self.selectAll()
        self.setFocus()

    def keySequence(self):
        return QtGui.QKeySequence(self.text())

    def keyPressEvent(self, event):
        if self.hasSelectedText():
            self.clear()
        sequence = keyevent_to_keysequence(event, prefixes=self.text())
        if not sequence.isEmpty():
            self.setText(sequence.toString())