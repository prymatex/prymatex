#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PrymatexEditorAddon

class CodeEditorBaseMode(PrymatexEditorAddon, QtCore.QObject):
    def __init__(self, **kwargs):
        super(CodeEditorBaseMode, self).__init__(**kwargs)
        self.preEventHandlers = {
            QtCore.QEvent.KeyPress: {}
        }
        self.postEventHandlers = {
            QtCore.QEvent.KeyPress: {}
        }
        self.setObjectName(self.__class__.__name__)

    def registerKeyPressHandler(self, key, handler, after=False):
        handlers = self.postEventHandlers if after else self.preEventHandlers
        handlers[QtCore.QEvent.KeyPress].setdefault(key, []).append(handler)

    def preKeyPressHandlers(self):
        return self.preEventHandlers[QtCore.QEvent.KeyPress]

    def postKeyPressHandlers(self):
        return self.postEventHandlers[QtCore.QEvent.KeyPress]

    def name(self):
        return self.objectName()

    def setPalette(self, palette):
        pass
        
    def setFont(self, font):
        pass

    def activate(self):
        self.editor.beginCodeEditorMode(self)

    def deactivate(self):
        self.editor.endCodeEditorMode(self)
    
    isActive = lambda self: self.editor.currentMode() == self
