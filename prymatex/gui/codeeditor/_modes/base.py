#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditorAddon

class CodeEditorBaseMode(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def isActive(self):
        return False

    def inactive(self):
        pass
    
    def eventFilter(self, obj, event):
        return False

class CodeEditorTestMode(CodeEditorBaseMode):
    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)

    def eventFilter(self, obj, event):
        return False
        