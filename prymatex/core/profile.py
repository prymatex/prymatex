#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, shutil
from ConfigParser import ConfigParser

from prymatex.qt import QtCore

from prymatex.core.config import (  get_prymatex_app_path,
                                    get_prymatex_home_path,
                                    get_textmate_preferences_user_path)

from prymatex.core.settings import (TextMateSettings,
                                    SettingsGroup,
                                    pmxConfigPorperty)

PRYMATEX_SETTINGS_NAME = "settings.ini"
PRYMATEX_PROFILES_NAME = "profiles.ini"
PRYMATEX_STATE_NAME = "state.ini"
TEXTMATE_SETTINGS_NAME = "com.macromates.textmate.plist"

def build_prymatex_profile(path):
    '''
    @see: PMXObject.pmxApp.getProfilePath(what, file)
    '''
    os.makedirs(path)
    os.makedirs(os.path.join(path, 'tmp'), 0700)
    os.makedirs(os.path.join(path, 'log'), 0700)
    os.makedirs(os.path.join(path, 'cache'), 0700)
    os.makedirs(os.path.join(path, 'screenshot'), 0700)

class PMXProfile(object):
    PMX_SETTING_NAME = PRYMATEX_SETTINGS_NAME
    PMX_STATE_NAME = PRYMATEX_STATE_NAME
    TM_SETTINGS_NAME = TEXTMATE_SETTINGS_NAME
    PMX_APP_PATH = get_prymatex_app_path()
    PMX_SHARE_PATH = os.path.join(PMX_APP_PATH, 'share')
    PMX_HOME_PATH = get_prymatex_home_path()
    PMX_PLUGINS_PATH = os.path.join(PMX_HOME_PATH, 'Plugins')
    PMX_PREFERENCES_PATH = get_textmate_preferences_user_path()
    # Profiles
    PMX_PROFILES_FILE = os.path.join(PMX_HOME_PATH, PRYMATEX_PROFILES_NAME)
    PMX_PROFILES = {}
    PMX_PROFILE_DEFAULT = None
    PMX_PROFILES_DONTASK = True
    
    # ===================
    # = Profile methods =
    # ===================
    @classmethod
    def get_or_create_profile(cls, name, path = None):
        name = name.lower()
        if name in cls.PMX_PROFILES:
            return cls.PMX_PROFILES[name], False
        path = path if path is not None else os.path.abspath(os.path.join(cls.PMX_HOME_PATH, name))
        profile = { "name": name, "path": path, "default": True }
        if not os.path.exists(path):
            build_prymatex_profile(path)
        cls.PMX_PROFILES[name] = profile 
        cls.saveProfiles()
        return profile, True

    @classmethod
    def saveProfiles(cls):
        config = ConfigParser()
        config.add_section("General")
        config.set("General", "dontask", str(cls.PMX_PROFILES_DONTASK))
        for index, profile in enumerate(cls.PMX_PROFILES.values()):
            section = "Profile%d" % index
            config.add_section(section)
            for key, value in profile.iteritems():
                config.set(section, key, str(value))
        f = open(cls.PMX_PROFILES_FILE, "w")
        config.write(f)
        f.close()

    @classmethod
    def createProfile(cls, name):
        profile, created = cls.get_or_create_profile(name)
        return profile["name"]
    
    @classmethod
    def renameProfile(cls, oldName, newName):
        newName = newName.lower()
        profile = PMXProfile.PMX_PROFILES.pop(oldName)
        profile["name"] = newName.lower()
        PMXProfile.PMX_PROFILES[profile["name"]] = profile
        cls.saveProfiles()
        return newName

    @classmethod
    def deleteProfile(cls, name, files = False):
        profile = PMXProfile.PMX_PROFILES.pop(name)
        if files:
            shutil.rmtree(profile["path"])
        cls.saveProfiles()

    def __init__(self, name):
        profile, created = self.get_or_create_profile(name)
        self.PMX_PROFILE_NAME = profile["name"]
        self.PMX_PROFILE_PATH = profile["path"]
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_CACHE_PATH = os.path.join(self.PMX_PROFILE_PATH, 'cache')
        self.PMX_SCREENSHOT_PATH = os.path.join(self.PMX_PROFILE_PATH, 'screenshot')
        self.GROUPS = {}
        self.qsettings = QtCore.QSettings(os.path.join(self.PMX_PROFILE_PATH, self.PMX_SETTING_NAME), QtCore.QSettings.IniFormat)
        self.tmsettings = TextMateSettings(os.path.join(self.PMX_PREFERENCES_PATH, self.TM_SETTINGS_NAME))
        self.state = QtCore.QSettings(os.path.join(self.PMX_PROFILE_PATH, self.PMX_STATE_NAME), QtCore.QSettings.IniFormat)

    def getGroup(self, name):
        if name not in self.GROUPS:
            self.GROUPS[name] = SettingsGroup(name, self.qsettings, self.tmsettings)
        return self.GROUPS[name]
    
    def registerConfigurable(self, configurableClass):
        #Prepare class group
        groupName = configurableClass.__dict__['SETTINGS_GROUP'] if 'SETTINGS_GROUP' in configurableClass.__dict__ else configurableClass.__name__
        configurableClass.settings = self.getGroup(groupName)
        #Prepare configurable attributes
        for key, value in configurableClass.__dict__.iteritems():
            if isinstance(value, pmxConfigPorperty):
                value.name = key
                configurableClass.settings.addSetting(value)
        
    def configure(self, configurableInstance):
        configurableInstance.settings.addListener(configurableInstance)
        configurableInstance.settings.configure(configurableInstance)

    def saveState(self, component):
        self.state.setValue(component.objectName(), component.saveState())
        self.state.sync()

    def restoreState(self, component):
        state = self.state.value(component.objectName())
        if state:
            component.restoreState(state)
        
    def setValue(self, name, value):
        self.qsettings.setValue(name, value)
    
    def value(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        value = self.qsettings.value(name)
        return value

    def clear(self):
        self.qsettings.clear()
        
    def sync(self):
        #Save capture values from qt
        for group in self.GROUPS.values():
            group.sync()
        self.qsettings.sync()
        
# ============
# = Profiles =
# ============
def load_prymatex_profiles():
    """docstring for load_prymatex_profiles"""
    config = ConfigParser()
    if os.path.exists(PMXProfile.PMX_PROFILES_FILE):
        config.read(PMXProfile.PMX_PROFILES_FILE)
        for section in config.sections():
            if section.startswith("Profile"):
                profile = { "name": config.get(section, "name"),
                            "path": config.get(section, "path"),
                            "default": config.getboolean(section, "default")}
                if profile["default"]:
                    PMXProfile.PMX_PROFILE_DEFAULT = profile["name"]
                PMXProfile.PMX_PROFILES[profile["name"]] = profile
        PMXProfile.PMX_PROFILES_DONTASK = config.getboolean("General", "dontask")
    else:
        PMXProfile.PMX_PROFILE_DEFAULT = "default"
        PMXProfile.PMX_PROFILES_DONTASK = True
        PMXProfile.PMX_PROFILES = {}

load_prymatex_profiles()