#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.configure import ConfigureTreeNode, ProxyConfigureTreeNode, ConfigureTreeModelBase
from prymatex.models.configure import SortFilterConfigureProxyModel

#=========================================
# Properties Tree Node
#=========================================
class PropertyTreeNode(ConfigureTreeNode):
    def __init__(self, name, parent = None):
        ConfigureTreeNode.__init__(self, name, parent)

    def acceptFileSystemItem(self, fileSystemItem):
        return True
        
    def edit(self, fileSystemItem):
        pass

    def saveChanges(self):
        pass

class ProxyPropertyTreeNode(ProxyConfigureTreeNode):
    def acceptFileSystemItem(self, fileSystemItem):
        return True
        
    def edit(self, fileSystemItem):
        pass

    def saveChanges(self):
        pass

class PropertiesTreeModel(ConfigureTreeModelBase):
    def treeNodeFactory(self, nodeName, nodeParent = None):
        return ProxyPropertyTreeNode(nodeName, nodeParent)


# Proxy for namespaced models
class PropertiesProxyModel(SortFilterConfigureProxyModel):
    def __init__(self, parent = None):
        SortFilterConfigureProxyModel.__init__(self, parent)
        self.fileSystemItem = None
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        if self.fileSystemItem is None:
            return False
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        if not node.acceptFileSystemItem(self.fileSystemItem):
            return False
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            return regexp.indexIn(node.filterString()) != -1
        return True
    
    def setFilterFileSystem(self, fileSystemItem):
        self.fileSystemItem = fileSystemItem
        self.setFilterRegExp("")
    