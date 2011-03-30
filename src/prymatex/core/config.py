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
PMX_APP_PATH = PMX_BASE_PATH = PMX_BASE_PATH
PMX_BUNDLES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Bundles')
PMX_THEMES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Themes')
PMX_SUPPORT_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Support')

settings = QSettings(os.path.join(PMX_USER_PATH, 'settings.ini'), QSettings.IniFormat)
    
class SettingsGroup(object):
    def __init__(self, name):
        self.name = name
        self.listeners = []
        self.settings = {}
    
    def sync(self):
        settings.sync()
        
    def setValue(self, name, value):
        settings.beginGroup(self.name)
        settings.setValue(name, value)
        settings.endGroup()
    
    def addSetting(self, setting):
        self.settings[setting.name] = setting
        
    def addListener(self, listener):
        self.listeners.append(listener)
    
    def configure(self, obj):
        for key, setting in self.settings.iteritems():
            value = setting.__get__(obj)
            setattr(obj, key, value)
        
class Setting(object):
    def __init__(self, default = None):
        self.__default = default
        
    def contributeToClass(self, cls, name):
        self.name = name
        self.__fget = getattr(cls, name, None)
        self.__fset = getattr(cls, "set" + name.title(), None)
        cls._meta.settings.addSetting(self)
        setattr(cls, name, self)
        
    def __get__(self, instance, instance_type = None):
        if self.__fget != None and self.__default == None:
            return self.__fget(instance)
        return self.__default
        
    def __set__(self, instance, value):
        if self.__fset != None:
            self.__fset(instance, value)