#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.gui.dialogs.project import ProjectDialog
from prymatex.gui.dialogs.about import AboutDialog
from prymatex.gui.dialogs.selector import SelectorDialog
from prymatex.gui.dialogs.settings import SettingsDialog
from prymatex.gui.dialogs.bundles import BundleEditorDialog
from prymatex.gui.dialogs.profile import ProfileDialog


def registerPlugin(manager):
    manager.registerDialog(ProjectDialog)
    manager.registerDialog(AboutDialog)
    manager.registerDialog(SelectorDialog)
    manager.registerDialog(SettingsDialog)
    manager.registerDialog(BundleEditorDialog)
    manager.registerDialog(ProfileDialog)


    