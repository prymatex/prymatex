# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/plugins.ui'
#
# Created: Wed May 27 08:01:33 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Plugins(object):
    def setupUi(self, Plugins):
        Plugins.setObjectName("Plugins")
        Plugins.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Plugins)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtWidgets.QLineEdit(Plugins)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.listViewPlugins = QtWidgets.QListView(Plugins)
        self.listViewPlugins.setObjectName("listViewPlugins")
        self.verticalLayout_2.addWidget(self.listViewPlugins)

        self.retranslateUi(Plugins)
        QtCore.QMetaObject.connectSlotsByName(Plugins)

    def retranslateUi(self, Plugins):
        _translate = QtCore.QCoreApplication.translate
        Plugins.setWindowTitle(_translate("Plugins", "Terminal"))

