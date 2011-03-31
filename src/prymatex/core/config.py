#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from PyQt4.Qt import QSettings
import os

def get_prymatex_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_prymatex_user_path():
    path = os.path.join(os.path.expanduser("~"), ".prymatex")
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.abspath(path)

PMX_BASE_PATH = get_prymatex_base_path()
PMX_USER_PATH = get_prymatex_user_path()
PMX_APP_PATH = PMX_BASE_PATH
PMX_BUNDLES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Bundles')
PMX_THEMES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Themes')
PMX_SUPPORT_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Support')

class SettingsGroup(object):
    def __init__(self, name, qsettings):
        self.name = name
        self.listeners = []
        self.settings = {}
        self.qsettings = qsettings
            
    def setValue(self, name, value):
        self.qsettings.beginGroup(self.name)
        self.qsettings.setValue(name, value)
        self.qsettings.endGroup()
        for listener in self.listeners:
            setattr(listener, name, value)
    
    def value(self, name):
        self.qsettings.beginGroup(self.name)
        value = self.qsettings.value(name)
        self.qsettings.endGroup()
        return value.toPyObject()
        
    def addSetting(self, setting):
        self.settings[setting.name] = setting
        
    def addListener(self, listener):
        self.listeners.append(listener)
    
    def configure(self, obj):
        for key, setting in self.settings.iteritems():
            value = self.value(key)
            if not value:
                if setting.fget != None and setting.default == None:
                    value = setting.fget(obj)
                elif setting.default != None:
                    value = setting.default
            else:
                if setting.default != None:
                    value = type(setting.default)(value)
            setattr(obj, key, value)

    def sync(self):
        for key, setting in self.settings.iteritems():
            if setting.default == None and self.listeners:
                self.qsettings.beginGroup(self.name)
                self.qsettings.setValue(key, setting.__get__(self.listeners[0]))
                self.qsettings.endGroup()
                
class Setting(object):
    def __init__(self, default = None):
        self.default = default
        self.value = None
        
    def contributeToClass(self, cls, name):
        self.name = name
        self.fget = getattr(cls, name, None)
        self.fset = getattr(cls, "set" + name.title(), None)
        if self.default == None and self.fget == None:
            raise Exception("Value?")
        cls._meta.settings.addSetting(self)
        setattr(cls, name, self)
    
    def __get__(self, instance, instance_type = None):
        return self.value
        
    def __set__(self, instance, value):
        self.value = value
        if self.fset != None:
            self.fset(instance, value)
            
class PMXSettings(object):
    GROUPS = {}
    def __init__(self, profile):
        self.qsettings = QSettings(os.path.join(PMX_USER_PATH, 'settings.ini'), QSettings.IniFormat)
    
    def getGroup(self, name):
        if name not in self.GROUPS:
            self.GROUPS[name] = SettingsGroup(name, self.qsettings)
        return self.GROUPS[name]
    
    def setValue(self, name, value):
        self.qsettings.setValue(name, value)
    
    def value(self, name):
        value = self.qsettings.value(name)
        return value.toPyObject()

    def sync(self):
        #Save capture values from qt
        for group in self.GROUPS.values():
            group.sync()
        self.qsettings.sync()