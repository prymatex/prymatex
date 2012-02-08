#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeNode, TreeModel

class PMXConfigTreeNode(TreeNode):
    def __init__(self, name, parent = None):
        TreeNode.__init__(self, name, parent)

    @property
    def icon(self):
        return QtGui.QIcon()
    
class PMXSettingsModel(TreeModel):  
    def __init__(self, parent = None):
        TreeModel.__init__(self, parent)
    
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return node.icon