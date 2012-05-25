# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification.ui'
#
# Created: Thu May 24 21:38:56 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NotificationDialog(object):
    def setupUi(self, NotificationDialog):
        NotificationDialog.setObjectName(_fromUtf8("NotificationDialog"))
        NotificationDialog.resize(300, 300)
        NotificationDialog.setMinimumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtGui.QVBoxLayout(NotificationDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelLog = QtGui.QLabel(NotificationDialog)
        self.labelLog.setText(_fromUtf8(""))
        self.labelLog.setObjectName(_fromUtf8("labelLog"))
        self.verticalLayout.addWidget(self.labelLog)
        self.textEditSummary = QtGui.QTextEdit(NotificationDialog)
        self.textEditSummary.setObjectName(_fromUtf8("textEditSummary"))
        self.verticalLayout.addWidget(self.textEditSummary)

        self.retranslateUi(NotificationDialog)
        QtCore.QMetaObject.connectSlotsByName(NotificationDialog)

    def retranslateUi(self, NotificationDialog):
        NotificationDialog.setWindowTitle(QtGui.QApplication.translate("NotificationDialog", "Notification", None, QtGui.QApplication.UnicodeUTF8))

