#!/usr/bin/env python

from prymatex.qt import QtCore

from prymatex.core.components import PrymatexComponent 
from prymatex.core.settings import (TextMateSettings, PrymatexSettings,
                                    ConfigurableItem, ConfigurableHook)
                                    
from prymatex.utils import text as textutils
from prymatex.utils import json
from prymatex.utils import plist

from prymatex.models.settings import SettingsTreeModel
from prymatex.models.settings import SortFilterSettingsProxyModel

class SettingsManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(SettingsManager, self).__init__(**kwargs)
        
        # Textmate Settings
        tm = plist.readPlist(self.profile().TM_PREFERENCES_PATH)
        self.textmate_settings = TextMateSettings('tm', tm or {})

        # Prymatex Settings
        settings = json.read_file(self.profile().PMX_SETTINGS_PATH)
        self.prymatex_settings = PrymatexSettings('settings', settings or {})
        self.prymatex_settings.setTm(self.textmate_settings)

        # Prymatex state
        state = json.read_file(self.profile().PMX_STATE_PATH)
        self.state = PrymatexSettings('state', state or {})

        # Settings Models
        self.settingsTreeModel = SettingsTreeModel(parent=self)
        self.sortFilterSettingsProxyModel = SortFilterSettingsProxyModel(parent=self)
        self.sortFilterSettingsProxyModel.setSourceModel(self.settingsTreeModel)
                
        self.application().aboutToQuit.connect(self.on_application_aboutToQuit)
        # Reload settings
        #notifier.watch(self.PMX_SETTINGS_PATH, notifier.CHANGED, self.reload_settings)

    # ------------------- Signals
    def on_application_aboutToQuit(self):
        # Save state
        self.saveState(self.application())
        plist.writePlist(self.textmate_settings, self.profile().TM_PREFERENCES_PATH)
        # Save settings
        self.prymatex_settings.purge()
        json.write_file(self.prymatex_settings, self.profile().PMX_SETTINGS_PATH)
        # Save state
        self.state.purge()
        json.write_file(self.state, self.profile().PMX_STATE_PATH)

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
    def reload_settings(self, path, changes):
        settings = json.read_file(path)
        if settings:
            self.prymatex_settings.reload(settings)
        
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
        
    def saveState(self, configurable):
        self.state[configurable.objectName()] = configurable.componentState()

    def restoreState(self, configurable):
        componentState = self.state.get(configurable.objectName())
        if componentState is not None:
            configurable.setComponentState(componentState)

    def settingValue(self, settingPath):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.scope(name)
        return settings.get(names[-1])

    def registerSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.scope(name)
        settings.add_callback(names[-1], handler)

    def unregisterSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.prymatex_settings
        for name in names[:-1]:
            settings = settings.get(name)
        settings.remove_callback(names[-1], handler)
        
    def clear(self):
        self.prymatex_settings.clear()
