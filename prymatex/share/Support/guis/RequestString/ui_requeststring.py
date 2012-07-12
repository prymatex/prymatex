# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requeststring.ui'
#
# Created: Tue May 29 10:44:51 2012
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RequestStringDialog(object):
    def setupUi(self, RequestStringDialog):
        RequestStringDialog.setObjectName(_fromUtf8("RequestStringDialog"))
        RequestStringDialog.resize(318, 39)
        self.verticalLayout = QtGui.QVBoxLayout(RequestStringDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit = QtGui.QLineEdit(RequestStringDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)

        self.retranslateUi(RequestStringDialog)
        QtCore.QMetaObject.connectSlotsByName(RequestStringDialog)

    def retranslateUi(self, RequestStringDialog):
        RequestStringDialog.setWindowTitle(QtGui.QApplication.translate("RequestStringDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

