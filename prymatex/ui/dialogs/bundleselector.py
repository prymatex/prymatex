# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/bundleselector.ui'
#
# Created: Tue Dec  6 18:43:55 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BundleSelectorDialog(object):
    def setupUi(self, BundleSelectorDialog):
        BundleSelectorDialog.setObjectName(_fromUtf8("BundleSelectorDialog"))
        BundleSelectorDialog.resize(600, 371)
        BundleSelectorDialog.setMinimumSize(QtCore.QSize(600, 371))
        self.verticalLayout = QtGui.QVBoxLayout(BundleSelectorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(BundleSelectorDialog)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.tableBundleItems = QtGui.QTableView(BundleSelectorDialog)
        self.tableBundleItems.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableBundleItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableBundleItems.setShowGrid(False)
        self.tableBundleItems.setObjectName(_fromUtf8("tableBundleItems"))
        self.tableBundleItems.horizontalHeader().setVisible(False)
        self.tableBundleItems.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableBundleItems)

        self.retranslateUi(BundleSelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(BundleSelectorDialog)

    def retranslateUi(self, BundleSelectorDialog):
        BundleSelectorDialog.setWindowTitle(_('Bundle Selector'))

