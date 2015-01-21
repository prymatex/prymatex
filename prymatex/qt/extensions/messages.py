#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtWidgets

class CheckableMessageBox(QtWidgets.QMessageBox):
    def __init__(self, *largs, **kwargs):
        super(CheckableMessageBox, self).__init__(*largs, **kwargs)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.layout().addWidget(self.checkBox, 1, 1)

    def setCheckBoxText(self, text):
        self.checkBox.setText(text)

    def isChecked(self):
        return self.checkBox.isChecked()

    @classmethod
    def questionFactory(cls, parent, title, text, checkText, buttons = QtWidgets.QMessageBox.Ok, defaultButton = QtWidgets.QMessageBox.NoButton):
        question = cls(parent)
        question.setIcon(QtWidgets.QMessageBox.Question)
        question.setStandardButtons(buttons)
        question.setDefaultButton(defaultButton)
        question.setWindowTitle(title)
        question.setText(text)
        question.setCheckBoxText(checkText)
        return question
