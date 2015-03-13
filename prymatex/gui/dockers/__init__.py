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

__plugin__.registerComponent(ProjectsDock)
__plugin__.registerComponent(FileSystemDock)
__plugin__.registerComponent(TerminalDock)
__plugin__.registerComponent(ConsoleDock)
__plugin__.registerComponent(BrowserDock)
__plugin__.registerComponent(SearchResultsDock)
__plugin__.registerComponent(ExternalProcessDock)
