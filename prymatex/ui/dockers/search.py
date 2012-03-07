# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/search.ui'
#
# Created: Wed Mar  7 15:22:52 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchDock(object):
    def setupUi(self, SearchDock):
        SearchDock.setObjectName(_fromUtf8("SearchDock"))
        SearchDock.resize(262, 220)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeView = QtGui.QTreeView(self.dockWidgetContents)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        SearchDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SearchDock)
        QtCore.QMetaObject.connectSlotsByName(SearchDock)

    def retranslateUi(self, SearchDock):
        SearchDock.setWindowTitle(_('Search'))

from prymatex import resources_rc
