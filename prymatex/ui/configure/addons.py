# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/addons.ui'
#
# Created: Sat Oct 27 10:13:15 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Terminal(object):
    def setupUi(self, Terminal):
        Terminal.setObjectName(_fromUtf8("Terminal"))
        Terminal.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Terminal)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineFont = QtGui.QLineEdit(Terminal)
        self.lineFont.setReadOnly(True)
        self.lineFont.setObjectName(_fromUtf8("lineFont"))
        self.verticalLayout_2.addWidget(self.lineFont)
        self.tableView = QtGui.QTableView(Terminal)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)

        self.retranslateUi(Terminal)
        QtCore.QMetaObject.connectSlotsByName(Terminal)

    def retranslateUi(self, Terminal):
        Terminal.setWindowTitle(_('Terminal'))

