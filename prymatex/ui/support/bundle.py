# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/support/bundle.ui'
#
# Created: Fri Nov  9 18:10:45 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName(_fromUtf8("Menu"))
        Menu.resize(458, 349)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Menu)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeMenuView = QtGui.QTreeView(Menu)
        self.treeMenuView.setDragEnabled(True)
        self.treeMenuView.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeMenuView.setAlternatingRowColors(True)
        self.treeMenuView.setHeaderHidden(True)
        self.treeMenuView.setObjectName(_fromUtf8("treeMenuView"))
        self.horizontalLayout_2.addWidget(self.treeMenuView)
        self.listExcludedView = QtGui.QListView(Menu)
        self.listExcludedView.setDragEnabled(True)
        self.listExcludedView.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.listExcludedView.setAlternatingRowColors(True)
        self.listExcludedView.setObjectName(_fromUtf8("listExcludedView"))
        self.horizontalLayout_2.addWidget(self.listExcludedView)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        Menu.setWindowTitle(_('Form'))

