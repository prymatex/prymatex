#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin import PMXBaseWidgetPlugin

class PMXBaseDock(PMXBaseWidgetPlugin):
    MENU_KEY_SEQUENCE = None
    MENU_ICON = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self):
        PMXBaseWidgetPlugin.__init__(self)
        if self.MENU_KEY_SEQUENCE is not None:
            keysequence = QtGui.QKeySequence(self.MENU_KEY_SEQUENCE)
            self.toggleViewAction().setShortcut(keysequence)
        if self.MENU_ICON is not None:
            self.toggleViewAction().setIcon(self.MENU_ICON)

    def setCurrentEditor(self, editor):
        pass
    
    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow