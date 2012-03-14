#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

class PMXBaseComponent(object):
    def initialize(self):
        raise NotImplemented
    
    def finalize(self):
        pass

    @classmethod
    def contributeToSettings(cls):
        return []

    @classmethod
    def contributeToMainMenu(cls):
        return {}

class PMXBaseWidgetComponent(PMXBaseComponent):
    def __init__(self):
        self.overlays = []
            
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
        for overlay in self.overlays:
            overlay.initialize(self)

    def updateOverlays(self):
        for overlay in self.overlays:
            overlay.updateOverlay()
    
    def addOverlay(self, overlay):
        self.overlays.append(overlay)

class PMXBaseOverlay(object):
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass
    
    def updateOverlay(self):
        pass

Key_Any = 0
class PMXBaseKeyHelper(object):
    KEY = Key_Any
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass
        
    def accept(self, editor, event, cursor = None, scope = None):
        return self.KEY == event.key()
    
    def execute(self, editor, event, cursor = None, scope = None):
        pass
    
class PMXBaseAddon(object):
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass
