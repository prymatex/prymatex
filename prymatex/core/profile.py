#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore
from prymatex.utils import json

from prymatex.core.config import (TM_PREFERENCES_PATH,
    PMX_SETTINGS_NAME, PMX_STATE_NAME, TM_SETTINGS_NAME)

from prymatex.core.settings import (TextMateSettings, SettingsGroup,
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

        self.settings = json.read_file(self.PMX_SETTINGS_PATH) or {}
        self.state = json.read_file(self.PMX_STATE_PATH) or {}

        self.settingsGroups = {}

        self.tmsettings = TextMateSettings(
            os.path.join(TM_PREFERENCES_PATH, TM_SETTINGS_NAME))

    # ------------------------ Setting Groups
    def __group_name(self, configurableClass):
        if hasattr(configurableClass, '_settings'):
            return configurableClass._settings.groupName()
        return getattr(configurableClass, 'SETTINGS', configurableClass.__name__)

    def groupByName(self, name):
        if name not in self.settingsGroups:
            self.settingsGroups[name] = SettingsGroup(
                name,
                self.settings.setdefault(name, {}),
                self.tmsettings)
        return self.settingsGroups[name]

    def settingsForClass(self, configurableClass):
        return self.groupByName(self.__group_name(configurableClass))

    def registerConfigurableInstance(self, configurable):
        settingsGroup = configurable.settings()
        settingsGroup.addListener(configurable)
        settingsGroup.configure(configurable)
        # Register hooks
        for path, hook in settingsGroup.configurableHooks.items():
            handler = hook.fset.__get__(
                configurable, configurable.__class__)
            self.registerSettingHook(path, handler)
            handler(self.settingValue(path))

    def unregisterConfigurableInstance(self, configurable):
        settingsGroup = configurable.settings()
        settingsGroup.removeListener(configurable)
        # Unregister hooks
        for path, hook in settingsGroup.configurableHooks.items():
            self.unregisterSettingHook(path, hook.fset)
        
    def saveState(self, configurable):
        self.state[configurable.objectName()] = configurable.componentState()

    def restoreState(self, configurable):
        componentState = self.state.get(configurable.objectName())
        if componentState is not None:
            configurable.setComponentState(componentState)

    def setValue(self, name, value):
        self.settings[name] = value

    def value(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return self.settings.get(name, default)

    # -------------- Hooks
    def settingValue(self, settingPath):
        groupName, settingName = settingPath.split(".")
        return self.groupByName(groupName).value(settingName)

    def registerSettingHook(self, settingPath, handler):
        groupName, settingName = settingPath.split(".")
        group = self.groupByName(groupName)
        group.addHook(settingName, handler)

    def unregisterSettingHook(self, settingPath, handler):
        groupName, settingName = settingPath.split(".")
        group = self.groupByName(groupName)
        group.removeHook(settingName, handler)
        
    def clear(self):
        self.settings.clear()

    def sync(self):
        #Save capture values from qt
        for group in self.settingsGroups.values():
            groupName = group.groupName()
            if not self.settings[groupName]:
                self.settings.pop(groupName)
        json.write_file(self.settings, self.PMX_SETTINGS_PATH)
        json.write_file(self.state, self.PMX_STATE_PATH)
