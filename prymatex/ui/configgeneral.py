# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configgeneral.ui'
#
# Created: Sun Jul 17 23:56:02 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName(_fromUtf8("General"))
        General.resize(454, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/Prymatex_Logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        General.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(General)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(General)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout.addWidget(self.checkBox_2)
        self.groupBox = QtGui.QGroupBox(General)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboTabVisibility = QtGui.QComboBox(self.groupBox)
        self.comboTabVisibility.setObjectName(_fromUtf8("comboTabVisibility"))
        self.gridLayout.addWidget(self.comboTabVisibility, 3, 1, 1, 3)
        self.labelTabVisibility = QtGui.QLabel(self.groupBox)
        self.labelTabVisibility.setObjectName(_fromUtf8("labelTabVisibility"))
        self.gridLayout.addWidget(self.labelTabVisibility, 3, 0, 1, 1)
        self.pushInsertAppName = QtGui.QPushButton(self.groupBox)
        self.pushInsertAppName.setObjectName(_fromUtf8("pushInsertAppName"))
        self.gridLayout.addWidget(self.pushInsertAppName, 2, 1, 1, 1)
        self.pushInsertProject = QtGui.QPushButton(self.groupBox)
        self.pushInsertProject.setObjectName(_fromUtf8("pushInsertProject"))
        self.gridLayout.addWidget(self.pushInsertProject, 2, 2, 1, 1)
        self.pushInsertFile = QtGui.QPushButton(self.groupBox)
        self.pushInsertFile.setObjectName(_fromUtf8("pushInsertFile"))
        self.gridLayout.addWidget(self.pushInsertFile, 2, 3, 1, 1)
        self.comboApplicationTitle = QtGui.QComboBox(self.groupBox)
        self.comboApplicationTitle.setEditable(True)
        self.comboApplicationTitle.setObjectName(_fromUtf8("comboApplicationTitle"))
        self.gridLayout.addWidget(self.comboApplicationTitle, 1, 1, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(_('General'))
        self.checkBox.setText(_('Highlight curent line'))
        self.checkBox_2.setText(_('Show right margin indicator'))
        self.groupBox.setTitle(_('Window Title'))
        self.label.setText(_('Title template'))
        self.labelTabVisibility.setText(_('Tab visibilty'))
        self.pushInsertAppName.setText(_('Application Name'))
        self.pushInsertProject.setText(_('Project Name'))
        self.pushInsertFile.setText(_('File Name'))

from prymatex import resources_rc
