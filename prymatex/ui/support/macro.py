# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/support/macro.ui'
#
# Created: Mon Nov  7 18:31:02 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Macro(object):
    def setupUi(self, Macro):
        Macro.setObjectName(_fromUtf8("Macro"))
        Macro.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Macro)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listViewAction = QtGui.QListView(Macro)
        self.listViewAction.setAlternatingRowColors(True)
        self.listViewAction.setObjectName(_fromUtf8("listViewAction"))
        self.verticalLayout.addWidget(self.listViewAction)
        self.content = QtGui.QPlainTextEdit(Macro)
        self.content.setObjectName(_fromUtf8("content"))
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(Macro)
        QtCore.QMetaObject.connectSlotsByName(Macro)

    def retranslateUi(self, Macro):
        Macro.setWindowTitle(_('Form'))

