#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================
from prymatex.utils.decorators.memoize import memoized

_fileIconProvider = QtGui.QFileIconProvider()

@memoized
def getIcon(index, default = None):
    '''
    Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance or None if no icon could be retrieved
    '''
    global ICONS
    #Try icon in db
    path = ICONS.get(index, None)
    if path is not None:
        return QtGui.QIcon(path)
    elif isinstance(index, basestring):
        #Try file path
        if os.path.isfile(index):
            return _fileIconProvider.icon(QtCore.QFileInfo(index))
        elif os.path.isdir(index):
            return _fileIconProvider.icon(QtGui.QFileIconProvider.Folder)
        elif QtGui.QIcon.hasThemeIcon(index):
            return QtGui.QIcon._fromTheme(index)
        elif default is not None:
            return default
        else:
            print "falta icono", index
            return QtGui.QIcon._fromTheme(index)
    elif isinstance(index, int):
        #Try icon by int index in fileicon provider
        return _fileIconProvider.icon(index)
