#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .filesystem import FileSystemDock
from .browser import BrowserDock
from .projects import ProjectsDock
from .terminal import TerminalDock
from .search import SearchResultsDock
from .process import PMXProcessDock

def registerPlugin(manager):
    manager.registerComponent(ProjectsDock)
    manager.registerComponent(FileSystemDock)
    manager.registerComponent(TerminalDock)
    manager.registerComponent(BrowserDock)
    manager.registerComponent(SearchResultsDock)
    manager.registerComponent(PMXProcessDock)
