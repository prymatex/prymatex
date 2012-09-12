#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

#TODO: Refactor del paquete plugin, por un nombre mas de base

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

    def buildEnvironment(self, **kwargs):
        return {}

class PMXBaseWidgetComponent(PMXBaseComponent):
    def __init__(self):
        self.overlays = []
        self.addons = []
        self.keyHelpers = {}
            
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
        for overlay in self.overlays:
            overlay.initialize(self)
        for addon in self.addons:
            addon.initialize(self)
        for keyHelpers in self.keyHelpers.values():
            map(lambda keyHelper: keyHelper.initialize(self), keyHelpers)

    def updateOverlays(self):
        for overlay in self.overlays:
            overlay.updateOverlay()
    
    def addOverlay(self, overlay):
        self.overlays.append(overlay)

    # Addons api    
    def addAddon(self, addon):
        self.addons.append(addon)
        
    def addonByClass(self, klass):
        addons = filter(lambda addon: isinstance(addon, klass), self.addons)
        #TODO: Solo uno
        return addons[0]

    # Helpers api
    def addKeyHelper(self, helper):
        helpers = self.keyHelpers.setdefault(helper.KEY, [])
        helpers.append(helper)

    def keyHelperByClass(self, klass):
        keyHelper = filter(lambda keyHelper: isinstance(keyHelper, klass), self.keyHelpers)
        #TODO: Solo uno
        return keyHelper[0]
        
    def findHelpers(self, key):
        helpers = self.keyHelpers[Key_Any][:]
        return helpers + self.keyHelpers.get(key, [])

    #TODO: Poder filtrar que key helpers no quiero que corra o otra cosa
    def runKeyHelper(self, key):
        runHelper = False
        for helper in self.findHelpers(key):
            runHelper = helper.accept(self, key)
            if runHelper:
                helper.execute(self, key)
                break
        return runHelper

    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        return PMXBaseComponent.contributeToMainMenu()
        
    def saveState(self):
        """Returns a Python dictionary containing the state of the editor."""
        return {}
    
    def restoreState(self, state):
        """Restore the state from the given state (returned by a previous call to saveState())."""
        pass
    
class PMXBaseOverlay(object):
    def __init__(self, widget):
        pass
        
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass
    
    def updateOverlay(self):
        pass

class PMXBaseAddon(object):
    def __init__(self, widget):
        pass
        
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass

    @classmethod
    def contributeToSettings(cls):
        return []

    @classmethod
    def contributeToMainMenu(cls):
        return {}

    def contributeToContextMenu(self):
        return []

Key_Any = 0
class PMXBaseKeyHelper(object):
    KEY = Key_Any
    def __init__(self, widget):
        pass
        
    def initialize(self, widget):
        pass
    
    def finalize(self):
        pass

    def accept(self, key):
        return self.KEY == key
    
    def execute(self, key):
        pass

