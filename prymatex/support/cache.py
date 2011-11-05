#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PMXSupportCache(object):
    def __init__(self):
        self.keyValues = {}

    def setcallable(self, key, function, *args):
        if key not in self.keyValues:
            self.keyValues[key] = function(*args)
        return self.keyValues[key]
        