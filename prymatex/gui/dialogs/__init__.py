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

__prymatex__.registerComponent(NewProjectDialog)
__prymatex__.registerComponent(AboutDialog)
__prymatex__.registerComponent(BundleFilterDialog)
__prymatex__.registerComponent(SelectorDialog)
__prymatex__.registerComponent(SettingsDialog)
__prymatex__.registerComponent(BundleEditorDialog)
__prymatex__.registerComponent(ProfileDialog)
__prymatex__.registerComponent(TemplateDialog)
__prymatex__.registerComponent(PropertiesDialog)
__prymatex__.registerComponent(EnvironmentDialog)
