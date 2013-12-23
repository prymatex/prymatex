#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PMXBaseEditorAddon

class CodeEditorBaseMode(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self._is_active = False
        self._completion_state = False

    def activate(self):
        self._is_active = True
        # Capture and disable completition
        self._completion_state = self.editor.enableAutoCompletion
        self.editor.enableAutoCompletion = False
        self.editor.beginMode.emit(self.objectName())

    def deactivate(self):
        self._is_active = False
        # Restore completition state
        self.editor.enableAutoCompletion = self._completion_state
        self.editor.endMode.emit(self.objectName())
    
    isActive = lambda self: self._is_active
