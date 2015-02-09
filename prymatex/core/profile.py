#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore
from prymatex.utils import json, plist

from . import notifier

from prymatex.core.config import (TM_PREFERENCES_PATH,
    PMX_SETTINGS_NAME, PMX_STATE_NAME, TM_SETTINGS_NAME)

from prymatex.core.settings import (TextMateSettings, PrymatexSettings,
                                    ConfigurableItem, ConfigurableHook)
class PrymatexProfile(object):
    def __init__(self, name, path, default=True):
        self.PMX_PROFILE_NAME = name
        self.PMX_PROFILE_PATH = path
        self.PMX_PROFILE_DEFAULT = default
        self.PMX_SETTINGS_PATH = os.path.join(self.PMX_PROFILE_PATH, PMX_SETTINGS_NAME)
        self.PMX_STATE_PATH = os.path.join(self.PMX_PROFILE_PATH, PMX_STATE_NAME)
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_CACHE_PATH = os.path.join(self.PMX_PROFILE_PATH, 'cache')
        self.PMX_SCREENSHOT_PATH = os.path.join(self.PMX_PROFILE_PATH, 'screenshot')
        self.TM_PREFERENCES_PATH = os.path.join(TM_PREFERENCES_PATH, TM_SETTINGS_NAME)
        
        tm = {}
        try:
            tm = plist.readPlist(self.TM_PREFERENCES_PATH)
        except Exception as e:
            print(("Exception raised while reading settings file: %s" % e))
        self.tmsettings = TextMateSettings('tm', tm)

        settings = json.read_file(self.PMX_SETTINGS_PATH)
        self.settings = PrymatexSettings('settings', settings)
        self.settings.setTm(self.tmsettings)
        # Reload settings
        notifier.watch(self.PMX_SETTINGS_PATH, notifier.CHANGED, self.reload_settings)

        state = json.read_file(self.PMX_STATE_PATH)
        self.state = PrymatexSettings('state', state)

    # ------------------------ Paths
    def ensure_paths(self):
        new_paths = filter(lambda p: not os.path.exists(p), (self.PMX_PROFILE_PATH, 
            self.PMX_TMP_PATH, self.PMX_LOG_PATH, self.PMX_CACHE_PATH, self.PMX_SCREENSHOT_PATH))
        for new_path in new_paths:
            os.makedirs(new_path, 0o700)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return self.settings.get(name, default)

    # ------------------------ Setting
    def reload_settings(self, path, changes):
        settings = json.read_file(path)
        if settings:
            self.settings.reload(settings)
        
    def settingsForClass(self, configurableClass):
        name = configurableClass._settings.name() \
            if configurableClass._settings is not None else \
            getattr(configurableClass, 'SETTINGS', configurableClass.__name__)
        settings = self.settings.scope(name)
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
        settings = self.settings
        for name in names[:-1]:
            settings = settings.get(name)
        return settings.get(names[-1])

    def registerSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.settings
        for name in names[:-1]:
            settings = settings.get(name)
        settings.add_callback(names[-1], handler)

    def unregisterSettingCallback(self, settingPath, handler):
        names = settingPath.split(".")
        settings = self.settings
        for name in names[:-1]:
            settings = settings.get(name)
        settings.remove_callback(names[-1], handler)
        
    def clear(self):
        self.settings.clear()

    def sync(self):
        #Save capture values from qt
        plist.writePlist(self.tmsettings, self.TM_PREFERENCES_PATH)
        self.settings.purge()
        json.write_file(self.settings, self.PMX_SETTINGS_PATH)
        self.state.purge()
        json.write_file(self.state, self.PMX_STATE_PATH)
