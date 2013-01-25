# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/edit.ui'
#
# Created: Fri Jan 25 10:19:09 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Edit(object):
    def setupUi(self, Edit):
        Edit.setObjectName(_fromUtf8("Edit"))
        Edit.resize(279, 305)
        self.verticalLayout = QtGui.QVBoxLayout(Edit)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(Edit)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(Edit)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.checkBox_5 = QtGui.QCheckBox(self.groupBox_3)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox_5)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(Edit)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.checkBox_6 = QtGui.QCheckBox(self.groupBox_4)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox_6)
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.spinBox = QtGui.QSpinBox(self.groupBox_4)
        self.spinBox.setMinimum(3)
        self.spinBox.setMaximum(10)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem = QtGui.QSpacerItem(17, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Edit)
        QtCore.QMetaObject.connectSlotsByName(Edit)

    def retranslateUi(self, Edit):
        Edit.setWindowTitle(_('Edit'))
        self.groupBox_2.setTitle(_('Misc'))
        self.checkBox_3.setText(_('Auto brackets'))
        self.checkBox_2.setText(_('Remove trailing spaces while editing'))
        self.groupBox_3.setTitle(_('Text Cursor'))
        self.checkBox_5.setText(_('Smart home and smart end'))
        self.groupBox_4.setTitle(_('Auto Completion'))
        self.checkBox_6.setText(_('Enable auto completion'))
        self.label.setText(_('Minimal word length to complete:'))

