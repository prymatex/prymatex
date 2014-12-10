# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/widgets/multidicttableeditor.ui'
#
# Created: Wed Dec 10 13:43:29 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MultiDictTableEditor(object):
    def setupUi(self, MultiDictTableEditor):
        MultiDictTableEditor.setObjectName("MultiDictTableEditor")
        MultiDictTableEditor.resize(415, 352)
        self.verticalLayout = QtWidgets.QVBoxLayout(MultiDictTableEditor)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewDictionaries = QtWidgets.QTableView(MultiDictTableEditor)
        self.tableViewDictionaries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewDictionaries.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewDictionaries.setSortingEnabled(True)
        self.tableViewDictionaries.setObjectName("tableViewDictionaries")
        self.verticalLayout.addWidget(self.tableViewDictionaries)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(MultiDictTableEditor)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxNamespaces = QtWidgets.QComboBox(MultiDictTableEditor)
        self.comboBoxNamespaces.setObjectName("comboBoxNamespaces")
        self.horizontalLayout.addWidget(self.comboBoxNamespaces)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtWidgets.QPushButton(MultiDictTableEditor)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtWidgets.QPushButton(MultiDictTableEditor)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MultiDictTableEditor)
        QtCore.QMetaObject.connectSlotsByName(MultiDictTableEditor)

    def retranslateUi(self, MultiDictTableEditor):
        _translate = QtCore.QCoreApplication.translate
        MultiDictTableEditor.setWindowTitle(_translate("MultiDictTableEditor", "Editor"))
        self.label.setText(_translate("MultiDictTableEditor", "Namespaces:"))

