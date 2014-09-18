# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/widgets/multidicttableeditor.ui'
#
# Created: Thu Sep 18 10:11:59 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MultiDictTableEditor(object):
    def setupUi(self, MultiDictTableEditor):
        MultiDictTableEditor.setObjectName(_fromUtf8("MultiDictTableEditor"))
        MultiDictTableEditor.resize(415, 352)
        self.verticalLayout = QtGui.QVBoxLayout(MultiDictTableEditor)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewDictionaries = QtGui.QTableView(MultiDictTableEditor)
        self.tableViewDictionaries.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewDictionaries.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewDictionaries.setSortingEnabled(True)
        self.tableViewDictionaries.setObjectName(_fromUtf8("tableViewDictionaries"))
        self.verticalLayout.addWidget(self.tableViewDictionaries)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(MultiDictTableEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxNamespaces = QtGui.QComboBox(MultiDictTableEditor)
        self.comboBoxNamespaces.setObjectName(_fromUtf8("comboBoxNamespaces"))
        self.horizontalLayout.addWidget(self.comboBoxNamespaces)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtGui.QPushButton(MultiDictTableEditor)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(MultiDictTableEditor)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MultiDictTableEditor)
        QtCore.QMetaObject.connectSlotsByName(MultiDictTableEditor)

    def retranslateUi(self, MultiDictTableEditor):
        MultiDictTableEditor.setWindowTitle(_translate("MultiDictTableEditor", "Editor", None))
        self.label.setText(_translate("MultiDictTableEditor", "Namespaces:", None))

