#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.utils import plist

class TextMateSettings(object):
    def __init__(self, file):
        self.file = file

        if os.path.exists(self.file):
            try:
                self.settings = plist.readPlist(self.file)
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
        plist.writePlist(self.settings, self.file)

class SettingsGroup(object):
    def __init__(self, name, settings, tmsettings):
        self.__groupName = name
        self.settings = settings
        self.tmsettings = tmsettings
        # Listener classes
        self.listeners = set()
        # Setting attrs
        self.configurableItems = {}
        # Setting hooks
        self.configurableHooks = {}
        # Hooks
        self.hooks = {}
        
    def groupName(self):
        return self.__groupName

    def default(self, name):
        return self.configurableItems.get(name).getDefault()

    def setValue(self, name, value):
        item = self.configurableItems.get(name)
        if item:
            # If default value then pop from settings
            if name in self.settings and value == item.getDefault():
                self.settings.pop(name)
            else:
                self.settings[name] = value
            if item.tm_name is not None:
                self.tmsettings.setValue(item.tm_name, value)
            for listener in self.listeners:
                setattr(listener, name, value)
            for hookFunction in self.hooks.get(name, []):
                hookFunction(value)

    def value(self, name, default = None):
        value = self.settings.get(name, default)
        if value is None and name in self.configurableItems:
            value = self.configurableItems.get(name).getDefault()
        return value
	
    def hasValue(self, name):
        value = self.settings.get(name)
        return name in self.configurableItems and value is not None

    def addConfigurableItem(self, item):
        self.configurableItems[item.name] = item
        if item.tm_name is not None and self.tmsettings.value(item.tm_name) is None:
            self.tmsettings.setValue(item.tm_name, item.getDefault())
        
    def addConfigurableHook(self, hook):
        self.configurableHooks[hook.path] = hook

    def addListener(self, listener):
        self.listeners.add(listener)

    def removeListener(self, listener):
        self.listeners.remove(listener)

    def addHook(self, name, handler):
        # Add hook
        hooks = self.hooks.setdefault(name, [])
        if handler not in hooks:
            hooks.append(handler)

    def removeHook(self, name, handler):
        hooks = self.hooks.setdefault(name, [])
        if handler in hooks:
            hooks.remove(handler)

    def configure(self, obj):
        for name, item in self.configurableItems.items():
            value = self.settings.get(name, item.getDefault())
            if value is not None:
                setattr(obj, name, value)

class ConfigurableItem(object):
    """Configuration descriptor"""
    def __init__(self, name = None, default = None, fset = None,
            tm_name = None):
        self.name = name
        self.default = default
        self.fset = fset
        self.tm_name = tm_name

    def getDefault(self):
        return self.default

    def __call__(self, function):
        self.fset = function
        return self

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.name, owner.__name__))
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        return self.getDefault()

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        if self.fset is not None:
            self.fset(instance, value)
            
class ConfigurableHook(object):
    def __init__(self, path, fset = None):
        self.path = path
        self.fset = fset

    def __call__(self, function):
        self.fset = function
        return self

pmxConfigPorperty = ConfigurableItem
