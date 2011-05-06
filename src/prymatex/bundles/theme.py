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
    def __init__(self, hash):
        for key in [    'scope', 'name', 'settings' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Style has more values (%s)" % (', '.join(hash.keys()))

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
    UUIDS = {}
    STYLES_CACHE = {}
    scores = PMXScoreManager()
    
    def __init__(self, hash, namespace, path = None):
        self.sytles = []
        for key in [    'uuid', 'name', 'comment', 'author', 'settings' ]:
            value = hash.pop(key, None)
            if key == 'settings':
                self.default = PMXStyle(value[0])
                for setting in value[1:]:
                    self.sytles.append(PMXStyle(setting))
            else:
                setattr(self, key, value)
        self.namespace = namespace
        self.path = path

    @classmethod
    def loadTheme(cls, path, namespace):
        try:
            data = plistlib.readPlist(path)
            theme = PMXTheme(data, namespace, path)
            cls.UUIDS[theme.uuid] = theme
            return theme
        except Exception, e:
            print "Error en bundle %s (%s)" % (path, e)

    @classmethod
    def getThemeByName(cls, name):
        for theme in cls.UUIDS.values():
            if theme.name == name:
                return theme

    @classmethod
    def getThemeByUUID(cls, uuid):
        if uuid in cls.UUIDS:
            return cls.UUIDS[uuid]

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