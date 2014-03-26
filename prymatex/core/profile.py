#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore
from prymatex.utils import json

from prymatex.core.config import (TM_PREFERENCES_PATH,
    PMX_SETTINGS_NAME, PMX_STATE_NAME, TM_SETTINGS_NAME)

from prymatex.core.settings import (TextMateSettings, SettingsGroup,
                                    ConfigurableItem)
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
        return configurableClass.__dict__['SETTINGS_GROUP'] \
            if 'SETTINGS_GROUP' in configurableClass.__dict__ \
            else configurableClass.__name__

    def groupByName(self, name):
        if name not in self.settingsGroups:
            self.settingsGroups[name] = SettingsGroup(
                name,
                self.settings.setdefault(name, {}),
                self.tmsettings)
        return self.settingsGroups[name]

    def groupByClass(self, configurableClass):
        return self.groupByName(self.__group_name(configurableClass))

    def registerConfigurable(self, configurableClass):
        # Prepare class group
        # TODO: Una forma de obtener y setear los valores en las settings
        # Las configurableClass tiene que tener esos metodos
        configurableClass._settings = self.groupByClass(configurableClass)
        # Prepare configurable attributes
        for key, value in configurableClass.__dict__.items():
            if isinstance(value, ConfigurableItem):
                if value.name is None:
                    value.name = key
                configurableClass._settings.addConfigurableItem(value)

    def configure(self, component):
        settingsGroup = self.groupByClass(component.__class__)
        settingsGroup.addListener(component)
        settingsGroup.configure(component)

    def saveState(self, component):
        self.state[component.objectName()] = component.componentState()

    def restoreState(self, component):
        componentState = self.state.get(component.objectName())
        if componentState is not None:
            component.setComponentState(componentState)

    def setValue(self, name, value):
        self.settings[name] = value

    def value(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return self.settings.get(name, default)

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
