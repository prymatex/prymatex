#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PMXBaseEditorAddon

class CodeEditorBaseMode(QtCore.QObject, PMXBaseEditorAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self._is_active = False

    def activate(self):
        self._is_active = True

    def deactivate(self):
        self._is_active = False
    
    isActive = lambda self: self._is_active
