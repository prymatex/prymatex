#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, plistlib
import uuid as uuidmodule
from xml.parsers.expat import ExpatError
from prymatex.support.score import PMXScoreManager
from prymatex.support.bundle import PMXManagedObject

'''
    foreground, background, selection, invisibles, lineHighlight, caret, gutter
'''

class PMXThemeStyle(object):
    KEYS = [ 'scope', 'name', 'settings' ]
    def __init__(self, hash, theme):
        self.theme = theme
        self.load(hash)

    def load(self, hash):
        for key in PMXThemeStyle.KEYS:
            setattr(self, key, hash.get(key, None))

    @property
    def hash(self):
        hash = {'scope': self.scope, 'name': self.name, 'settings': self.settings}
        return hash
    
class PMXTheme(PMXManagedObject):
    KEYS = [    'name', 'comment', 'author']
    scores = PMXScoreManager()
    
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXTheme, self).__init__(uuid, namespace)
        self.path = path
        self.styles = []
        self.settings = None
        self.load(hash)

    def load(self, hash):
        for key in PMXTheme.KEYS:
            value = hash.get(key, None)
            if value != None:
                setattr(self, key, value)

    def setSettings(self, settings):
        self.settings = settings
        
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
                    theme.setSettings(settings[0].settings)
                for setting in settings[1:]:
                    style = PMXThemeStyle(setting, theme)
                    style = manager.addThemeStyle(style)
                    theme.styles.append(style)
                manager.addManagedObject(theme)
            elif theme is not None:
                theme.addNamespace(namespace)
        except Exception, e:
            print "Error en bundle %s (%s)" % (path, e)
