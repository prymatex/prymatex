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

    def handle(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            return any(self._handle(self.keyPress_handlers(event.key()), event))
        return False

    def _handle(self, handlers, event):
        for handler in handlers:
            yield handler(event)

    def keyPress_handlers(self, key):
        for _key, handlers in self.eventHandlers[QtCore.QEvent.KeyPress].items():
            if self.isActive() and _key in (key, QtCore.Qt.Key_Any):
                for handler in handlers:
                    yield handler
        if self != self.editor.defaultMode():
            for handler in self.editor.previousMode(self).keyPress_handlers(key):
                yield handler

    def name(self):
        return self.objectName()

    activate = lambda self: self.editor.beginMode(self)
    deactivate = lambda self: self.editor.endMode(self)
    isActive = lambda self: self.editor.isModeActive(self)
