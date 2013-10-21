#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.core.components.base import PMXBaseComponent

Key_Any = 0
class PMXBaseKeyHelper(PMXBaseComponent):
    KEY = Key_Any
    def accept(self, key):
        return self.KEY == key
    
    def execute(self, key):
        pass

class PMXKeyHelperMixin(object):
    @property
    def keyHelpers(self):
        try:
            return self._keyHelpers
        except AttributeError:
            self._keyHelpers = {}
            return self._keyHelpers
            
    def addKeyHelper(self, helper):
        try:
            self.keyHelpers.setdefault(helper.KEY, []).append(helper)
        except:
            self.keyHelpers = { helper.KEY: [ helper ]}

    def keyHelpersByClass(self, klass):
        return [keyHelper for keyHelper in self.keyHelpers[klass.KEY] if isinstance(keyHelper, klass)]
        
    def findHelpers(self, key):
        helpers = []
        if Key_Any in self.keyHelpers:
            helpers += self.keyHelpers[Key_Any]
        helpers += self.keyHelpers.get(key, [])
        return helpers

    def runKeyHelper(self, *largs, **kwargs):
        raise NotImplemented
