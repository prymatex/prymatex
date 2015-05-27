# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/shortcuts.ui'
#
# Created: Wed May 27 08:01:33 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Shortcuts(object):
    def setupUi(self, Shortcuts):
        Shortcuts.setObjectName("Shortcuts")
        Shortcuts.resize(499, 617)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Shortcuts)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Shortcuts)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditFilter = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout.addWidget(self.lineEditFilter)
        self.treeViewShortcuts = QtWidgets.QTreeView(self.groupBox)
        self.treeViewShortcuts.setObjectName("treeViewShortcuts")
        self.verticalLayout.addWidget(self.treeViewShortcuts)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonResetAll = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonResetAll.setObjectName("pushButtonResetAll")
        self.horizontalLayout.addWidget(self.pushButtonResetAll)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonImport = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonImport.setObjectName("pushButtonImport")
        self.horizontalLayout.addWidget(self.pushButtonImport)
        self.pushButtonExport = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.horizontalLayout.addWidget(self.pushButtonExport)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Shortcuts)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEditShortcut = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditShortcut.setObjectName("lineEditShortcut")
        self.horizontalLayout_3.addWidget(self.lineEditShortcut)
        self.pushButtonCleanShortcut = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonCleanShortcut.setText("")
        icon = QtGui.QIcon.fromTheme("clear-shortcut")
        self.pushButtonCleanShortcut.setIcon(icon)
        self.pushButtonCleanShortcut.setObjectName("pushButtonCleanShortcut")
        self.horizontalLayout_3.addWidget(self.pushButtonCleanShortcut)
        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.retranslateUi(Shortcuts)
        QtCore.QMetaObject.connectSlotsByName(Shortcuts)

    def retranslateUi(self, Shortcuts):
        _translate = QtCore.QCoreApplication.translate
        Shortcuts.setWindowTitle(_translate("Shortcuts", "Terminal"))
        self.groupBox.setTitle(_translate("Shortcuts", "Keyboard Shortcuts"))
        self.pushButtonResetAll.setText(_translate("Shortcuts", "Reset All"))
        self.pushButtonImport.setText(_translate("Shortcuts", "Import"))
        self.pushButtonExport.setText(_translate("Shortcuts", "Export"))
        self.groupBox_2.setTitle(_translate("Shortcuts", "Shortcut"))

