# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/general.ui'
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

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName(_fromUtf8("General"))
        General.resize(506, 274)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(General)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.comboBoxQtStyle = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxQtStyle.setEditable(True)
        self.comboBoxQtStyle.setObjectName(_fromUtf8("comboBoxQtStyle"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxQtStyle)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxQtTheme = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxQtTheme.setEditable(True)
        self.comboBoxQtTheme.setObjectName(_fromUtf8("comboBoxQtTheme"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxQtTheme)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(General)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.labelEncoding = QtGui.QLabel(self.groupBox)
        self.labelEncoding.setObjectName(_fromUtf8("labelEncoding"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelEncoding)
        self.comboBoxEncoding = QtGui.QComboBox(self.groupBox)
        self.comboBoxEncoding.setObjectName(_fromUtf8("comboBoxEncoding"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.labelLineEnding = QtGui.QLabel(self.groupBox)
        self.labelLineEnding.setObjectName(_fromUtf8("labelLineEnding"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLineEnding)
        self.comboBoxLineEnding = QtGui.QComboBox(self.groupBox)
        self.comboBoxLineEnding.setObjectName(_fromUtf8("comboBoxLineEnding"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxLineEnding)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(_('General'))
        self.groupBox_2.setTitle(_('Interface'))
        self.label_2.setText(_('Qt style:'))
        self.label_3.setText(_('Qt theme:'))
        self.groupBox.setTitle(_('Files'))
        self.labelEncoding.setText(_('Encoding'))
        self.labelLineEnding.setText(_('Line Ending'))

