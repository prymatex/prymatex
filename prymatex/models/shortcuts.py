#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.models.trees import AbstractNamespaceTreeModel, TreeNodeBase

class ContextTreeNode(TreeNodeBase):
    def __init__(self, name, parent = None):
        TreeNodeBase.__init__(self, name, parent)

    def keySequence(self):
        return None

    def description(self):
        return None
        
class ContextKeySequenceTreeNode(TreeNodeBase):
    def __init__(self, context_sequence, parent = None):
        TreeNodeBase.__init__(self, context_sequence.name, parent)
        self.context_sequence = context_sequence
        self.qobjects = []

    def registerObject(self, qobject):
        if isinstance(qobject, QtWidgets.QAction):
            qobject.setShortcut(self.context_sequence.keySequence())
        elif isinstance(qobject, QtWidgets.QShortcut):
            qobject.setKey(self.context_sequence.keySequence())
        self.qobjects.append(qobject)

    def keySequence(self):
        return self.context_sequence.keySequence()
    
    def setKeySequence(self, sequence):
        print(sequence)

    def description(self):
        return self.context_sequence.description

class ShortcutsTreeModel(AbstractNamespaceTreeModel):
    def __init__(self, parent = None):
        AbstractNamespaceTreeModel.__init__(self, separator = ".", parent = parent)

    def loadStandardSequences(self, resources):
        for name in dir(QtGui.QKeySequence):
            if isinstance(getattr(QtGui.QKeySequence, name), QtGui.QKeySequence.StandardKey):
                node = self.nodeForNamespace("Global.%s" % name)
                if node is None:
                    context_sequence = resources.get_context_sequence("Global", name)
                    node = ContextKeySequenceTreeNode(context_sequence)
                    self.insertNamespaceNode(context_sequence.context, node)

    def registerShortcut(self, qobject, context_sequence):
        node = self.nodeForNamespace(context_sequence.fullName())
        if node is None:
            node = ContextKeySequenceTreeNode(context_sequence)
            self.insertNamespaceNode(context_sequence.context, node)
        node.registerObject(qobject)

    def applyShortcuts(self):
        """Apply shortcuts settings to all widgets/plugins
        """
        # TODO Usar los item del tree
        toberemoved = []
        for index, (qobject, context_sequence) in enumerate(self.shortcuts):
            try:
                if isinstance(qobject, QtWidgets.QAction):
                    qobject.setShortcut(context_sequence.keySequence())
                elif isinstance(qobject, QtWidgets.QShortcut):
                    qobject.setKey(context_sequence.keySequence())
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
                return node.keySequence()
