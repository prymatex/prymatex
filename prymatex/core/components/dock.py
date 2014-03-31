#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import (PrymatexComponentWidget, 
    PrymatexKeyHelper, PrymatexAddon)

class PrymatexDock(PrymatexComponentWidget):
    SEQUENCE = None
    ICON = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def initialize(self, parent = None, **kwargs):
        super(PrymatexDock, self).initialize(**kwargs)
        self.mainWindow = parent

#======================================================================
# Base Helper
#======================================================================    
class PrymatexDockKeyHelper(PrymatexKeyHelper):
    def initialize(self, parent = None, **kwargs):
        super(PrymatexDockKeyHelper, self).initialize(**kwargs)
        self.dock = parent

#========================================
# BASE ADDON
#========================================
class PrymatexDockAddon(PrymatexAddon):
    def initialize(self, parent = None, **kwargs):
        super(PrymatexDockAddon, self).initialize(**kwargs)
        self.dock = parent

