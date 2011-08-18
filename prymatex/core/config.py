#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Application configuration based on Qt's QSettings module.

'''
from PyQt4 import QtCore
from os.path import abspath, expanduser, dirname, exists
import os, plistlib

PRYMATEX_HOME_NAME = ".prymatex"
PRYMATEX_SETTING_NAME = "settings.ini"
TEXTMATE_SETTINGS_NAME = "com.macromates.textmate.plist"
TEXTMATE_WEBPREVIEW_NAME = "com.macromates.textmate.webpreview.plist"
TEXTMATE_PREFERENCE_NAMES = ["Library","Preferences"]

def get_prymatex_base_path():
    return abspath(os.path.join(dirname(__file__), '..'))

def get_prymatex_user_path():
    path = abspath(os.path.join(expanduser("~"), PRYMATEX_HOME_NAME))
    if not exists(path):
        os.makedirs(path)
    #Create extra paths
    bundles = os.path.join(path, 'Bundles')
    if not exists(bundles):
        os.makedirs(bundles, 0700)
    themes = os.path.join(path, 'Themes')
    if not exists(themes):
        os.makedirs(themes, 0700)
    return path

def get_textmate_preferences_user_path():
    path = abspath(os.path.join(expanduser("~"), *TEXTMATE_PREFERENCE_NAMES))
    if not exists(path):
        os.makedirs(path)
    #Create extra files
    webpreview = os.path.join(path, TEXTMATE_WEBPREVIEW_NAME)
    if not exists(webpreview):
        plistlib.writePlist({"SelectedTheme": "bright"}, webpreview)
    return path
    
def build_prymatex_profile(path):
    '''
    @see: PMXObject.pmxApp.getProfilePath(what, file)
    '''
    os.makedirs(path)
    os.makedirs(os.path.join(path, 'tmp'), 0700)
    os.makedirs(os.path.join(path, 'log'), 0700)
    os.makedirs(os.path.join(path, 'var'), 0700)
    
def get_prymatex_profile_path(name, base):
    path = abspath(os.path.join(base, name.lower()))
    if not exists(path):
        build_prymatex_profile(path)
    return path

#Deprecated use qApp.settings
PMX_BASE_PATH = get_prymatex_base_path()
#Cuidado esta la necesita el paquete support en el modulo utils, ver como quitarla igualmente
PMX_SUPPORT_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Support')

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
    '''
    Configuration descriptor
    '''
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
        value = self.value if hasattr(self, 'value') else self.default
        return value
        
    def __set__(self, instance, value):
        self.value = value
        if self.fset != None:
            self.fset(instance, value)

class PMXSettings(object):
    PMX_APP_PATH = get_prymatex_base_path()
    PMX_SHARE_PATH = os.path.join(PMX_APP_PATH, 'share')
    PMX_USER_PATH = get_prymatex_user_path()
    PMX_PREFERENCES_PATH = TM_PREFERENCES_PATH

    def __init__(self, profile_path):
        self.PMX_PROFILE_PATH = profile_path
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_VAR_PATH = os.path.join(self.PMX_PROFILE_PATH, 'var')
        self.GROUPS = {}
        #TODO Defaults settings
        self.qsettings = QtCore.QSettings(os.path.join(profile_path, PRYMATEX_SETTING_NAME), QtCore.QSettings.IniFormat)
        self.tmsettings = TextMateSettings(os.path.join(TM_PREFERENCES_PATH, TEXTMATE_SETTINGS_NAME))
    
    @classmethod
    def getSettingsForProfile(cls, profile):
        return PMXSettings(get_prymatex_profile_path(profile, cls.PMX_USER_PATH))
    
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
        return value

    def sync(self):
        #Save capture values from qt
        for group in self.GROUPS.values():
            group.sync()
        self.qsettings.sync()