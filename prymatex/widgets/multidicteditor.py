#!/usr/bin/env python
# -*- coding: utf-8 -*-


import StringIO

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath("../.."))

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import create_action, add_actions, keybinding
from prymatex.utils.i18n import ugettext as _

from prymatex.models.tables import SelectableMultiDictTableModel
from prymatex.models.lists import CheckableListModel
from prymatex import resources

class MultiDictTableEditorWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
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


    def model(self):
        return self.selectableMultiDictTableModel

    def setupUi(self, MultiDictTableEditorWidget):
        MultiDictTableEditorWidget.setObjectName("MultiDictTableEditorWidget")
        self._2 = QtGui.QVBoxLayout(MultiDictTableEditorWidget)
        self._2.setObjectName("_2")
        self.tableViewDictionaries = QtGui.QTableView(MultiDictTableEditorWidget)
        self.tableViewDictionaries.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewDictionaries.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewDictionaries.setSortingEnabled(True)
        self.tableViewDictionaries.setObjectName("tableViewDictionaries")
        self._2.addWidget(self.tableViewDictionaries)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(MultiDictTableEditorWidget)
        self.label.setObjectName("label")
        self.label.setText('Namespaces:')
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxNamespaces = QtGui.QComboBox(MultiDictTableEditorWidget)
        self.comboBoxNamespaces.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBoxNamespaces.setObjectName("comboBoxNamespaces")
        self.horizontalLayout.addWidget(self.comboBoxNamespaces)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtGui.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self._2.addLayout(self.horizontalLayout)
        
        self.menuAdd = QtGui.QMenu(MultiDictTableEditorWidget)
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
        action = QtGui.QAction(name, self)
        action.triggered.connect(lambda checked, name = name: self.on_actionInsertItem_triggered(name))
        action.setEnabled(editable)
        self.menuAdd.addAction(action)


    def resize_to_contents(self, dictionaryName = None):
        self.tableViewDictionaries.resizeColumnsToContents()
        self.tableViewDictionaries.resizeRowsToContents()
        self.tableViewDictionaries.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)


    def on_actionInsertItem_triggered(self, dictionaryName):
        if not self.selectableMultiDictTableModel.isVisible(dictionaryName):
            self.checkableListModel.setSelected(dictionaryName, True)
        itemName, ok = QtGui.QInputDialog.getText(self, "Title", "Item name:")
        while ok and self.selectableMultiDictTableModel.hasItem(dictionaryName, itemName):
            itemName, ok = QtGui.QInputDialog.getText(self, "Title", "Item name:", text = itemName)
        if ok:
            self.selectableMultiDictTableModel.insertItem(dictionaryName, itemName)

        
    def on_pushButtonRemove_pressed(self):
        index = self.tableViewDictionaries.currentIndex()
        self.selectableMultiDictTableModel.removeRows(index.row() , 1)


    def accept_changes(self):
        """Accept changes"""
        for (i, j), value in self.model.changes.iteritems():
            self.data[i][j] = value


    def clear(self):
        pass

class MultiDictTableEditorDialog(QtGui.QDialog):
    """Array Editor Dialog"""    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.data = None

    def setup_and_check(self, data, title='', editable = False):
        """
        Setup ListEditor:
        return False if data is not supported, True otherwise
        """
        self.data = data
        if len(data) == 0:
            self.error(_("Data is empty"))
            return False
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        if title:
            title = unicode(title) # in case title is not a string
        else:
            title = _("List editor")
        if editable:
            title += ' (' + _('read only') + ')'
        self.setWindowTitle(title)
        self.resize(600, 500)
        
        # Stack widget
        self.stack = QtGui.QStackedWidget(self)
        self.tablewidget = MultiDictTableEditorWidget(self)
        self.stack.addWidget(self.tablewidget)
        self.connect(self.stack, QtCore.SIGNAL('currentChanged(int)'),
                     self.current_widget_changed)
        self.layout.addWidget(self.stack, 1, 0)

        # Buttons configuration
        btn_layout = QtGui.QHBoxLayout()
        bbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.connect(bbox, QtCore.SIGNAL("accepted()"), QtCore.SLOT("accept()"))
        self.connect(bbox, QtCore.SIGNAL("rejected()"), QtCore.SLOT("reject()"))
        btn_layout.addWidget(bbox)
        self.layout.addLayout(btn_layout, 2, 0)
        
        self.setMinimumSize(400, 300)
        
        # Make the dialog act as a window
        self.setWindowFlags(QtCore.Qt.Window)
        
        for key, value in self.data.iteritems():
            self.tablewidget.addDictionary(key, value, editable = editable)
        
        return True
        
    def current_widget_changed(self, index):
        self.tablewidget = self.stack.widget(index)
        
    def accept(self):
        """Reimplement Qt method"""
        for index in range(self.stack.count()):
            self.stack.widget(index).accept_changes()
        QtGui.QDialog.accept(self)
        
    def get_value(self):
        """Return modified array -- this is *not* a copy"""
        # It is import to avoid accessing Qt C++ object as it has probably
        # already been destroyed, due to the QtCore.Qt.WA_DeleteOnClose attribute
        return self.data

    def error(self, message):
        """An error occured, closing the dialog box"""
        QtGui.QMessageBox.critical(self, _("Array editor"), message)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.reject()


def test_edit(data, title="", editable = False):
    """Test subroutine"""
    dlg = MultiDictTableEditorDialog()
    if dlg.setup_and_check(data, title, editable = editable) and dlg.exec_():
        return dlg.get_value()
    else:
        import sys
        sys.exit()


def test():
    """Array editor test"""
    _app = QtGui.QApplication([])
    
    data = {"uno": {"uno": 1, "dos": 2},
            "dos": {"uno": 1, "dos": 2},
            "tres": {"uno": 1, "dos": 2}}
    arr_out = test_edit(data, "bool array", editable = True)
    print "out:", arr_out
    
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath("../.."))
    print sys.path
    test()
