#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.core.plugin.dock import PMXBaseDockKeyHelper

class RefreshHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_F5
    def execute(self, event):
        print "actualizar"
        
class CopyHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_C
    def accept(self, event):
        print "test c", bool(event.modifiers() & QtCore.Qt.ControlModifier)
        return bool(event.modifiers() & QtCore.Qt.ControlModifier)
        
    def execute(self, event):
        print "copy"
        
class PasteHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_V
    def accept(self, event):
        print "test v", bool(event.modifiers() & QtCore.Qt.ControlModifier)
        return bool(event.modifiers() & QtCore.Qt.ControlModifier)
        
    def execute(self, event):
        print "paste"
        