#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from prymatex import resources_rc

IMAGES = {
    #BUNDLES
    "template": QtGui.QPixmap(":/icons/bundles/templates.png"),
    "command": QtGui.QPixmap(":/icons/bundles/commands.png"),
    "syntax": QtGui.QPixmap(":/icons/bundles/languages.png"),
    "preference": QtGui.QPixmap(":/icons/bundles/preferences.png"),
    "dragcommand": QtGui.QPixmap(":/icons/bundles/drag-commands.png"),
    "snippet": QtGui.QPixmap(":/icons/bundles/snippets.png"),
    "macro": QtGui.QPixmap(":/icons/bundles/macros.png"),
    "templatefile": QtGui.QPixmap(":/icons/bundles/template-files.png"),
    "foldingtop": QtGui.QPixmap(":/editor/sidebar/folding-top.png"),
    "foldingbottom": QtGui.QPixmap(":/editor/sidebar/folding-bottom.png"),
    "foldingcollapsed": QtGui.QPixmap(":/editor/sidebar/folding-collapsed.png"),
    "foldingellipsis": QtGui.QPixmap(":/editor/sidebar/folding-ellipsis.png"),
    "bookmarkflag": QtGui.QPixmap(":/editor/sidebar/bookmark-flag.png")
}

ICONS = {
    "save": QtGui.QIcon(":/icons/actions/document-save.png"),
    "inserttext": QtGui.QIcon(":/icons/actions/insert-text.png"),
}
