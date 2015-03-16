#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import get_std_icon, get_path_icon, get_type_icon
from prymatex.core import PrymatexComponent
from prymatex.utils import text as textutils

from .media import default_media_mapper
from .stylesheets import load_stylesheets
from .styles import default_styles

__all__ = ["LICENSES", "build_resource_key", "Resource", "ResourceProvider"]

logger = logging.getLogger(__name__)

LICENSES = [
    'Apache License 2.0',
    'Artistic License/GPL',
    'Eclipse Public License 1.0',
    'GNU General Public License v2',
    'GNU General Public License v3',
    'GNU Lesser General Public License',
    'MIT License',
    'Mozilla Public License 1.1',
    'New BSD License',
    'Other Open Source',
    'Other'
]

def build_resource_key(path):
    return ":/%s" % "/".join(osextra.path.fullsplit(path))

class Resource(dict):
    def __init__(self, name, path=None, builtin=False):
        self._name = name
        self._path = path
        self._builtin = builtin
        self._mapper = default_media_mapper
        self._from_theme = QtGui.QIcon._fromTheme

    def builtin(self):
        return self._builtin

    def name(self):
        return self._name

    def path(self):
        return self._path

    def map_index(self, index):
        return self._mapper.get(index, index)

    def find_source(self, name, sections=None):
        if sections is None:
            sections = self.keys()
        elif not isinstance(sections, (list, tuple)):
            sections = (sections, )
        for section in sections:
            if section in self and name in self[section]:
                return self[section].get(name)
    
    def get_image(self, index):
        index = self.map_index(index)
        
        std = get_std_icon(index)
        if not std.isNull():
            return std.pixmap(32)

        path = self.find_source(index, ["Images", "Icons"])
        if path is not None:
            return QtGui.QPixmap(path)

        return self._from_theme(index).pixmap(32)

    def get_icon(self, index):
        index = self.map_index(index)
        
        std = get_std_icon(index)
        if not std.isNull():
            return std

        path = self.find_source(index, ["Icons", "External"])
        if path is not None:
            return QtGui.QIcon(path)
    
        return self._from_theme(index)

    def set_theme(self, name):
        self._mapper = self.find_source(name, ["Mapping"]) or default_media_mapper
        theme = self.find_source(name, ["Themes"])
        if theme:
            if theme.type == "pix":
                # Pixmap
                QtGui.QIcon.setThemeName(theme.name)
                self._from_theme = QtGui.QIcon._fromTheme
            elif theme.type == "glyph":
                # Glyph
                glyph = self.find_source(name, ["Glyphs"])
                self._from_theme = glyph.icon

class ResourceProvider(object):
    def __init__(self, resources):
        self.resources = resources

    def names(self):
        return tuple([ res.name() for res in self.resources ])

    def sources(self):
        return self.resources[:]

    def _section(self, name):
        section = {}
        for resource in reversed(self.resources):
            if name in resource:
                section.update(resource[name])
        return section
    
    # ------------- Get data
    def get_image(self, index, fallback = None):
        fallback = fallback or QtGui.QPixmap()
        for res in self.resources:
            image = res.get_image(index)
            if not image.isNull():
                return image
        return fallback

    def get_icon(self, index, fallback=None):
        if os.path.exists(index) and os.path.isabs(index):
            return get_path_icon(index)
        elif isinstance(index, int):
            return get_type_icon(index)
        fallback = fallback or QtGui.QIcon()
        for res in self.resources:
            icon = res.get_icon(index)
            if not icon.isNull():
                return icon
        logger.info("Unknown icon with %s key" % index)
        return fallback
    
    def get_themes(self):
        return self._section("Themes")

    def get_stylesheets(self):
        return self._section("StyleSheets")

    def get_styles(self):
        return default_styles

    def get_shortcuts(self):
        return self._section("Shortcuts")
        
    def get_software_licenses(self):
        return LICENSES

    # --------- Some sets    
    def set_theme(self, name):
        for res in self.resources:
            res.set_theme(name)
