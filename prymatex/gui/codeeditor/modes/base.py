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
        self._allow_default_handlers = True
        self.setObjectName(self.__class__.__name__)

    def setAllowDefaultHandlers(self, allow):
        self._allow_default_handlers = allow

    def registerKeyPressHandler(self, key, handler, after=False):
        handlers = self.postEventHandlers if after else self.preEventHandlers
        handlers[QtCore.QEvent.KeyPress].setdefault(key, []).append(handler)
        
    def unregisterKeyPressHandler(self, handler):
        for handlers in self.postEventHandlers.values():
            if handler in handlers:
                handlers.remove(handler)
        for handlers in self.preEventHandlers.values():
            if handler in handlers:
                handlers.remove(handler)

    def preKeyPressHandlers(self, key):
        handlers = self.preEventHandlers[QtCore.QEvent.KeyPress].get(key, [])
        if self._allow_default_handlers and self != self.editor.defaultMode():
            return handlers + self.editor.defaultMode().preKeyPressHandlers(key)
        return handlers

    def postKeyPressHandlers(self, key):
        handlers = self.postEventHandlers[QtCore.QEvent.KeyPress].get(key, [])
        if self._allow_default_handlers and self != self.editor.defaultMode():
            return handlers + self.editor.defaultMode().postKeyPressHandlers(key)
        return handlers

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
