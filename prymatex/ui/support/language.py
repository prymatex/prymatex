# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/support/language.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Language(object):
    def setupUi(self, Language):
        Language.setObjectName("Language")
        Language.resize(274, 210)
        self.verticalLayout = QtWidgets.QVBoxLayout(Language)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content = QtWidgets.QPlainTextEdit(Language)
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(Language)
        QtCore.QMetaObject.connectSlotsByName(Language)

    def retranslateUi(self, Language):
        _translate = QtCore.QCoreApplication.translate
        Language.setWindowTitle(_translate("Language", "Form"))

