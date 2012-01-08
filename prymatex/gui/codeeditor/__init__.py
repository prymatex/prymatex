# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PyQt4 import QtCore

from prymatex.gui.codeeditor.dockers import PMXCodeBookmarksDock, PMXCodeSymbolsDock
from prymatex.gui.codeeditor.editor import PMXCodeEditor

def setup(manager):
    manager.registerEditor(PMXCodeEditor)
    manager.registerDocker(PMXCodeBookmarksDock, QtCore.Qt.RightDockWidgetArea)
    manager.registerDocker(PMXCodeSymbolsDock, QtCore.Qt.RightDockWidgetArea)
    #manager.registerAddon(KeyEquivalentHelper, PMXCodeEditor)
    #manager.loadResources(__file__)