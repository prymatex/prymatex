#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PMXBaseEditorAddon

class CodeEditorBaseMode(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def isActive(self):
        return False

    def inactive(self):
        pass
