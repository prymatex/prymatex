#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from prymatex.qt import QtCore, QtGui
from prymatex.qt.helpers import keyevent_to_keysequence

from ..addons import CodeEditorAddon

class CodeEditorBaseMode(CodeEditorAddon):
    def __init__(self, **kwargs):
        super(CodeEditorBaseMode, self).__init__(**kwargs)
        self.eventHandlers = {
            QtCore.QEvent.KeyPress: []
        }
        self.setObjectName(self.__class__.__name__)

    def registerKeyPressHandler(self, keys, handler):
        keys = keys if isinstance(keys, (list, tuple)) else (keys, )
        self.eventHandlers[QtCore.QEvent.KeyPress].extend(
            [(QtGui.QKeySequence(key), handler) for key in keys]
        )

    def unregisterKeyPressHandler(self, handler):
        self.eventHandlers[QtCore.QEvent.KeyPress] = \
            [t for t in self.eventHandlers[QtCore.QEvent.KeyPress] \
                if t[1] == handler] 

    def keyPress_handlers(self, event):
        trigger = keyevent_to_keysequence(event)
        for sequence, handler in self.eventHandlers[QtCore.QEvent.KeyPress]:
            if self.isActive() and sequence.matches(trigger):
                yield handler

    def name(self):
        return self.objectName()

    activate = lambda self: self.editor.beginMode(self)
    deactivate = lambda self: self.editor.endMode(self)
    isActive = lambda self: self.editor.isModeActive(self)
