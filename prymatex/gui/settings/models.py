#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeNode, TreeModel

class PMXSettingTreeNode(TreeNode):
    def __init__(self, settingGroup, name, parent = None):
        TreeNode.__init__(self, name, parent)
        self.settingGroup = settingGroup

    def setInstance(self, instance):
        self.instance = instance

    @property
    def icon(self):
        return QtGui.QIcon()
    
class PMXSettingsModel(TreeModel):  
    def __init__(self, parent = None):
        TreeModel.__init__(self, parent)
    
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.windowTitle()
        elif role == QtCore.Qt.DecorationRole:
            return node.windowIcon()

    def appendSetting(self, setting):
        self.beginInsertRows(QtCore.QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
        self.rootNode.appendChild(setting)
        self.endInsertRows()
        
class PMXSettingsProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        return True

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    