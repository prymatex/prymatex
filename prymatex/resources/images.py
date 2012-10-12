#!/usr/bin/env python
# -*- coding: utf-8 -*-

@memoized
def getImage(index):
    path = getImagePath(index)
    if path is not None:
        return QtGui.QPixmap(path)