# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tabchoose.ui'
#
# Created: Sun Jul 17 21:59:52 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ChooseTab(object):
    def setupUi(self, ChooseTab):
        ChooseTab.setObjectName(_fromUtf8("ChooseTab"))
        ChooseTab.resize(310, 170)
        self.verticalLayout = QtGui.QVBoxLayout(ChooseTab)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit = QtGui.QLineEdit(ChooseTab)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.listView = QtGui.QListView(ChooseTab)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOpen = QtGui.QPushButton(ChooseTab)
        self.pushOpen.setDefault(True)
        self.pushOpen.setObjectName(_fromUtf8("pushOpen"))
        self.horizontalLayout.addWidget(self.pushOpen)
        self.pushCancel = QtGui.QPushButton(ChooseTab)
        self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ChooseTab)
        QtCore.QMetaObject.connectSlotsByName(ChooseTab)

    def retranslateUi(self, ChooseTab):
        ChooseTab.setWindowTitle(_('Dialog'))
        self.pushOpen.setText(_('OK'))
        self.pushCancel.setText(_('Cancel'))

