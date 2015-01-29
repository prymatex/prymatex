#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.extensions import ContextKeySequence

from prymatex.models.trees import AbstractNamespaceTreeModel, TreeNodeBase

class ContextTreeNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)
        self.sequence = QtGui.QKeySequence()

    def keySequence(self):
        return self.sequence

    def description(self):
        return ""
        
class ContextKeySequenceTreeNode(TreeNodeBase):
    def __init__(self, sequence, parent = None):
        TreeNodeBase.__init__(self, sequence.name(), parent)
        self.sequence = sequence
        self.qobjects = []

    def _set_shortcut(self, qobject):
        if isinstance(qobject, QtWidgets.QAction):
            qobject.setShortcut(self.sequence)
        elif isinstance(qobject, QtWidgets.QShortcut):
            qobject.setKey(self.sequence)
            
    def registerObject(self, qobject):
        self.qobjects.append(qobject)
        self._set_shortcut(qobject)

    def keySequence(self):
        return self.sequence
    
    def setKeySequence(self, sequence):
        self.sequence.swap(sequence)
        for qobject in self.qobjects:
            self._set_shortcut(qobject)

    def description(self):
        return self.sequence.description()

class ShortcutsTreeModel(AbstractNamespaceTreeModel):
    def __init__(self, parent=None):
        AbstractNamespaceTreeModel.__init__(self, separator=".", parent=parent)

    def loadStandardSequences(self, resources):
        for name in dir(QtGui.QKeySequence):
            if isinstance(getattr(QtGui.QKeySequence, name), QtGui.QKeySequence.StandardKey):
                node = self.nodeForNamespace("Global.%s" % name)
                if node is None:
                    sequence = ContextKeySequence("Global", name)
                    node = ContextKeySequenceTreeNode(sequence)
                    self.insertNamespaceNode(sequence.context(), node)

    def registerShortcut(self, qobject, sequence):
        node = self.nodeForNamespace(sequence.identifier())
        if node is None:
            node = ContextKeySequenceTreeNode(sequence)
            self.insertNamespaceNode(sequence.context(), node)
        node.registerObject(qobject)

    def _applyShortcuts(self):
        """Apply shortcuts settings to all widgets/plugins
        """
        # TODO Usar los item del tree
        toberemoved = []
        for index, (qobject, sequence) in enumerate(self.shortcuts):
            try:
                if isinstance(qobject, QtWidgets.QAction):
                    qobject.setShortcut(sequence)
                elif isinstance(qobject, QtWidgets.QShortcut):
                    qobject.setKey(sequence)
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
                return node.keySequence().toString()
