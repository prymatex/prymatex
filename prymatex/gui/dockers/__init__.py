#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .filesystem import FileSystemDock
from .browser import BrowserDock
from .projects import ProjectDock
from .terminal import TerminalDock
from .search import PMXSearchDock
from .process import PMXProcessDock

def registerPlugin(manager):
    manager.registerComponent(ProjectDock)
    manager.registerComponent(FileSystemDock)
    manager.registerComponent(TerminalDock)
    manager.registerComponent(BrowserDock)
    manager.registerComponent(PMXSearchDock)
    manager.registerComponent(PMXProcessDock)
