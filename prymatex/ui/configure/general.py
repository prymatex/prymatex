# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/general.ui'
#
# Created: Thu Feb 16 14:56:59 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GeneralWidget(object):
    def setupUi(self, GeneralWidget):
        GeneralWidget.setObjectName(_fromUtf8("GeneralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(GeneralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(GeneralWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboApplicationTitle_2 = QtGui.QComboBox(self.groupBox_2)
        self.comboApplicationTitle_2.setEditable(True)
        self.comboApplicationTitle_2.setObjectName(_fromUtf8("comboApplicationTitle_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboApplicationTitle_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushInsertAppName_2 = QtGui.QPushButton(self.groupBox_2)
        self.pushInsertAppName_2.setObjectName(_fromUtf8("pushInsertAppName_2"))
        self.horizontalLayout.addWidget(self.pushInsertAppName_2)
        self.pushInsertFile_2 = QtGui.QPushButton(self.groupBox_2)
        self.pushInsertFile_2.setObjectName(_fromUtf8("pushInsertFile_2"))
        self.horizontalLayout.addWidget(self.pushInsertFile_2)
        self.pushInsertProject_2 = QtGui.QPushButton(self.groupBox_2)
        self.pushInsertProject_2.setObjectName(_fromUtf8("pushInsertProject_2"))
        self.horizontalLayout.addWidget(self.pushInsertProject_2)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.labelTabVisibility_2 = QtGui.QLabel(self.groupBox_2)
        self.labelTabVisibility_2.setObjectName(_fromUtf8("labelTabVisibility_2"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelTabVisibility_2)
        self.comboTabVisibility_2 = QtGui.QComboBox(self.groupBox_2)
        self.comboTabVisibility_2.setObjectName(_fromUtf8("comboTabVisibility_2"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.comboTabVisibility_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(GeneralWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelEncoding = QtGui.QLabel(self.groupBox)
        self.labelEncoding.setObjectName(_fromUtf8("labelEncoding"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelEncoding)
        self.comboBoxEncoding = QtGui.QComboBox(self.groupBox)
        self.comboBoxEncoding.setObjectName(_fromUtf8("comboBoxEncoding"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.labelLineEnding = QtGui.QLabel(self.groupBox)
        self.labelLineEnding.setObjectName(_fromUtf8("labelLineEnding"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLineEnding)
        self.comboBoxLineEnding = QtGui.QComboBox(self.groupBox)
        self.comboBoxLineEnding.setObjectName(_fromUtf8("comboBoxLineEnding"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxLineEnding)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(GeneralWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBox)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(GeneralWidget)
        QtCore.QMetaObject.connectSlotsByName(GeneralWidget)

    def retranslateUi(self, GeneralWidget):
        GeneralWidget.setWindowTitle(_('General'))
        self.groupBox_2.setTitle(_('Main Window'))
        self.label_2.setText(_('Title template:'))
        self.pushInsertAppName_2.setText(_('Application Name'))
        self.pushInsertFile_2.setText(_('File Name'))
        self.pushInsertProject_2.setText(_('Project Name'))
        self.labelTabVisibility_2.setText(_('Tab visibilty:'))
        self.groupBox.setTitle(_('File Format'))
        self.labelEncoding.setText(_('Encoding'))
        self.labelLineEnding.setText(_('Line Ending'))
        self.groupBox_3.setTitle(_('Save / Backup'))
        self.checkBox.setText(_('Auto save on lost focus'))

