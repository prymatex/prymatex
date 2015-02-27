#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.support import Ui_Support
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _

class SupportSettingsWidget(SettingsTreeNode, Ui_Support, QtGui.QWidget):
    def __init__(self, component_class, **kwargs):
        super(SupportSettingsWidget, self).__init__(component_class, nodeName="support", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(SupportSettingsWidget, self).loadSettings()
        self.setTitle("Support")
        self.setIcon(self.application().resources().get_icon("gears")
