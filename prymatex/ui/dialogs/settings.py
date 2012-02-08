# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/settings.ui'
#
# Created: Tue Feb  7 16:05:51 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(700, 433)
        SettingsDialog.setMinimumSize(QtCore.QSize(700, 433))
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(SettingsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.treeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setMargin(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.lineEditFilter = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.treeLayout.addWidget(self.lineEditFilter)
        self.treeViewSetting = QtGui.QTreeView(self.verticalLayoutWidget)
        self.treeViewSetting.setObjectName(_fromUtf8("treeViewSetting"))
        self.treeLayout.addWidget(self.treeViewSetting)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.settingLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.settingLayout.setSpacing(2)
        self.settingLayout.setMargin(0)
        self.settingLayout.setObjectName(_fromUtf8("settingLayout"))
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_('Settings'))

from prymatex import resources_rc
