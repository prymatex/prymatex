#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin import PMXBaseWidgetComponent

class PMXBaseDock(PMXBaseWidgetComponent):
    SHORTCUT = ""
    ICON = QtGui.QIcon()
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self):
        PMXBaseWidgetComponent.__init__(self)
        self.toggleViewAction().setShortcut(QtGui.QKeySequence(self.SHORTCUT))
        self.toggleViewAction().setIcon(self.ICON)