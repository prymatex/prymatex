# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/dockers/symbols.ui'
#
# Created: Tue May 14 21:59:13 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
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

class Ui_SymbolsDock(object):
    def setupUi(self, SymbolsDock):
        SymbolsDock.setObjectName(_fromUtf8("SymbolsDock"))
        SymbolsDock.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeViewSymbols = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewSymbols.setObjectName(_fromUtf8("treeViewSymbols"))
        self.verticalLayout.addWidget(self.treeViewSymbols)
        SymbolsDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SymbolsDock)
        QtCore.QMetaObject.connectSlotsByName(SymbolsDock)

    def retranslateUi(self, SymbolsDock):
        SymbolsDock.setWindowTitle(_translate("SymbolsDock", "Symbols", None))

