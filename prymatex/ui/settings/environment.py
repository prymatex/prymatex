# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/settings/environment.ui'
#
# Created: Thu Feb  9 14:57:25 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EnvVariables(object):
    def setupUi(self, EnvVariables):
        EnvVariables.setObjectName(_fromUtf8("EnvVariables"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EnvVariables.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(EnvVariables)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(EnvVariables)
        self.tableView.setShowGrid(False)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushAdd = QtGui.QPushButton(EnvVariables)
        self.pushAdd.setObjectName(_fromUtf8("pushAdd"))
        self.horizontalLayout.addWidget(self.pushAdd)
        self.pushRemove = QtGui.QPushButton(EnvVariables)
        self.pushRemove.setObjectName(_fromUtf8("pushRemove"))
        self.horizontalLayout.addWidget(self.pushRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(EnvVariables)
        QtCore.QMetaObject.connectSlotsByName(EnvVariables)

    def retranslateUi(self, EnvVariables):
        EnvVariables.setWindowTitle(_('Enviroment Variables'))
        self.pushAdd.setText(_('+'))
        self.pushRemove.setText(_('-'))

from prymatex import resources_rc
