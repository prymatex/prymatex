#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from glob import glob
from logging import getLogger

try:
    import json
except ImportError:
    import simplejson as json

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseComponent
from prymatex.utils.importlib import import_module, import_from_directory

PLUGIN_EXTENSION = 'pmxplugin'
PLUGIN_DESCRIPTOR_FILE = 'info.json'

class PMXPluginManager(PMXBaseComponent):
    def __init__(self, application):
        self.application = application
        self.directories = []
        
        self.modules = {}
        self.editors = []
        self.dockers = []
        self.statusBars = []
        self.keyHelpers = {}
        self.overlays = {}
        self.addons = {}
        self.instances = {}
    
    def addPluginDirectory(self, directory):
        self.directories.append(directory)

    #==================================================
    # Cargando clases
    #==================================================
    def registerEditor(self, editorClass):
        self.application.populateComponent(editorClass)
        self.editors.append(editorClass)
 
    def registerDocker(self, dockerClass):
        self.application.populateComponent(dockerClass)
        self.dockers.append(dockerClass)
        
    def registerStatusBar(self, statusBarClass):
        self.application.populateComponent(statusBarClass)
        self.statusBars.append(statusBarClass)
    
    def registerKeyHelper(self, editorClass, helperClass):
        self.application.extendComponent(helperClass)
        editorClass.addKeyHelper(helperClass())
        
    def registerOverlay(self, widgetClass, overlayClass):
        self.application.extendComponent(overlayClass)
        overlayClasses = self.overlays.setdefault(widgetClass, [])
        overlayClasses.append(overlayClass)

    def registerAddon(self, widgetClass, addonClass):
        self.application.extendComponent(addonClass)
        addonClasses = self.addons.setdefault(widgetClass, [])
        addonClasses.append(addonClass)
                
    def createWidgetInstance(self, widgetClass, mainWindow):
        instance = widgetClass(mainWindow)
        
        for overlayClass in self.overlays.get(widgetClass, []):
            overlay = overlayClass(instance)
            instance.addOverlay(overlay)

        for addonClass in self.addons.get(widgetClass, []):
            addon = addonClass(instance)
            instance.addAddon(addon)
            
        self.application.settings.configure(instance)
        instance.initialize(mainWindow)
        
        instances = self.instances.setdefault(widgetClass, [])
        instances.append(instance)
        return instance
    
    def createEditor(self, filePath, mainWindow):
        editorClass = self.editors[0]
        if filePath is not None:
            mimetype = self.application.fileManager.mimeType(filePath)
            for Klass in self.editors:
                if Klass.acceptFile(filePath, mimetype):
                    editorClass = Klass
                    break
        editor = self.createWidgetInstance(editorClass, mainWindow)
        return editor
    
    def createCustomActions(self, mainWindow):
        for editorClass in self.editors:
            menus = editorClass.contributeToMainMenu()
            if menus is not None:
                customEditorActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customEditorActions.extend(actions)
            mainWindow.registerEditorClassActions(editorClass, customEditorActions)
        
        for dockClass in self.dockers:
            menus = dockClass.contributeToMainMenu()
            if menus is not None:
                customDockActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customDockActions.extend(actions)
            mainWindow.registerDockClassActions(dockClass, customDockActions)
        
        for statusClass in self.statusBars:
            menus = statusClass.contributeToMainMenu()
            if menus is not None:
                customStatusActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customStatusActions.extend(actions)
            mainWindow.registerStatusClassActions(statusClass, customStatusActions)
            
    def populateMainWindow(self, mainWindow):
        self.createCustomActions(mainWindow)
            
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        for dockClass in self.dockers:
            dock = self.createWidgetInstance(dockClass, mainWindow)
            mainWindow.addDock(dock, dock.PREFERED_AREA)

        for statusBarClass in self.statusBars:
            status = self.createWidgetInstance(statusBarClass, mainWindow)
            mainWindow.addStatusBar(status)
    
    def _load_module(self, moduleName, moduleId = None, moduleDirectory = None, registerFunction = "registerPlugin"):
        moduleId = moduleId or moduleName
        try:
            module = import_from_directory(moduleDirectory, moduleName) if moduleDirectory is not None else import_module(moduleName)
            registerPluginFunction = getattr(module, registerFunction)
            registerPluginFunction(self)
            self.modules[moduleId] = module
        except (ImportError, AttributeError), reason:
            #TODO: Manejar estos errores
            raise reason

    def _load_plugin(self, pluginPath, pluginDescriptorPath):
        descriptorFile = open(pluginDescriptorPath, 'r')
        pluginInfo = json.load(descriptorFile)
        descriptorFile.close()
        moduleId = pluginInfo.get("id", None)
        moduleName = pluginInfo.get("module", None)
        registerFunction = pluginInfo.get("register", "registerPlugin")
        self._load_module(moduleName, moduleId = moduleId, moduleDirectory = pluginPath, registerFunction = registerFunction)
    
    def loadPlugins(self):
        self._load_module('prymatex.gui.codeeditor')
        self._load_module('prymatex.gui.dockers')
        for directory in self.directories:
            if not os.path.isdir(directory):
                continue
            for pluginPath in glob(os.path.join(directory, '*.%s' % PLUGIN_EXTENSION)):
                pluginDescriptorPath = os.path.join(pluginPath, PLUGIN_DESCRIPTOR_FILE)
                if os.path.isdir(pluginPath) and os.path.isfile(pluginDescriptorPath):
                    self._load_plugin(pluginPath, pluginDescriptorPath)
                    