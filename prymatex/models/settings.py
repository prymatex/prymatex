#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.configure import ConfigureTreeNode, ConfigureTreeProxyNode, ConfigureTreeModelBase
from prymatex.models.configure import SortFilterConfigureProxyModel as SortFilterSettingsProxyModel

class SettingsTreeNode(ConfigureTreeNode):
    def __init__(self, settings = None, profile = None, **kwargs):
        super(SettingsTreeNode, self).__init__(**kwargs)
        self.settings = settings
        self.profile = profile

    def loadSettings(self):
        for settingsNode in self.childNodes():
            settingsNode.loadSettings()

# Proxy for namespaced models
class SettingsTreeProxyNode(ConfigureTreeProxyNode):
    def loadSettings(self):
        for proxyNode in self.childNodes():
            proxyNode.loadSettings()

class SettingsTreeModel(ConfigureTreeModelBase):
    def treeNodeFactory(self, nodeName, nodeParent = None):
        return SettingsTreeProxyNode(
            nodeName = nodeName, nodeParent = nodeParent)

    def loadSettings(self):
        self.rootNode.loadSettings()

    