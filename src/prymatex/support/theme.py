#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, plistlib
import uuid as uuidmodule
from copy import copy
from xml.parsers.expat import ExpatError
from prymatex.support.score import PMXScoreManager
from prymatex.support.bundle import PMXManagedObject
#Deprecated use decorator like bundle items
from prymatex.gui.support.qtadapter import buildQTextFormat, buildQColor

'''
    foreground, background, selection, invisibles, lineHighlight, caret, gutter
'''

class PMXThemeStyle(object):
    KEYS = [ 'scope', 'name', 'settings' ]
    SETTING_ATTRIBUTES = [ 'fontStyle', 'foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter' ]
    def __init__(self, hash, theme):
        self.theme = theme
        self.load(hash)

    def load(self, hash):
        for key in PMXThemeStyle.KEYS:
            value = hash.get(key, None)
            if value != None and key == 'settings':
                for attr in PMXThemeStyle.SETTING_ATTRIBUTES:
                    if attr in value:
                        setattr(self, key, value[attr])
            elif value != None:
                setattr(self, key, value)

    @property
    def hash(self):
        hash = {'scope': self.scope, 'name': self.name}
        for attr in PMXThemeStyle.SETTING_ATTRIBUTES:
            if hasattr(self, attr):
                hash[attr] = getattr(self, attr))
        return hash
        
    def __copy__(self):
        obj = PMXThemeStyle(self.hash, self.theme)
        return obj

    def update(self, other):
        for attr in PMXThemeStyle.SETTING_ATTRIBUTES:
            if hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))
    
class PMXTheme(PMXManagedObject):
    KEYS = [    'name', 'comment', 'author']
    STYLES_CACHE = {}
    scores = PMXScoreManager()
    
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXTheme, self).__init__(uuid, namespace)
        self.path = path
        self.styles = []
        self.default = None
        self.load(hash)

    def load(self, hash):
        for key in PMXTheme.KEYS:
            value = hash.get(key, None)
            if value != None:
                setattr(self, key, value)

    def setDefault(self, default):
        self.default = default
        
    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])
    
    @property
    def hash(self):
        hash = super(PMXTheme, self).hash
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
        
    def save(self):
        dir = os.path.dirname(self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        plistlib.writePlist(self.hash, self.path)

    @classmethod
    def loadTheme(cls, path, namespace, manager):
        try:
            data = plistlib.readPlist(path)
            uuid = uuidmodule.UUID(data.pop('uuid'))
            theme = manager.getManagedObject(uuid)
            if theme is None and not manager.isDeleted(uuid):
                theme = PMXTheme(uuid, namespace, data, path)
                theme = manager.addTheme(theme)
                settings = data.pop('settings', [])
                if settings:
                    style = PMXThemeStyle(settings[0], theme)
                    theme.setDefault(style)
                for setting in settings[1:]:
                    style = PMXThemeStyle(setting, theme)
                    style = manager.addThemeStyle(style)
                    theme.styles.append(style)
                manager.addManagedObject(theme)
            elif theme is not None:
                theme.addNamespace(namespace)
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
        for style in self.styles:
            if style.scope != None:
                score = self.scores.score(style.scope, scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style)
        PMXTheme.STYLES_CACHE[scope] = base
        return base