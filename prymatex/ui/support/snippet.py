# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/snippet.ui'
#
# Created: Tue Nov  4 08:31:36 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Snippet(object):
    def setupUi(self, Snippet):
        Snippet.setObjectName("Snippet")
        Snippet.resize(274, 210)
        self.verticalLayout = QtWidgets.QVBoxLayout(Snippet)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content = QtWidgets.QPlainTextEdit(Snippet)
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(Snippet)
        QtCore.QMetaObject.connectSlotsByName(Snippet)

    def retranslateUi(self, Snippet):
        _translate = QtCore.QCoreApplication.translate
        Snippet.setWindowTitle(_translate("Snippet", "Form"))

