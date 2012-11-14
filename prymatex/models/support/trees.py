#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent2keysequence, keysequence2keyequivalent

from prymatex.models.trees import AbstractTreeModel
from prymatex.models.support.nodes import BundleItemTreeNode, BundleItemMenuTreeNode
from prymatex.models.support.lists import BundleItemExcludedListModel

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
        treeNode.setNodeName(treeNode.bundleItem().name)
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

    def removeRows(self, position = 0, count = 1,  parent = QtCore.QModelIndex()):
        # TODO Quien usa este metodo?
        node = self.node(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.popChild(position)  
        self.endRemoveRows()

    #========================================================================
    # Functions
    #========================================================================
    def appendBundle(self, bundle):
        self.appendNode(bundle)
    
    def removeBundle(self, bundle):
        self.removeNode(bundle)
    
    def appendBundleItem(self, bundleItem):
        self.appendNode(bundleItem, bundleItem.bundle)

    def removeBundleItem(self, bundleItem):
        self.removeNode(bundleItem, bundleItem.bundle)
    
    def appendTemplateFile(self, templateFile):
        self.appendNode(templateFile, templateFile.template)

    def removeTemplateFile(self, templateFile):
        self.removeNode(templateFile, templateFile.template)

#===============================================
# Bundle Menu Tree Model
#===============================================
class BundleItemMenuTreeModel(AbstractTreeModel):
    menuChanged = QtCore.pyqtSignal()
    
    def __init__(self, manager, parent = None):
        AbstractTreeModel.__init__(self, parent)
        self.excludedModel = BundleItemExcludedListModel(manager, self)
        self.manager = manager
    
    def excludedListModel(self):
        return self.excludedModel
    
    def _build_menu(self, items, parent, submenus = {}, allActionItems = []):
        for uuid in items:
            if uuid.startswith("-"):
                separatorNode = BundleItemMenuTreeNode(uuid, BundleItemMenuTreeNode.SEPARATOR, parent = parent)
                parent.appendChild(separatorNode)
            else:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    if item in allActionItems:
                        allActionItems.remove(item)
                    bundleItemNode = BundleItemMenuTreeNode(item.name, BundleItemMenuTreeNode.ITEM, item, parent)
                    parent.appendChild(bundleItemNode)
                elif uuid in submenus:
                    submenuNode = BundleItemMenuTreeNode(submenus[uuid]['name'], BundleItemMenuTreeNode.SUBMENU, uuid, parent)
                    parent.appendChild(submenuNode)
                    self._build_menu(submenus[uuid]['items'], submenuNode, submenus, allActionItems)

    def setBundle(self, bundle):
        self.clear()
        # allActionItems is a list with all bundleItems in te bundle
        allActionItems = self.manager.findBundleItems(bundle = bundle, TYPE = "command")
        allActionItems += self.manager.findBundleItems(bundle = bundle, TYPE = "snippet")
        allActionItems += self.manager.findBundleItems(bundle = bundle, TYPE = "macro")
        if bundle.mainMenu is not None:
            self._build_menu(bundle.mainMenu['items'], self.rootNode, bundle.mainMenu['submenus'], allActionItems)
            # allActionItems tiene los items que no estan el menu
            if 'excludedItems' in bundle.mainMenu:
                for uuid in bundle.mainMenu['excludedItems']:
                    item = self.manager.getBundleItem(uuid)
                    if item != None:
                        if item in allActionItems:
                            allActionItems.remove(item)
                        self.excludedModel.appendExcludedItem(item)
        # allActionItems tiene los items que no estan en el menu ni en la lista de excluidos
        for item in allActionItems:
            self.excludedModel.appendExcludedItem(item)
        self.layoutChanged.emit()
    
    def clear(self):
        self.excludedModel.clear()
        AbstractTreeModel.clear(self)

    def add_submenu(self, submenuNode, submenus):
        items = []
        for node in submenuNode.childNodes():
            if node.nodeType == BundleItemMenuTreeNode.ITEM:
                items.append(str(node.data.uuid).upper())
            elif node.nodeType == BundleItemMenuTreeNode.SUBMENU:
                self.add_submenu(node, submenus)
            elif node.nodeType == BundleItemMenuTreeNode.SEPARATOR:
                items.append(node.nodeName())
        submenus[submenuNode.data] = { "items": items, "name": submenuNode.nodeName() }
        
    def getMainMenu(self):
        items = []
        submenus = {}
        for node in self.rootNode.childNodes():
            if node.nodeType == BundleItemMenuTreeNode.ITEM:
                items.append(str(node.data.uuid).upper())
            elif node.nodeType == BundleItemMenuTreeNode.SUBMENU:
                items.append(node.data)
                self.add_submenu(node, submenus)
            elif node.nodeType == BundleItemMenuTreeNode.SEPARATOR:
                items.append(node.nodeName())
        mainMenu = {"items": items, "submenus": submenus }
        excludedItems = self.excludedModel.getExcludedItems()
        if excludedItems:
            mainMenu['excludedItems'] = excludedItems
        return mainMenu

    def data(self, index, role):
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            node = self.node(index)
            return node.nodeName()
        else:
            return None

    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        if role == QtCore.Qt.EditRole:  
            node = self.node(index)
            if node.nodeType == BundleItemMenuTreeNode.SUBMENU:
                node.setNodeName(value)
                self.menuChanged.emit()
            elif node.nodeType == BundleItemMenuTreeNode.ITEM:
                self.manager.updateBundleItem(node.data, name = value)
                node.setNodeName(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        if index.isValid():
            node = self.node(index)
            if node.nodeType == BundleItemMenuTreeNode.SUBMENU:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable
            elif node.nodeType == BundleItemMenuTreeNode.SEPARATOR:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled
            elif node.nodeType == BundleItemMenuTreeNode.ITEM:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsDropEnabled | defaultFlags
    
    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = self.node(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        
        parentNode = self.node(parentIndex)
        
        if dragNode.nodeParent() == None:
            #The node belongs to a exludeListModel
            if dragNode.nodeType == BundleItemMenuTreeNode.SEPARATOR:
                #Make a copy of separator
                separatorNode = BundleItemMenuTreeNode(dragNode.nodeName(), BundleItemMenuTreeNode.SEPARATOR)
                parentNode.insertChild(row, separatorNode)
            elif dragNode.nodeType == BundleItemMenuTreeNode.SUBMENU:
                #Make a copy of submenu
                uuid = str(self.manager.uuidgen()).upper()
                submenuNode = BundleItemMenuTreeNode(dragNode.nodeName(), BundleItemMenuTreeNode.SUBMENU, uuid)
                parentNode.insertChild(row, submenuNode)
            elif dragNode.nodeType == BundleItemMenuTreeNode.ITEM:
                self.excludedModel.removeMenuItem(dragNode)
                parentNode.insertChild(row, dragNode)
        elif dragNode.nodeParent() == parentNode:
            #Reparent
            currentRow = dragNode.row()
            row = row if currentRow >= row else row - 1
            parentNode.removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        else:
            #Reparent
            dragNode.nodeParent().removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        self.menuChanged.emit()
        self.layoutChanged.emit()
        return True
        
    def removeMenuItem(self, item):
        index = self.createIndex(item.row(), 0, item)
        parentIndex = self.parent(index)
        parentNode = self.node(parentIndex)
        self.beginRemoveRows(parentIndex, item.row(), item.row())
        parentNode.removeChild(item)
        self.endRemoveRows()
        self.menuChanged.emit()