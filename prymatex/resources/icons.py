#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================

import os

from collections import namedtuple

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import get_std_icon

from prymatex.utils.decorators.memoize import memoized
from prymatex.utils import six

from .base import find_resource
from .base import buildResourceKey

__fileIconProvider = QtGui.QFileIconProvider()

STANDARD_ICON_NAME = [name for name in dir(QtGui.QStyle) if name.startswith('SP_') ]
ICONNAMES = set()

def get_icon(index, fallback = QtGui.QIcon()):
    icon = __get_icon(index)
    return icon.isNull() and fallback or icon

@memoized
def __get_icon(index):
    '''Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance'''
    if isinstance(index, six.string_types):
        ICONNAMES.add(index)
        if os.path.exists(index) and os.path.isabs(index):
            #File path Icon
            ICONNAMES.remove(index)
            return __fileIconProvider.icon(QtCore.QFileInfo(index))
        elif QtGui.QIcon.hasThemeIcon(index):
            #Theme Icon
            return QtGui.QIcon._fromTheme(index)
        else: 
            #Try icon in the prymatex's resources
            path = find_resource(index, ["Icons", "External"])
            if path is not None:
                return QtGui.QIcon(path)
        #Standard Icon
        return get_std_icon(index)
    elif isinstance(index, six.integer_types):
        #Icon by int index in fileicon provider
        return __fileIconProvider.icon(index)

IconTheme = namedtuple("IconTheme", "name path")

def loadIconThemes(resourcesPath):
    icon_themes = {}
    themePaths = set(QtGui.QIcon.themeSearchPaths())
    if os.path.exists("/usr/share/icons"):
        themePaths.add("/usr/share/icons")
    themePaths.add(os.path.join(resourcesPath, "IconThemes"))
    themeNames = [ ]
    for themePath in themePaths:
        if not os.path.exists(themePath):
            continue
        for theme_name in os.listdir(themePath):
            descriptor = os.path.join(themePath, theme_name, "index.theme")
            if os.path.exists(descriptor):
                icon_themes[theme_name] = IconTheme(theme_name, os.path.join(themePath, theme_name))
    return {"IconThemes": icon_themes}

def installCustomFromThemeMethod():
    QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
    QtGui.QIcon.fromTheme = staticmethod(get_icon)

def loadIcons(resourcesPath):
    icons = {}
    iconsPath = os.path.join(resourcesPath, "Icons")
    if os.path.exists(iconsPath):
        for dirpath, dirnames, filenames in os.walk(iconsPath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                name = buildResourceKey(iconPath[len(iconsPath):])
                print(name)
                icons[name] = iconPath
    return { "Icons": icons }