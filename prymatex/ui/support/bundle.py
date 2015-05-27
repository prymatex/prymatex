# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/bundle.ui'
#
# Created: Wed May 27 08:01:33 2015
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

