#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import inspect
from prymatex.core.plugin import PMXBaseComponent

class PMXCache(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.cachedValues = {}
        
    def add(self, key, value):
        return True

    def get(self, key):
        return None

    def set(self, key, value):
        pass

    def setcallable(self, key, function, *args):
        if key not in self.cachedValues:
            if inspect.isgeneratorfunction(function):
                self.cachedValues[key] = list(function(*args))
            else:
                self.cachedValues[key] = function(*args)
        return self.cachedValues[key]
        
    def delete(self, key):
        pass

    def hasKey(self, key):
        return False

    def getMany(self, keys):
        return {}

    def setMany(self, data):
        pass

    def deleteMany(self, keys):
        pass
    
    def clear(self):
        pass
