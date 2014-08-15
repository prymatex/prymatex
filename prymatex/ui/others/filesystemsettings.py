# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/others/filesystemsettings.ui'
#
# Created: Fri Aug 15 10:26:58 2014
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

class Ui_FSSettingsDialog(object):
    def setupUi(self, FSSettingsDialog):
        FSSettingsDialog.setObjectName(_fromUtf8("FSSettingsDialog"))
        FSSettingsDialog.resize(503, 291)
        self.verticalLayout = QtGui.QVBoxLayout(FSSettingsDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(FSSettingsDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabFilters = QtGui.QWidget()
        self.tabFilters.setObjectName(_fromUtf8("tabFilters"))
        self.gridLayout = QtGui.QGridLayout(self.tabFilters)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.tabFilters)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tabFilters)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.texteditIncludeFiles = QtGui.QTextEdit(self.tabFilters)
        self.texteditIncludeFiles.setObjectName(_fromUtf8("texteditIncludeFiles"))
        self.gridLayout.addWidget(self.texteditIncludeFiles, 1, 0, 1, 1)
        self.texteditExcludeFiles = QtGui.QTextEdit(self.tabFilters)
        self.texteditExcludeFiles.setObjectName(_fromUtf8("texteditExcludeFiles"))
        self.gridLayout.addWidget(self.texteditExcludeFiles, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tabFilters)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.tabFilters)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.texteditIncludeDirs = QtGui.QTextEdit(self.tabFilters)
        self.texteditIncludeDirs.setObjectName(_fromUtf8("texteditIncludeDirs"))
        self.gridLayout.addWidget(self.texteditIncludeDirs, 3, 0, 1, 1)
        self.texteditExcludeDirs = QtGui.QTextEdit(self.tabFilters)
        self.texteditExcludeDirs.setObjectName(_fromUtf8("texteditExcludeDirs"))
        self.gridLayout.addWidget(self.texteditExcludeDirs, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tabFilters)
        self.label_5.setStyleSheet(_fromUtf8("QLabel {\n"
"    border: 1px solid yellow;\n"
"    background: white;\n"
"    padding: 6px;\n"
"}"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2)
        self.tabWidget.addTab(self.tabFilters, _fromUtf8(""))
        self.tabEnviroment = QtGui.QWidget()
        self.tabEnviroment.setObjectName(_fromUtf8("tabEnviroment"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabEnviroment)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tableView = QtGui.QTableView(self.tabEnviroment)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)
        self.tabWidget.addTab(self.tabEnviroment, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(FSSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FSSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FSSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FSSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FSSettingsDialog)

    def retranslateUi(self, FSSettingsDialog):
        FSSettingsDialog.setWindowTitle(_translate("FSSettingsDialog", "File System Panel Settings", None))
        self.label.setText(_translate("FSSettingsDialog", "Include Files...", None))
        self.label_2.setText(_translate("FSSettingsDialog", "Exclude Files...", None))
        self.label_3.setText(_translate("FSSettingsDialog", "Include Dirs...", None))
        self.label_4.setText(_translate("FSSettingsDialog", "Exclude Dirs...", None))
        self.label_5.setText(_translate("FSSettingsDialog", "Use commas for filter separation, i.e. *.o, *~", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), _translate("FSSettingsDialog", "Filters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEnviroment), _translate("FSSettingsDialog", "Enviroment", None))

