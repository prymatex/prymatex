# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requestitem.ui'
#
# Created: Tue Aug 28 17:06:13 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.qt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RequestItemDialog(object):
    def setupUi(self, RequestItemDialog):
        RequestItemDialog.setObjectName(_fromUtf8("RequestItemDialog"))
        RequestItemDialog.resize(318, 66)
        self.verticalLayout = QtGui.QVBoxLayout(RequestItemDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelPrompt = QtGui.QLabel(RequestItemDialog)
        self.labelPrompt.setObjectName(_fromUtf8("labelPrompt"))
        self.verticalLayout.addWidget(self.labelPrompt)
        self.comboBoxItems = QtGui.QComboBox(RequestItemDialog)
        self.comboBoxItems.setObjectName(_fromUtf8("comboBoxItems"))
        self.verticalLayout.addWidget(self.comboBoxItems)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton1 = QtGui.QPushButton(RequestItemDialog)
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.horizontalLayout.addWidget(self.pushButton1)
        self.pushButton2 = QtGui.QPushButton(RequestItemDialog)
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.horizontalLayout.addWidget(self.pushButton2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RequestItemDialog)
        QtCore.QMetaObject.connectSlotsByName(RequestItemDialog)

    def retranslateUi(self, RequestItemDialog):
        RequestItemDialog.setWindowTitle(QtGui.QApplication.translate("RequestItemDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

