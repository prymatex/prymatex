#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import (PrymatexComponentWidget, 
    PrymatexKeyHelper, PrymatexAddon)

class PrymatexDock(PrymatexComponentWidget):
    SEQUENCE = None
    ICON = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea

#======================================================================
# Base Helper
#======================================================================    
class PrymatexDockKeyHelper(PrymatexKeyHelper):
     def __init__(self, **kwargs):
        super(PrymatexDockKeyHelper, self).__init__(**kwargs)
        self.dock = kwargs.get("parent")

#========================================
# BASE ADDON
#========================================
class PrymatexDockAddon(PrymatexAddon):
    def __init__(self, **kwargs):
        super(PrymatexDockAddon, self).__init__(**kwargs)
        self.dock = kwargs.get("parent")
