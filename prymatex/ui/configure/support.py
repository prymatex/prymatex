# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/support.ui'
#
# Created: Fri Jan 11 11:36:45 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Shebang(object):
    def setupUi(self, Shebang):
        Shebang.setObjectName(_fromUtf8("Shebang"))
        Shebang.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Shebang)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewShebangs = QtGui.QTableView(Shebang)
        self.tableViewShebangs.setObjectName(_fromUtf8("tableViewShebangs"))
        self.verticalLayout.addWidget(self.tableViewShebangs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtGui.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(Shebang)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Shebang)
        QtCore.QMetaObject.connectSlotsByName(Shebang)

    def retranslateUi(self, Shebang):
        Shebang.setWindowTitle(_('Support Settings'))

