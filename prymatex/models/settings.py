#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.configure import ConfigureTreeNode, ProxyConfigureTreeNode, ConfigureTreeModelBase
from prymatex.models.configure import SortFilterConfigureProxyModel as SortFilterSettingsProxyModel

class SettingsTreeNode(ConfigureTreeNode):
    def __init__(self, group = None, **kwargs):
        super(SettingsTreeNode, self).__init__(**kwargs)
        self.settingGroup = group

    def loadSettings(self):
        print("cargando")
        for node in self.childNodes():
            node.loadSettings()

# Proxy for namespaced models
class ProxySettingsTreeNode(ProxyConfigureTreeNode):
    def loadSettings(self):
        for node in self.childNodes():
            node.loadSettings()

class SettingsTreeModel(ConfigureTreeModelBase):
    def treeNodeFactory(self, nodeName, nodeParent = None):
        return ProxySettingsTreeNode(
            nodeName = nodeName, nodeParent = nodeParent)

    def loadSettings(self):
        self.rootNode.loadSettings()

    