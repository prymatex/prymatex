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

class PackageDescriptor(object):
    name = ""
    title = ""
    description = ""
    icon = ":/prymatex.png"
    namespace = None
    resources = None

    def __init__(self, application, entry):
        for key, value in entry.items():
            setattr(self, key, value)
        self.application = application
        self.modules = []
        self.resources = application.resourceManager.get_provider(self.namespace and self.namespace.name)
        self.icon = self.resources.get_icon(self.icon)
        if self.icon.isNull():
            self.icon = self.resources.get_icon(":/prymatex.png")

    def registerComponent(self, klass, base=PrymatexMainWindow, default=False):
        if self.namespace and not hasattr(klass, "RESOURCES"):
            setattr(klass, "RESOURCES", self.namespace.name)
        klass._package = self
        klass.package = classmethod(lambda cls: cls._package)
        self.application.registerComponent(klass, base, default)

class PackageManager(PrymatexComponent, QtCore.QObject):
    # ------------- Settings
    def __init__(self, **kwargs):
        super(PackageManager, self).__init__(**kwargs)

        self.namespaces = {}
        self.packages = {}

    def loadPackages(self, message_handler):
        self.loadCorePackage('prymatex.gui.codeeditor', 'org.prymatex.codeeditor')
        self.loadCorePackage('prymatex.gui.dockers', 'org.prymatex.dockers')
        self.loadCorePackage('prymatex.gui.dialogs', 'org.prymatex.dialogs')
        loadLaterEntries = []
        for name, directory in self.namespaces.items():
            for name in os.listdir(directory):
                package_path = os.path.join(directory, name)
                package_descriptor_path = os.path.join(package_path, config.PMX_PACKAGE_DESCRIPTOR)
                entry = { "id": name }
                if os.path.isfile(package_descriptor_path):
                    with open(package_descriptor_path, 'r') as f:
                        entry.update(json.load(f))

                # Package name
                entry["name"] = name

                # Load paths
                entry["path"] = package_path

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
                    self.loadPackage(entry)
                else:
                    loadLater.append(entry)
            if not loadLater or unsolvedCount == len(loadLater):
                break
            else:
                loadLaterEntries = loadLater
                unsolvedCount = len(loadLaterEntries)
        #Si me quedan packages tendira que avisar o mostrar algo es que no se cumplieron todas las dependencias

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addNamespace(self, namespace, bultin=False):
        directory=os.path.join(namespace.path, config.PMX_PACKAGES_NAME)
        if os.path.exists(directory) and os.path.isdir(directory):
            self.namespaces[namespace.name] = directory

    # ---------- Load packages
    def _import_package(self, descriptor, name=None, directory=None):
        builtins.__prymatex__ = descriptor
        if directory:
            descriptor.modules.extend(import_from_directory(directory))
        elif name:
            descriptor.modules.append(import_module(name)) 
        del(builtins.__prymatex__)

    def loadPackage(self, entry):
        _id = entry.get("id")
        directory = entry.get("path")
        try:
            share_path = os.path.join(directory, entry.get("share", config.PMX_SHARE_NAME))
            if os.path.isdir(share_path):
                entry["namespace"] = self.application().addNamespace(entry["name"], share_path)
            self.packages[_id] = PackageDescriptor(self.application(), entry)
            self._import_package(self.packages[_id], directory=directory)
        except Exception as reason:
            # On exception remove entry
            if _id in self.packages:
                del self.packages[_id]
            traceback.print_exc()
    
    def loadCorePackage(self, module_name, _id):
        entry = {"id": _id}
        try:
            self.packages[_id] = PackageDescriptor(self.application(), entry)
            self._import_package(self.packages[_id], name=module_name)
            # Core path
            self.packages[_id].path = self.packages[_id].modules[0].__path__[0]
        except (ImportError, AttributeError) as reason:
            # On exception remove entry
            if _id in self.packages:
                del(self.packages[_id])
            traceback.print_exc()
        
    def hasDependenciesResolved(self, entry):
        return all([dep in self.packages for dep in entry.get("depends", [])])
        
