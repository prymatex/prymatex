#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .newproject import NewProjectDialog
from .about import AboutDialog
from .selector import SelectorDialog
#from .selector2 import SelectorDialog
from .settings import SettingsDialog
from .bundles import BundleEditorDialog
from .profile import ProfileDialog
from .template import TemplateDialog
from .properties import PropertiesDialog
from .environment import EnvironmentDialog

def registerPlugin(manager, descriptor):
    manager.registerComponent(NewProjectDialog)
    manager.registerComponent(AboutDialog)
    manager.registerComponent(SelectorDialog)
    manager.registerComponent(SettingsDialog)
    manager.registerComponent(BundleEditorDialog)
    manager.registerComponent(ProfileDialog)
    manager.registerComponent(TemplateDialog)
    manager.registerComponent(PropertiesDialog)
    manager.registerComponent(EnvironmentDialog)
