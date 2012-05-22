#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
Application configuration based on Qt's QSettings module.
"""
import os, plistlib
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui

try:
    from win32com.shell import shellcon, shell
    USER_HOME_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
except ImportError:
    USER_HOME_PATH = os.path.expanduser("~")

PRYMATEX_HOME_NAME = ".prymatex"
PRYMATEX_SETTING_NAME = "settings.ini"
PRYMATEX_PROFILES_NAME = "profiles.ini"
TEXTMATE_SETTINGS_NAME = "com.macromates.textmate.plist"
TEXTMATE_WEBPREVIEW_NAME = "com.macromates.textmate.webpreview.plist"
TEXTMATE_PREFERENCE_NAMES = ["Library", "Preferences"]

def get_prymatex_app_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_prymatex_home_path():
    path = os.path.join(USER_HOME_PATH, PRYMATEX_HOME_NAME)
    if not os.path.exists(path):
        os.makedirs(path)
    #Create extra paths
    for extra in ['Bundles', 'Themes', 'Plugins']:
        extraPath = os.path.join(path, extra)
        if not os.path.exists(extraPath):
            os.makedirs(extraPath, 0700)
    return path

def get_textmate_preferences_user_path():
    path = os.path.join(USER_HOME_PATH, *TEXTMATE_PREFERENCE_NAMES)
    if not os.path.exists(path):
        os.makedirs(path)
    #Create extra files
    webpreview = os.path.join(path, TEXTMATE_WEBPREVIEW_NAME)
    if not os.path.exists(webpreview):
        plistlib.writePlist({"SelectedTheme": "bright"}, webpreview)
    return path

def build_prymatex_profile(path):
    '''
    @see: PMXObject.pmxApp.getProfilePath(what, file)
    '''
    os.makedirs(path)
    os.makedirs(os.path.join(path, 'tmp'), 0700)
    os.makedirs(os.path.join(path, 'log'), 0700)
    os.makedirs(os.path.join(path, 'cache'), 0700)
    os.makedirs(os.path.join(path, 'screenshot'), 0700)

def get_prymatex_profiles_file(path):
    filePath = os.path.join(path, PRYMATEX_PROFILES_NAME)
    if not os.path.exists(filePath):
        pf = open(filePath, 'w')
        pf.write("\n".join(["[General]", "dontask=True", "", "[Profile0]", "name=default", "path=" + os.path.join(path, "default"), "default=True"]))
        pf.flush()
        pf.close()
    return filePath
    
class TextMateSettings(object):
    def __init__(self, file):
        self.file = file

        if os.path.exists(self.file):
            try:
                self.settings = plistlib.readPlist(self.file)
            except Exception as e:
                print("Exception raised while reading settings file: %s" % e)
        
        not hasattr(self, "settings") and self.initializeSettings()
    
    def initializeSettings(self):
        self.settings = {}
        self.sync()

    def setValue(self, name, value):
        if name in self.settings and self.settings[name] == value:
            return
        self.settings[name] = value
        self.sync()
    
    def value(self, name):
        try:
            return self.settings[name]
        except KeyError:
            return None
    
    def clear(self):
        self.initializeSettings()
        
    def sync(self):
        plistlib.writePlist(self.settings, self.file)

class SettingsGroup(object):
    def __init__(self, name, qsettings, tmsettings):
        self.name = name
        self.listeners = []
        self.settings = {}
        self.qsettings = qsettings
        self.tmsettings = tmsettings
            
    def setValue(self, name, value):
        #TODO: Ver que pasa con las listas
        if name in self.settings:
            self.qsettings.beginGroup(self.name)
            self.qsettings.setValue(name, value)
            self.qsettings.endGroup()
            if self.settings[name].tm_name != None:
                self.tmsettings.setValue(self.settings[name].tm_name, value)
            for listener in self.listeners:
                setattr(listener, name, value)
    
    @staticmethod
    def toPyObject(obj):
        if isinstance(obj, list):
            return [SettingsGroup.toPyObject(o) for o in obj ]
        elif isinstance(obj, dict):
            return dict([(SettingsGroup.toPyObject(o[0]), SettingsGroup.toPyObject(o[1])) for o in obj.iteritems() ])
        else:
            return obj
    
    def value(self, name):
        self.qsettings.beginGroup(self.name)
        value = self.qsettings.value(name)
        self.qsettings.endGroup()
        if value == None and name in self.settings:
            #TODO: ver si tengo que pasarle un objeto
            return self.settings[name].getDefault()
        return SettingsGroup.toPyObject(value)
        
    def hasValue(self, name):
        self.qsettings.beginGroup(self.name)
        value = self.qsettings.value(name)
        self.qsettings.endGroup()
        if value == None and name in self.settings:
            #TODO: ver si tengo que pasarle un objeto
            return True
        else:
            return SettingsGroup.toPyObject(value) is not None
    
    def addSetting(self, setting):
        self.settings[setting.name] = setting
        if setting.tm_name != None and self.tmsettings.value(setting.tm_name) == None:
            self.tmsettings.setValue(setting.tm_name, setting.getDefault())

    def addListener(self, listener):
        self.listeners.append(listener)
    
    def removeListener(self, listener):
        self.listeners.remove(listener)
    
    def configure(self, obj):
        for key, setting in self.settings.iteritems():
            value = self.value(key)
            if value is None:
                value = setting.getDefault(obj)
            else:
                value = setting.toPyType(value)
            setattr(obj, key, value)

    def sync(self):
        for key, setting in self.settings.iteritems():
            if setting.default == None and self.listeners:
                self.qsettings.beginGroup(self.name)
                self.qsettings.setValue(key, setting.getDefault(self.listeners[0]))
                self.qsettings.endGroup()

class pmxConfigPorperty(object):
    """
    Configuration descriptor
    """
    def __init__(self, default = None, fset = None, tm_name = None):
        self.default = default
        self.fset = fset
        self.tm_name = tm_name
    
    def getDefault(self, obj = None):
        if self.default != None:
            return self.default
        elif self.fget != None and obj != None:
            return self.fget(obj)
        raise Exception("No value for %s" % self.name)
    
    def toPyType(self, obj):
        if self.default != None:
            obj_type = type(self.default)
        elif self.fget != None:
            obj_type = type(self.fget(obj))
        return obj_type(obj)

    def __call__(self, function):
        self.fset = function
        return self
        
    def __get__(self, instance, instance_type = None):
        value = self.value if hasattr(self, 'value') else self.default
        return value
        
    def __set__(self, instance, value):
        self.value = value
        if self.fset != None:
            self.fset(instance, value)

class PMXSettings(object):
    PMX_APP_PATH = get_prymatex_app_path()
    PMX_SHARE_PATH = os.path.join(PMX_APP_PATH, 'share')
    PMX_HOME_PATH = get_prymatex_home_path()
    PMX_PLUGINS_PATH = os.path.join(PMX_HOME_PATH, 'Plugins')
    PMX_PROFILES_FILE = get_prymatex_profiles_file(PMX_HOME_PATH)
    USER_HOME_PATH = USER_HOME_PATH
    PMX_PREFERENCES_PATH = get_textmate_preferences_user_path()

    @classmethod
    def get_prymatex_profile_path(cls, name):
        path = os.path.abspath(os.path.join(cls.PMX_HOME_PATH, name.lower()))
        if not os.path.exists(path):
            build_prymatex_profile(path)
        return path
    
    @classmethod
    def defaultProfile(cls):
        config = ConfigParser()
        config.read(cls.PMX_PROFILES_FILE)
        for section in config.sections():
            if section.startswith("Profile"):
                if config.getboolean(section, "default"):
                    return config.get(section, "name")
        return "default"
    
    @classmethod
    def askForProfile(cls):
        config = ConfigParser()
        config.read(cls.PMX_PROFILES_FILE)
        return not config.getboolean("General", "dontask")

    def __init__(self, profile):
        self.PMX_PROFILE_NAME = profile
        self.PMX_PROFILE_PATH = self.get_prymatex_profile_path(profile)
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_CACHE_PATH = os.path.join(self.PMX_PROFILE_PATH, 'cache')
        self.PMX_SCREENSHOT_PATH = os.path.join(self.PMX_PROFILE_PATH, 'screenshot')
        self.GROUPS = {}
        #TODO Defaults settings
        self.qsettings = QtCore.QSettings(os.path.join(self.PMX_PROFILE_PATH, PRYMATEX_SETTING_NAME), QtCore.QSettings.IniFormat)
        self.tmsettings = TextMateSettings(os.path.join(self.PMX_PREFERENCES_PATH, TEXTMATE_SETTINGS_NAME))

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