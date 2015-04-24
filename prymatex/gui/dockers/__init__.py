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

__prymatex__.registerComponent(ProjectsDock)
__prymatex__.registerComponent(FileSystemDock)
#__prymatex__.registerComponent(TerminalDock)
__prymatex__.registerComponent(ConsoleDock)
__prymatex__.registerComponent(BrowserDock)
__prymatex__.registerComponent(SearchResultsDock)
__prymatex__.registerComponent(ExternalProcessDock)
