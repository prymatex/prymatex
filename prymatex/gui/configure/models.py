#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeNode, NamespaceTreeModel

#=========================================
# Configure Model
#=========================================
class PMXConfigureTreeNode(TreeNode):
    NAMESPACE = ""
    ICON = QtGui.QIcon()
    TITLE = ""
    def __init__(self, name, parent = None):
        TreeNode.__init__(self, name, parent)
        self.__title = self.TITLE
        self.__icon = self.ICON
        
    def filterString(self):
        return self.name + self.title + reduce(lambda initial, child: initial + child.filterString(), self.childrenNodes, "")

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        self.__title = title
    
    @property
    def icon(self):
        return self.__icon
    
    @icon.setter
    def icon(self, icon):
        self.__icon = icon

class PMXConfigureTreeModel(NamespaceTreeModel):
    def __init__(self, parent = None):
        NamespaceTreeModel.__init__(self, separator = ".", parent = parent)

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def addConfigNode(self, node):
        self.addNamespaceNode(node.NAMESPACE, node)