# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/support.ui'
#
# Created: Fri Aug 15 10:26:59 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Shebang(object):
    def setupUi(self, Shebang):
        Shebang.setObjectName(_fromUtf8("Shebang"))
        Shebang.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Shebang)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewShebangs = QtGui.QTableView(Shebang)
        self.tableViewShebangs.setObjectName(_fromUtf8("tableViewShebangs"))
        self.verticalLayout.addWidget(self.tableViewShebangs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtGui.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Shebang)
        QtCore.QMetaObject.connectSlotsByName(Shebang)

    def retranslateUi(self, Shebang):
        Shebang.setWindowTitle(_translate("Shebang", "Support Settings", None))

