#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#===============================================================
# PRYMATEX STYLES
# http://developer.qt.nokia.com/doc/qt-4.8/stylesheet-reference.html
#===============================================================
import os
from collections import namedtuple

__all__ = ["load_stylesheets"]

Stylesheet = namedtuple('Stylesheet', 'name path content')

def load_stylesheets(resourcesPath):
    stylesheets = {}
    stylesPath = os.path.join(resourcesPath, "StyleSheets")
    if os.path.exists(stylesPath):
        for styleFileName in os.listdir(stylesPath):
            name = os.path.splitext(styleFileName)[0]
            stylePath = os.path.join(stylesPath, styleFileName)
            with open(stylePath) as styleFile:
                stylesheets[name] = Stylesheet(name, stylePath, styleFile.read())
    return { "StyleSheets": stylesheets }
