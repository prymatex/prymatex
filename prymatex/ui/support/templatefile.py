# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/support/templatefile.ui'
#
# Created: Wed Dec 10 16:51:29 2014
#      by: PyQt5 UI code generator 5.3.2
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

