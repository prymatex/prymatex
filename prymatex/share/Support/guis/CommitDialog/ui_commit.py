# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commit.ui'
#
# Created: Sat Sep  8 15:29:44 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.qt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CommitDialog(object):
    def setupUi(self, CommitDialog):
        CommitDialog.setObjectName(_fromUtf8("CommitDialog"))
        CommitDialog.resize(500, 384)
        CommitDialog.setMinimumSize(QtCore.QSize(500, 0))
        self.verticalLayout = QtGui.QVBoxLayout(CommitDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(CommitDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBoxSummary = QtGui.QComboBox(CommitDialog)
        self.comboBoxSummary.setObjectName(_fromUtf8("comboBoxSummary"))
        self.horizontalLayout_2.addWidget(self.comboBoxSummary)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textEditSummary = QtGui.QTextEdit(CommitDialog)
        self.textEditSummary.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textEditSummary.setObjectName(_fromUtf8("textEditSummary"))
        self.verticalLayout.addWidget(self.textEditSummary)
        self.label_2 = QtGui.QLabel(CommitDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.tableViewFiles = QtGui.QTableView(CommitDialog)
        #self.tableViewFiles.setAlternatingRowColors(True)
        self.tableViewFiles.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewFiles.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewFiles.setObjectName(_fromUtf8("tableViewFiles"))
        self.verticalLayout.addWidget(self.tableViewFiles)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.toolButtonSelect = QtGui.QToolButton(CommitDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-select"))
        self.toolButtonSelect.setIcon(icon)
        self.toolButtonSelect.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonSelect.setAutoRaise(True)
        self.toolButtonSelect.setObjectName(_fromUtf8("toolButtonSelect"))
        self.horizontalLayout.addWidget(self.toolButtonSelect)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonOk = QtGui.QPushButton(CommitDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-ok"))
        self.buttonOk.setIcon(icon)
        self.buttonOk.setObjectName(_fromUtf8("buttonOk"))
        self.horizontalLayout.addWidget(self.buttonOk)
        self.buttonCancel = QtGui.QPushButton(CommitDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CommitDialog)
        QtCore.QMetaObject.connectSlotsByName(CommitDialog)

    def retranslateUi(self, CommitDialog):
        CommitDialog.setWindowTitle(QtGui.QApplication.translate("CommitDialog", "GitHub Client", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CommitDialog", "Summary of changes:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CommitDialog", "Chose files to commit:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOk.setText(QtGui.QApplication.translate("CommitDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("CommitDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

