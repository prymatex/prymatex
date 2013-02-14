# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/environment.ui'
#
# Created: Thu Feb 14 10:35:13 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MultiDictTableEditorWidget(object):
    def setupUi(self, MultiDictTableEditorWidget):
        MultiDictTableEditorWidget.setObjectName(_fromUtf8("MultiDictTableEditorWidget"))
        self._2 = QtGui.QVBoxLayout(MultiDictTableEditorWidget)
        self._2.setObjectName(_fromUtf8("_2"))
        self.tableViewVariables = QtGui.QTableView(MultiDictTableEditorWidget)
        self.tableViewVariables.setShowGrid(False)
        self.tableViewVariables.setSortingEnabled(True)
        self.tableViewVariables.setObjectName(_fromUtf8("tableViewVariables"))
        self._2.addWidget(self.tableViewVariables)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBoxNamespaces = QtGui.QComboBox(MultiDictTableEditorWidget)
        self.comboBoxNamespaces.setObjectName(_fromUtf8("comboBoxNamespaces"))
        self.horizontalLayout.addWidget(self.comboBoxNamespaces)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtGui.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(MultiDictTableEditorWidget)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self._2.addLayout(self.horizontalLayout)

        self.retranslateUi(MultiDictTableEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(MultiDictTableEditorWidget)

    def retranslateUi(self, MultiDictTableEditorWidget):
        pass

