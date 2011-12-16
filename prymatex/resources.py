#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from prymatex import resources_rc

IMAGES = {
    #Bundles
    "template": ":/icons/bundles/templates.png",
    "command": ":/icons/bundles/commands.png"),
    "syntax": ":/icons/bundles/languages.png"),
    "preference": ":/icons/bundles/preferences.png"),
    "dragcommand": ":/icons/bundles/drag-commands.png"),
    "snippet": ":/icons/bundles/snippets.png"),
    "macro": ":/icons/bundles/macros.png"),
    "templatefile": ":/icons/bundles/template-files.png"),
    #Editor Sidebar
    "foldingtop": ":/editor/sidebar/folding-top.png"),
    "foldingbottom": ":/editor/sidebar/folding-bottom.png"),
    "foldingcollapsed": ":/editor/sidebar/folding-collapsed.png"),
    "foldingellipsis": ":/editor/sidebar/folding-ellipsis.png"),
    "bookmarkflag": ":/editor/sidebar/bookmark-flag.png"),
    #Icons
    "save": ":/icons/actions/document-save.png"),
    "inserttext": ":/icons/actions/insert-text.png"),
    "codefunction": ":/icons/actions/code-function.png"),
    "projectnew": ":/icons/actions/project-development-new-template.png"),
    "projectopen": ":/icons/actions/project-open.png"),
    "projectclose": ":/icons/actions/project-development-close.png"),
}

FileIconProvider = QtGui.QFileIconProvider()

def getImage(index):
    if isinstance(index, (str, unicode)) and index in IMAGES:
        return QtGui.QPixmap(IMAGES[index])

def getIcon(index):
    if isinstance(index, (str, unicode)) and index in IMAGES:
        return QtGui.QIcon(IMAGES[index])
    elif isinstance(index, QtCore.QFileInfo):
        if fileInfo.exists():
            return FileIconProvider.icon(fileInfo)
        return FileIconProvider.icon(QtGui.QFileIconProvider.File)
    elif isinstance(index, int):
        return FileIconProvider.icon(index)

def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)
