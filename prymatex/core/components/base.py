#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: No son Mixin?

class PMXBaseComponent(object):
    def initialize(self):
        raise NotImplemented
    
    def finalize(self):
        pass

    @classmethod
    def contributeToSettings(cls):
        """Class contributions to the settings dialog"""
        return []

    @classmethod
    def contributeToMainMenu(cls):
        """Contributions to the main menu"""
        return {}
        
    def environmentVariables(self):
        """Return a dictionary with the defined variables of this component."""
        return {}

class PMXBaseWidgetComponent(PMXBaseComponent):
    def __init__(self):
        self.addons = []
        self.keyHelpers = {}
            
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
        for addon in self.addons:
            addon.initialize(self)
        for keyHelpers in self.keyHelpers.values():
            map(lambda keyHelper: keyHelper.initialize(self), keyHelpers)

    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        return PMXBaseComponent.contributeToMainMenu()
    
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
        helpers = []
        if Key_Any in self.keyHelpers:
            helpers += self.keyHelpers[Key_Any]
        helpers += self.keyHelpers.get(key, [])
        return helpers

    def runKeyHelper(self, *largs, **kwargs):
        raise NotImplemented
            
    def saveState(self):
        """Returns a Python dictionary containing the state of the editor."""
        return {}
    
    def restoreState(self, state):
        """Restore the state from the given state (returned by a previous call to saveState())."""
        pass

    def showMessage(self, message, timeout = 0):
        """Show message in main window's"""
        self.mainWindow.showMessage(message, timeout)
        
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

