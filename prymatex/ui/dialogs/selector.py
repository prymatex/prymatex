# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/dialogs/selector.ui'
#
# Created: Wed Jun  5 22:34:44 2013
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

class Ui_SelectorDialog(object):
    def setupUi(self, SelectorDialog):
        SelectorDialog.setObjectName(_fromUtf8("SelectorDialog"))
        SelectorDialog.resize(600, 371)
        SelectorDialog.setMinimumSize(QtCore.QSize(600, 371))
        self.verticalLayout = QtGui.QVBoxLayout(SelectorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(SelectorDialog)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.listItems = QtGui.QListView(SelectorDialog)
        self.listItems.setAlternatingRowColors(True)
        self.listItems.setUniformItemSizes(True)
        self.listItems.setObjectName(_fromUtf8("listItems"))
        self.verticalLayout.addWidget(self.listItems)

        self.retranslateUi(SelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(SelectorDialog)

    def retranslateUi(self, SelectorDialog):
        pass

