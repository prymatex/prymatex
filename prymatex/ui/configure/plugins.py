# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/plugins.ui'
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

class Ui_Plugins(object):
    def setupUi(self, Plugins):
        Plugins.setObjectName(_fromUtf8("Plugins"))
        Plugins.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Plugins)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEditFilter = QtGui.QLineEdit(Plugins)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.listViewPlugins = QtGui.QListView(Plugins)
        self.listViewPlugins.setObjectName(_fromUtf8("listViewPlugins"))
        self.verticalLayout_2.addWidget(self.listViewPlugins)

        self.retranslateUi(Plugins)
        QtCore.QMetaObject.connectSlotsByName(Plugins)

    def retranslateUi(self, Plugins):
        Plugins.setWindowTitle(_('Terminal'))

