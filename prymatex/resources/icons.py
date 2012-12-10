#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================

import os

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import get_std_icon

from prymatex.resources.loader import getResourcePath
from prymatex.utils.decorators.memoize import memoized

__fileIconProvider = QtGui.QFileIconProvider()

def get_icon(index, size = None, default = None):
    icon = __get_icon(index)
    if icon is None and default is not None:
        icon = default
    elif icon is None:
        icon = QtGui.QIcon(getResourcePath("notfound", ["Icons"]))
    if size is not None:
        size = size if isinstance(size, (tuple, list)) else (size, size)
        icon = QtGui.QIcon( icon.pixmap(*size) )
    return icon

@memoized
def __get_icon(index):
    '''
    Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance or None if no icon could be retrieved
    '''
    if isinstance(index, basestring):
        if os.path.isfile(index):
            #File path Icon
            return __fileIconProvider.icon(QtCore.QFileInfo(index))
        elif os.path.isdir(index):
            #Folder Icon
            return __fileIconProvider.icon(QtGui.QFileIconProvider.Folder)
        elif QtGui.QIcon.hasThemeIcon(index):
            #Theme Icon
            return QtGui.QIcon._fromTheme(index)
        else: 
            #Try icon in the prymatex's resources
            path = getResourcePath(index, ["Icons", "External"])
            if path is not None:
                return QtGui.QIcon(path)
        #Standard Icon
        return get_std_icon(index)
    elif isinstance(index, int):
        #Icon by int index in fileicon provider
        return __fileIconProvider.icon(index)
