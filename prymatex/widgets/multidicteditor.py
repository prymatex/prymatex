#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.utils.i18n import ugettext as _

from prymatex.models.tables import SelectableMultiDictTableModel
from prymatex.models.lists import CheckableListModel
from prymatex.ui.widgets.multidicttableeditor import Ui_MultiDictTableEditor

class MultiDictTableEditorWidget(Ui_MultiDictTableEditor, QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(MultiDictTableEditorWidget, self).__init__(parent)
        self.setupUi(self)

        self.menuAdd = QtWidgets.QMenu(self)
        self.pushButtonAdd.setMenu(self.menuAdd)

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
