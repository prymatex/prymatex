# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/search.ui'
#
# Created: Thu Dec 11 08:36:24 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchDock(object):
    def setupUi(self, SearchDock):
        SearchDock.setObjectName("SearchDock")
        SearchDock.resize(262, 220)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        SearchDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SearchDock)
        QtCore.QMetaObject.connectSlotsByName(SearchDock)

    def retranslateUi(self, SearchDock):
        _translate = QtCore.QCoreApplication.translate
        SearchDock.setWindowTitle(_translate("SearchDock", "Search"))

