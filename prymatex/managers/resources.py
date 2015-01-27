#!/usr/bin/env python

from prymatex.qt import QtCore, QtGui
from prymatex.core import PrymatexComponent

from prymatex.resources import (Resource, ResourceProvider, load_media,
    load_fonts, load_stylesheets)

class ResourceManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(ResourceManager, self).__init__(**kwargs)
        self.resources = []
        self.providers = {}
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.shortcuts import ShortcutsSettingsWidget

        return [ShortcutsSettingsWidget]
        
    def add_source(self, name, path, default=False):
        res = Resource(name, path, default)
        res.update(load_fonts(path))
        res.update(load_media(path))
        res.update(load_stylesheets(path))
        self.resources.insert(0, res)

    def get_provider(self, sources):
        if sources not in self.providers:
            self.providers[sources] = ResourceProvider(
                [ res for res in self.resources if res.name() in sources ]
            )
        return self.providers[sources]

    def defaults(self):
        return tuple([ res.name() for res in self.resources if res.default() ])

    def providerForClass(self, componentClass):
        sources = getattr(componentClass, "RESOURCES", self.defaults())
        return self.get_provider(sources)

    def install_icon_handler(self):
        QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
        QtGui.QIcon.fromTheme = self.icon_from_theme

    def icon_from_theme(self, index):
        # TODO: default provider
        for res in self.resources:
            icon = res.get_icon(index)
            if not icon.isNull():
                return icon
        return QtGui.QIcon()
