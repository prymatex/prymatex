# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/others/filesystemsettings.ui'
#
# Created: Thu Jan 29 12:30:34 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FSSettingsDialog(object):
    def setupUi(self, FSSettingsDialog):
        FSSettingsDialog.setObjectName("FSSettingsDialog")
        FSSettingsDialog.resize(503, 291)
        self.verticalLayout = QtWidgets.QVBoxLayout(FSSettingsDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(FSSettingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFilters = QtWidgets.QWidget()
        self.tabFilters.setObjectName("tabFilters")
        self.gridLayout = QtWidgets.QGridLayout(self.tabFilters)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.tabFilters)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tabFilters)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.texteditIncludeFiles = QtWidgets.QTextEdit(self.tabFilters)
        self.texteditIncludeFiles.setObjectName("texteditIncludeFiles")
        self.gridLayout.addWidget(self.texteditIncludeFiles, 1, 0, 1, 1)
        self.texteditExcludeFiles = QtWidgets.QTextEdit(self.tabFilters)
        self.texteditExcludeFiles.setObjectName("texteditExcludeFiles")
        self.gridLayout.addWidget(self.texteditExcludeFiles, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tabFilters)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tabFilters)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.texteditIncludeDirs = QtWidgets.QTextEdit(self.tabFilters)
        self.texteditIncludeDirs.setObjectName("texteditIncludeDirs")
        self.gridLayout.addWidget(self.texteditIncludeDirs, 3, 0, 1, 1)
        self.texteditExcludeDirs = QtWidgets.QTextEdit(self.tabFilters)
        self.texteditExcludeDirs.setObjectName("texteditExcludeDirs")
        self.gridLayout.addWidget(self.texteditExcludeDirs, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tabFilters)
        self.label_5.setStyleSheet("QLabel {\n"
"    border: 1px solid yellow;\n"
"    background: white;\n"
"    padding: 6px;\n"
"}")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2)
        self.tabWidget.addTab(self.tabFilters, "")
        self.tabEnviroment = QtWidgets.QWidget()
        self.tabEnviroment.setObjectName("tabEnviroment")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabEnviroment)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.tabEnviroment)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.tabWidget.addTab(self.tabEnviroment, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(FSSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FSSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(FSSettingsDialog.accept)
        self.buttonBox.rejected.connect(FSSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FSSettingsDialog)

    def retranslateUi(self, FSSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        FSSettingsDialog.setWindowTitle(_translate("FSSettingsDialog", "File System Panel Settings"))
        self.label.setText(_translate("FSSettingsDialog", "Include Files..."))
        self.label_2.setText(_translate("FSSettingsDialog", "Exclude Files..."))
        self.label_3.setText(_translate("FSSettingsDialog", "Include Dirs..."))
        self.label_4.setText(_translate("FSSettingsDialog", "Exclude Dirs..."))
        self.label_5.setText(_translate("FSSettingsDialog", "Use commas for filter separation, i.e. *.o, *~"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), _translate("FSSettingsDialog", "Filters"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEnviroment), _translate("FSSettingsDialog", "Enviroment"))

