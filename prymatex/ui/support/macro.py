# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/macro.ui'
#
# Created: Wed May 27 08:01:32 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Macro(object):
    def setupUi(self, Macro):
        Macro.setObjectName("Macro")
        Macro.resize(274, 210)
        self.verticalLayout = QtWidgets.QVBoxLayout(Macro)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listActionWidget = QtWidgets.QListWidget(Macro)
        self.listActionWidget.setAlternatingRowColors(True)
        self.listActionWidget.setObjectName("listActionWidget")
        self.verticalLayout.addWidget(self.listActionWidget)
        self.argument = QtWidgets.QPlainTextEdit(Macro)
        self.argument.setReadOnly(True)
        self.argument.setObjectName("argument")
        self.verticalLayout.addWidget(self.argument)

        self.retranslateUi(Macro)
        QtCore.QMetaObject.connectSlotsByName(Macro)

    def retranslateUi(self, Macro):
        _translate = QtCore.QCoreApplication.translate
        Macro.setWindowTitle(_translate("Macro", "Form"))

