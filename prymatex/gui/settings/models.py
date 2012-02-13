#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.models.tree import TreeNode, TreeModel

class PMXSettingTreeNode(TreeNode):
    NAMESPACE = ""
    ICON = QtGui.QIcon()
    TITLE = ""
    def __init__(self, name, settingGroup = None, parent = None):
        TreeNode.__init__(self, name, parent)
        self.settingGroup = settingGroup
        self.__title = self.TITLE
        self.__icon = self.ICON
        
    def filterString(self):
        return self.name + self.title + reduce(lambda initial, child: initial + child.filterString(), self.childrenNodes, "")

    def loadSettings(self):
        pass

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

class PMXProxySettingTreeNode(PMXSettingTreeNode):
    def __init__(self, name, parent = None):
        PMXSettingTreeNode.__init__(self, name, parent = parent)
        self.title = self.name.title()

class PMXSettingsModel(TreeModel):  
    def __init__(self, parent = None):
        TreeModel.__init__(self, parent)
    
    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def nodeForNamespace(self, namespace, createProxy = False):
        node = self.rootNode
        names = namespace.split(".")
        for name in names:
            if name != "":
                nextNode = node.findChildByName(name)
                if nextNode is None and createProxy:
                    nextNode = PMXProxySettingTreeNode(name, node)
                    node.appendChild(nextNode)
                    self.layoutChanged.emit()
                elif nextNode is None:
                    return None
                node = nextNode
        return node
    
    def addSetting(self, setting):
        node = self.nodeForNamespace(setting.NAMESPACE, True)
        index = self.createIndex(node.row(), 0, node) if not node.isRootNode() else QtCore.QModelIndex()
        #Check if exit proxy for setting
        proxy = node.findChildByName(setting.name)
        if proxy != None:
            #Reparent
            for child in proxy.childrenNodes:
                setting.appendChild(child)
            proxy.parentNode.removeChild(proxy)
            self.layoutChanged.emit()
        self.beginInsertRows(index, node.childCount(), node.childCount())
        node.appendChild(setting)
        self.endInsertRows()
        
class PMXSettingsProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            return regexp.indexIn(node.filterString()) != -1
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        return True

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    