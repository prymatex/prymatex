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
    def addKeyHelper(self, helper):
        try:
            self._keyHelpers.setdefault(helper.KEY, []).append(helper)
        except:
            self._keyHelpers = { helper.KEY: [ helper ]}

    def keyHelperByClass(self, klass):
        keyHelper = filter(lambda keyHelper: isinstance(keyHelper, klass), self._keyHelpers)
        #TODO: Solo uno
        return keyHelper[0]
        
    def findHelpers(self, key):
        helpers = []
        if Key_Any in self._keyHelpers:
            helpers += self._keyHelpers[Key_Any]
        helpers += self._keyHelpers.get(key, [])
        return helpers

    def runKeyHelper(self, *largs, **kwargs):
        raise NotImplemented
