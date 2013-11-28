#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.trees import AbstractNamespaceTreeModel, TreeNodeBase

class ContextTreeNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)

    def shortcut(self):
        return None

    def description(self):
        return None
        
class ContextSequenceTreeNode(TreeNodeBase):
    def __init__(self, sequence, parent = None):
        TreeNodeBase.__init__(self, sequence.name, parent)
        self.sequence = sequence

    def shortcut(self):
        return self.sequence.key()
    
    def description(self):
        return self.sequence.description

class ShortcutsTreeModel(AbstractNamespaceTreeModel):
    def __init__(self, parent = None):
        AbstractNamespaceTreeModel.__init__(self, separator = ".", parent = parent)
        self.shortcuts = []
    
    def registerShortcut(self, qobject, sequence):
        self.shortcuts.append( (qobject, sequence) )
        if isinstance(qobject, QtGui.QAction):
            qobject.setShortcut(sequence.key())
        elif isinstance(qobject, QtGui.QShortcut):
            qobject.setKey(sequence.key())

        node = self.nodeForNamespace(sequence.fullName())
        if node is None:
            self.insertNamespaceNode(sequence.context, ContextSequenceTreeNode(sequence))
        else:
            print("Agregar el objeto")

    def applyShortcuts(self):
        """Apply shortcuts settings to all widgets/plugins"""
        toberemoved = []
        for index, (qobject, sequence) in enumerate(self.shortcuts):
            try:
                if isinstance(qobject, QtGui.QAction):
                    qobject.setShortcut(sequence.key())
                elif isinstance(qobject, QtGui.QShortcut):
                    qobject.setKey(sequence.key())
            except RuntimeError:
                # Object has been deleted
                toberemoved.append(index)
        for index in sorted(toberemoved, reverse=True):
            self.shortcuts.pop(index)

    def treeNodeFactory(self, name, parent = None):
        return ContextTreeNode(name, parent)
        
    # -------------- Override Tree Methods
    def columnCount(self, parentIndex):
        return 3
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Command"
                elif section == 1:
                    return "Description"
                elif section == 2:
                    return "Shortcut"
    
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.nodeName()
            elif index.column() == 1:
                return node.description()
            elif index.column() == 2:
                return node.shortcut()
