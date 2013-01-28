#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.support import Ui_Support
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _

class PMXSupportSettings(QtGui.QWidget, SettingsTreeNode, Ui_Support):
    ICON = resources.getIcon('gear')
    TITLE = "Support"
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "support", settingGroup, profile)
        self.setupUi(self)