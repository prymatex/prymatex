#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from .styles import loadStylesheets
from .icons import loadIconThemes, loadIcons
from .images import loadImages
from .fonts import loadGlyphs

STANDARD_ICON_NAME = [name for name in dir(QtGui.QStyle) if name.startswith('SP_') ]

STATICMAPPING = (
    # Process
    (os.path.normcase("/bullets/red.png"), "porcess-not-running"),
    (os.path.normcase("/bullets/yellow.png"), "porcess-starting"),
    (os.path.normcase("/bullets/green.png"), "porcess-running"),
    
    # Symbols
    (os.path.normcase("/bullets/blue.png"), "symbol-class"),
    (os.path.normcase("/bullets/green.png"), "symbol-block"),
    (os.path.normcase("/bullets/yellow.png"), "symbol-context"),
    (os.path.normcase("/bullets/ligthblue.png"), "symbol-function"),
    (os.path.normcase("/bullets/brown.png"), "symbol-typedef"),
    (os.path.normcase("/bullets/red.png"), "symbol-variable"),
    
    # Scope Root Groups
    (os.path.normcase("/bullets/blue.png"), "scope-root-comment"),
    (os.path.normcase("/bullets/yellow.png"), "scope-root-constant"),
    (os.path.normcase("/bullets/ligthblue.png"), "scope-root-entity"),
    (os.path.normcase("/bullets/red.png"), "scope-root-invalid"),
    (os.path.normcase("/bullets/green.png"), "scope-root-keyword"),
    (os.path.normcase("/bullets/violet.png"), "scope-root-markup"),
    (os.path.normcase("/bullets/darkviolet.png"), "scope-root-meta"),
    (os.path.normcase("/bullets/gray.png"), "scope-root-storage"),
    (os.path.normcase("/bullets/darkgreen.png"), "scope-root-string"),
    (os.path.normcase("/bullets/brown.png"), "scope-root-support"),
    (os.path.normcase("/bullets/orange.png"), "scope-root-variable"),
    (os.path.normcase("/bullets/darkgreen.png"), "scope-root-none"),
    
    #Bundles
    (os.path.normcase("/bundles/bundle.png"), "bundle-item-bundle"),
    (os.path.normcase("/bundles/templates.png"), "bundle-item-template"),
    (os.path.normcase("/bundles/commands.png"), "bundle-item-command"),
    (os.path.normcase("/bundles/languages.png"), "bundle-item-syntax"),
    (os.path.normcase("/bundles/project.png"), "bundle-item-project"),
    (os.path.normcase("/bundles/preferences.png"), "bundle-item-preference"),
    (os.path.normcase("/bundles/drag-commands.png"), "bundle-item-dragcommand"),
    (os.path.normcase("/bundles/snippets.png"), "bundle-item-snippet"),
    (os.path.normcase("/bundles/macros.png"), "bundle-item-macro"),
    (os.path.normcase("/bundles/template-files.png"), "bundle-item-staticfile"),
    
    #Editor Mode
    (os.path.normcase("/bullets/red.png"), "editor-mode"),
)

def loadResources(resourcesPath):
    resources = {}
    # Load Icons Themes
    resources.update(loadIconThemes(resourcesPath))
    # Load Icons
    resources.update(loadIcons(resourcesPath, STATICMAPPING))
    # Load Images
    resources.update(loadImages(resourcesPath, STATICMAPPING))
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
