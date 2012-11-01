#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent2keysequence, keysequence2keyequivalent

from prymatex.models.trees import AbstractTreeModel
from prymatex.models.bundles.nodes import BundleItemTreeNode

#====================================================
# Bundle Tree Model
#====================================================
class BundleItemTreeModel(AbstractTreeModel): 
    def __init__(self, manager, parent = None):
        AbstractTreeModel.__init__(self, parent)
        self.manager = manager
        self.manager.bundleChanged.connect(self.on_manager_bundleItemChanged)
        self.manager.bundleItemChanged.connect(self.on_manager_bundleItemChanged)
    
    def on_manager_bundleItemChanged(self, treeNode):
        treeNode.setNodeName(treeNode.item.name)
        index = self.createIndex(treeNode.row(), 0, treeNode)
        self.dataChanged.emit(index, index)
    
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.CheckStateRole:
            node = self.node(index)
            if node.TYPE == "bundle":
                self.manager.disableBundle(node, not value)
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def data(self, index, role):  
        if not index.isValid():  
            return None
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            node = self.node(index)
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            node = self.node(index)
            return node.icon

    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def removeRows(self, position = 0, count = 1,  parent=QtCore.QModelIndex()):
        node = self.node(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.popChild(position)  
        self.endRemoveRows()

    #========================================================================
    # Functions
    #========================================================================
    def appendBundle(self, bundle):
        self.beginInsertRows(QtCore.QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
        self.rootNode.appendChild(bundle)
        self.endInsertRows()
    
    def removeBundle(self, bundle):
        self.beginRemoveRows(QtCore.QModelIndex(), bundle.row(), bundle.row())
        self.rootNode.removeChild(bundle)
        self.endRemoveRows()
    
    def appendBundleItem(self, bundleItem):
        bundle = bundleItem.bundle
        pindex = self.createIndex(bundle.row(), 0, bundle)
        self.beginInsertRows(pindex, bundle.childCount(), bundle.childCount())
        bundle.appendChild(bundleItem)
        self.endInsertRows()
    
    def removeBundleItem(self, bundleItem):
        bundle = bundleItem.bundle
        pindex = self.createIndex(bundle.row(), 0, bundle)
        self.beginRemoveRows(pindex, bundleItem.row(), bundleItem.row())
        bundle.removeChild(bundleItem)
        self.endRemoveRows()
    
    def appendTemplateFile(self, templateFile):
        template = templateFile.template
        pindex = self.createIndex(template.row(), 0, template)
        self.beginInsertRows(pindex, template.childCount(), template.childCount())
        template.appendChild(templateFile)
        self.endInsertRows()

    def removeTemplateFile(self, templateFile):
        template = templateFile.template
        pindex = self.createIndex(template.row(), 0, template)
        self.beginRemoveRows(pindex, templateFile.row(), templateFile.row())
        template.removeChild(templateFile)
        self.endRemoveRows()