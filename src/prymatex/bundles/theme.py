#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plistlib
from copy import copy
from xml.parsers.expat import ExpatError
# for run as main
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager
from prymatex.bundles.qtadapter import buildQTextFormat, buildQColor

'''
    caret = Cursor, foreground, selection, invisibles, lineHighlight, gutter, background
'''

class PMXStyle(object):
    KEYS = [    'scope', 'name', 'settings' ]
    def __init__(self, hash = None):
        if hash != None:
            self.load(hash)

    def load(self, hash):
        for key in PMXStyle.KEYS:
            setattr(self, key, hash.get(key, None))

    @property
    def hash(self):
        hash = {'scope': self.scope, 'name': self.name, 'settings': copy(self.settings)}
        return hash
        
    def __getitem__(self, name):
        return self.settings[name]
    
    def __contains__(self, name):
        return name in self.settings
    
    def __copy__(self):
        values = {'scope': self.scope, 'name': self.name, 'settings': copy(self.settings)}
        obj = PMXStyle(values)
        return obj
        
    def update(self, other):
        self.settings.update(other.settings)
    
    @property
    def QTextFormat(self):
        return buildQTextFormat(self)
    
    def getQColor(self, item):
        return buildQColor(self[item])
    
class PMXTheme(object):
    KEYS = [    'uuid', 'name', 'comment', 'author', 'settings' ]
    STYLES_CACHE = {}
    scores = PMXScoreManager()
    
    def __init__(self, namespace, hash = None, path = None):
        self.namespace = namespace
        self.path = path
        if hash != None:
            self.load(hash)

    def load(self, hash):
        self.sytles = []
        for key in PMXTheme.KEYS:
            value = hash.get(key, None)
            if value != None and key == 'settings':
                self.default = PMXStyle(value[0])
                for setting in value[1:]:
                    self.sytles.append(PMXStyle(setting))
            else:
                setattr(self, key, value)
    
    @property
    def hash(self):
        hash = {}
        for key in PMXTheme.KEYS:
            value = getattr(self, key)
            if value != None:
                if key == 'settings':
                    result = [ self.default.hash ]
                    for v in value:
                        result.append(v.hash)
                    value = result
                hash[key] = value
        return hash
        
    def save(self, base = None):
        if base != None:
            file = os.path.join(base , os.path.basename(self.path))
        else:
            file = self.path
        plistlib.writePlist(self.hash, file)

    @classmethod
    def loadTheme(cls, path, namespace):
        try:
            data = plistlib.readPlist(path)
            theme = PMXTheme(namespace, data, path)
            return theme
        except Exception, e:
            print "Error en bundle %s (%s)" % (path, e)

    def clearCache(self):
        PMXTheme.STYLES_CACHE = {}
        
    def getStyle(self, scope = None):
        if scope in PMXTheme.STYLES_CACHE:
            return PMXTheme.STYLES_CACHE[scope]
        base = copy(self.default)
        if scope == None:
            return base
        styles = []
        for style in self.sytles:
            if style.scope != None:
                score = self.scores.score(style.scope, scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style)
        PMXTheme.STYLES_CACHE[scope] = base
        return base