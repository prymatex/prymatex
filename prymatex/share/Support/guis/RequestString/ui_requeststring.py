# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requeststring.ui'
#
# Created: Tue Aug 28 17:38:43 2012
#      by: PyQt4 UI code generator 4.9.4
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
        RequestStringDialog.resize(318, 63)
        self.verticalLayout = QtGui.QVBoxLayout(RequestStringDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelPrompt = QtGui.QLabel(RequestStringDialog)
        self.labelPrompt.setObjectName(_fromUtf8("labelPrompt"))
        self.verticalLayout.addWidget(self.labelPrompt)
        self.lineEdit = QtGui.QLineEdit(RequestStringDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton1 = QtGui.QPushButton(RequestStringDialog)
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.horizontalLayout.addWidget(self.pushButton1)
        self.pushButton2 = QtGui.QPushButton(RequestStringDialog)
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.horizontalLayout.addWidget(self.pushButton2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RequestStringDialog)
        QtCore.QMetaObject.connectSlotsByName(RequestStringDialog)

    def retranslateUi(self, RequestStringDialog):
        RequestStringDialog.setWindowTitle(QtGui.QApplication.translate("RequestStringDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

