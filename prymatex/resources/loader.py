#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from .styles import loadStylesheets
from .icons import loadIconThemes, loadIcons
from .images import loadImages
from .fonts import loadGlyphs

def loadResources(resourcesPath):
    resources = {}
    # Load Icons Themes
    resources.update(loadIconThemes(resourcesPath))
    # Load Icons
    resources.update(loadIcons(resourcesPath))
    # Load Images
    resources.update(loadImages(resourcesPath))
    # Load Stylesheets
    resources.update(loadStylesheets(resourcesPath))
    # Load Glyphs
    resources.update(loadGlyphs(resourcesPath))
    return resources

#===============================================================
# FUNCTIONS
#===============================================================
def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)
