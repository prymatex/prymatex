# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/process.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExternalProcessDock(object):
    def setupUi(self, ExternalProcessDock):
        ExternalProcessDock.setObjectName("ExternalProcessDock")
        ExternalProcessDock.resize(330, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewExternalProcess = QtWidgets.QTreeView(self.dockWidgetContents)
        self.tableViewExternalProcess.setAlternatingRowColors(True)
        self.tableViewExternalProcess.setUniformRowHeights(True)
        self.tableViewExternalProcess.setHeaderHidden(True)
        self.tableViewExternalProcess.setObjectName("tableViewExternalProcess")
        self.verticalLayout.addWidget(self.tableViewExternalProcess)
        ExternalProcessDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(ExternalProcessDock)
        QtCore.QMetaObject.connectSlotsByName(ExternalProcessDock)

    def retranslateUi(self, ExternalProcessDock):
        _translate = QtCore.QCoreApplication.translate
        ExternalProcessDock.setWindowTitle(_translate("ExternalProcessDock", "Process"))

