# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/editorbundle.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
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
        Menu.setWindowTitle(_('Form'))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Menu)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeMenuWidget = QtGui.QTreeWidget(Menu)
        self.treeMenuWidget.setDragEnabled(True)
        self.treeMenuWidget.setDragDropOverwriteMode(False)
        self.treeMenuWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeMenuWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeMenuWidget.setObjectName(_fromUtf8("treeMenuWidget"))
        self.treeMenuWidget.headerItem().setText(0, _('Menu Structure'))
        self.horizontalLayout_2.addWidget(self.treeMenuWidget)
        self.treeExcludedWidget = QtGui.QTreeWidget(Menu)
        self.treeExcludedWidget.setDragEnabled(True)
        self.treeExcludedWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeExcludedWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeExcludedWidget.setObjectName(_fromUtf8("treeExcludedWidget"))
        self.treeExcludedWidget.headerItem().setText(0, _('Excluded Items'))
        self.horizontalLayout_2.addWidget(self.treeExcludedWidget)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        pass

