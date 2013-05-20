# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/support/macro.ui'
#
# Created: Tue May 14 21:59:16 2013
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

class Ui_Macro(object):
    def setupUi(self, Macro):
        Macro.setObjectName(_fromUtf8("Macro"))
        Macro.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Macro)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listActionWidget = QtGui.QListWidget(Macro)
        self.listActionWidget.setAlternatingRowColors(True)
        self.listActionWidget.setObjectName(_fromUtf8("listActionWidget"))
        self.verticalLayout.addWidget(self.listActionWidget)
        self.argument = QtGui.QPlainTextEdit(Macro)
        self.argument.setReadOnly(True)
        self.argument.setObjectName(_fromUtf8("argument"))
        self.verticalLayout.addWidget(self.argument)

        self.retranslateUi(Macro)
        QtCore.QMetaObject.connectSlotsByName(Macro)

    def retranslateUi(self, Macro):
        Macro.setWindowTitle(_translate("Macro", "Form", None))

