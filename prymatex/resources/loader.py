#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from prymatex.utils.decorators.memoize import memoized

RESOURCES = {}
RESOURCES_READY = False

THEME_ICON_TEST = "folder-sync"
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
    (os.path.normcase("/sidebar/folding-top.png"), "foldingtop"),
    (os.path.normcase("/sidebar/folding-bottom.png"), "foldingbottom"),
    (os.path.normcase("/sidebar/folding-collapsed.png"), "foldingcollapsed"),
    (os.path.normcase("/sidebar/folding-ellipsis.png"), "foldingellipsis"),
    (os.path.normcase("/sidebar/bookmark-flag.png"), "bookmarkflag"),
    
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

#===============================================================
# LOAD
#===============================================================
def buildResourceKey(filename, namePrefixes, installedKeys):
    resourceKey, _ = os.path.splitext(filename)
    index = -1
    while resourceKey in installedKeys and index:
        newKey = "-".join(namePrefixes[index:] + [resourceKey])
        if newKey == resourceKey:
            raise Exception("Esto no puede ocurrir")
        index -= 1
        resourceKey = newKey
    return resourceKey

def loadResources(resourcesPath, staticMapping = []):
    from prymatex.utils import osextra
    def loadSourcePath(sourcePath):
        sections ={}
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                staticNames = [path_names for path_names in staticMapping if iconPath.endswith(path_names[0])]
                if staticNames:
                    for name in staticNames:
                        sections[name[1]] = iconPath
                else:
                    name = buildResourceKey(filename, osextra.path.fullsplit(dirpath), sections)
                    sections[name] = iconPath
        return sections
    resources = {}
    for section in [ "Icons", "Images" ]:
        resources[section] = loadSourcePath(os.path.join(resourcesPath, section))
    return resources

def loadStyles(resourcesPath):
    styles = {}
    stylesPath = os.path.join(resourcesPath, "Styles")
    for styleFileName in os.listdir(stylesPath):
        name = os.path.splitext(styleFileName)[0]
        styles[name] = os.path.join(stylesPath, styleFileName)
    return {"Styles": styles}

def loadPrymatexResources(resourcesPath, preferedThemeName = "oxygen"):
    global RESOURCES, RESOURCES_READY
    if not RESOURCES_READY:
        # Test default theme:
        if not QtGui.QIcon.hasThemeIcon(THEME_ICON_TEST):
            themePaths = QtGui.QIcon.themeSearchPaths()
            if os.path.exists("/usr/share/icons") and "/usr/share/icons" not in themePaths:
                themePaths.append("/usr/share/icons")
            themePaths.append(os.path.join(resourcesPath, "IconThemes"))
            themeNames = [ preferedThemeName ]
            for themePath in themePaths:
                if os.path.exists(themePath):
                    themeNames.extend(os.listdir(themePath))
            # Set and test
            QtGui.QIcon.setThemeSearchPaths( themePaths )
            for themeName in themeNames:
                QtGui.QIcon.setThemeName(themeName)
                if QtGui.QIcon.hasThemeIcon(THEME_ICON_TEST):
                    break
        # Load Icons and Images
        RESOURCES.update(loadResources(resourcesPath, STATICMAPPING))
        # Load Styles
        RESOURCES.update(loadStyles(resourcesPath))

        installCustomFromThemeMethod()
        RESOURCES_READY = True

def installCustomFromThemeMethod():
    #Install fromTheme custom function
    from prymatex.resources.icons import get_icon
    QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
    QtGui.QIcon.fromTheme = staticmethod(get_icon)
            
def registerImagePath(name, path):
    global RESOURCES
    external = RESOURCES.setdefault("External", {})
    external[name] = path

def getResource(name, sections = None):
    global RESOURCES
    if sections is not None:
        sections = sections if isinstance(sections, (list, tuple)) else (sections, )
    else:
        sections = list(RESOURCES.keys())
    for section in sections:
        if section in RESOURCES and name in RESOURCES[section]:
            return RESOURCES[section].get(name)

def setResource(section, name, value):
    global RESOURCES
    RESOURCES.setdefault(section, {})[name] = value

def removeSection(name):
    global RESOURCES
    RESOURCES["name"] = {}

def getSection(name):
    global RESOURCES
    return RESOURCES.setdefault(name, {})

#===============================================================
# FUNCTIONS
#===============================================================
def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)
