# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requestsecurestring.ui'
#
# Created: Tue May 29 10:43:34 2012
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RequestSecureStringDialog(object):
    def setupUi(self, RequestSecureStringDialog):
        RequestSecureStringDialog.setObjectName(_fromUtf8("RequestSecureStringDialog"))
        RequestSecureStringDialog.resize(318, 39)
        self.verticalLayout = QtGui.QVBoxLayout(RequestSecureStringDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit = QtGui.QLineEdit(RequestSecureStringDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)

        self.retranslateUi(RequestSecureStringDialog)
        QtCore.QMetaObject.connectSlotsByName(RequestSecureStringDialog)

    def retranslateUi(self, RequestSecureStringDialog):
        RequestSecureStringDialog.setWindowTitle(QtGui.QApplication.translate("RequestSecureStringDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

