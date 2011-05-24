import os, sys
sys.path.append(os.path.abspath('..'))

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PMBBundleTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):  
        super(PMBBundleTreeModel, self).__init__(parent)  
        self.parents = []
        self.manager = manager
        self.rootItem = PMBBundleTreeItem("", u"Bundles", "root")
        for bundle in self.manager.getAllBundles():
            bti = PMBBundleTreeItem(bundle.uuid, bundle.name, "bundle", self.rootItem)
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
            biti = PMBBundleTreeItem(item.uuid, item.name, item.TYPE, parent)
            parent.appendChild(biti)
    
class PMBBundleTreeItem(object):  
    def __init__(self, uuid, name, tipo, parent=None):
        self.name = name
        self.uuid = uuid
        self.tipo = tipo
        self.parentItem = parent
        self.childItems = []
        self.setIcon(self.tipo)

    def setIcon(self, tipo):
        self.icon = QtGui.QPixmap(12,12)
        if tipo == "template":
            self.icon.fill(QtCore.Qt.green)
        elif tipo == "command":
            self.icon.fill(QtCore.Qt.red)
        elif tipo == "bundle":
            self.icon.fill(QtCore.Qt.gray)
        elif tipo == "syntax":
            self.icon.fill(QtCore.Qt.yellow)
        elif tipo == "preference":
            self.icon.fill(QtCore.Qt.lightGray)
        elif tipo == "dragcommand":
            self.icon.fill(QtCore.Qt.magenta)
        elif tipo == "snippet":
            self.icon.fill(QtCore.Qt.cyan)
        else:
            self.icon.fill(QtCore.Qt.blue)
        
    def appendChild(self, item):
        self.childItems.append(item)

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
    
    def setData(self, name):  
        self.name = name

class ColumnView(QTreeView):
    def __init__(self, manager):
        super(ColumnView,  self).__init__()

        self.model = PMBBundleTreeModel(manager)
        self.setModel(self.model)

        self.setSortingEnabled(True)
        self.resize(700,  700)
        self.show()

if __name__ == "__main__":
    from prymatex.support.manager import PMXSupportManager
    manager = PMXSupportManager()
    manager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    manager.loadSupport()
    app = QApplication([])
    m = ColumnView(manager)
    app.exec_()
