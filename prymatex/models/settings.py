#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.configure import ConfigureTreeNode, ConfigureTreeProxyNode, ConfigureTreeModelBase
from prymatex.models.configure import SortFilterConfigureProxyModel as SortFilterSettingsProxyModel

class SettingsTreeNode(ConfigureTreeNode):
    def __init__(self, component_class, **kwargs):
        super(SettingsTreeNode, self).__init__(**kwargs)
        self.component_class = component_class

    def loadSettings(self):
        self.settings = self.component_class.settings
        self.application = self.component_class.application
        for settingsNode in self.children():
            settingsNode.loadSettings()

# Proxy for namespaced models
class SettingsTreeProxyNode(ConfigureTreeProxyNode):
    def loadSettings(self):
        for proxyNode in self.children():
            proxyNode.loadSettings()

class SettingsTreeModel(ConfigureTreeModelBase):
    def treeNodeFactory(self, nodeName, nodeParent=None):
        return SettingsTreeProxyNode(nodeName=nodeName, nodeParent=nodeParent)

    def loadSettings(self):
        self.rootNode.loadSettings()

    
