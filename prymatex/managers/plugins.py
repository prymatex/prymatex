#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os, sys
from glob import glob

try:
    import json
except ImportError:
    import simplejson as json

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.utils import osextra
from prymatex.core import PMXBaseComponent
from prymatex.utils.importlib import import_module, import_from_directory

PLUGIN_EXTENSION = 'pmxplugin'
PLUGIN_DESCRIPTOR_FILE = 'info.json'

class ResourceProvider():
    def __init__(self, resources):
        self.resources = resources

    def getImage(self, index, size = None, default = None):
        if index in self.resources:
            return QtGui.QPixmap(self.resources[index])
        return resources.getImage(index, size, default)
        
    def getIcon(self, index, size = None, default = None):
        if index in self.resources:
            return QtGui.QIcon(self.resources[index])
        return resources.getIcon(index, size, default)

class PluginDescriptor(object):
    name = ""
    description = ""
    icon = None
    def __init__(self, entry):
        for key, value in entry.iteritems():
            setattr(self, key, value)
        
class PluginManager(QtCore.QObject, PMXBaseComponent):
    
    #=========================================================
    # Settings
    #=========================================================
    SETTINGS_GROUP = 'PluginManager'
    
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)

        self.directories = []
        
        self.currentPluginDescriptor = None
        self.plugins = {}
        
        self.editors = []
        self.dockers = []
        self.statusBars = []
        self.keyHelpers = {}
        self.addons = {}
        self.instances = {}

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addPluginDirectory(self, directory):
        self.directories.append(directory)

    #==================================================
    # Cargando clases
    #==================================================
    def registerEditor(self, editorClass):
        self.application.populateComponent(editorClass)
        editorClass.plugin = self.currentPluginDescriptor
        self.editors.append(editorClass)

    def registerDocker(self, dockerClass):
        self.application.populateComponent(dockerClass)
        dockerClass.plugin = self.currentPluginDescriptor
        self.dockers.append(dockerClass)

    def registerStatusBar(self, statusBarClass):
        self.application.populateComponent(statusBarClass)
        statusBarClass.plugin = self.currentPluginDescriptor
        self.statusBars.append(statusBarClass)

    def registerKeyHelper(self, widgetClass, helperClass):
        self.application.extendComponent(helperClass)
        helperClass.plugin = self.currentPluginDescriptor
        keyHelperClasses = self.keyHelpers.setdefault(widgetClass, [])
        keyHelperClasses.append(helperClass)

    def registerAddon(self, widgetClass, addonClass):
        self.application.populateComponent(addonClass)
        addonClass.plugin = self.currentPluginDescriptor
        addonClasses = self.addons.setdefault(widgetClass, [])
        addonClasses.append(addonClass)

    # -------------- Creando instancias
    def createWidgetInstance(self, widgetClass, parent):
        instance = widgetClass(parent)
        
        for addonClass in self.addons.get(widgetClass, []):
            addon = addonClass(instance)
            instance.addComponentAddon(addon)
        
        for keyHelperClass in self.keyHelpers.get(widgetClass, []):
            keyHelper = keyHelperClass(instance)
            instance.addKeyHelper(keyHelper)
            
        instances = self.instances.setdefault(widgetClass, [])
        instances.append(instance)
        return instance
    
    
    def createCustomActions(self, mainWindow):
        for editorClass in self.editors:
            addonClasses = self.addons.get(editorClass, [])
            menus = editorClass.contributeToMainMenu(addonClasses)
            if menus is not None:
                customEditorActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customEditorActions.extend(actions)
            mainWindow.registerEditorClassActions(editorClass, customEditorActions)
        
        for dockClass in self.dockers:
            addonClasses = self.addons.get(dockClass, [])
            menus = dockClass.contributeToMainMenu(addonClasses)
            if menus is not None:
                customDockActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customDockActions.extend(actions)
            mainWindow.registerDockClassActions(dockClass, customDockActions)
        
        for statusClass in self.statusBars:
            addonClasses = self.addons.get(statusClass, [])
            menus = statusClass.contributeToMainMenu(addonClasses)
            if menus is not None:
                customStatusActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customStatusActions.extend(actions)
            mainWindow.registerStatusClassActions(statusClass, customStatusActions)
            
    def populateMainWindow(self, mainWindow):
        self.createCustomActions(mainWindow)
            
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        # TODO: Ver esto de llamar a la application para crear que por otro lado llama nuevamente a esta instancia
        for dockClass in self.dockers:
            dock = self.application.createWidgetComponentInstance(dockClass, mainWindow)
            mainWindow.addDock(dock, dock.PREFERED_AREA)

        for statusBarClass in self.statusBars:
            status = self.application.createWidgetComponentInstance(statusBarClass, mainWindow)
            mainWindow.addStatusBar(status)
    
    #==================================================
    # Handle editor classes
    #==================================================
    def findEditorClassForFile(self, filePath):
        mimetype = self.application.fileManager.mimeType(filePath)
        for Klass in self.editors:
            if Klass.acceptFile(filePath, mimetype):
                return Klass
    
    def defaultEditor(self):
        return self.editors[0]

    #==================================================
    # Load plugins
    #==================================================
    def loadResources(self, pluginDirectory, pluginEntry):
        if "icon" in pluginEntry:
            iconPath = os.path.join(pluginDirectory, pluginEntry["icon"])
            pluginEntry["icon"] = QtGui.QIcon(iconPath)
        if "share" in pluginEntry:
            pluginEntry["share"] = os.path.join(pluginDirectory, pluginEntry["share"])
            res = resources.loadResources(pluginEntry["share"])
            pluginEntry["resources"] = ResourceProvider(res)
        else:
            # Global resources
            pluginEntry["resources"] = resources
        
    def loadPlugin(self, pluginEntry):
        pluginId = pluginEntry.get("id")
        packageName = pluginEntry.get("package")
        registerFunction = pluginEntry.get("register", "registerPlugin")
        pluginDirectory = pluginEntry.get("path")
        self.loadResources(pluginDirectory, pluginEntry)
        try:
            pluginEntry["module"] = import_from_directory(pluginDirectory, packageName)
            registerPluginFunction = getattr(pluginEntry["module"], registerFunction)
            if callable(registerPluginFunction):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self)
        except Exception as reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
            raise reason
        self.currentPluginDescriptor = None
    
    def loadCoreModule(self, moduleName, pluginId):
        pluginEntry = {"id": pluginId,
                       "resources": resources}
        try:
            pluginEntry["module"] = import_module(moduleName)
            registerPluginFunction = getattr(pluginEntry["module"], "registerPlugin")
            if callable(registerPluginFunction):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self)
        except (ImportError, AttributeError), reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
            raise reason
        self.currentPluginDescriptor = None
        
    def hasDependenciesResolved(self, pluginEntry):
        return all(map(lambda dep: dep in self.plugins, pluginEntry.get("depends", [])))
    
    def loadPlugins(self):
        self.loadCoreModule('prymatex.gui.codeeditor', 'org.prymatex.codeeditor')
        self.loadCoreModule('prymatex.gui.dockers', 'org.prymatex.dockers')
        loadLaterEntries = []
        for directory in self.directories:
            if not os.path.isdir(directory):
                continue
            for pluginPath in glob(os.path.join(directory, '*.%s' % PLUGIN_EXTENSION)):
                pluginDescriptorPath = os.path.join(pluginPath, PLUGIN_DESCRIPTOR_FILE)
                if os.path.isdir(pluginPath) and os.path.isfile(pluginDescriptorPath):
                    descriptorFile = open(pluginDescriptorPath, 'r')
                    pluginEntry = json.load(descriptorFile)
                    descriptorFile.close()
                    pluginEntry["path"] = pluginPath
                    if self.hasDependenciesResolved(pluginEntry):
                        self.loadPlugin(pluginEntry)
                    else:
                        loadLaterEntries.append(pluginEntry)
        #Cargar las que quedaron bloqueadas por dependencias hasta consumirlas
        # dependencias circulares? son ridiculas pero por lo menos detectarlas
        unsolvedCount = len(loadLaterEntries)
        while True:
            loadLater = []
            for pluginEntry in loadLaterEntries:
                if self.hasDependenciesResolved(pluginEntry):
                    self.loadPlugin(pluginEntry)
                else:
                    loadLater.append(pluginEntry)
            if not loadLater or unsolvedCount == len(loadLater):
                break
            else:
                loadLaterEntries = loadLater
                unsolvedCount = len(loadLaterEntries)
        #Si me quedan plugins tendira que avisar o mostrar algo es que no se cumplieron todas las dependencias