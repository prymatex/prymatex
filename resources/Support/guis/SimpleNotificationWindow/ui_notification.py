# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification.ui'
#
# Created: Thu May 24 21:38:56 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.qt import QtCore, QtGui

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
        self.labelSummary = QtGui.QLabel(NotificationDialog)
        self.labelSummary.setText(_fromUtf8(""))
        self.labelSummary.setObjectName(_fromUtf8("labelSummary"))
        self.verticalLayout.addWidget(self.labelSummary)
        self.textEditLog = QtGui.QTextEdit(NotificationDialog)
        self.textEditLog.setObjectName(_fromUtf8("textEditLog"))
        self.verticalLayout.addWidget(self.textEditLog)

        self.retranslateUi(NotificationDialog)
        QtCore.QMetaObject.connectSlotsByName(NotificationDialog)

    def retranslateUi(self, NotificationDialog):
        NotificationDialog.setWindowTitle(QtGui.QApplication.translate("NotificationDialog", "Notification", None, QtGui.QApplication.UnicodeUTF8))

