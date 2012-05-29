# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requestitem.ui'
#
# Created: Tue May 29 10:42:17 2012
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RequestItemDialog(object):
    def setupUi(self, RequestItemDialog):
        RequestItemDialog.setObjectName(_fromUtf8("RequestItemDialog"))
        RequestItemDialog.resize(318, 39)
        self.verticalLayout = QtGui.QVBoxLayout(RequestItemDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit = QtGui.QLineEdit(RequestItemDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)

        self.retranslateUi(RequestItemDialog)
        QtCore.QMetaObject.connectSlotsByName(RequestItemDialog)

    def retranslateUi(self, RequestItemDialog):
        RequestItemDialog.setWindowTitle(QtGui.QApplication.translate("RequestItemDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

