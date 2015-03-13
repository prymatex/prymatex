#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .newproject import NewProjectDialog
from .about import AboutDialog
from .selector import SelectorDialog
#from .selector2 import SelectorDialog
from .settings import SettingsDialog
from .bundles import BundleEditorDialog, BundleFilterDialog
from .profile import ProfileDialog
from .template import TemplateDialog
from .properties import PropertiesDialog
from .environment import EnvironmentDialog

__plugin__.registerComponent(NewProjectDialog)
__plugin__.registerComponent(AboutDialog)
__plugin__.registerComponent(BundleFilterDialog)
__plugin__.registerComponent(SelectorDialog)
__plugin__.registerComponent(SettingsDialog)
__plugin__.registerComponent(BundleEditorDialog)
__plugin__.registerComponent(ProfileDialog)
__plugin__.registerComponent(TemplateDialog)
__plugin__.registerComponent(PropertiesDialog)
__plugin__.registerComponent(EnvironmentDialog)
