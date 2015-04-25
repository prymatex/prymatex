#!/usr/bin/env python
import os
from prymatex.qt import QtCore

from prymatex.core.components import PrymatexComponent 
from prymatex.core.settings import (TextMateSettings, PrymatexSettings,
                                    ConfigurableItem, ConfigurableHook)
from prymatex.core import source
                                    
from prymatex.utils import text as textutils
from prymatex.utils import json
from prymatex.utils import settings

from prymatex.models.settings import SettingsTreeModel
from prymatex.models.settings import SortFilterSettingsProxyModel

class SettingsManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(SettingsManager, self).__init__(**kwargs)
        self._settings = []

        # Settings Models
        self.settingsTreeModel = SettingsTreeModel(parent=self)
        self.sortFilterSettingsProxyModel = SortFilterSettingsProxyModel(parent=self)
        self.sortFilterSettingsProxyModel.setSourceModel(self.settingsTreeModel)
        
        self.application().aboutToQuit.connect(self.on_application_aboutToQuit)
        
        # Reload settings
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.fileChanged.connect(
            self.on_fileSystemWatcher_pathChanged
        )
        self.fileSystemWatcher.directoryChanged.connect(
            self.on_fileSystemWatcher_pathChanged
        )

    def on_fileSystemWatcher_pathChanged(self, path):
        settings = [s for s in self._settings if s.source.name == path or s.source.path == path].pop()
        if settings.source.hasChanged():
            if settings.source.exists:
                data = settings.get_data(settings.source.path)
                settings.reload(data)
            else:
                settings.reload({})
            settings.source = settings.source.newUpdatedTime()

    def getSettings(self, path, klass=settings.Settings):
        settings = [s for s in self._settings if s.source.name == path or s.source.path == path]
        if settings:
            return settings[0]
        basename = os.path.basename(path)
        directory = os.path.dirname(path)
        _source = source.Source(directory, path)
        data = klass.get_data(_source.path) if _source.exists else {}
        settings = klass(basename, data)
        settings.source = _source
        self._settings.append(settings)
        self.fileSystemWatcher.addPath(_source.exists and _source.path or _source.name)
        return settings
    
    def initialize(self):
        # Textmate Settings
        self.textmate_settings = self.getSettings(
            self.profile().TM_PREFERENCES_PATH,
            TextMateSettings
        )
        
        # Prymatex Settings
        self.prymatex_settings = self.getSettings(
            self.profile().PMX_SETTINGS_PATH,
            PrymatexSettings
        )
        self.prymatex_settings.setTm(self.textmate_settings)
        
    # ------------------- Signals
    def on_application_aboutToQuit(self):
        # Save textmate
        self.textmate_settings.write(self.profile().TM_PREFERENCES_PATH)
        # Save settings
        self.prymatex_settings.purge()
        self.prymatex_settings.write(self.profile().PMX_SETTINGS_PATH)

        state = self.application().componentState()
        json.write_file(state, self.profile().PMX_STATE_PATH)

    # -------------------- Public API
    def loadSettings(self, message_handler):
        # Load settings
        self.settingsTreeModel.loadSettings()

    def populateConfigurableClass(self, component_class):
        if hasattr(component_class, '_settings_widgets'):
            return
        component_class._settings_widgets = []
        for klass in component_class.contributeToSettings():
            settings_widget = klass(component_class)
            component_class._settings_widgets.append(settings_widget)
            self.settingsTreeModel.addConfigNode(settings_widget)

    # ------------------------ Setting
    def settingsForClass(self, configurableClass):
        scope_name = getattr(configurableClass, 'SETTINGS',
            "_".join(textutils.camelcase_to_text(configurableClass.__name__).split())
        )
        settings = self.prymatex_settings.scope(scope_name, create=True)
        # --------- Register settings values
        for key, value in configurableClass.__dict__.items():
            if isinstance(value, ConfigurableItem):
                if value.name is None:
                    value.name = key
                settings.addItem(value)
            elif isinstance(value, ConfigurableHook):
                settings.addHook(value)
        return settings

    def registerConfigurableInstance(self, configurable):
        settings = configurable.settings()
        settings.addListener(configurable)
        settings.configure(configurable)
        # Register hooks
        for path, hook in settings.hooks().items():
            handler = hook.fset.__get__(
                configurable, configurable.__class__)
            self.registerSettingCallback(path, handler)
            handler(self.settingValue(path))

    def unregisterConfigurableInstance(self, configurable):
        settings = configurable.settings()
        settings.removeListener(configurable)
        # Unregister hooks
        for path, hook in settings.hooks().items():
            self.unregisterSettingCallback(path, hook.fset)

    def restoreApplicationState(self):
        state = json.read_file(self.profile().PMX_STATE_PATH)
        self.application().setComponentState(state or {})

    def settingValue(self, settingPath, default=None):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.scope(name)
        if settings:
            return settings.get(names[-1], default)
        return default

    def registerSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.scope(name)
        if settings:
            settings.add_callback(names[-1], handler)

    def unregisterSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.get(name)
        if settings:
            settings.remove_callback(names[-1], handler)
        
    def clear(self):
        self.prymatex_settings.clear()
