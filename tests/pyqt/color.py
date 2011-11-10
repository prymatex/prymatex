import sys
from PyQt4 import QtCore, QtGui

class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName(_fromUtf8("Menu"))
        Menu.resize(458, 349)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Menu)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeMenuWidget = QtGui.QTreeWidget(Menu)
        self.treeMenuWidget.setDragEnabled(True)
        self.treeMenuWidget.setDragDropOverwriteMode(False)
        self.treeMenuWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeMenuWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeMenuWidget.setObjectName(_fromUtf8("treeMenuWidget"))
        self.horizontalLayout_2.addWidget(self.treeMenuWidget)
        self.treeExcludedWidget = QtGui.QTreeWidget(Menu)
        self.treeExcludedWidget.setDragEnabled(True)
        self.treeExcludedWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeExcludedWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeExcludedWidget.setObjectName(_fromUtf8("treeExcludedWidget"))
        self.horizontalLayout_2.addWidget(self.treeExcludedWidget)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        Menu.setWindowTitle(_('Form'))
        self.treeMenuWidget.headerItem().setText(0, _('Menu Structure'))
        self.treeExcludedWidget.headerItem().setText(0, _('Excluded Items'))

class PMXBundleWidget(QtGui.QWidget, Ui_Menu):
    TYPE = 'bundle'
    BUNDLEITEM = 0
    SEPARATOR = 1
    SUBMENU = 2
    NEWGROUP = 3
    NEWSEPARATOR = 4
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

    def buildMenu(self, items, parent, submenus = {}):
        for uuid in items:
            if uuid.startswith('-'):
                separator = QtGui.QTreeWidgetItem(parent, self.SEPARATOR)
                separator.setData(0, QtCore.Qt.EditRole, "")
                separator.setText(0, '--------------------------------')
                continue
            item = self.manager.getBundleItem(uuid)
            if item != None:
                node = QtGui.QTreeWidgetItem(parent, self.BUNDLEITEM)
                node.setData(0, QtCore.Qt.EditRole, uuid)
                node.setText(0, item.name)
            elif uuid in submenus:
                submenu = QtGui.QTreeWidgetItem(parent, self.SUBMENU)
                submenu.setData(0, QtCore.Qt.EditRole, uuid)
                submenu.setText(0, submenus[uuid]['name'])
                self.buildMenu(submenus[uuid]['items'], submenu, submenus)
    
    def edit(self, bundleItem):
        self.treeExcludedWidget.clear()
        self.treeMenuWidget.clear()
        newGroup = QtGui.QTreeWidgetItem(self.treeExcludedWidget, self.NEWGROUP)
        newGroup.setText(0, 'New Group')
        separator = QtGui.QTreeWidgetItem(self.treeExcludedWidget, self.NEWSEPARATOR)
        separator.setText(0, '--------------------------------')
        if mainMenu == None:
            return
        if 'items' in mainMenu:
            self.buildMenu(mainMenu['items'], self.treeMenuWidget, mainMenu['submenus'])
        if 'excludedItems' in mainMenu:
            for uuid in mainMenu['excludedItems']:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    node = QtGui.QTreeWidgetItem(self.treeExcludedWidget, self.BUNDLEITEM)
                    node.setText(0, item.name)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = SomeQtWidget()
    window.show()
    sys.exit(app.exec_())
