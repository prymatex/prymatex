#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.support import Ui_Support
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _

class SupportSettingsWidget(SettingsTreeNode, Ui_Support, QtGui.QWidget):
    ICON = resources.getIcon('gear')
    TITLE = "Support"
    def __init__(self, **kwargs):
        super(SupportSettingsWidget, self).__init__(nodeName = "support", **kwargs)
        self.setupUi(self)