#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.support import Ui_Support
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _

class SupportSettingsWidget(SettingsTreeNode, Ui_Support, QtGui.QWidget):
    def __init__(self, **kwargs):
        super(SupportSettingsWidget, self).__init__(nodeName = "support", **kwargs)
        self.setupUi(self)
        self.setTitle("Support")
        self.setIcon(self.resources().get_icon("gears")
