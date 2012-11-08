#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from prymatex.resources.loader import getResourcePath
from prymatex.utils.decorators.memoize import memoized

@memoized
def get_image(index, default = None):
    path = getResourcePath(index, ["Images", "Icons"])
    if path is not None:
        return QtGui.QPixmap(path)
    elif default is not None:
        return default
    else:
        return QtGui.QPixmap(getResourcePath("notfound", ["Icons"]))