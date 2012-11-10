#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.core import PMXBaseDockKeyHelper

class RefreshHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_F5
    def execute(self, event):
        self.dock.refresh()
        
class CopyHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_C
    def accept(self, event):
        return bool(event.modifiers() & QtCore.Qt.ControlModifier)
        
    def execute(self, event):
        self.dock.copy()
        
class PasteHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_V
    def accept(self, event):
        return bool(event.modifiers() & QtCore.Qt.ControlModifier)
        
    def execute(self, event):
        self.dock.paste()
        
class CutHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_X
    def accept(self, event):
        return bool(event.modifiers() & QtCore.Qt.ControlModifier)
        
    def execute(self, event):
        self.dock.cut()
        
class DeleteHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def execute(self, event):
        self.dock.delete()

class RenameHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_F2
    def execute(self, event):
        self.dock.rename()