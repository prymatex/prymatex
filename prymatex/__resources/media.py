#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================

import os
import json

from collections import namedtuple

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import get_std_icon

from prymatex.utils.decorators.memoize import memoized
from prymatex.utils import six
from prymatex.utils import encoding

from prymatex.widgets import glyph

from .base import find_resource
from .base import buildResourceKey

_fileIconProvider = QtGui.QFileIconProvider()
_media_mapper = {}
_media_from_theme = lambda index: QtGui.QIcon()

ICONNAMES = set()

def get_image(index, fallback = None):
    fallback = fallback or QtGui.QPixmap()
    image = _get_icon(index)
    return image.isNull() and fallback or image

def get_icon(index, fallback = None):
    fallback = fallback or QtGui.QIcon()
    icon = _get_icon(index)
    return icon.isNull() and fallback or icon

@memoized
def _get_image(index):
    path = getResource(index, ["Images", "Icons"])
    if path is not None:
        return QtGui.QPixmap(path)
    else:
        #Standard Icon
        return get_std_icon(index).pixmap(32)

@memoized
def _get_icon(index):
    '''Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance'''
    global _media_mapper, _media_from_theme
    if index in _media_mapper:
        index = _media_mapper[index]
    if isinstance(index, six.string_types):

        if os.path.exists(index) and os.path.isabs(index):
            return _fileIconProvider.icon(QtCore.QFileInfo(index))
	
        std = get_std_icon(index)
        if not std.isNull():
            return std

        path = find_resource(index, ["Icons", "External"])
        if path is not None:
            return QtGui.QIcon(path)
        
        return _media_from_theme(index)
    elif isinstance(index, six.integer_types):
        return _fileIconProvider.icon(index)

IconTheme = namedtuple("IconTheme", "name type path")

def set_icon_theme(theme_name):
    global _media_mapper, _media_from_theme
    _media_mapper = find_resource(theme_name, ["Mapping"]) or find_resource("default", ["Mapping"])
    theme = find_resource(theme_name, ["Themes"])
    print(theme_name)
    if theme is None:
        QtGui.QIcon.setThemeName(theme_name)
        _media_from_theme = QtGui.QIcon._fromTheme
    elif theme.type == "pix":
        QtGui.QIcon.setThemeName(theme.name)
        _media_from_theme = QtGui.QIcon._fromTheme
    elif theme.type == "glyph":
        glyph = find_resource(theme.name, ["Glyphs"])
        _media_from_theme = glyph.icon

def load_media(resourcesPath):
    resources = { "Images": {}, "Icons": {}, "Themes": {}, "Mapping": {}, "Glyphs": {}, "External": {} }
    # Load Icons
    iconsPath = os.path.join(resourcesPath, "Media", "Icons")
    if os.path.exists(iconsPath):
        for dirpath, dirnames, filenames in os.walk(iconsPath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                name = buildResourceKey(iconPath[len(iconsPath):])
                resources["Icons"][name] = iconPath

    # Load Images
    imagesPath = os.path.join(resourcesPath, "Media", "Images")
    if os.path.exists(imagesPath):
        for dirpath, dirnames, filenames in os.walk(imagesPath):
            for filename in filenames:
                imagePath = os.path.join(dirpath, filename)
                name = buildResourceKey(imagePath[len(imagesPath):])
                resources["Images"][name] = imagePath
                
    # Load Themes
    themePaths = set(QtGui.QIcon.themeSearchPaths())
    if os.path.exists("/usr/share/icons"):
        themePaths.add("/usr/share/icons")
    themePaths.add(os.path.join(resourcesPath, "Media", "Themes"))
    themeNames = [ ]
    for themePath in themePaths:
        if not os.path.exists(themePath):
            continue
        for name in os.listdir(themePath):
            descriptor = os.path.join(themePath, name, "index.theme")
            if os.path.exists(descriptor):
                resources["Themes"][name] = IconTheme(name, "pix", os.path.join(themePath, name))
    
    # Load Glyphs
    glyphsPath = os.path.join(resourcesPath, "Media", "Glyphs")
    if os.path.exists(glyphsPath):
        for glyphFileName in os.listdir(glyphsPath):
            name = os.path.splitext(glyphFileName)[0]
            glyphPath = os.path.join(glyphsPath, glyphFileName)
            gly = glyph.QtGlyph.initGlyph(glyphPath)
            resources["Glyphs"][gly.name()] = gly
            resources["Themes"][gly.name()] = IconTheme(gly.name(), "glyph", glyphPath)
    
    # Load Mapping
    mappingsPath = os.path.join(resourcesPath, "Media", "Mapping")
    if os.path.exists(mappingsPath):
        for mappingFileName in os.listdir(mappingsPath):
            name = os.path.splitext(mappingFileName)[0]
            file_content, _ = encoding.read(os.path.join(mappingsPath, mappingFileName))
            resources["Mapping"][name] = json.loads(file_content)

    return resources
