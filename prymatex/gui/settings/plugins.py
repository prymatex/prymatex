#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.plugins import Ui_Plugins
from prymatex.models.settings import SettingsTreeNode

class PluginsSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Plugins):
    TITLE = "Plugins"
    ICON = resources.getIcon("preferences-plugin-script")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "plugins", settingGroup)
        self.setupUi(self)