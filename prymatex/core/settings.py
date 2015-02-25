#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.utils import settings

# --------------- Settings
class TextMateSettings(settings.Settings):
    pass

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
        
    def scope(self, name):
        if name not in self or not isinstance(self[name], PrymatexSettings):
            self[name] = PrymatexSettings(name, self.setdefault(name, {}))
            self[name].setTm(self._tm)
        return self[name]
    
    def default(self, name):
        return self._items.get(name).getDefault()

    def purge(self):
        # remove all empty scopes from settings
        for name in list(self.keys()):
            if isinstance(self[name], PrymatexSettings) and not self[name]:
                del self[name]

    def clear(self):
        # clear all settings values except scopes
        for name in list(self.keys()):
            if isinstance(self[name], PrymatexSettings):
                self[name].clear()
            else:
                del self[name]

    def reload(self, attrs):
        for name, value in attrs.items():
            if name in self and isinstance(self[name], PrymatexSettings):
                self[name].reload(value)
            else:
                self.set(name, value)

    def set(self, name, value):
        super(PrymatexSettings, self).set(name, value)
        item = self._items.get(name)
        if item:
            if name in self and value == item.getDefault():
                self.erase(name)
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

# --------------- Items and Hooks
class ConfigurableItem(object):
    """Configuration descriptor"""
    def __init__(self, name=None, default=None, fset=None, tm_name=None):
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
