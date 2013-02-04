#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.gui.dialogs.project import ProjectDialog
from prymatex.gui.dialogs.about import AboutDialog
from prymatex.gui.dialogs.selector import SelectorDialog

def registerPlugin(manager):
    manager.registerDialog(ProjectDialog)
    manager.registerDialog(AboutDialog)
    manager.registerDialog(SelectorDialog)
