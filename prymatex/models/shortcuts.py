#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.models.trees import AbstractNamespaceTreeModel, TreeNodeBase

from prymatex.utils import osextra

class ContextTreeNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)

class ContextSequenceTreeNode(TreeNodeBase):
    def __init__(self, sequence, parent = None):
        TreeNodeBase.__init__(self, sequence.name, parent)

class ShortcutsTreeModel(AbstractNamespaceTreeModel):
    def treeNodeFactory(self, name, parent = None):
        return ContextTreeNode(name, parent)
        
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.nodeName()
        elif role == QtCore.Qt.DecorationRole:
            return node.icon()

    def addContextSequence(self, sequence):
        self.insertNamespaceNode(sequence.context, ContextSequenceTreeNode(sequence))
