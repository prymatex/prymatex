# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/environment.ui'
#
# Created: Thu Jan 17 19:51:02 2013
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
        Environment.resize(201, 275)
        self.verticalLayout = QtGui.QVBoxLayout(Environment)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewVariables = QtGui.QTableView(Environment)
        self.tableViewVariables.setShowGrid(False)
        self.tableViewVariables.setSortingEnabled(True)
        self.tableViewVariables.setObjectName(_fromUtf8("tableViewVariables"))
        self.verticalLayout.addWidget(self.tableViewVariables)
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
        self.pushButtonAdd = QtGui.QPushButton(Environment)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(Environment)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Environment)
        QtCore.QMetaObject.connectSlotsByName(Environment)

    def retranslateUi(self, Environment):
        Environment.setWindowTitle(_('Form'))

