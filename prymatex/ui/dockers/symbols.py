# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/symbols.ui'
#
# Created: Tue Dec  9 12:44:19 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SymbolsDock(object):
    def setupUi(self, SymbolsDock):
        SymbolsDock.setObjectName("SymbolsDock")
        SymbolsDock.resize(400, 300)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeViewSymbols = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewSymbols.setObjectName("treeViewSymbols")
        self.verticalLayout.addWidget(self.treeViewSymbols)
        SymbolsDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SymbolsDock)
        QtCore.QMetaObject.connectSlotsByName(SymbolsDock)

    def retranslateUi(self, SymbolsDock):
        _translate = QtCore.QCoreApplication.translate
        SymbolsDock.setWindowTitle(_translate("SymbolsDock", "Symbols"))

