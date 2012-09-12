#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin import PMXBaseWidgetComponent, PMXBaseAddon, PMXBaseKeyHelper

class PMXBaseDock(PMXBaseWidgetComponent):
    SHORTCUT = ""
    ICON = QtGui.QIcon()
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self):
        PMXBaseWidgetComponent.__init__(self)
        self.toggleViewAction().setShortcut(QtGui.QKeySequence(self.SHORTCUT))
        self.toggleViewAction().setIcon(self.ICON)

#======================================================================
# Base Helper
#======================================================================    
class PMXBaseDockKeyHelper(PMXBaseKeyHelper):
    def initialize(self, dock):
        PMXBaseKeyHelper.initialize(self, dock)
        self.dock = dock

    def accept(self, event):
        return PMXBaseKeyHelper.accept(self, event.key())
    
    def execute(self, event):
        PMXBaseKeyHelper.accept(self, event.key())

#========================================
# BASE ADDON
#========================================
class PMXBaseDockAddon(PMXBaseAddon):
    def initialize(self, dock):
        PMXBaseAddon.initialize(self, dock)
        self.dock = dock

    def finalize(self):
        pass
