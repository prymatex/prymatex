#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.gui.dockers.filesystem import PMXFileSystemDock
from prymatex.gui.dockers.browser import PMXBrowserDock
from prymatex.gui.dockers.console import PMXConsoleDock
from prymatex.gui.dockers.logger import PMXLoggerDock
from prymatex.gui.dockers.projects import PMXProjectDock
from prymatex.gui.dockers.terminal import PMXTerminalDock

def registerPlugin(manager):
    manager.registerDocker(PMXFileSystemDock)
    manager.registerDocker(PMXBrowserDock)
    manager.registerDocker(PMXConsoleDock)
    manager.registerDocker(PMXLoggerDock)
    manager.registerDocker(PMXProjectDock)
    manager.registerDocker(PMXTerminalDock)