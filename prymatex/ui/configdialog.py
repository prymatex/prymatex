# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configdialog.ui'
#
# Created: Sun Jul 17 21:59:52 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PMXSettingsDialog(object):
    def setupUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setObjectName(_fromUtf8("PMXSettingsDialog"))
        PMXSettingsDialog.resize(725, 225)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PMXSettingsDialog.sizePolicy().hasHeightForWidth())
        PMXSettingsDialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PMXSettingsDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PMXSettingsDialog)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(PMXSettingsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(self.layoutWidget)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.treeView = PMXConfigTreeView(self.layoutWidget)
        self.treeView.setMinimumSize(QtCore.QSize(250, 0))
        self.treeView.setLineWidth(0)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.mainContainer = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainContainer.sizePolicy().hasHeightForWidth())
        self.mainContainer.setSizePolicy(sizePolicy)
        self.mainContainer.setMinimumSize(QtCore.QSize(470, 0))
        self.mainContainer.setObjectName(_fromUtf8("mainContainer"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.mainContainer)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.labelTitle = QtGui.QLabel(self.mainContainer)
        self.labelTitle.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout_3.addWidget(self.labelTitle)
        self.container = QtGui.QWidget(self.mainContainer)
        self.container.setObjectName(_fromUtf8("container"))
        self.verticalLayout_3.addWidget(self.container)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(PMXSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(PMXSettingsDialog)

    def retranslateUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setWindowTitle(_('Prymatex Settings'))
        self.labelTitle.setText(_('TextLabel'))

from prymatex.gui.config.widgets import PMXConfigTreeView
from prymatex import resources_rc
