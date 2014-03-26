#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import (PrymatexComponentWidget, 
    PrymatexKeyHelper, PrymatexAddon, Key_Any)

class PrymatexDock(PrymatexComponentWidget):
    SEQUENCE = None
    ICON = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, **kwargs):
        super(PrymatexDock, self).__init__(**kwargs)
    
    def initialize(self, parent = None, **kwargs):
        super(PrymatexDock, self).initialize(**kwargs)
        self.mainWindow = parent

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
class PrymatexDockKeyHelper(PrymatexKeyHelper):
    def __init__(self, **kwargs):
        super(PrymatexDockKeyHelper, self).__init__(**kwargs)

    def initialize(self, parent = None, **kwargs):
        super(PrymatexDockKeyHelper, self).initialize(**kwargs)
        self.dock = parent

    def accept(self, key = Key_Any, **kwargs):
        return super(PrymatexDockKeyHelper, self).accept(key, **kwargs)

    def execute(self, **kwargs):
        super(PrymatexDockKeyHelper, self).execute(**kwargs)

#========================================
# BASE ADDON
#========================================
class PrymatexDockAddon(PrymatexAddon):
    def __init__(self, **kwargs):
        super(PrymatexDockAddon, self).__init__(**kwargs)

    def initialize(self, parent = None, **kwargs):
        super(PrymatexDockAddon, self).initialize(**kwargs)
        self.dock = parent

    def finalize(self):
        pass

PMXBaseDock = PrymatexDock
PMXBaseDockKeyHelper = PrymatexDockKeyHelper
PMXBaseDockAddon = PrymatexDockAddon