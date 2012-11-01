#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.gui.dockers.filesystem import PMXFileSystemDock
from prymatex.gui.dockers.browser import PMXBrowserDock
#from prymatex.gui.dockers.externalconsole import ExternalConsole
from prymatex.gui.dockers.projects import PMXProjectDock
from prymatex.gui.dockers.terminal import PMXTerminalDock
from prymatex.gui.dockers.search import PMXSearchDock
from prymatex.gui.dockers.process import PMXProcessDock

from prymatex.gui.dockers import helpers

def registerPlugin(manager):
    manager.registerDocker(PMXProjectDock)
    #manager.registerKeyHelper(PMXProjectDock, helpers.RefreshHelper)
    manager.registerKeyHelper(PMXProjectDock, helpers.PasteHelper)
    manager.registerKeyHelper(PMXProjectDock, helpers.CopyHelper)
    manager.registerKeyHelper(PMXProjectDock, helpers.CutHelper)
    manager.registerKeyHelper(PMXProjectDock, helpers.DeleteHelper)
    manager.registerDocker(PMXFileSystemDock)
    manager.registerDocker(PMXTerminalDock)
    manager.registerDocker(PMXBrowserDock)
    manager.registerDocker(PMXSearchDock)
    manager.registerDocker(PMXProcessDock)
    #manager.registerDocker(ExternalConsole)
