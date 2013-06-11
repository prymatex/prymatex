#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, plistlib


class TextMateSettings(object):
    def __init__(self, file):
        self.file = file

        if os.path.exists(self.file):
            try:
                self.settings = plistlib.readPlist(self.file)
            except Exception as e:
                print(("Exception raised while reading settings file: %s" % e))
        
        not hasattr(self, "settings") and self.initializeSettings()


    def initializeSettings(self):
        self.settings = {}
        self.sync()


    def setValue(self, name, value):
        if name in self.settings and self.settings[name] == value:
            return
        self.settings[name] = value
        self.sync()


    def value(self, name, default = None):
        try:
            return self.settings[name]
        except KeyError:
            return default


    def clear(self):
        self.initializeSettings()


    def sync(self):
        plistlib.writePlist(self.settings, self.file)


class SettingsGroup(object):
    def __init__(self, name, qsettings, tmsettings):
        self.__groupName = name
        self.qsettings = qsettings
        self.tmsettings = tmsettings
        # Listener classes
        self.listeners = []
        # Setting attrs
        self.settings = {}
        # Hooks
        self.hooks = {}
        # Dialogs
        self.dialogs = []


    def groupName(self):
        return self.__groupName


    def setValue(self, name, value):
        setting = self.settings.get(name)
        if setting:
            self.qsettings.beginGroup(self.__groupName)
            self.qsettings.setValue(name, value)
            self.qsettings.endGroup()
            if setting.tm_name != None:
                self.tmsettings.setValue(setting.tm_name, value)
            for listener in self.listeners:
                setattr(listener, name, value)
            for hookFunction in self.hooks.get(name, []):
                hookFunction(value)


    def value(self, name, default = None):
        setting = self.settings.get(name)
        if setting:
            self.qsettings.beginGroup(self.__groupName)
            value = self.qsettings.value(name, default)
            self.qsettings.endGroup()
            if value is None:
                return self.settings[name].getDefault()
            return setting.toPython(value)


    def hasValue(self, name):
        self.qsettings.beginGroup(self.__groupName)
        value = self.qsettings.value(name)
        self.qsettings.endGroup()
        return name in self.settings and value is not None


    def addSetting(self, setting):
        self.settings[setting.name] = setting
        if setting.tm_name != None and self.tmsettings.value(setting.tm_name) == None:
            self.tmsettings.setValue(setting.tm_name, setting.getDefault())


    def addListener(self, listener):
        self.listeners.append(listener)

    
    def removeListener(self, listener):
        self.listeners.remove(listener)

    def addHook(self, name, handler):
        hooks = self.hooks.setdefault(name, [])
        if handler not in hooks:
            hooks.append(handler)

    def removeHook(self, name, handler):
        hooks = self.hooks.setdefault(name, [])
        if handler in hooks:
            hooks.remove(handler)

    def addDialog(self, dialog):
        self.dialogs.append(dialog)


    def configure(self, obj):
        for key, setting in self.settings.items():
            value = self.value(key)
            if value is None:
                value = setting.getDefault()
            else:
                value = setting.toPython(value)
            if value is not None:
                setattr(obj, key, value)


    def sync(self):
        for key, setting in self.settings.items():
            if setting.default == None and self.listeners:
                self.qsettings.beginGroup(self.__groupName)
                self.qsettings.setValue(key, setting.getDefault())
                self.qsettings.endGroup()


class pmxConfigPorperty(object):
    """Configuration descriptor"""
    def __init__(self, valueType = None, default = None, fset = None, tm_name = None):
        assert valueType is not None or default is not None, "Not type and not default value"
        self.default = default
        self.valueType = valueType if valueType is not None else type(default)
        self.fset = fset
        self.tm_name = tm_name

    def getDefault(self):
        return self.default


    def toPython(self, value):
        if self.valueType == bool and isinstance(value, str):
            return value.lower() not in ('false', '0')
        else:
            return self.valueType(value)
    
    def __call__(self, function):
        self.fset = function
        return self


    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.value if hasattr(self, 'value') else self.default

    def __set__(self, obj, value):
        self.value = value
        if self.fset is not None:
            self.fset(obj, value)
