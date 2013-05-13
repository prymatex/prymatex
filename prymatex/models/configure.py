#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.trees import TreeNodeBase
from prymatex.models.trees import AbstractNamespaceTreeModel
import collections

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
        
    def filterAcceptsNode(self, string):
        string = string.lower()
        if string in (self.nodeName() + self.title()).lower():
            return True
        for child in self.childNodes():
            if child.filterAcceptsNode(string):
                return True
        textItems = [value for value in [getattr(self, key) for key in dir(self)] if isinstance(getattr(value, "text", None), collections.Callable)]
        for item in textItems:
            if string in item.text().lower():
                return True
        return False
    
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

    def __collect_nodes(self, parentNode):
        nodes = [ parentNode ]
        for node in parentNode.childNodes():
            nodes.extend(self.__collect_nodes(node))
        return nodes

    def configNodes(self):
        return self.__collect_nodes(self.rootNode)

        
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
            return node.filterAcceptsNode(regexp.pattern())
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        return True

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
        
    def configNodes(self):
        return self.sourceModel().configNodes()