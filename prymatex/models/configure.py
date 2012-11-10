#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.trees import TreeNodeBase
from prymatex.models.trees import AbstractNamespaceTreeModel

#=========================================
# Nodes and Models
#=========================================
class ConfigureTreeNode(TreeNodeBase):
    NAMESPACE = ""
    ICON = QtGui.QIcon()
    TITLE = ""
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)
        self.setTitle(self.TITLE)
        self.setIcon(self.ICON)
        
    def filterString(self):
        return self.nodeName() + self.title() + reduce(lambda initial, child: initial + child.filterString(), self.childrenNodes, "")

    def title(self):
        return self.__title
    
    def setTitle(self, title):
        self.__title = title
    
    def icon(self):
        return self.__icon
    
    def setIcon(self, icon):
        self.__icon = icon

# Proxy for namespaced models
class ProxyConfigureTreeNode(QtGui.QWidget, ConfigureTreeNode):
    def __init__(self, name, parent):
        QtGui.QWidget.__init__(self)
        ConfigureTreeNode.__init__(self, name, parent)
        self.setObjectName(name.title() + "Widget")

class ConfigureTreeModelBase(AbstractNamespaceTreeModel):
    def __init__(self, parent = None):
        AbstractNamespaceTreeModel.__init__(self, separator = ".", parent = parent)

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()

    def addConfigNode(self, node):
        self.insertNamespaceNode(node.NAMESPACE, node)
       
class ConfigureTreeModel(ConfigureTreeModelBase):
    proxyConfigureCreated = QtCore.pyqtSignal(object)
    def treeNodeFactory(self, nodeName, nodeParent = None):
        proxy = ProxyConfigureTreeNode(nodeName, nodeParent)
        self.proxyConfigureCreated.emit(proxy)
        return proxy
        
#=========================================
# Proxies
#=========================================
class SortFilterConfigureProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            return regexp.indexIn(node.filterString()) != -1
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        return True

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)