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
