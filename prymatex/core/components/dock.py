#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseComponent
from prymatex.core.components.keyhelper import PMXBaseKeyHelper, PMXKeyHelperMixin

__all__ = ["PMXBaseDock", "PMXBaseDockKeyHelper", "PMXBaseDockAddon"]

class PMXBaseDock(PMXBaseComponent, PMXKeyHelperMixin):
    SHORTCUT = ""
    ICON = QtGui.QIcon()
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
        self.toggleViewAction().setShortcut(QtGui.QKeySequence(self.SHORTCUT))
        self.toggleViewAction().setIcon(self.ICON)

    def runKeyHelper(self, event):
        runHelper = False
        for helper in self.findHelpers(event.key()):
            runHelper = helper.accept(event)
            if runHelper:
                helper.execute(event)
                break
        return runHelper


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
class PMXBaseDockAddon(PMXBaseComponent):
    def initialize(self, dock):
        PMXBaseComponent.initialize(self, dock)
        self.dock = dock

    def finalize(self):
        pass
