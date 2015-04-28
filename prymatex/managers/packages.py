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
    icon = None
    namespace = None
    resources = None

    def __init__(self, application, entry):
        self.name = entry.get("name")
        self.application = application
        self.depends = entry.pop('depends', [])
        self.share = entry.pop('share', None)
        if self.share:
            self.namespace = application.addNamespace(self.name, self.share)
        self._icon = entry.pop('icon', ":/prymatex.png")
        self._load = False
        self.modules = []

        # TODO: Controlar que no todo porque es un despelote
        for key, value in entry.items():
            setattr(self, key, value)

    def loadResources(self, names):
        self.resources = self.application.resourceManager.get_provider(names)
        self.icon = self.resources.get_icon(self._icon)

    def load(self):
        return self._load

    def setLoad(self, _load):
        self._load = _load

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

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.plugins import PluginsSettingsWidget
        return [ PluginsSettingsWidget ]

    def addNamespace(self, namespace, bultin=False):
        directory=os.path.join(namespace.path, config.PMX_PACKAGES_NAME)
        if os.path.exists(directory) and os.path.isdir(directory):
            self.namespaces[namespace.name] = directory

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
                share_path = os.path.join(package_path, entry.get("share", config.PMX_SHARE_NAME))
                if os.path.isdir(share_path):
                    entry["share"] = share_path

                self.packages[entry.get('id', name)] = PackageDescriptor(self.application(), entry)
        # Cargar las que quedaron bloqueadas por dependencias hasta consumirlas
        # dependencias circulares? son ridiculas pero por lo menos detectarlas
        while any((not desc.load() for desc in self.packages.values())):
            for descriptor in list(self.packages.values()):
                # If not load and has all deps
                if not descriptor.load() and \
                    all((self.packages[dep].load() for dep in descriptor.depends)):
                    try:
                        self._import_package(descriptor)
                        descriptor.setLoad(True)
                    except Exception as reason:
                        traceback.print_exc()
                        del self.packages[descriptor.id]
    
    # ---------- Import package
    def _import_package(self, descriptor):
        builtins.__prymatex__ = descriptor
        if descriptor.core:
            descriptor.modules.append(import_module(descriptor.name)) 
        else:
            # Collect deps
            deps = self.collect_deps(descriptor)
            paths = [dep.directory for dep in deps]
            resources = [dep.namespace.name for dep in [descriptor] + deps if dep.namespace]
            descriptor.loadResources(resources)
            descriptor.modules.extend(import_from_directory(descriptor.directory, paths=paths))

        del(builtins.__prymatex__)
        
    def collect_deps(self, descriptor, core=False):
        def _collect_deps(descriptor):
            deps = []
            for dep in descriptor.depends:
                if not core and self.packages[dep].core:
                    continue
                deps.append(self.packages[dep])
                deps.extend(_collect_deps(self.packages[dep]))
            return deps
        return _collect_deps(descriptor)
