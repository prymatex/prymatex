#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from prymatex.utils.decorators.memoize import memoized

#===============================================================
# IMAGES AND ICONS
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
#===============================================================

THEME_ICON_TEST = "document-open"

# TODO: Migrar al uso de la calve por defecto
STATICMAPPING = (
    # Process
    (os.path.normcase("groups/red.png"), "porcess-not-running"),
    (os.path.normcase("groups/yellow.png"), "porcess-starting"),
    (os.path.normcase("groups/green.png"), "porcess-running"),
    
    # Symbols
    (os.path.normcase("groups/blue.png"), "symbol-class"),
    (os.path.normcase("groups/green.png"), "symbol-block"),
    (os.path.normcase("groups/yellow.png"), "symbol-context"),
    (os.path.normcase("groups/ligthblue.png"), "symbol-function"),
    (os.path.normcase("groups/brown.png"), "symbol-typedef"),
    (os.path.normcase("groups/red.png"), "symbol-variable"),
    
    # Scope Root Groups
    (os.path.normcase("groups/blue.png"), "scope-root-comment"),
    (os.path.normcase("groups/yellow.png"), "scope-root-constant"),
    (os.path.normcase("groups/ligthblue.png"), "scope-root-entity"),
    (os.path.normcase("groups/red.png"), "scope-root-invalid"),
    (os.path.normcase("groups/green.png"), "scope-root-keyword"),
    (os.path.normcase("groups/violet.png"), "scope-root-markup"),
    (os.path.normcase("groups/darkviolet.png"), "scope-root-meta"),
    (os.path.normcase("groups/gray.png"), "scope-root-storage"),
    (os.path.normcase("groups/darkgreen.png"), "scope-root-string"),
    (os.path.normcase("groups/brown.png"), "scope-root-support"),
    (os.path.normcase("groups/orange.png"), "scope-root-variable"),
    
    #Editor Sidebar
    (os.path.normcase("sidebar/folding-top.png"), "foldingtop"),
    (os.path.normcase("sidebar/folding-bottom.png"), "foldingbottom"),
    (os.path.normcase("sidebar/folding-collapsed.png"), "foldingcollapsed"),
    (os.path.normcase("sidebar/folding-ellipsis.png"), "foldingellipsis"),
    (os.path.normcase("sidebar/bookmark-flag.png"), "bookmarkflag"),
    
    #Bundles
    (os.path.normcase("bundles/bundle.png"), "bundle-item-bundle"),
    (os.path.normcase("bundles/templates.png"), "bundle-item-template"),
    (os.path.normcase("bundles/commands.png"), "bundle-item-command"),
    (os.path.normcase("bundles/languages.png"), "bundle-item-syntax"),
    (os.path.normcase("bundles/project.png"), "bundle-item-project"),
    (os.path.normcase("bundles/preferences.png"), "bundle-item-preference"),
    (os.path.normcase("bundles/drag-commands.png"), "bundle-item-dragcommand"),
    (os.path.normcase("bundles/snippets.png"), "bundle-item-snippet"),
    (os.path.normcase("bundles/macros.png"), "bundle-item-macro"),
    (os.path.normcase("bundles/template-files.png"), "bundle-item-templatefile"),
    
    #Editor Sidebar
    (os.path.normcase("modes/cursors.png"), "modes-cursors"),
    (os.path.normcase("modes/snippet.png"), "modes-snippet"),
    (os.path.normcase("modes/insert.png"), "modes-insert"),
)

RESOURCES = {}
RESOURCES_READY = False

FileIconProvider = QtGui.QFileIconProvider()

def getResourcePath(name, sources = None):
    if sources is not None:
        sources = sources if isinstance(sources, (list, tuple)) else (sources, )
    else:
        sources = RESOURCES.keys()
    for source in sources:
        if source in RESOURCES and name in RESOURCES[source]:
            return RESOURCES[source].get(name)

@memoized
def getImage(index):
    path = getResourcePath(index, ["Icons", "Images"])
    if path is not None:
        return QtGui.QPixmap(path)

#http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
@memoized
def getIcon(index, default = None):
    '''
    Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance or None if no icon could be retrieved
    '''
    #Try icon in db
    path = getResourcePath(index, ["Icons", "External"])
    if path is not None:
        return QtGui.QIcon(path)
    elif isinstance(index, basestring):
        #Try file path
        if os.path.isfile(index):
            return FileIconProvider.icon(QtCore.QFileInfo(index))
        elif os.path.isdir(index):
            return FileIconProvider.icon(QtGui.QFileIconProvider.Folder)
        elif QtGui.QIcon.hasThemeIcon(index):
            return QtGui.QIcon._fromTheme(index)
        elif default is not None:
            return default
        else:
            print "falta icono", index
            return QtGui.QIcon._fromTheme(index)
    elif isinstance(index, int):
        #Try icon by int index in fileicon provider
        return FileIconProvider.icon(index)

#===============================================================
# LOAD RESOURCES
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
        sources ={}
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                staticNames = filter(lambda (path, names): iconPath.endswith(path), staticMapping)
                if staticNames:
                    for name in staticNames:
                        sources[name[1]] = iconPath
                else:
                    name = buildResourceKey(filename, osextra.path.fullsplit(dirpath), sources)
                    sources[name] = iconPath
        return sources
    resources = {}
    for source in [ "Icons", "Images" ]:
        resources[source] = loadSourcePath(os.path.join(resourcesPath, source))
    return resources

def loadPrymatexResources(resourcesPath, themeName = "oxygen"):
    global RESOURCES, RESOURCES_READY
    if not RESOURCES_READY:
        themesPath = os.path.join(resourcesPath, "IconThemes")
        #Test icon theme:
        if not QtGui.QIcon.hasThemeIcon(THEME_ICON_TEST):
            #Add icon theme
            QtGui.QIcon.setThemeSearchPaths([ themesPath ])
            QtGui.QIcon.setThemeName(themeName)
        RESOURCES = loadResources(resourcesPath, STATICMAPPING)
        installCustomFromThemeMethod()
        RESOURCES_READY = True
        
def installCustomFromThemeMethod():
    #Install fromTheme custom function
    QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
    QtGui.QIcon.fromTheme = staticmethod(getIcon)
    
    
#===============================================================
# PRYMATEX STYLES
# http://developer.qt.nokia.com/doc/qt-4.8/stylesheet-reference.html
#===============================================================

APPLICATION_STYLE = """
QTreeView {
    font-size: 11px;
}
QTreeView::item {
    padding: 1px;
}
QTableView {
    font-size: 11px;
}
QListView {
     font-size: 11px;
}
QListView::item {
    padding: 1px;    
}
"""

# TODO: Take colors from Theme rather than HARDCODING
FIND_NO_MATCH_STYLE = 'background-color: red; color: #fff;'
FIND_MATCH_STYLE = 'background-color: #dea;'

#===============================================================
# FUNCTIONS
#===============================================================
def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)

def registerImagePath(name, path):
    external = RESOURCES.setdefault("External", {})
    external[name] = path
    
class ResourceProvider(dict):
    def getImage(self, index):
        if index in self:
            return QtGui.QPixmap(self[index])
        return getImage(index)
        
    def getIcon(self, index):
        if index in self:
            return QtGui.QIcon(self[index])
        return getIcon(index)
