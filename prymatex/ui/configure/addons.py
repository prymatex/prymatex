# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/addons.ui'
#
# Created: Wed May 22 20:00:23 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
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

class Ui_Addons(object):
    def setupUi(self, Addons):
        Addons.setObjectName(_fromUtf8("Addons"))
        Addons.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Addons)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEditFilter = QtGui.QLineEdit(Addons)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.listViewAddons = QtGui.QListView(Addons)
        self.listViewAddons.setObjectName(_fromUtf8("listViewAddons"))
        self.verticalLayout_2.addWidget(self.listViewAddons)

        self.retranslateUi(Addons)
        QtCore.QMetaObject.connectSlotsByName(Addons)

    def retranslateUi(self, Addons):
        Addons.setWindowTitle(_translate("Addons", "Terminal", None))

