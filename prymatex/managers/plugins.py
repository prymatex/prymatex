#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os, sys
from glob import glob
import collections

try:
    import json
except ImportError:
    import simplejson as json

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.utils import osextra
from prymatex.core import PMXBaseComponent, PMXBaseEditor
from prymatex.utils.importlib import import_module, import_from_directory

from prymatex.gui.mainwindow import PrymatexMainWindow

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
        for key, value in entry.items():
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
        
        self.components = {}
        
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addPluginDirectory(self, directory):
        self.directories.append(directory)

    # ------------- Cargando clases
    def registerComponent(self, componentClass, componentBase = PrymatexMainWindow):
        self.application.populateComponentClass(componentClass)
        componentClass.plugin = self.currentPluginDescriptor
        self.components.setdefault(componentBase, []).append(componentClass)
    
    # ------------ Handle component classes
    def findComponentsForClass(self, klass):
        return self.components.get(klass, [])
    
    def componentHierarchyForClass(self, klass):
        hierarchy = [ ]
        while klass != PrymatexMainWindow:
            hierarchy.append(klass)
            parent = [p_children for p_children in iter(self.components.items()) if klass in p_children[1]]
            if len(parent) != 1:
                break
            klass = parent.pop()[0]
        hierarchy.reverse()
        return hierarchy
        
    # ------------ Handle editor classes
    def findEditorClassForFile(self, filePath):
        mimetype = self.application.fileManager.mimeType(filePath)
        editors = [cmp for cmp in self.components.get(PrymatexMainWindow, []) if issubclass(cmp, PMXBaseEditor)]
        for Klass in editors:
            if Klass.acceptFile(filePath, mimetype):
                return Klass
    
    def defaultEditor(self):
        editors = [cmp for cmp in self.components.get(PrymatexMainWindow, []) if issubclass(cmp, PMXBaseEditor)]
        return editors[0]

    # ---------- Load plugins
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
            if isinstance(registerPluginFunction, collections.Callable):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self)
        except Exception as reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
        self.currentPluginDescriptor = None
    
    def loadCoreModule(self, moduleName, pluginId):
        pluginEntry = {"id": pluginId,
                       "resources": resources}
        try:
            pluginEntry["module"] = import_module(moduleName)
            registerPluginFunction = getattr(pluginEntry["module"], "registerPlugin")
            if isinstance(registerPluginFunction, collections.Callable):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self)
        except (ImportError, AttributeError) as reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
            raise reason
        self.currentPluginDescriptor = None
        
    def hasDependenciesResolved(self, pluginEntry):
        return all([dep in self.plugins for dep in pluginEntry.get("depends", [])])
    
    def loadPlugins(self):
        self.loadCoreModule('prymatex.gui.codeeditor', 'org.prymatex.codeeditor')
        self.loadCoreModule('prymatex.gui.dockers', 'org.prymatex.dockers')
        self.loadCoreModule('prymatex.gui.dialogs', 'org.prymatex.dialogs')
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