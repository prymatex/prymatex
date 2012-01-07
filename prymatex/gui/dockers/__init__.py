#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.gui.dockers.filesystem import PMXFileSystemDock
from prymatex.gui.dockers.browser import PMXBrowserDock
from prymatex.gui.dockers.console import PMXConsoleDock
from prymatex.gui.dockers.logger import QtLogHandler, PMXLoggerDock
from prymatex.gui.dockers.projects import PMXProjectDock

def setup(manager):
    manager.registerDocker(PMXFileSystemDock, QtCore.Qt.LeftDockWidgetArea)
    manager.registerDocker(PMXBrowserDock, QtCore.Qt.BottomDockWidgetArea)
    manager.registerDocker(PMXConsoleDock, QtCore.Qt.BottomDockWidgetArea)
    manager.registerDocker(QtLogHandler, QtCore.Qt.BottomDockWidgetArea)
    manager.registerDocker(PMXLoggerDock, QtCore.Qt.BottomDockWidgetArea)
    manager.registerDocker(PMXProjectDock, QtCore.Qt.LeftDockWidgetArea)