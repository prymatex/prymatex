#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
from prymatex.qt.helpers import get_std_icon

from prymatex.resources.loader import getResourcePath
from prymatex.utils.decorators.memoize import memoized

def get_image(index, size = None, default = None):
    image = __get_image(index)
    if image is None and default is not None:
        image = default
    elif image is None:
        image = QtGui.QPixmap(getResourcePath("notfound", ["Icons"]))
    if size is not None:
        size = size if isinstance(size, (tuple, list)) else (size, size)
        image = image.scaled(*size)
    return image

@memoized
def __get_image(index):
    path = getResourcePath(index, ["Images", "Icons"])
    if path is not None:
        return QtGui.QPixmap(path)
    else:
        #Standard Icon
        return get_std_icon(index).pixmap(32)
