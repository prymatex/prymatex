#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

class PMXSupportCache(object):
    def __init__(self):
        self.keyValues = {}
        
    def hasKey(self, key):
        return key in self.keyValues

    def get(self, key, default = None):
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
    
    def clear(self):
        pass

    def deleteMany(self, keys):
        for value in keys:
            if value in self.keyValues:
                del self.keyValues[value]