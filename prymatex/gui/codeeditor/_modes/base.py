#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditorAddon

class CodeEditorBaseMode(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def active(self, event, scope):
        pass
    
    def isActive(self):
        return False

    def inactive(self):
        pass
    
    def eventFilter(self, obj, event):
        return False

    # ------------ Mouse Events
    def mousePressEvent(self, event):
        return self.editor.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        return self.editor.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        return self.editor.mouseReleaseEvent(event)

    # ------------ Key Events
    def keyPressEvent(self, event):
        return self.editor.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        return self.editor.keyReleaseEvent(event)

class CodeEditorTestMode(CodeEditorBaseMode):
    def initialize(self, editor):
        CodeEditorBaseMode.initialize(self, editor)

    def eventFilter(self, obj, event):
        return False