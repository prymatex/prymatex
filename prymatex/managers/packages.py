#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from glob import glob
import collections

try:
    import json
except ImportError:
    import simplejson as json

try:
    import builtins
except ImportError as ex:
    import __builtin__ as builtins

from prymatex import resources

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core import config
from prymatex.core.components import PrymatexComponent, PrymatexEditor

from prymatex.utils import osextra
from prymatex.utils.importlib import import_module, import_from_directory

from prymatex.gui.main import PrymatexMainWindow

class PluginDescriptor(object):
    name = ""
    title = ""
    description = ""
    icon = None

    def __init__(self, application, entry):
        for key, value in entry.items():
            setattr(self, key, value)
        self.application = application
        self.modules = []

    def registerComponent(self, klass, base=PrymatexMainWindow, default=False):
        if not hasattr(klass, "RESOURCES"):
            setattr(klass, "RESOURCES", self.resources.names())
        klass._plugin = self
        klass.plugin = classmethod(lambda cls: cls._plugin)
        self.application.registerComponent(klass, base, default)

class PackageManager(PrymatexComponent, QtCore.QObject):
    # ------------- Settings
    def __init__(self, **kwargs):
        super(PackageManager, self).__init__(**kwargs)

        self.namespaces = {}
        self.packages = {}
        
        self.currentPluginDescriptor = None
        
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addNamespace(self, name, base_path):
        directory=os.path.join(base_path, config.PMX_PACKAGES_NAME)
        if os.path.exists(directory) and os.path.isdir(directory):
            self.namespaces[name] = directory

    # ---------- Load plugins
    def loadResources(self, directory, entry):
        defaults = self.application().resourceManager.defaults()
        #  TODO: Dependencias
        share_path = os.path.join(directory, entry.get("share", config.PMX_SHARE_NAME))
        if os.path.isdir(share_path):
            self.application().resourceManager.add_source(entry["name"], share_path)
            defaults = (entry["name"],) + defaults
        entry["resources"] = self.application().resourceManager.get_provider(defaults)
        if "icon" in entry:
            entry["icon"] = entry["resources"].get_icon(entry.get("icon", ":/prymatex.png"))

    def loadBundles(self, directory, entry):
        defaults = self.application().resourceManager.defaults()
        bundles_path = os.path.join(directory, entry.get("bundles", config.PMX_BUNDLES_NAME))
        if os.path.isdir(bundles_path):
            print("Bundles en", bundles_path)
            
    def _import_package(self, entry, name=None, directory=None):
        descriptor = PluginDescriptor(self.application(), entry)
        builtins.__plugin__ = descriptor
        if directory:
            descriptor.modules.extend(import_from_directory(directory))
        elif name:
            descriptor.modules.append(import_module(name)) 
        del(builtins.__plugin__)
        return descriptor

    def loadPackage(self, entry):
        _id = entry.get("id")
        directory = entry.get("path")
        try:
            self.loadResources(directory, entry)
            self.loadBundles(directory, entry)
            self.packages[_id] = self._import_package(entry, directory=directory)
        except Exception as reason:
            # On exception remove entry
            if _id in self.packages:
                del self.packages[_id]
            traceback.print_exc()
    
    def loadCorePackage(self, module_name, _id):
        entry = {
            "id": _id,
            "icon": self.application().resources().get_icon(':/prymatex.png'),
            "resources": self.application().resources()
        }
        try:
            self.packages[_id] = self._import_package(entry, name=module_name)
        except (ImportError, AttributeError) as reason:
            # On exception remove entry
            if _id in self.packages:
                del(self.packages[_id])
            traceback.print_exc()
        
    def hasDependenciesResolved(self, entry):
        return all([dep in self.packages for dep in entry.get("depends", [])])
    
    def loadPackages(self):
        self.loadCorePackage('prymatex.gui.codeeditor', 'org.prymatex.codeeditor')
        self.loadCorePackage('prymatex.gui.dockers', 'org.prymatex.dockers')
        self.loadCorePackage('prymatex.gui.dialogs', 'org.prymatex.dialogs')
        loadLaterEntries = []
        for name, directory in self.namespaces.items():
            for name in os.listdir(directory):
                plugin_path = os.path.join(directory, name)
                plugin_descriptor_path = os.path.join(plugin_path, config.PMX_PACKAGE_DESCRIPTOR_NAME)
                entry = { "id": name }
                if os.path.isfile(plugin_descriptor_path):
                    with open(plugin_descriptor_path, 'r') as f:
                        entry.update(json.load(f))

                # Package name
                entry["name"] = name

                # Load paths
                entry["path"] = plugin_path

                if self.hasDependenciesResolved(entry):
                    self.loadPackage(entry)
                else:
                    loadLaterEntries.append(entry)
        # Cargar las que quedaron bloqueadas por dependencias hasta consumirlas
        # dependencias circulares? son ridiculas pero por lo menos detectarlas
        unsolvedCount = len(loadLaterEntries)
        while True:
            loadLater = []
            for entry in loadLaterEntries:
                if self.hasDependenciesResolved(entry):
                    self.loadPlugin(entry)
                else:
                    loadLater.append(entry)
            if not loadLater or unsolvedCount == len(loadLater):
                break
            else:
                loadLaterEntries = loadLater
                unsolvedCount = len(loadLaterEntries)
        #Si me quedan plugins tendira que avisar o mostrar algo es que no se cumplieron todas las dependencias
