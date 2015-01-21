#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from collections import OrderedDict

from prymatex.qt import QtCore

from ..addons import CodeEditorAddon

class CodeEditorBaseMode(CodeEditorAddon):
    def __init__(self, **kwargs):
        super(CodeEditorBaseMode, self).__init__(**kwargs)
        self.eventHandlers = {
            QtCore.QEvent.KeyPress: OrderedDict()
        }
        self.setObjectName(self.__class__.__name__)

    def registerKeyPressHandler(self, key, handler):
        self.eventHandlers[QtCore.QEvent.KeyPress].setdefault(key, []).append(handler)
        
    def unregisterKeyPressHandler(self, handler):
        for handlers in self.eventHandlers.values():
            if handler in handlers:
                handlers.remove(handler)

    def keyPress_handlers(self, key):
        for _key, handlers in self.eventHandlers[QtCore.QEvent.KeyPress].items():
            if self.isActive() and _key in (key, QtCore.Qt.Key_Any):
                for handler in handlers:
                    yield handler

    def name(self):
        return self.objectName()

    activate = lambda self: self.editor.beginMode(self)
    deactivate = lambda self: self.editor.endMode(self)
    isActive = lambda self: self.editor.isModeActive(self)
