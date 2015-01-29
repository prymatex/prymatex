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

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex import resources
from prymatex.utils import osextra
from prymatex.core import config
from prymatex.core import PrymatexComponent, PrymatexEditor
from prymatex.utils.importlib import import_module, import_from_directories

from prymatex.gui.main import PrymatexMainWindow

class PluginDescriptor(object):
    name = ""
    title = ""
    description = ""
    icon = None
    def __init__(self, entry):
        for key, value in entry.items():
            setattr(self, key, value)
        
class PluginManager(PrymatexComponent, QtCore.QObject):
    
    #=========================================================
    # Settings
    #=========================================================
    SETTINGS = 'PluginManager'
    
    def __init__(self, **kwargs):
        super(PluginManager, self).__init__(**kwargs)

        self.namespaces = {}
        
        self.currentPluginDescriptor = None
        self.plugins = {}
        
        self.components = {}
        self.defaultComponent = QtWidgets.QPlainTextEdit
        
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def install(self):
         for source in self.resources().sources():
            self.addNamespace(source.name(), source.path())

    def addNamespace(self, name, base_path):
        #TODO Validar que existe el base_path + PMX_PLUGINS_NAME
        self.namespaces[name] = os.path.join(base_path, config.PMX_PLUGINS_NAME)

    # ------------- Cargando clases
    def registerComponent(self, componentClass, componentBase = PrymatexMainWindow, default = False):
        if not hasattr(componentClass, "RESOURCES"):
            setattr(componentClass, "RESOURCES", self.currentPluginDescriptor.resources.names())
        
        self.application().populateComponentClass(componentClass)
        self.application().populateConfigurableClass(componentClass)

        componentClass._plugin = self.currentPluginDescriptor
        componentClass.plugin = classmethod(lambda cls: cls._plugin)
        self.components.setdefault(componentBase, []).append(componentClass)
        if default:
            self.defaultComponent = componentClass
    
    # ------------ Handle component classes
    def findComponentsForClass(self, klass):
        return self.components.get(klass, [])
    
    def componentHierarchyForClass(self, klass):
        hierarchy = []
        while klass != PrymatexMainWindow:
            hierarchy.append(klass)
            for parent, childs in self.components.items():
                if klass in childs:
                    klass = parent
                    break
        return hierarchy[::-1]
        
    # ------------ Handle editor classes
    def findEditorClassByName(self, name):
        editors = (cmp for cmp in self.components.get(PrymatexMainWindow, []) if issubclass(cmp, PrymatexEditor))
        for klass in editors:
            if name == klass.__name__:
                return klass

    def findEditorClassForFile(self, filepath):
        mimetype = self.application().fileManager.mimeType(filepath)
        editors = (cmp for cmp in self.components.get(PrymatexMainWindow, []) if issubclass(cmp, PrymatexEditor))
        for klass in editors:
            if klass.acceptFile(filepath, mimetype):
                return klass
    
    def defaultEditor(self):
        return self.defaultComponent

    # ---------- Load plugins
    def loadResources(self, pluginDirectory, pluginEntry):
        defaults = self.application().resourceManager.defaults()
        #  TODO: Dependencias
        if "share" in pluginEntry:
            pluginEntry["share"] = os.path.join(pluginDirectory, pluginEntry["share"])
            self.application().resourceManager.add_source(pluginEntry["name"], pluginEntry["share"])
            defaults = (pluginEntry["name"],) + defaults
        pluginEntry["resources"] = self.application().resourceManager.get_provider(defaults)
        if "icon" in pluginEntry:
            pluginEntry["icon"] = pluginEntry["resources"].get_icon(pluginEntry["icon"])

    def loadPlugin(self, pluginEntry):
        pluginId = pluginEntry.get("id")
        packageName = pluginEntry.get("package")
        registerFunction = pluginEntry.get("register", "registerPlugin")
        pluginDirectories = pluginEntry.get("paths")
        pluginDirectory = pluginEntry.get("path")
        self.loadResources(pluginDirectory, pluginEntry)
        try:
            pluginEntry["module"] = import_from_directories(pluginDirectories, packageName)
            registerPluginFunction = getattr(pluginEntry["module"], registerFunction)
            if isinstance(registerPluginFunction, collections.Callable):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self, self.currentPluginDescriptor)
        except Exception as reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
        self.currentPluginDescriptor = None
    
    def loadCoreModule(self, moduleName, pluginId):
        pluginEntry = {
            "id": pluginId,
            "icon": self.application().resources().get_icon(':/prymatex.png'),
            "resources": self.application().resources()
        }
        try:
            pluginEntry["module"] = import_module(moduleName)
            registerPluginFunction = getattr(pluginEntry["module"], "registerPlugin")
            if isinstance(registerPluginFunction, collections.Callable):
                self.currentPluginDescriptor = self.plugins[pluginId] = PluginDescriptor(pluginEntry)
                registerPluginFunction(self, self.currentPluginDescriptor)
        except (ImportError, AttributeError) as reason:
            # On exception remove entry
            if pluginId in self.plugins:
                del self.plugins[pluginId]
            traceback.print_exc()
        self.currentPluginDescriptor = None
        
    def hasDependenciesResolved(self, pluginEntry):
        return all([dep in self.plugins for dep in pluginEntry.get("depends", [])])
    
    def loadPlugins(self):
        self.loadCoreModule('prymatex.gui.codeeditor', 'org.prymatex.codeeditor')
        self.loadCoreModule('prymatex.gui.dockers', 'org.prymatex.dockers')
        self.loadCoreModule('prymatex.gui.dialogs', 'org.prymatex.dialogs')
        loadLaterEntries = []
        for name, directory in self.namespaces.items():
            if not os.path.isdir(directory):
                continue
            for pluginPath in glob(os.path.join(directory, config.PMX_PLUGIN_GLOB)):
                pluginDescriptorPath = os.path.join(pluginPath, config.PMX_DESCRIPTOR_NAME)
                if os.path.isfile(pluginDescriptorPath):
                    descriptorFile = open(pluginDescriptorPath, 'r')
                    pluginEntry = json.load(descriptorFile)
                    descriptorFile.close()

                    # Plugin name
                    pluginEntry["name"], _ = os.path.splitext(os.path.basename(pluginPath))

                    # Load paths
                    pluginEntry["path"] = pluginPath
                    paths = [ pluginPath ]
                    for path in pluginEntry.get("paths", []):
                        if not os.path.isabs(path):
                            path = os.path.abspath(os.path.join(pluginPath, path))
                        paths.append(path)
                    pluginEntry["paths"] = paths

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
