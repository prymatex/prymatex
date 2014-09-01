#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from .base import CodeEditorBaseMode

class CodeEditorOverwriteMode(CodeEditorBaseMode):
    def __init__(self, **kwargs):
        super(CodeEditorOverwriteMode, self).__init__(**kwargs)
        self.completer = None

    def name(self):
        return "Overwrite"

    def initialize(self, **kwargs):
        super(CodeEditorOverwriteMode, self).initialize(**kwargs)
        self.editor.registerPreKeyPressHandler(QtCore.Qt.Key_Insert,
            self.toggle_overwrite)

    def toggle_overwrite(self, event):
        overwrite = not self.editor.overwriteMode()
        self.editor.setOverwriteMode(overwrite)
        if overwrite:
            self.activate()
        else:
            self.deactivate()
