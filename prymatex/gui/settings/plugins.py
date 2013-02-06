#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.plugins import Ui_Plugins
from prymatex.models.settings import SettingsTreeNode

from prymatex.models.plugins import PluginsTableModel

class PluginsSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Plugins):
    TITLE = "Plugins"
    ICON = resources.getIcon("preferences-plugin-script")
    NAMESPACE = "general"
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "plugins", settingGroup, profile)
        self.setupUi(self)
        
    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        self.model = PluginsTableModel(self.application.pluginManager)
        self.listViewPlugins.setModel(self.model)