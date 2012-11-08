#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================

import os

from prymatex.qt import QtGui, QtCore

from prymatex.resources.loader import getResourcePath
from prymatex.utils.decorators.memoize import memoized

__fileIconProvider = QtGui.QFileIconProvider()

@memoized
def get_icon(index, default = None):
    '''
    Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance or None if no icon could be retrieved
    '''
    #Try icon in db
    path = getResourcePath(index, ["Icons", "External"])
    if path is not None:
        return QtGui.QIcon(path)
    elif isinstance(index, basestring):
        #Try file path
        if os.path.isfile(index):
            return __fileIconProvider.icon(QtCore.QFileInfo(index))
        elif os.path.isdir(index):
            return __fileIconProvider.icon(QtGui.QFileIconProvider.Folder)
        elif QtGui.QIcon.hasThemeIcon(index):
            return QtGui.QIcon._fromTheme(index)
        elif default is not None:
            return default
        else:
            return QtGui.QIcon(getResourcePath("notfound", ["Icons"]))
    elif isinstance(index, int):
        #Try icon by int index in fileicon provider
        return __fileIconProvider.icon(index)
