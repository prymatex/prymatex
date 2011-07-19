# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/bundleselector.ui'
#
# Created: Tue Jul 19 15:22:13 2011
#      by: PyQt4 UI code generator 4.8.3
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
        BundleSelector.resize(274, 236)
        self.verticalLayout = QtGui.QVBoxLayout(BundleSelector)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(BundleSelector)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.listBundleItems = QtGui.QListView(BundleSelector)
        self.listBundleItems.setObjectName(_fromUtf8("listBundleItems"))
        self.verticalLayout.addWidget(self.listBundleItems)

        self.retranslateUi(BundleSelector)
        QtCore.QMetaObject.connectSlotsByName(BundleSelector)

    def retranslateUi(self, BundleSelector):
        BundleSelector.setWindowTitle(_('Dialog'))

