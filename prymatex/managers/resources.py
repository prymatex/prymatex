#!/usr/bin/env python

import logging

from prymatex.qt import QtCore, QtGui
from prymatex.core import PrymatexComponent, config

from prymatex.resources import (Resource, ResourceProvider)
from prymatex.models.shortcuts import ShortcutsTreeModel

logger = logging.getLogger(__name__)

class ResourceManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(ResourceManager, self).__init__(**kwargs)
        # Icon Handler
        QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
        QtGui.QIcon.fromTheme = self.icon_from_theme

        self.prymatex_resources = []
        
        self.base = Resource(self.application().createNamespace('base', ''))
        # Shortcut Models
        self.shortcutsTreeModel = ShortcutsTreeModel(self)

    def loadResources(self, message_handler):
        # Load standard shortcuts
        self.shortcutsTreeModel.loadStandardSequences(self.resources())

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.shortcuts import ShortcutsSettingsWidget

        return [ ShortcutsSettingsWidget ]

    def registerShortcut(self, qobject, sequence):
        return self.shortcutsTreeModel.registerShortcut(qobject, sequence)
        
    def addNamespace(self, namespace):
        self.prymatex_resources.insert(0, Resource(namespace))

    def get_provider(self, names, builtins=True):
        names = names if isinstance(names, (list, tuple)) else [ names ]  
        resources = [res for res in self.prymatex_resources if res.namespace().name in names]
        if builtins:
            resources = resources + self.builtins()
        resources.append(self.base)
        logger.debug("get_provider for [%s] got [%s]" % (
            ",".join(names), 
            ",".join([r.namespace().name for r in resources])
        ))
        return ResourceProvider(resources)

    def builtins(self):
        return [res for res in self.prymatex_resources if res.namespace().builtin]

    def providerForClass(self, componentClass):
        resource_name = getattr(componentClass, "RESOURCES", '')
        return self.get_provider(resource_name)

    def icon_from_theme(self, index):
        # TODO: default provider
        for res in self.prymatex_resources:
            icon = res.get_icon(index)
            if not icon.isNull():
                return icon
        return QtGui.QIcon()
