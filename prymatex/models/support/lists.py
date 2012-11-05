#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.utils.lists import bisect_key
from prymatex.models.support.nodes import BundleItemMenuTreeNode

#====================================================
# Themes List Model
#====================================================
class ThemeListModel(QtCore.QAbstractListModel):
    def __init__(self, manager, parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.manager = manager
        self.themes = []
        
    def index(self, row, column = 0, parent = None):
        return self.createIndex(row, column, self.themes[row])
    
    def rowCount (self, parent = None):
        return len(self.themes)

    def data (self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        theme = self.themes[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return theme.name

    def findIndex(self, theme):
        return self.themes.index(theme)
        
    def themeForIndex(self, index):
        return self.themes[index]
        
    # -------------------- Functions -----------------------
    def appendTheme(self, theme):
        index = bisect_key(self.themes, theme, lambda t: t.name)
        self.beginInsertRows(QtCore.QModelIndex(), index, index)
        self.themes.insert(index, theme)
        self.endInsertRows()

    def removeTheme(self, theme):
        index = self.themes.index(theme)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.themes.remove(style)
        self.endRemoveRows()
        
    def getAllItems(self):
        return self.themes
        
#===============================================
# Bundle Excluded Menu List Model
#===============================================
class BundleItemExcludedListModel(QtCore.QAbstractListModel):
    def __init__(self, manager, menuModel):
        QtCore.QAbstractListModel.__init__(self, menuModel)
        self.manager = manager
        self.menuModel = menuModel
        self.submenuNode = BundleItemMenuTreeNode("New Group", BundleItemMenuTreeNode.SUBMENU)
        self.separatorNode = BundleItemMenuTreeNode("-" * 36, BundleItemMenuTreeNode.SEPARATOR)
        self.nodes = [ self.submenuNode, self.separatorNode ]
    
    def appendExcludedItem(self, item):
        bundleItemNode = BundleItemMenuTreeNode(item.name, BundleItemMenuTreeNode.ITEM, item)
        self.nodes.append(bundleItemNode)
        self.layoutChanged.emit()
    
    def clear(self):
        self.nodes = self.nodes[:2]
        self.layoutChanged.emit()
    
    def getExcludedItems(self):
        items = []
        for node in self.nodes[2:]:
            items.append(str(node.data.uuid).upper())
        return items
    
    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])
    
    def rowCount(self, parent):
        return len(self.nodes)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            node = self.nodes[index.row()]
            return node.nodeName()
        else:
            return None
    
    def columnCount(self, parent):  
        return 1

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        node = index.internalPointer()
        if node.nodeType == BundleItemMenuTreeNode.SUBMENU:
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled
    
    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = index[0].internalPointer()
        mimeData = PyMimeData(node)
        return mimeData

    def appendMenuNode(self, node):
        if node.nodeType == BundleItemMenuTreeNode.SEPARATOR:
            self.menuModel.removeMenuItem(node)
        elif node.nodeType == BundleItemMenuTreeNode.SUBMENU:
            for child in node.childNodes():
                self.appendMenuNode(child)
            self.menuModel.removeMenuItem(node)
        elif node.nodeType == BundleItemMenuTreeNode.ITEM and node not in self.nodes:
            self.menuModel.removeMenuItem(node)
            self.nodes.append(node)
        
    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        if dragNode not in self.nodes:
            self.appendMenuNode(dragNode)
            self.layoutChanged.emit()
            return True
        return False
        
    def removeMenuItem(self, node):
        index = self.nodes.index(node) - 1 
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.nodes.remove(node)
        self.endRemoveRows()