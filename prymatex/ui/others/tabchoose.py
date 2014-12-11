# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/others/tabchoose.ui'
#
# Created: Thu Dec 11 08:36:21 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChooseTab(object):
    def setupUi(self, ChooseTab):
        ChooseTab.setObjectName("ChooseTab")
        ChooseTab.resize(310, 170)
        self.verticalLayout = QtWidgets.QVBoxLayout(ChooseTab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(ChooseTab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listView = QtWidgets.QListView(ChooseTab)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOpen = QtWidgets.QPushButton(ChooseTab)
        self.pushOpen.setDefault(True)
        self.pushOpen.setObjectName("pushOpen")
        self.horizontalLayout.addWidget(self.pushOpen)
        self.pushCancel = QtWidgets.QPushButton(ChooseTab)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ChooseTab)
        QtCore.QMetaObject.connectSlotsByName(ChooseTab)

    def retranslateUi(self, ChooseTab):
        _translate = QtCore.QCoreApplication.translate
        ChooseTab.setWindowTitle(_translate("ChooseTab", "Dialog"))
        self.pushOpen.setText(_translate("ChooseTab", "OK"))
        self.pushCancel.setText(_translate("ChooseTab", "Cancel"))

