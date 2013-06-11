#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================
# PRYMATEX STYLES
# http://developer.qt.nokia.com/doc/qt-4.8/stylesheet-reference.html
#===============================================================
import os
import prymatex

FIND_NO_MATCH_STYLE = 'background-color: red; color: #fff;'
FIND_MATCH_STYLE = 'background-color: #dea;'

STYLESHEETS = {}

stylesPath = os.path.join(os.path.dirname(prymatex.__file__), "share", "Styles")
for styleFileName in os.listdir(stylesPath):
    stylePath = os.path.join(stylesPath, styleFileName)
    with open(stylePath) as styleFile:
        STYLESHEETS[os.path.splitext(styleFileName)[0]] = styleFile.read()

