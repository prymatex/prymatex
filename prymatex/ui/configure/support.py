# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/support.ui'
#
# Created: Wed Dec 10 16:51:32 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Shebang(object):
    def setupUi(self, Shebang):
        Shebang.setObjectName("Shebang")
        Shebang.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Shebang)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewShebangs = QtWidgets.QTableView(Shebang)
        self.tableViewShebangs.setObjectName("tableViewShebangs")
        self.verticalLayout.addWidget(self.tableViewShebangs)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtWidgets.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtWidgets.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Shebang)
        QtCore.QMetaObject.connectSlotsByName(Shebang)

    def retranslateUi(self, Shebang):
        _translate = QtCore.QCoreApplication.translate
        Shebang.setWindowTitle(_translate("Shebang", "Support Settings"))

