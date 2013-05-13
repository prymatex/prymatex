#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, shutil

from prymatex.qt import QtCore

from prymatex.core.config import (  PMX_APP_PATH,
                                    get_textmate_preferences_user_path)

from prymatex.core.settings import (TextMateSettings,
                                    SettingsGroup,
                                    pmxConfigPorperty)

PRYMATEX_SETTINGS_NAME = "settings.ini"
PRYMATEX_STATE_NAME = "state.ini"
TEXTMATE_SETTINGS_NAME = "com.macromates.textmate.plist"

class PMXProfile(object):
    PMX_SETTING_NAME = PRYMATEX_SETTINGS_NAME
    PMX_STATE_NAME = PRYMATEX_STATE_NAME
    TM_SETTINGS_NAME = TEXTMATE_SETTINGS_NAME
    PMX_PREFERENCES_PATH = get_textmate_preferences_user_path()

    def __init__(self, name, path, default = True):
        self.PMX_PROFILE_NAME = name
        self.PMX_PROFILE_PATH = path
        self.PMX_PROFILE_DEFAULT = default
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_CACHE_PATH = os.path.join(self.PMX_PROFILE_PATH, 'cache')
        self.PMX_SCREENSHOT_PATH = os.path.join(self.PMX_PROFILE_PATH, 'screenshot')
        self.GROUPS = {}
        self.qsettings = QtCore.QSettings(os.path.join(self.PMX_PROFILE_PATH, self.PMX_SETTING_NAME), QtCore.QSettings.IniFormat)
        self.tmsettings = TextMateSettings(os.path.join(self.PMX_PREFERENCES_PATH, self.TM_SETTINGS_NAME))
        self.state = QtCore.QSettings(os.path.join(self.PMX_PROFILE_PATH, self.PMX_STATE_NAME), QtCore.QSettings.IniFormat)

    # ------------------------ Setting Groups
    def __group_name(self, configurableClass):
        if hasattr(configurableClass, 'settings'):
            return configurableClass.settings.groupName()
        return configurableClass.__dict__['SETTINGS_GROUP'] if 'SETTINGS_GROUP' in configurableClass.__dict__ else configurableClass.__name__

    def groupByName(self, name):
        if name not in self.GROUPS:
            self.GROUPS[name] = SettingsGroup(name, self.qsettings, self.tmsettings)
        return self.GROUPS[name]

    
    def groupByClass(self, configurableClass):
        return self.groupByName(self.__group_name(configurableClass))

    def registerConfigurable(self, configurableClass):
        # Prepare class group
        configurableClass.settings = self.groupByClass(configurableClass)
        # Prepare configurable attributes
        for key, value in configurableClass.__dict__.items():
            if isinstance(value, pmxConfigPorperty):
                # TODO: Migrar a un sistema de nombres explicito
                value.name = key
                configurableClass.settings.addSetting(value)

    def saveState(self, component):
        self.state.setValue(component.objectName(), component.saveState())
        self.state.sync()

    def restoreState(self, component):
        state = self.state.value(component.objectName())
        if state:
            component.restoreState(state)

    def setValue(self, name, value):
        self.qsettings.setValue(name, value)

    def value(self, name, default = None):
        if hasattr(self, name):
            return getattr(self, name)
        return self.qsettings.value(name, default)

    def clear(self):
        self.qsettings.clear()
        
    def sync(self):
        #Save capture values from qt
        for group in list(self.GROUPS.values()):
            group.sync()
        self.qsettings.sync()
