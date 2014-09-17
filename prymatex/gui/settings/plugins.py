#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.plugins import Ui_Plugins
from prymatex.models.settings import SettingsTreeNode

from prymatex.models.plugins import PluginsTableModel

class PluginsSettingsWidget(SettingsTreeNode, Ui_Plugins, QtWidgets.QWidget):
    NAMESPACE = "general"
    
    def __init__(self, **kwargs):
        super(PluginsSettingsWidget, self).__init__(nodeName = "plugins", **kwargs)
        self.setupUi(self)
        self.setTitle("Plugins")
        self.setIcon(self.resources().get_icon("settings-plugins"))

    def loadSettings(self):
        super(PluginsSettingsWidget, self).loadSettings()
        self.pluginManager = PluginsTableModel(self.application().pluginManager)
        self.listViewPlugins.setModel(self.pluginManager)
