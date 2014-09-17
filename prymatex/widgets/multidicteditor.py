#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.utils.i18n import ugettext as _

from prymatex.models.tables import SelectableMultiDictTableModel
from prymatex.models.lists import CheckableListModel

class MultiDictTableEditorWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(MultiDictTableEditorWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.selectableMultiDictTableModel = SelectableMultiDictTableModel(self)
        self.checkableListModel = CheckableListModel(self)
        
        self.tableViewDictionaries.setModel(self.selectableMultiDictTableModel)
        self.comboBoxNamespaces.setModel(self.checkableListModel)
        
        self.selectableMultiDictTableModel.layoutChanged.connect(self.resize_to_contents)
        self.selectableMultiDictTableModel.dictionaryChanged.connect(self.resize_to_contents)
        self.checkableListModel.dataChanged.connect(
            self.on_checkableListModel_dataChanged
        )
        self.insertActions = []

    def dumpData(self, name):
        return self.selectableMultiDictTableModel.dumpData(name)

    def model(self):
        return self.selectableMultiDictTableModel

    def setupUi(self, MultiDictTableEditorWidget):
        MultiDictTableEditorWidget.setObjectName("MultiDictTableEditorWidget")
        self._2 = QtWidgets.QVBoxLayout(MultiDictTableEditorWidget)
        self._2.setObjectName("_2")
        self.tableViewDictionaries = QtWidgets.QTableView(MultiDictTableEditorWidget)
        self.tableViewDictionaries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewDictionaries.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewDictionaries.setSortingEnabled(True)
        self.tableViewDictionaries.setObjectName("tableViewDictionaries")
        self._2.addWidget(self.tableViewDictionaries)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(MultiDictTableEditorWidget)
        self.label.setObjectName("label")
        self.label.setText('Namespaces:')
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxNamespaces = QtWidgets.QComboBox(MultiDictTableEditorWidget)
        self.comboBoxNamespaces.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBoxNamespaces.setObjectName("comboBoxNamespaces")
        self.horizontalLayout.addWidget(self.comboBoxNamespaces)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtWidgets.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtWidgets.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self._2.addLayout(self.horizontalLayout)
        
        self.menuAdd = QtWidgets.QMenu(MultiDictTableEditorWidget)
        self.pushButtonAdd.setMenu(self.menuAdd)
        
        QtCore.QMetaObject.connectSlotsByName(MultiDictTableEditorWidget)

    # ----------------------- Signals
    def on_checkableListModel_dataChanged(self, topLeft, bottomRight):
        selected = self.checkableListModel.selectedItems()
        for name in self.selectableMultiDictTableModel.dictionaryNames():
            self.selectableMultiDictTableModel.setVisible(name, name in selected)

    def addDictionary(self, name, dictionary, editable = False, selectable = False, visible = True):
        self.selectableMultiDictTableModel.addDictionary(name, dictionary, editable = editable,
            selectable = selectable, visible = visible)
        self.checkableListModel.addItem(name, visible)
        action = QtWidgets.QAction(name, self)
        action.triggered.connect(lambda checked, name = name: self.on_actionInsertItem_triggered(name))
        action.setEnabled(editable)
        self.menuAdd.addAction(action)

    def addTuples(self, name, values, editable = False, selectable = False, visible = True):
        self.selectableMultiDictTableModel.addTuples(name, values, editable = editable,
            selectable = selectable, visible = visible)
        self.checkableListModel.addItem(name, visible)
        action = QtWidgets.QAction(name, self)
        action.triggered.connect(lambda checked, name = name: self.on_actionInsertItem_triggered(name))
        action.setEnabled(editable)
        self.menuAdd.addAction(action)

    def resize_to_contents(self, dictionaryName = None):
        self.tableViewDictionaries.resizeColumnsToContents()
        self.tableViewDictionaries.resizeRowsToContents()
        self.tableViewDictionaries.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def on_actionInsertItem_triggered(self, dictionaryName):
        if not self.selectableMultiDictTableModel.isVisible(dictionaryName):
            self.checkableListModel.setSelected(dictionaryName, True)
        itemName, ok = QtWidgets.QInputDialog.getText(self, "Title", "Item name:")
        while ok and self.selectableMultiDictTableModel.hasItem(dictionaryName, itemName):
            itemName, ok = QtWidgets.QInputDialog.getText(self, "Title", "Item name:", text = itemName)
        if ok:
            self.selectableMultiDictTableModel.insertItem(dictionaryName, itemName)
        
    def on_pushButtonRemove_pressed(self):
        index = self.tableViewDictionaries.currentIndex()
        self.selectableMultiDictTableModel.removeRows(index.row() , 1)

    def clear(self):
        self.selectableMultiDictTableModel.clear()
        self.checkableListModel.clear()
        self.menuAdd.clear()
