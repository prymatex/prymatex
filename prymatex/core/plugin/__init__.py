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
    KEY_HELPERS = {}
    def __init__(self):
        self.overlays = []
        self.addons = []
            
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
        for overlay in self.overlays:
            overlay.initialize(self)
        for addon in self.addons:
            addon.initialize(self)

    def updateOverlays(self):
        for overlay in self.overlays:
            overlay.updateOverlay()
    
    def addOverlay(self, overlay):
        self.overlays.append(overlay)

    # Addons api    
    def addAddon(self, addon):
        self.addons.append(addon)
        
    def addonByClassName(self, className):
        addons = filter(lambda addon: addon.__class__.__name__ == className, self.addons)
        #TODO: Solo uno
        return addons[0]

    # Helpers api
    @classmethod
    def addKeyHelper(cls, helper):
        helpers = cls.KEY_HELPERS.setdefault(helper.KEY, [])
        helpers.append(helper)

    def findHelpers(self, key):
        helpers = self.KEY_HELPERS[Key_Any][:]
        return helpers + self.KEY_HELPERS.get(key, [])

    def runKeyHelper(self, key):
        runHelper = False
        for helper in self.findHelpers(key):
            runHelper = helper.accept(self, key)
            if runHelper:
                helper.execute(self, key)
        return runHelper

    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        return PMXBaseComponent.contributeToMainMenu()
        
class PMXBaseOverlay(object):
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass
    
    def updateOverlay(self):
        pass

class PMXBaseAddon(object):
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass

    def contributeToContextMenu(self):
        return []

    @classmethod
    def contributeToMenu(cls):
        return []

Key_Any = 0
class PMXBaseKeyHelper(object):
    KEY = Key_Any
    def accept(self, widget, key):
        return self.KEY == key
    
    def execute(self, widget, key):
        pass
