#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.models.trees import TreeNodeBase
from prymatex.models.trees import AbstractNamespaceTreeModel
import collections

#=========================================
# Nodes and Models
#=========================================
class ConfigureTreeNode(TreeNodeBase):
    NAMESPACE = ""
    def __init__(self, **kwarg):
        super(ConfigureTreeNode, self).__init__(**kwarg)
        self._icon = QtGui.QIcon()
        self._title = ""
        
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
        return self._title
    
    def setTitle(self, title):
        self._title = title
    
    def icon(self):
        return self._icon
    
    def setIcon(self, icon):
        self._icon = icon

# Proxy for namespaced models
class ConfigureTreeProxyNode(ConfigureTreeNode, QtWidgets.QWidget):
    def __init__(self, **kwarg):
        super(ConfigureTreeProxyNode, self).__init__(**kwarg)
        self.setObjectName(self.nodeName().title() + " Widget")

class ConfigureTreeModelBase(AbstractNamespaceTreeModel):
    def __init__(self, **kwargs):
        super(ConfigureTreeModelBase, self).__init__(separator = ".", **kwargs)

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
class SortFilterConfigureProxyModel(QtCore.QSortFilterProxyModel):
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
