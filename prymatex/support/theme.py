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
    def __init__(self, dataHash, theme):
        self.theme = theme
        self.load(dataHash)

    def load(self, dataHash):
        for key in PMXThemeStyle.KEYS:
            setattr(self, key, dataHash.get(key, None))

    @property
    def hash(self):
        dataHash = {'name': self.name}
        if self.scope is not None:
            dataHash['scope'] = self.scope
        dataHash['settings'] = {}
        for name, setting in self.settings.iteritems():
            if setting != None:
                dataHash['settings'][name] = setting
        return dataHash
        
    def update(self, dataHash):
        for key in dataHash.keys():
            if key == 'settings':
                self.settings.update(dataHash[key])
                self.settings = dict(filter(lambda tupla: tupla[1] != None, self.settings.iteritems()))
            else:
                setattr(self, key, dataHash[key])
    
class PMXTheme(PMXManagedObject):
    KEYS = [    'name', 'comment', 'author', 'settings']
    
    def __init__(self, uuid, dataHash):
        super(PMXTheme, self).__init__(uuid)
        self.styles = []
        self.load(dataHash)

    def load(self, dataHash):
        for key in PMXTheme.KEYS:
            setattr(self, key, dataHash.get(key, None))

    def setSettings(self, settings):
        self.settings = settings
        
    def update(self, dataHash):
        for key in dataHash.keys():
            if key == 'settings':
                self.settings.update(dataHash[key])
                self.settings = dict(filter(lambda tupla: tupla[1] != None, self.settings.iteritems()))
                print self.settings
            else:
                setattr(self, key, dataHash[key])
    
    @property
    def hash(self):
        dataHash = super(PMXTheme, self).hash
        for key in PMXTheme.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        dataHash['settings'] = [ { 'settings': self.settings } ]
        for style in self.styles:
            dataHash['settings'].append(style.hash)
        return dataHash
        
    def save(self, namespace):
        folder = os.path.dirname(self.path(namespace))
        if not os.path.exists(folder):
            os.makedirs(folder)
        plist.writePlist(self.hash, self.path(namespace))

    @classmethod
    def loadTheme(cls, path, namespace, manager):
        try:
            data = plist.readPlist(path)
            uuid = manager.uuidgen(data.pop('uuid', None))
            theme = manager.getManagedObject(uuid)
            if theme is None and not manager.isDeleted(uuid):
                theme = PMXTheme(uuid, data)
                theme.setManager(manager)
                theme.addSource(namespace, path)
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
            elif theme is not None:
                theme.addSource(namespace, path)
        except Exception, e:
            print "Error en theme %s (%s)" % (path, e)
