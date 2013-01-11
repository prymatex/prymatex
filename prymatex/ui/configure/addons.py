# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/addons.ui'
#
# Created: Fri Jan 11 10:55:13 2013
#      by: PyQt4 UI code generator 4.9.3
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
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEditFilter = QtGui.QLineEdit(Addons)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.listViewAddons = QtGui.QListView(Addons)
        self.listViewAddons.setObjectName(_fromUtf8("listViewAddons"))
        self.verticalLayout_2.addWidget(self.listViewAddons)

        self.retranslateUi(Addons)
        QtCore.QMetaObject.connectSlotsByName(Addons)

    def retranslateUi(self, Addons):
        Addons.setWindowTitle(_('Terminal'))

