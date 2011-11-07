#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PMXSupportCache(object):
    def __init__(self):
        self.keyValues = {}
        self.settings = {}

    def setcallable(self, key, function, *args):
        if key not in self.keyValues:
            self.keyValues[key] = function(*args)
        return self.keyValues[key]
    
    def setSettings(self, scope, settings):
        self.settings[scope] = settings

    def hasSettings(self, scope):
        return scope in self.settings
        
    def getSettings(self, scope):
        return self.settings.get(scope, None)