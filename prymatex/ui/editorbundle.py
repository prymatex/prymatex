# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prymatex\resources\ui\editorbundle.ui'
#
# Created: Fri Jul 01 12:35:45 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.translation import ugettext as _
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
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeView = QtGui.QTreeView(Menu)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.horizontalLayout_2.addWidget(self.treeView)
        self.listView = QtGui.QListView(Menu)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.horizontalLayout_2.addWidget(self.listView)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        Menu.setWindowTitle(_('Form'))

from prymatex import resources_rc
