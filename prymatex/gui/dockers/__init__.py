#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .filesystem import PMXFileSystemDock
from .browser import BrowserDock
from .projects import ProjectDock
from .terminal import TerminalDock
from .search import PMXSearchDock
from .process import PMXProcessDock

def registerPlugin(manager):
    manager.registerDocker(ProjectDock)
    manager.registerDocker(PMXFileSystemDock)
    manager.registerDocker(TerminalDock)
    manager.registerDocker(BrowserDock)
    manager.registerDocker(PMXSearchDock)
    manager.registerDocker(PMXProcessDock)
