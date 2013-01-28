#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.configure import ConfigureTreeNode, ProxyConfigureTreeNode, ConfigureTreeModelBase
from prymatex.models.configure import SortFilterConfigureProxyModel as SortFilterSettingsProxyModel


class SettingsTreeNode(ConfigureTreeNode):
    def __init__(self, name, settingGroup, profile = None, parent = None):
        ConfigureTreeNode.__init__(self, name, parent)
        self.settingGroup = settingGroup


    def loadSettings(self):
        pass


    @property
    def childrenNodes(self):
        return []


# Proxy for namespaced models
class ProxySettingsTreeNode(ProxyConfigureTreeNode):
    def loadSettings(self):
        pass


class SettingsTreeModel(ConfigureTreeModelBase):
    proxySettingsCreated = QtCore.pyqtSignal(object)
    def treeNodeFactory(self, nodeName, nodeParent = None):
        proxy = ProxySettingsTreeNode(nodeName, nodeParent)
        self.proxySettingsCreated.emit(proxy)
        return proxy