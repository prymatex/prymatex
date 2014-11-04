# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/templatefile.ui'
#
# Created: Tue Nov  4 08:31:37 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TemplateFile(object):
    def setupUi(self, TemplateFile):
        TemplateFile.setObjectName("TemplateFile")
        TemplateFile.resize(274, 210)
        self.verticalLayout = QtWidgets.QVBoxLayout(TemplateFile)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content = QtWidgets.QPlainTextEdit(TemplateFile)
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(TemplateFile)
        QtCore.QMetaObject.connectSlotsByName(TemplateFile)

    def retranslateUi(self, TemplateFile):
        _translate = QtCore.QCoreApplication.translate
        TemplateFile.setWindowTitle(_translate("TemplateFile", "Form"))

