#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

class PMXColorDelegate(QtGui.QItemDelegate):
    CHOICES = ()
    
    def createEditor(self, parent, option, index):
        button = QtGui.QPushButton(parent)
        return button

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass
