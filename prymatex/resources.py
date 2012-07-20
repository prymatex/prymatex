#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore

from prymatex import resources_rc
from prymatex.utils.decorators.memoize import memoized

#===============================================================
# IMAGES AND ICONS
#===============================================================

INTERNAL = {
    #Bundles
    "bundle-item-bundle": ":/items/bundles/bundle.png",
    "bundle-item-template": ":/items/bundles/templates.png",
    "bundle-item-command": ":/items/bundles/commands.png",
    "bundle-item-syntax": ":/items/bundles/languages.png",
    "bundle-item-project": ":/items/bundles/project.png",
    "bundle-item-preference": ":/items/bundles/preferences.png",
    "bundle-item-dragcommand": ":/items/bundles/drag-commands.png",
    "bundle-item-snippet": ":/items/bundles/snippets.png",
    "bundle-item-macro": ":/items/bundles/macros.png",
    "bundle-item-templatefile": ":/items/bundles/template-files.png",
    
    #Editor Sidebar
    "foldingtop": ":/editor/sidebar/folding-top.png",
    "foldingbottom": ":/editor/sidebar/folding-bottom.png",
    "foldingcollapsed": ":/editor/sidebar/folding-collapsed.png",
    "foldingellipsis": ":/editor/sidebar/folding-ellipsis.png",
    "bookmarkflag": ":/editor/sidebar/bookmark-flag.png",
    
    #Icons
    "save": ":/icons/actions/document-save.png",
    "inserttext": ":/icons/actions/insert-text.png",
    "codefunction": ":/icons/actions/code-function.png",
    "codevariable": ":/icons/actions/code-variable.png",
    "projectnew": ":/icons/actions/project-development-new-template.png",
    "projectopen": ":/icons/actions/project-open.png",
    "projectclose": ":/icons/actions/project-development-close.png",
    "important": ":/icons/emblems/emblem-important.png",
    "stack-open": ":/icons/emblems/image-stack-open.png",
    "stack": ":/icons/emblems/image-stack.png",    

    "gearfile": ":/icons/actions/run-build-file.png",
    "gearconfigure": ":/icons/actions/run-build-configure.png",
    "textcolor": ":/icons/actions/format-text-color.png",
    
    # For menus
    "close":":/icons/actions/document-close.png", 
    "closeall":":/icons/actions/project-development-close-all.png",
    "copy":":/icons/actions/edit-copy.png",
    "find":":/icons/actions/edit-find.png",

    # Bullets
    "bulletred": ":/icons/icons/bullet-red.png",
    "bulletblue": ":/icons/icons/bullet-blue.png",
    "bulletgreen": ":/icons/icons/bullet-green.png",
    
    # For Dock
    "terminal":":/icons/apps/utilities-terminal.png", 
    "browser":":/icons/apps/internet-web-browser.png",
    "filemanager":":/icons/apps/system-file-manager.png",
    "project": ":/icons/actions/project-development.png",
    "bookmark": ":/icons/actions/rating.png",
    "symbols": ":/icons/actions/code-context.png",
    "console": ":/icons/dockers/console.png",
    
    # Scope Root Groups
    "scope-root-comment": ":/bullets/groups/blue.png",
    "scope-root-constant": ":/bullets/groups/yellow.png",
    "scope-root-entity": ":/bullets/groups/ligthblue.png",
    "scope-root-invalid": ":/bullets/groups/red.png",
    "scope-root-keyword": ":/bullets/groups/green.png",
    "scope-root-markup": ":/bullets/groups/violet.png",
    "scope-root-meta": ":/bullets/groups/darkviolet.png",
    "scope-root-storage": ":/bullets/groups/gray.png",
    "scope-root-string": ":/bullets/groups/darkgreen.png",
    "scope-root-support": ":/bullets/groups/brown.png",
    "scope-root-variable": ":/bullets/groups/orange.png"
}

EXTERNAL = {}

PLUGINS = {}

FileIconProvider = QtGui.QFileIconProvider()

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

FIND_NO_MATCH_STYLE = 'background-color: red; color: #fff;'
FIND_MATCH_STYLE = 'background-color: #dea;'

#===============================================================
# FUNCTIONS
#===============================================================

def getImagePath(index):
    return INTERNAL.get(index) or EXTERNAL.get(index)

@memoized
def getImage(index):
    path = getImagePath(index)
    if path is not None:
        return QtGui.QPixmap(path)

@memoized
def getIcon(index):
    '''
    Makes the best effort to find an icon for an index.
    Index can be a path, a Qt resource path, an integer.
    @return: QIcon instance or None if no icon could be retrieved
    '''
    #Try icon in db
    path = getImagePath(index)
    if path is not None:
        return QtGui.QIcon(path)
    elif isinstance(index, basestring):
        #Try file path
        if os.path.isfile(index):
            return FileIconProvider.icon(QtCore.QFileInfo(index))
        elif os.path.isdir(index):
            return FileIconProvider.icon(QtGui.QFileIconProvider.Folder)
        return FileIconProvider.icon(QtGui.QFileIconProvider.File)
    elif isinstance(index, int):
        #Try icon by int index in fileicon provider
        return FileIconProvider.icon(index)

def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)

def registerImagePath(index, path):
    EXTERNAL[index] = path
    
class ResourceProvider(dict):
    def getImage(self, index):
        if index in self:
            return QtGui.QPixmap(self[index])
        return getImage(index)
        
    def getIcon(self, index):
        if index in self:
            return QtGui.QIcon(self[index])
        return getIcon(index)
    