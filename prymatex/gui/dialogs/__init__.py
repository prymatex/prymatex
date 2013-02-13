#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .project import ProjectDialog
from .about import AboutDialog
from .selector import SelectorDialog
from .settings import SettingsDialog
from .bundles import BundleEditorDialog
from .profile import ProfileDialog
from .template import TemplateDialog
from .properties import PropertiesDialog

def registerPlugin(manager):
    manager.registerDialog(ProjectDialog)
    manager.registerDialog(AboutDialog)
    manager.registerDialog(SelectorDialog)
    manager.registerDialog(SettingsDialog)
    manager.registerDialog(BundleEditorDialog)
    manager.registerDialog(ProfileDialog)
    manager.registerDialog(TemplateDialog)
    manager.registerDialog(PropertiesDialog)
