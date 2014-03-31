#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.plugins import Ui_Plugins
from prymatex.models.settings import SettingsTreeNode

from prymatex.models.plugins import PluginsTableModel

class PluginsSettingsWidget(SettingsTreeNode, Ui_Plugins, QtGui.QWidget):
    TITLE = "Plugins"
    ICON = resources.get_icon("preferences-plugin-script")
    NAMESPACE = "general"
    
    def __init__(self, **kwargs):
        super(PluginsSettingsWidget, self).__init__(nodeName = "plugins", **kwargs)
        self.setupUi(self)
        
    def loadSettings(self):
        super(PluginsSettingsWidget, self).loadSettings()
        self.pluginManager = PluginsTableModel(self.application.pluginManager)
        self.listViewPlugins.setModel(self.pluginManager)