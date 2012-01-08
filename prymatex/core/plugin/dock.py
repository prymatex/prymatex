#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseWidgetPlugin

class PMXBaseDock(PMXBaseWidgetPlugin):
    MENU_KEY_SEQUENCE = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self):
        PMXBaseWidgetPlugin.__init__(self)
        if self.MENU_KEY_SEQUENCE:
            keysequence = QtGui.QKeySequence(self.MENU_KEY_SEQUENCE)
            self.toggleViewAction().setShortcut(keysequence)
    
    def setCurrentEditor(self, editor):
        pass