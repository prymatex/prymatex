#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

class PMXSupportCache(object):
    def __init__(self):
        self.keyValues = {}
        self.settings = {}

    def hasKey(self, key):
        return key in self.keyValues

    def get(self, key, default):
        if self.hasKey(key):
            return self.keyValues[key]
        return default

    def set(self, key, value):
        self.keyValues[key] = value

    def setcallable(self, key, function, *args):
        if key not in self.keyValues:
            if inspect.isgeneratorfunction(function):
                self.keyValues[key] = list(function(*args))
            else:
                self.keyValues[key] = function(*args)
        return self.keyValues[key]
    
    def deprecateAll(self):
        pass

    def deprecateValues(self, *values):
        for value in values:
            if value in self.keyValues:
                del self.keyValues[value]
    
    def setSettings(self, scope, settings):
        self.settings[scope] = settings

    def hasSettings(self, scope):
        return scope in self.settings
        
    def getSettings(self, scope):
        return self.settings.get(scope, None)