#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from ..addons import CodeEditorAddon

class CodeEditorBaseMode(CodeEditorAddon):
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

    def preHandle(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            return self.handle(self.pre_KeyPress_handlers(event.key()), event)

    def postHandle(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            return self.handle(self.post_KeyPress_handlers(event.key()), event)

    def handle(self, handlers, event):
        for handler in handlers:
            yield handler(event)

    def pre_KeyPress_handlers(self, key):
        for hander in self.preEventHandlers[QtCore.QEvent.KeyPress].get(QtCore.Qt.Key_Any, []):
            yield hander
        for hander in self.preEventHandlers[QtCore.QEvent.KeyPress].get(key, []):
            yield hander
        if self._allow_default_handlers and self != self.editor.defaultMode():
            for hander in self.editor.defaultMode().pre_KeyPress_handlers(key):
                yield hander

    def post_KeyPress_handlers(self, key):
        for hander in self.postEventHandlers[QtCore.QEvent.KeyPress].get(QtCore.Qt.Key_Any, []):
            yield hander
        for hander in self.postEventHandlers[QtCore.QEvent.KeyPress].get(key, []):
            yield hander
        if self._allow_default_handlers and self != self.editor.defaultMode():
            for hander in self.editor.defaultMode().post_KeyPress_handlers(key):
                yield hander

    def name(self):
        return self.objectName()

    def activate(self):
        self.editor.beginCodeEditorMode(self)

    def deactivate(self):
        self.editor.endCodeEditorMode(self)
    
    isActive = lambda self: self.editor.currentMode() == self
