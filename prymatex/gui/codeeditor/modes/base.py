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
        self._allow_default_handlers = True
        self.setObjectName(self.__class__.__name__)

    def setAllowDefaultHandlers(self, allow):
        self._allow_default_handlers = allow

    def registerKeyPressHandler(self, key, handler):
        self.eventHandlers[QtCore.QEvent.KeyPress].setdefault(key, []).append(handler)
        
    def unregisterKeyPressHandler(self, handler):
        for handlers in self.eventHandlers.values():
            if handler in handlers:
                handlers.remove(handler)

    def handle(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            return self._handle(self.keyPress_handlers(event.key()), event)

    def _handle(self, handlers, event):
        for handler in handlers:
            yield handler(event)

    def keyPress_handlers(self, key):
        for _key, handlers in self.eventHandlers[QtCore.QEvent.KeyPress].items():
            if _key in (key, QtCore.Qt.Key_Any):
                for handler in handlers:
                    yield handler
        if self._allow_default_handlers and self != self.editor.defaultMode():
            for handler in self.editor.defaultMode().keyPress_handlers(key):
                yield handler

    def name(self):
        return self.objectName()

    def activate(self):
        self.editor.beginCodeEditorMode(self)

    def deactivate(self):
        self.editor.endCodeEditorMode(self)
    
    isActive = lambda self: self.editor.currentMode() == self
