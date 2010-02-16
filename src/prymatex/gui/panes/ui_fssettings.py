# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/fssettings.ui'
#
# Created: Tue Feb 16 12:31:10 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FSSettingsDialog(object):
    def setupUi(self, FSSettingsDialog):
        FSSettingsDialog.setObjectName("FSSettingsDialog")
        FSSettingsDialog.resize(503, 290)
        self.verticalLayout = QtGui.QVBoxLayout(FSSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(FSSettingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFilters = QtGui.QWidget()
        self.tabFilters.setObjectName("tabFilters")
        self.gridLayout = QtGui.QGridLayout(self.tabFilters)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.tabFilters)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tabFilters)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.texteditIncludeFiles = QtGui.QTextEdit(self.tabFilters)
        self.texteditIncludeFiles.setObjectName("texteditIncludeFiles")
        self.gridLayout.addWidget(self.texteditIncludeFiles, 1, 0, 1, 1)
        self.texteditExcludeFiles = QtGui.QTextEdit(self.tabFilters)
        self.texteditExcludeFiles.setObjectName("texteditExcludeFiles")
        self.gridLayout.addWidget(self.texteditExcludeFiles, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tabFilters)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.tabFilters)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.texteditIncludeDirs = QtGui.QTextEdit(self.tabFilters)
        self.texteditIncludeDirs.setObjectName("texteditIncludeDirs")
        self.gridLayout.addWidget(self.texteditIncludeDirs, 3, 0, 1, 1)
        self.texteditExcludeDirs = QtGui.QTextEdit(self.tabFilters)
        self.texteditExcludeDirs.setObjectName("texteditExcludeDirs")
        self.gridLayout.addWidget(self.texteditExcludeDirs, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tabFilters)
        self.label_5.setStyleSheet("""QLabel {
    border: 1px solid yellow;
    background: white;
    padding: 6px;
}""")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2)
        self.tabWidget.addTab(self.tabFilters, "")
        self.tabEnviroment = QtGui.QWidget()
        self.tabEnviroment.setObjectName("tabEnviroment")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabEnviroment)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtGui.QTableView(self.tabEnviroment)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.tabWidget.addTab(self.tabEnviroment, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(FSSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FSSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), FSSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), FSSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FSSettingsDialog)

    def retranslateUi(self, FSSettingsDialog):
        FSSettingsDialog.setWindowTitle(QtGui.QApplication.translate("FSSettingsDialog", "File System Panel Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FSSettingsDialog", "Include Files...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FSSettingsDialog", "Exclude Files...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FSSettingsDialog", "Include Dirs...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FSSettingsDialog", "Exclude Dirs...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FSSettingsDialog", "Use commas for filter separation, i.e. *.o, *~", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), QtGui.QApplication.translate("FSSettingsDialog", "Filters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEnviroment), QtGui.QApplication.translate("FSSettingsDialog", "Enviroment", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FSSettingsDialog = QtGui.QDialog()
    ui = Ui_FSSettingsDialog()
    ui.setupUi(FSSettingsDialog)
    FSSettingsDialog.show()
    sys.exit(app.exec_())

