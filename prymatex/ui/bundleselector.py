# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/bundleselector.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BundleSelector(object):
    def setupUi(self, BundleSelector):
        BundleSelector.setObjectName(_fromUtf8("BundleSelector"))
        BundleSelector.resize(600, 371)
        BundleSelector.setMinimumSize(QtCore.QSize(600, 371))
        BundleSelector.setWindowTitle(_('Bundle Selector'))
        self.verticalLayout = QtGui.QVBoxLayout(BundleSelector)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(BundleSelector)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.tableBundleItems = QtGui.QTableView(BundleSelector)
        self.tableBundleItems.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableBundleItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableBundleItems.setShowGrid(False)
        self.tableBundleItems.setObjectName(_fromUtf8("tableBundleItems"))
        self.tableBundleItems.horizontalHeader().setVisible(False)
        self.tableBundleItems.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableBundleItems)

        self.retranslateUi(BundleSelector)
        QtCore.QMetaObject.connectSlotsByName(BundleSelector)

    def retranslateUi(self, BundleSelector):
        pass

