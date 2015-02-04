#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.utils import plist, settings

# --------------- Settings
class TextMateSettings(settings.Settings):
    def __init__(self, file):
        self.file = file
        settings = {}
        if os.path.exists(self.file):
            try:
                settings = plist.readPlist(self.file)
            except Exception as e:
                print(("Exception raised while reading settings file: %s" % e))
        super(TextMateSettings, self).__init__(os.path.basename(file), settings)

    def set(self, name, value):
        super(TextMateSettings, self).set(name, value)
        self.sync()

    def clear(self):
        super(TextMateSettings, self).clear()
        self.sync()

    def sync(self):
        plist.writePlist(self, self.file)

class PrymatexSettings(settings.Settings):
    def __init__(self, name, settings):
        super(PrymatexSettings, self).__init__(name, settings)
        self._tm = None
        self._listeners = set()
        # Setting attrs
        self._items = {}
        # Setting hooks
        self._hooks = {}

    def setTm(self, tm):
        self._tm = tm

    def default(self, name):
        return self._items.get(name).getDefault()

    def set(self, name, value):
        item = self._items.get(name)
        if item:
            if name in self and value == item.getDefault():
                self.erase(name)
            else:
                super(PrymatexSettings, self).set(name, value)
            if self._tm and item.tm_name:
                self._tm.set(item.tm_name, value)
            for listener in self._listeners:
                setattr(listener, name, value)
            
    def get(self, name, default=None):
        value = super(PrymatexSettings, self).get(name, default)
        if value is None and name in self._items:
            value = self._items.get(name).getDefault()
        return value

    def has(self, name):
        return name in self.items

    def addItem(self, item):
        self._items[item.name] = item
        if item.tm_name and self._tm.get(item.tm_name) is not None:
            self._tm.set(item.tm_name, item.getDefault())

    def hooks(self):
        return self._hooks

    def addHook(self, hook):
        self._hooks[hook.path] = hook

    def addListener(self, listener):
        self._listeners.add(listener)

    def removeListener(self, listener):
        self._listeners.remove(listener)

    def configure(self, obj):
        for name, item in self._items.items():
            value = self.get(name)
            if value is not None:
                setattr(obj, name, value)

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

# --------------- Items and Hooks
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
