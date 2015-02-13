#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .filesystem import FileSystemDock
from .browser import BrowserDock
from .projects import ProjectsDock
from .terminal import TerminalDock
from .console import ConsoleDock
from .search import SearchResultsDock
from .process import ExternalProcessDock

def registerPlugin(manager, descriptor):
    manager.registerComponent(ProjectsDock)
    manager.registerComponent(FileSystemDock)
    manager.registerComponent(TerminalDock)
    manager.registerComponent(ConsoleDock)
    manager.registerComponent(BrowserDock)
    manager.registerComponent(SearchResultsDock)
    manager.registerComponent(ExternalProcessDock)
