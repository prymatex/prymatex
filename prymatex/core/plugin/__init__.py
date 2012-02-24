#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

#TODO: en inicialize deberia pasar un proveedro de servicios o otra forma menos directa de que un plguin hable con el core
class PMXBasePlugin(object):
    
    def initialize(self):
        raise NotImplemented
    
    def finalize(self):
        pass
    
class PMXBaseWidgetPlugin(PMXBasePlugin):
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

    @classmethod
    def contributeToSettings(cls):
        return []

    @classmethod
    def contributeToMainMenu(cls):
        return {}

class PMXBaseOverlay(PMXBasePlugin):
    def initialize(self, widget):
        pass
    
    def updateOverlay(self):
        pass

Key_Any = 0
class PMXBaseKeyHelper(PMXBasePlugin):
    KEY = Key_Any
    def accept(self, editor, event, cursor = None, scope = None):
        return self.KEY == event.key()
    
    def execute(self, editor, event, cursor = None, scope = None):
        pass
    
class PMXBaseAddon(PMXBasePlugin):
    pass
