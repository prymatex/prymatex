# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/support/bundle.ui'
#
# Created: Thu Dec 11 08:36:21 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(458, 349)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Menu)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeMenuView = QtWidgets.QTreeView(Menu)
        self.treeMenuView.setDragEnabled(True)
        self.treeMenuView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeMenuView.setAlternatingRowColors(True)
        self.treeMenuView.setHeaderHidden(True)
        self.treeMenuView.setObjectName("treeMenuView")
        self.horizontalLayout_2.addWidget(self.treeMenuView)
        self.listExcludedView = QtWidgets.QListView(Menu)
        self.listExcludedView.setDragEnabled(True)
        self.listExcludedView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listExcludedView.setAlternatingRowColors(True)
        self.listExcludedView.setObjectName("listExcludedView")
        self.horizontalLayout_2.addWidget(self.listExcludedView)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        _translate = QtCore.QCoreApplication.translate
        Menu.setWindowTitle(_translate("Menu", "Form"))

