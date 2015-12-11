#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from prymatex.utils import osextra

from .base import BundleItem

"""foreground, background, selection, invisibles, lineHighlight, caret, gutter
prymatex add gutterForeground
gutterDivider: Border between text view and gutter.
gutterForeground: Text color.
gutterBackground: Background color.
gutterIcons: Color of the images in the gutter.
gutterSelectionForeground: Text color for lines containing caret / part of a selection.
gutterSelectionBackground: Background color for lines containing caret / part of a selection.
gutterSelectionIcons: Color of images on lines containing caret / part of a selection.
gutterSelectionBorder: Border between selected and non-selected lines."""

DEFAULT_THEME_SETTINGS = {'background':         '#FFFFFF',
                          'caret':              '#000000',
                          'foreground':         '#000000',
                          'invisibles':         '#BFBFBF',
                          'lineHighlight':      '#00000012',
                          'gutterBackground':   '#FFFFFF',
                          'gutterForeground':   '#000000',
                          'lineHighlight':      '#00000012',
                          'selection':          '#A6CBFF'}


DEFAULT_SCOPE_SELECTORS = [('Comment', 'comment'),
                           ('String', 'string'),
                           ('Number', 'constant.numeric'),
                           ('Built-in constant', 'constant.language'),
                           ('User-defined constant', 'constant.character, constant.other'),
                           ('Variable', 'variable.language, variable.other'),
                           ('Keyword', 'keyword'),
                           ('Storage', 'storage'),
                           ('Class name', 'entity.name.class'),
                           ('Inherited class', 'entity.other.inherited-class'),
                           ('Function name', 'entity.name.function'),
                           ('Function argument', 'variable.parameter'),
                           ('Tag name', 'entity.name.tag'),
                           ('Tag attribute', 'entity.other.attribute-name'),
                           ('Library function', 'support.function'),
                           ('Library constant', 'support.constant'),
                           ('Library class/type', 'support.type, support.class'),
                           ('Library variable', 'support.other.variable'),
                           ('Invalid', 'invalid')]


class ThemeStyle(object):
    KEYS = ( 'scope', 'name', 'settings' )
    def __init__(self, theme):
        self.theme = theme
        self.__settings = {}

    def settings(self):
        return self.__settings

    def __load_update(self, dataHash, initialize):
        for key in ThemeStyle.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if key == 'settings':
                    self.__settings.update(value or {})
                    self.__settings = dict([ item for item in self.__settings.items() if item[1] is not None])
                    continue
                elif key == 'scope':
                    self.selector = self.theme.manager.selectorFactory(value)
                setattr(self, key, value)

    def load(self, dataHash):
        self.__load_update(dataHash, True)
        
    def update(self, dataHash):
        self.__load_update(dataHash, False)

    def dump(self):
        dataHash = {'name': self.name}
        if self.scope is not None:
            dataHash['scope'] = self.scope
        if self.__settings is not None:
            dataHash['settings'] = self.__settings
        return dataHash

class Theme(BundleItem):
    KEYS = ( 'name', 'comment', 'author', 'settings' )
    EXTENSION = 'tmTheme'
    PATTERNS = ( '*.tmTheme', )
    FOLDER = 'Themes'
    
    def __load_update(self, dataHash, initialize):
        for key in Theme.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if key == 'settings' and isinstance(value, list):
                    value = [ self.createThemeStyle(settings) for settings in value ]
                setattr(self, key, value)

    def load(self, dataHash):
        super(Theme, self).load(dataHash)
        self.__load_update(dataHash, True)
        
    def update(self, dataHash):
        super(Theme, self).update(dataHash)
        self.__load_update(dataHash, False)

    #def setSettings(self, settings):
    #    if "gutter" in settings:
    #        settings["gutterBackground"] = settings.pop("gutter")
    #    self.defaultSettings.update(settings or {})
    #    self.defaultSettings = dict([ item for item in self.defaultSettings.items() if item[1] is not None])

    #def settings(self):
        # Asegurar los basicos
    #    settings = self.defaultSettings.copy()
    #    for key, color in DEFAULT_THEME_SETTINGS.items():
    #        if key not in settings:
    #            settings[key] = color
    #    return settings

    def execute(self, processor):
        processor.beginExecution(self)
        if not processor.managed():
            processor.endExecution(self)    

    def dump(self, allKeys = False):
        dataHash = super(Theme, self).dump(allKeys)
        for key in Theme.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                if key == "settings":
                    value = [ style.dump() for style in value ]
                dataHash[key] = value
        return dataHash

    def createThemeStyle(self, settings):
        if 'name' not in settings or not settings['name']:
            settings['name'] = 'untitled'
        style = self.manager.addThemeStyle(ThemeStyle(self))
        style.load(settings)
        return style

    @staticmethod
    def buildSettings(settings):
        """El orden si importa, los settings vienen ordenados por score de mayor a menor"""
        base = DEFAULT_THEME_SETTINGS.copy()
        for s in settings:
            base.update(s.settings())
        return base
    
    def removeThemeStyle(self, style):
        self.styles.remove(style)

    def createSourcePath(self, baseDirectory):
        return osextra.path.ensure_not_exists(os.path.join(baseDirectory, "%%s.%s" % self.EXTENSION), osextra.to_valid_name(self.name))

