# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/addons.ui'
#
# Created: Thu Dec 11 08:36:22 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Addons(object):
    def setupUi(self, Addons):
        Addons.setObjectName("Addons")
        Addons.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Addons)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtWidgets.QLineEdit(Addons)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.listViewAddons = QtWidgets.QListView(Addons)
        self.listViewAddons.setObjectName("listViewAddons")
        self.verticalLayout_2.addWidget(self.listViewAddons)

        self.retranslateUi(Addons)
        QtCore.QMetaObject.connectSlotsByName(Addons)

    def retranslateUi(self, Addons):
        _translate = QtCore.QCoreApplication.translate
        Addons.setWindowTitle(_translate("Addons", "Terminal"))

