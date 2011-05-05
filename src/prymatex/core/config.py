#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Application configuration based on Qt's QSettings module.

'''

from PyQt4.Qt import QSettings
from os.path import join, abspath, expanduser, dirname, exists
from os import makedirs
import plistlib
from prymatex.lib import deco

PRYMATEX_HOME_NAME = ".prymatex"
PRYMATEX_SETTING_NAME = "settings.ini"
TEXTMATE_SETTINGS_NAME = "com.macromates.textmate.plist"
TEXTMATE_WEBPREVIEW_NAME = "com.macromates.textmate.webpreview.plist"
TEXTMATE_PREFERENCE_NAMES = ["Library","Preferences"]

def get_prymatex_base_path():
    return abspath(join(dirname(__file__), '..'))

def get_prymatex_user_path():
    path = abspath(join(expanduser("~"), PRYMATEX_HOME_NAME))
    if not exists(path):
        makedirs(path)
    return path

def get_textmate_preferences_user_path():
    path = abspath(join(expanduser("~"), *TEXTMATE_PREFERENCE_NAMES))
    if not exists(path):
        makedirs(path)
    #create extra files
    webpreview = join(path, TEXTMATE_WEBPREVIEW_NAME)
    if not exists(webpreview):
        plistlib.writePlist({"SelectedTheme": "bright"}, webpreview)
    return path
    
def build_prymatex_profile(path):
    '''
    @see: PMXObject.pmxApp.getProfilePath(what, file)
    '''
    makedirs(path)
    makedirs(join(path, 'tmp'))
    makedirs(join(path, 'log'))
    makedirs(join(path, 'var'))
    
@deco.printparams_and_output
def get_prymatex_profile_path(name, base):
    path = abspath(join(base, name.lower()))
    if not exists(path):
        build_prymatex_profile(path)
    return path

#Deprecated use qApp.settings
PMX_BASE_PATH = get_prymatex_base_path()
PMX_USER_PATH = get_prymatex_user_path()
PMX_APP_PATH = PMX_BASE_PATH
PMX_BUNDLES_PATH = join(PMX_BASE_PATH, 'share', 'Bundles')
PMX_THEMES_PATH = join(PMX_BASE_PATH, 'share', 'Themes')
PMX_SUPPORT_PATH = join(PMX_BASE_PATH, 'share', 'Support')

TM_PREFERENCES_PATH = get_textmate_preferences_user_path()

class TextMateSettings(object):
    def __init__(self, file):
        self.file = file
        if exists(self.file):
            self.settings = plistlib.readPlist(self.file)
        else:
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
        if name in self.settings:
            self.qsettings.beginGroup(self.name)
            self.qsettings.setValue(name, value)
            self.qsettings.endGroup()
            if self.settings[name].tm_name != None:
                self.tmsettings.setValue(self.settings[name].tm_name, value)
            for listener in self.listeners:
                setattr(listener, name, value)
    
    def value(self, name):
        self.qsettings.beginGroup(self.name)
        value = self.qsettings.value(name)
        self.qsettings.endGroup()
        return value.toPyObject()
        
    def addSetting(self, setting):
        self.settings[setting.name] = setting
        if setting.tm_name != None and self.tmsettings.value(setting.tm_name) == None:
            self.tmsettings.setValue(setting.tm_name, setting.getDefault())

    def addListener(self, listener):
        self.listeners.append(listener)
    
    def configure(self, obj):
        for key, setting in self.settings.iteritems():
            value = self.value(key)
            if not value:
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
        
    def contributeToClass(self, cls, name):
        self.name = name
        self.fget = getattr(cls, name, None)
        if self.fset == None:
            self.fset = getattr(cls, "set" + name.title(), None)
        cls._meta.settings.addSetting(self)
        setattr(cls, name, self)
    
    def __call__(self, function):
        self.name = function.__name__
        self.fset = function
        return self
        
    def __get__(self, instance, instance_type = None):
        return hasattr(self, 'value') and self.value or self.default
        
    def __set__(self, instance, value):
        self.value = value
        if self.fset != None:
            self.fset(instance, value)

class PMXSettings(object):
    PMX_APP_PATH = get_prymatex_base_path()
    PMX_USER_PATH = get_prymatex_user_path()
    PMX_PREFERENCES_PATH = TM_PREFERENCES_PATH
    PMX_BUNDLES_PATH = join(PMX_APP_PATH, 'share', 'Bundles')
    PMX_THEMES_PATH = join(PMX_APP_PATH, 'share', 'Themes')
    PMX_SUPPORT_PATH = join(PMX_APP_PATH, 'share', 'Support')
    #Profile
    PMX_PROFILE_PATH = None
    PMX_TMP_PATH = None
    PMX_LOG_PATH = None
    GROUPS = {}
    def __init__(self, profile_path):
        self.qsettings = QSettings(join(profile_path, PRYMATEX_SETTING_NAME), QSettings.IniFormat)
        self.tmsettings = TextMateSettings(join(TM_PREFERENCES_PATH, TEXTMATE_SETTINGS_NAME))
    
    @classmethod
    def getSettingsForProfile(cls, profile):
        cls.PMX_PROFILE_PATH = get_prymatex_profile_path(profile, cls.PMX_USER_PATH)
        cls.PMX_TMP_PATH = join(cls.PMX_PROFILE_PATH, 'tmp')
        cls.PMX_LOG_PATH = join(cls.PMX_PROFILE_PATH, 'log')
        return cls(cls.PMX_PROFILE_PATH)
    
    def getGroup(self, name):
        if name not in self.GROUPS:
            self.GROUPS[name] = SettingsGroup(name, self.qsettings, self.tmsettings)
        return self.GROUPS[name]
    
    def setValue(self, name, value):
        self.qsettings.setValue(name, value)
    
    def value(self, name):
        #FIXME keys for class values
        if name in self.__class__.__dict__:
            return self.__class__.__dict__[name]
        value = self.qsettings.value(name)
        return value.toPyObject()

    def sync(self):
        #Save capture values from qt
        for group in self.GROUPS.values():
            group.sync()
        self.qsettings.sync()