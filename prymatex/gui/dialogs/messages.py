#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtGui

class CheckableMessageBox(QtGui.QMessageBox):
    def __init__(self, *largs, **kwargs):
        QtGui.QMessageBox.__init__(self, *largs, **kwargs)
        self.checkBox = QtGui.QCheckBox(self)
        self.layout().addWidget(self.checkBox, 1, 1)

    def setCheckBoxText(self, text):
        self.checkBox.setText(text)

    def isChecked(self):
        return self.checkBox.isChecked()

    @classmethod
    def questionFactory(cls, parent, title, text, checkText, buttons = QtGui.QMessageBox.Ok, defaultButton = QtGui.QMessageBox.NoButton):
        question = cls(parent)
        question.setIcon(QtGui.QMessageBox.Question)
        question.setStandardButtons(buttons)
        question.setDefaultButton(defaultButton)
        question.setWindowTitle(title)
        question.setText(text)
        question.setCheckBoxText(checkText)
        return question
