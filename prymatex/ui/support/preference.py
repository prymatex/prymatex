# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/support/preference.ui'
#
# Created: Wed Oct 22 18:41:37 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preference(object):
    def setupUi(self, Preference):
        Preference.setObjectName("Preference")
        Preference.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Preference)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.settings = QtWidgets.QPlainTextEdit(Preference)
        self.settings.setObjectName("settings")
        self.verticalLayout.addWidget(self.settings)

        self.retranslateUi(Preference)
        QtCore.QMetaObject.connectSlotsByName(Preference)

    def retranslateUi(self, Preference):
        _translate = QtCore.QCoreApplication.translate
        Preference.setWindowTitle(_translate("Preference", "Form"))

