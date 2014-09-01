#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PrymatexEditorAddon

class CodeEditorBaseMode(PrymatexEditorAddon, QtCore.QObject):
    def __init__(self, **kwargs):
        super(CodeEditorBaseMode, self).__init__(**kwargs)
        self._is_active = False

    def setPalette(self, palette):
        pass
        
    def setFont(self, font):
        pass

    def activate(self):
        self._is_active = True
        self.editor.beginMode.emit(self.objectName())

    def deactivate(self):
        self._is_active = False
        self.editor.endMode.emit(self.objectName())
    
    isActive = lambda self: self._is_active
