#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#===============================================================
# PRYMATEX STYLES
# http://developer.qt.nokia.com/doc/qt-4.8/stylesheet-reference.html
#===============================================================
import os
import prymatex
from collections import namedtuple

Stylesheet = namedtuple('Stylesheet', 'name path content')

FIND_NO_MATCH_STYLE = 'background-color: red; color: #fff;'
FIND_MATCH_STYLE = 'background-color: #dea;'

def loadStylesheets(resourcesPath):
    stylesheets = {}
    stylesPath = os.path.join(resourcesPath, "Stylesheets")
    if os.path.exists(stylesPath):
        for styleFileName in os.listdir(stylesPath):
            name = os.path.splitext(styleFileName)[0]
            stylePath = os.path.join(stylesPath, styleFileName)
            with open(stylePath) as styleFile:
                stylesheets[name] = Stylesheet(name, stylePath, styleFile.read())
    return {"Stylesheets": stylesheets}
