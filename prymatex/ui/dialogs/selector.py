# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/dialogs/selector.ui'
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

class Ui_SelectorDialog(object):
    def setupUi(self, SelectorDialog):
        SelectorDialog.setObjectName(_fromUtf8("SelectorDialog"))
        SelectorDialog.resize(600, 371)
        SelectorDialog.setMinimumSize(QtCore.QSize(600, 371))
        self.verticalLayout = QtGui.QVBoxLayout(SelectorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(SelectorDialog)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.listItems = QtGui.QListView(SelectorDialog)
        self.listItems.setAlternatingRowColors(True)
        self.listItems.setUniformItemSizes(True)
        self.listItems.setObjectName(_fromUtf8("listItems"))
        self.verticalLayout.addWidget(self.listItems)

        self.retranslateUi(SelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(SelectorDialog)

    def retranslateUi(self, SelectorDialog):
        pass

