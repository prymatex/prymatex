# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/support/language.ui'
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

class Ui_Language(object):
    def setupUi(self, Language):
        Language.setObjectName(_fromUtf8("Language"))
        Language.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Language)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.content = QtGui.QPlainTextEdit(Language)
        self.content.setObjectName(_fromUtf8("content"))
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(Language)
        QtCore.QMetaObject.connectSlotsByName(Language)

    def retranslateUi(self, Language):
        Language.setWindowTitle(_translate("Language", "Form", None))

