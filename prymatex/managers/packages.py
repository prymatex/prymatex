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
        self.application = application
        self.resources = application.resources()
        self.depends = entry.pop('depends', [])
        self._load = False
        self.modules = []
        self._icon = entry.pop('icon', ":/prymatex.png")
        self.icon = self.resources.get_icon(self._icon)

        # TODO: Controlar que no todo porque es un despelote
        for key, value in entry.items():
            setattr(self, key, value)

    def load(self):
        return self._load

    def setLoad(self, _load):
        self._load = _load

    def addShare(self, directory):
        self.namespace = self.application.addNamespace(self.name, directory)
        self.resources = self.application.resourceManager.get_provider(self.namespace)
        icon = self.resources.get_icon(self._icon)
        if not icon.isNull():
            self.icon = icon

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
        # Core packages
        self.packages['org.prymatex.codeeditor'] = PackageDescriptor(self.application(), {
            'id': 'org.prymatex.codeeditor',
            'name': 'prymatex.gui.codeeditor',
            'core': True,
            'directory': os.path.join(config.PMX_APP_PATH, 'prymatex', 'gui', 'codeeditor')
        })
        self.packages['org.prymatex.dockers'] = PackageDescriptor(self.application(), {
            'id': 'org.prymatex.dockers',
            'name': 'prymatex.gui.dockers',
            'core': True,
            'directory': os.path.join(config.PMX_APP_PATH, 'prymatex', 'gui', 'dockers')
        })
        self.packages['org.prymatex.dialogs'] = PackageDescriptor(self.application(), {
            'id': 'org.prymatex.dialogs',
            'name': 'prymatex.gui.dialogs',
            'core': True,
            'directory': os.path.join(config.PMX_APP_PATH, 'prymatex', 'gui', 'dialogs')
        })
        for name, directory in self.namespaces.items():
            for name in os.listdir(directory):
                package_path = os.path.join(directory, name)
                package_descriptor_path = os.path.join(package_path, config.PMX_PACKAGE_DESCRIPTOR)
                entry = { "id": name }
                if os.path.isfile(package_descriptor_path):
                    with open(package_descriptor_path, 'r') as f:
                        entry.update(json.load(f))

                entry["name"] = name
                entry["directory"] = package_path
                entry["core"] = False

                self.packages[entry.get('id', name)] = PackageDescriptor(self.application(), entry)
        # Cargar las que quedaron bloqueadas por dependencias hasta consumirlas
        # dependencias circulares? son ridiculas pero por lo menos detectarlas
        while any((not desc.load() for desc in self.packages.values())):
            for descriptor in list(self.packages.values()):
                if not descriptor.load() and self.hasDependenciesResolved(descriptor):
                    descriptor.setLoad(self.loadPackage(descriptor))
                    if not descriptor.load():
                        del self.packages[descriptor.id]
                        #Tendira que avisar o mostrar algo es que no se cumplieron todas las dependencias

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addNamespace(self, namespace, bultin=False):
        directory=os.path.join(namespace.path, config.PMX_PACKAGES_NAME)
        if os.path.exists(directory) and os.path.isdir(directory):
            self.namespaces[namespace.name] = directory

    # ---------- Load packages
    def _import_package(self, descriptor):
        builtins.__prymatex__ = descriptor
        if descriptor.core:
            descriptor.modules.append(import_module(descriptor.name)) 
        else:
            descriptor.modules.extend(import_from_directory(descriptor.directory))
        del(builtins.__prymatex__)

    def loadPackage(self, descriptor):
        try:
            share_path = os.path.join(descriptor.directory, config.PMX_SHARE_NAME)
            if os.path.isdir(share_path):
                descriptor.addShare(share_path)
            self._import_package(descriptor)
        except Exception as reason:
            # On exception remove entry
            traceback.print_exc()
            return False
        return True
        
    def hasDependenciesResolved(self, descriptor):
        return all((self.packages[dep].load() for dep in descriptor.depends))
        
