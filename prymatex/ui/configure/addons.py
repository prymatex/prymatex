# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/addons.ui'
#
# Created: Mon Oct 29 22:41:39 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Addons(object):
    def setupUi(self, Addons):
        Addons.setObjectName(_fromUtf8("Addons"))
        Addons.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Addons)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEditFilter = QtGui.QLineEdit(Addons)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.tableViewAddons = QtGui.QTableView(Addons)
        self.tableViewAddons.setObjectName(_fromUtf8("tableViewAddons"))
        self.verticalLayout_2.addWidget(self.tableViewAddons)

        self.retranslateUi(Addons)
        QtCore.QMetaObject.connectSlotsByName(Addons)

    def retranslateUi(self, Addons):
        Addons.setWindowTitle(_('Terminal'))

