#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from prymatex.gui.dockers.filesystem import PMXFileSystemDock
from prymatex.gui.dockers.browser import BrowserDock
from prymatex.gui.dockers.projects import ProjectDock
from prymatex.gui.dockers.terminal import TerminalDock
from prymatex.gui.dockers.search import PMXSearchDock
from prymatex.gui.dockers.process import PMXProcessDock

def registerPlugin(manager):
    manager.registerDocker(ProjectDock)
    manager.registerDocker(PMXFileSystemDock)
    manager.registerDocker(TerminalDock)
    manager.registerDocker(BrowserDock)
    manager.registerDocker(PMXSearchDock)
    manager.registerDocker(PMXProcessDock)
