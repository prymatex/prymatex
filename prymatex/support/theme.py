#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from prymatex.support.bundle import PMXManagedObject
from prymatex.utils import plist

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
        hash = {'name': self.name}
        if self.scope is not None:
            hash['scope'] = self.scope
        hash['settings'] = {}
        for name, setting in self.settings.iteritems():
            if setting != None:
                hash['settings'][name] = setting
        return hash
        
    def update(self, hash):
        for key in hash.keys():
            if key == 'settings':
                self.settings.update(hash[key])
                self.settings = dict(filter(lambda tupla: tupla[1] != None, self.settings.iteritems()))
            else:
                setattr(self, key, hash[key])
    
class PMXTheme(PMXManagedObject):
    KEYS = [    'name', 'comment', 'author', 'settings']
    
    def __init__(self, uuid, hash):
        super(PMXTheme, self).__init__(uuid)
        self.styles = []
        self.load(hash)

    def load(self, hash):
        for key in PMXTheme.KEYS:
            setattr(self, key, hash.get(key, None))

    def setSettings(self, settings):
        self.settings = settings
        
    def update(self, hash):
        for key in hash.keys():
            if key == 'settings':
                self.settings.update(hash[key])
                self.settings = dict(filter(lambda tupla: tupla[1] != None, self.settings.iteritems()))
                print self.settings
            else:
                setattr(self, key, hash[key])
    
    @property
    def hash(self):
        hash = super(PMXTheme, self).hash
        for key in PMXTheme.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        hash['settings'] = [ { 'settings': self.settings } ]
        for style in self.styles:
            hash['settings'].append(style.hash)
        return hash
        
    def save(self):
        dir = os.path.dirname(self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        plist.writePlist(self.hash, self.path)

    @classmethod
    def loadTheme(cls, path, namespace, manager):
        try:
            data = plist.readPlist(path)
            uuid = manager.uuidgen(data.pop('uuid', None))
            theme = manager.getManagedObject(uuid)
            if theme is None and not manager.isDeleted(uuid):
                theme = PMXTheme(uuid, data)
                theme = manager.addTheme(theme)
                settings = data.pop('settings', [])
                if settings:
                    theme.setSettings(settings[0].settings)
                for setting in settings[1:]:
                    style = PMXThemeStyle(setting, theme)
                    style = manager.addThemeStyle(style)
                    theme.styles.append(style)
                manager.showMessage("Loading theme %s" % theme.name)
                manager.addManagedObject(theme)
            theme.addSource(namespace, path)
        except Exception, e:
            print "Error en theme %s (%s)" % (path, e)
