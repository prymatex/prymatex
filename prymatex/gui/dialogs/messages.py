#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from PyQt4 import QtGui

class CheckableMessageBox(QtGui.QMessageBox):
    def __init__(self, *largs, **kwargs):
        QtGui.QMessageBox.__init__(self, *largs, **kwargs)
        self.checkBox = QtGui.QCheckBox(self)
        self.layout().addWidget(self.checkBox, 1, 1)

    def setCheckBoxText(self, text):
        self.checkBox.setText(text)
        
    def isChecked(self):
        return self.checkBox.isChecked()