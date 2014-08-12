#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from .styles import loadStylesheets
from .icons import loadIconThemes, loadIcons
from .images import loadImages

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
    
    #Editor Sidebar
    #(os.path.normcase("/sidebar/folding-top.png"), "folding-top"),
    #(os.path.normcase("/sidebar/folding-bottom.png"), "folding-bottom"),
    #(os.path.normcase("/sidebar/folding-collapsed.png"), "folding-collapsed"),
    #(os.path.normcase("/sidebar/folding-ellipsis.png"), "folding-ellipsis"),
    #(os.path.normcase("/sidebar/bookmark-flag.png"), "bookmark-flag"),
    
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
    # Load Styles
    resources.update(loadStylesheets(resourcesPath))
    # Load Styles
    resources.update(loadGlyphs(resourcesPath))
    return resources

def loadGlyphs(resourcesPath):
    glyphs = {}
    glyphsPath = os.path.join(resourcesPath, "Glyphs")
    if os.path.exists(glyphsPath):
        for glyphFileName in os.listdir(glyphsPath):
            name = os.path.splitext(glyphFileName)[0]
            glyphs[name] = os.path.join(glyphsPath, glyphFileName)
    return {"Glyphs": glyphs}

#===============================================================
# FUNCTIONS
#===============================================================
def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)
