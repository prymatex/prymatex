# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/environment.ui'
#
# Created: Fri Sep  7 14:19:37 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Environment(object):
    def setupUi(self, Environment):
        Environment.setObjectName(_fromUtf8("Environment"))
        Environment.resize(189, 275)
        self.verticalLayout = QtGui.QVBoxLayout(Environment)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(Environment)
        self.tableView.setShowGrid(False)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox1 = QtGui.QCheckBox(Environment)
        self.checkBox1.setObjectName(_fromUtf8("checkBox1"))
        self.horizontalLayout.addWidget(self.checkBox1)
        self.checkBox2 = QtGui.QCheckBox(Environment)
        self.checkBox2.setObjectName(_fromUtf8("checkBox2"))
        self.horizontalLayout.addWidget(self.checkBox2)
        self.checkBox3 = QtGui.QCheckBox(Environment)
        self.checkBox3.setObjectName(_fromUtf8("checkBox3"))
        self.horizontalLayout.addWidget(self.checkBox3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushAdd = QtGui.QPushButton(Environment)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushAdd.setIcon(icon)
        self.pushAdd.setObjectName(_fromUtf8("pushAdd"))
        self.horizontalLayout.addWidget(self.pushAdd)
        self.pushRemove = QtGui.QPushButton(Environment)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushRemove.setIcon(icon)
        self.pushRemove.setObjectName(_fromUtf8("pushRemove"))
        self.horizontalLayout.addWidget(self.pushRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Environment)
        QtCore.QMetaObject.connectSlotsByName(Environment)

    def retranslateUi(self, Environment):
        Environment.setWindowTitle(_('Form'))

