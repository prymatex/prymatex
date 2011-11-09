import sys
from PyQt4 import QtCore, QtGui

import os, sys
sys.path.append(os.path.abspath('..'))

from prymatex.utils.i18n import ugettext as _
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class PMXMenuTreeNode(object):
    def __init__(self, item, parent = None):
        self.item = item
        self.parent = parent
        self.children = []
    
    def name(self):
        if isinstance(self.item, (str, unicode)) and self.item.startswith("-"):
            return '--------------------------------'
        elif isinstance(self.item, dict):
            return self.item['name']
        return self.item.name
    
    def appendChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        
    def child(self, row):
        if len(self.children) > row:
            return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent is not None and self in self.parent.children:  
            return self.parent.children.index(self)
            
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, manager):
        QtCore.QAbstractItemModel.__init__(self)
        self.manager = manager

    def buildMenu(self, items, parent, submenus = {}):
        for uuid in items:
            if uuid.startswith("-"):
                parent.appendChild(PMXMenuTreeNode(uuid, parent))
            else:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    parent.appendChild(PMXMenuTreeNode(item, parent))
                elif uuid in submenus:
                    submenu = PMXMenuTreeNode({"uuid": uuid, "name": submenus[uuid]['name']}, parent)
                    parent.appendChild(submenu)
                    self.buildMenu(submenus[uuid]['items'], submenu, submenus)

    def setMainMenu(self, mainMenu):
        # 'items' 'submenus'
        self.root = PMXMenuTreeNode("root")
        self.buildMenu(mainMenu['items'], self.root, mainMenu['submenus'])
        
    def index(self, row, column, parent):
        if not parent.isValid():
            parent = self.root
        else:
            parent = parent.internalPointer()
        
        child = parent.child(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():  
            return QtCore.QModelIndex()  

        child = index.internalPointer()  
        parent = child.parent
        row = parent.row()
        
        if parent == self.root or row is None:  
            return QtCore.QModelIndex()

        return self.createIndex(row, 0, parent)
    
    def rowCount(self, parent):
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parent = self.root  
        else:  
            parent = parent.internalPointer()  

        return parent.childCount()
    
    def columnCount(self, parent):  
        return 1

    def data(self, index, role):
        if role == 0:
            node = index.internalPointer()
            return node.name()
        else:
            return None

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction     

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
               QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled        

    def mimeTypes(self):
        return ['text/xml']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml', 'mimeData')
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        print 'dropMimeData %s %s %s %s' % (data.data('text/xml'), action, row, parent.internalPointer().name())

        return True
    
class PMXExcludedWidget(QtGui.QListWidget):
    pass
    
class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName(_fromUtf8("Menu"))
        Menu.resize(458, 349)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Menu)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeMenuWidget = QtGui.QTreeView(Menu)
        self.treeMenuWidget.setDragEnabled(True)
        self.treeMenuWidget.setDragDropOverwriteMode(False)
        self.treeMenuWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeMenuWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeMenuWidget.setObjectName(_fromUtf8("treeMenuWidget"))
        self.horizontalLayout_2.addWidget(self.treeMenuWidget)
        self.treeExcludedWidget = PMXExcludedWidget(Menu)
        self.treeExcludedWidget.setDragEnabled(True)
        self.treeExcludedWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeExcludedWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeExcludedWidget.setObjectName(_fromUtf8("treeExcludedWidget"))
        self.horizontalLayout_2.addWidget(self.treeExcludedWidget)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        Menu.setWindowTitle(_('Form'))

class PMXBundleWidget(QtGui.QWidget, Ui_Menu):
    TYPE = 'bundle'
    BUNDLEITEM = 0
    SEPARATOR = 1
    SUBMENU = 2
    NEWGROUP = 3
    NEWSEPARATOR = 4
    def __init__(self, manager, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.manager = manager
        self.treeModel = TreeModel(manager)
        self.treeMenuWidget.setModel(self.treeModel)

    
    
    def edit(self, bundleItem):
        newGroup = QtGui.QListWidgetItem('New Group', self.treeExcludedWidget, self.NEWGROUP)
        separator = QtGui.QListWidgetItem('--------------------------------', self.treeExcludedWidget, self.NEWSEPARATOR)
        if bundleItem.mainMenu == None:
            return
        self.treeModel.setMainMenu(bundleItem.mainMenu)
        if 'excludedItems' in bundleItem.mainMenu:
            for uuid in bundleItem.mainMenu['excludedItems']:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    node = QtGui.QListWidgetItem(item.name, self.treeExcludedWidget, self.BUNDLEITEM)

def loadManager():
    from prymatex.support.manager import PMXSupportPythonManager
    def loadCallback(message):
        print message
    manager = PMXSupportPythonManager()
    manager.addNamespace('prymatex', os.path.abspath('../prymatex/share'))
    manager.loadSupport(loadCallback)
    return manager
    
if __name__ == "__main__":
    manager = loadManager()
    app = QtGui.QApplication(sys.argv)
    window = PMXBundleWidget(manager)
    window.edit(manager.getBundle("4676FC6D-6227-11D9-BFB1-000D93589AF6"))
    window.show()
    sys.exit(app.exec_())
