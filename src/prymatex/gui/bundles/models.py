import os
from PyQt4 import QtCore, QtGui
from prymatex import res_rc

class PMXBundleTreeItem(object):  
    def __init__(self, data, parent=None):
        self.data = data
        self.parentItem = parent
        self.childItems = []
        self.setIcon(self.tipo)
        
    @property
    def name(self):
        return self.data.name
        
    @property
    def tipo(self):
        return self.data.TYPE
    
    def setIcon(self, tipo):
        self.icon = QtGui.QPixmap()
        if tipo == "template":
            self.icon.load(":/bundles/resources/bundles/templates.png")
        elif tipo == "command":
            self.icon.load(":/bundles/resources/bundles/commands.png")
        elif tipo == "syntax":
            self.icon.load(":/bundles/resources/bundles/languages.png")
        elif tipo == "preference":
            self.icon.load(":/bundles/resources/bundles/preferences.png")
        elif tipo == "dragcommand":
            self.icon.load(":/bundles/resources/bundles/drag-commands.png")
        elif tipo == "snippet":
            self.icon.load(":/bundles/resources/bundles/snippets.png")
        elif tipo == "macro":
            self.icon.load(":/bundles/resources/bundles/macros.png")
        elif tipo == "template-file":
            self.icon.load(":/bundles/resources/bundles/template-files.png")
        else:
            self.icon = None

    def appendChild(self, child):
        self.childItems.append(child)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 1

    def parent(self):  
        return self.parentItem  

    def row(self):  
        if self.parentItem:  
            return self.parentItem.childItems.index(self)  
        return 0
    
    def setData(self, data):  
        self.data = data

class RootItem(object):
    def __init__(self):
        self.name = "root"
        self.TYPE = "root"

class PMXBundleTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):
        super(PMXBundleTreeModel, self).__init__(parent)  
        self.manager = manager
        self.rootItem = PMXBundleTreeItem(RootItem())
        for bundle in self.manager.getAllBundles():
            bti = PMXBundleTreeItem(bundle, self.rootItem)
            self.rootItem.appendChild(bti)
            bundle_items = self.manager.findBundleItems(bundle = bundle)
            self.setupModelData(bundle_items, bti)
      
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.EditRole:  
            item = index.internalPointer()  
            item.name = unicode(value.toString())
            return True
        return False  
     
    def removeRows(self, position=0, count=1,  parent=QtCore.QModelIndex()):
        node = self.nodeFromIndex(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.childItems.pop(position)  
        self.endRemoveRows()  

    def nodeFromIndex(self, index):  
        if index.isValid():  
            return index.internalPointer()  
        else:  
            return self.rootItem  

    def columnCount(self, parent):  
        if parent.isValid():  
            return parent.internalPointer().columnCount()  
        else:  
            return self.rootItem.columnCount()  

    def data(self, index, role):  
        if not index.isValid():  
            return None
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return QtCore.QVariant(item.name)
        elif role == QtCore.Qt.DecorationRole:
            item = index.internalPointer()
            return item.icon

    def flags(self, index):  
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable  

    def headerData(self, section, orientation, role):  
        return None

    def index(self, row, column, parent):  
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):  
            return QtCore.QModelIndex()  

        if not parent.isValid():  
            parentItem = self.rootItem  
        else:  
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:  
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):  
        if not index.isValid():  
            return QtCore.QModelIndex()  

        childItem = index.internalPointer()  
        parentItem = childItem.parent()  

        if parentItem == self.rootItem:  
            return QtCore.QModelIndex()  

        return self.createIndex(parentItem.row(), 0, parentItem)  

    def rowCount(self, parent):  
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parentItem = self.rootItem  
        else:  
            parentItem = parent.internalPointer()  

        return parentItem.childCount()  

    def setupModelData(self, items, parent):
        for item in items:
            biti = PMXBundleTreeItem(item, parent)
            if item.TYPE == "template":
                for file in item.getTemplateFiles():
                    tifi = PMXBundleTreeItem(file, biti)
                    biti.appendChild(tifi)
            parent.appendChild(biti)

class PMXBundleTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleTreeProxyModel, self).__init__(parent)
        self.bundleItemTypeOrder = ["bundle", "command", "dragcommand", "macro", "snippet", "preference", "template", "template-file", "syntax"]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        if item.tipo == "bundle":
            return True
        else:
            return QtCore.QString(item.tipo).contains(regexp)
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        if leftData.tipo == rightData.tipo:
            return rightData.name > leftData.name
        else:
            return self.bundleItemTypeOrder.index(rightData.tipo) > self.bundleItemTypeOrder.index(leftData.tipo)
