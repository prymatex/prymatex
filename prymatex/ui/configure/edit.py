# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/edit.ui'
#
# Created: Wed May 22 20:00:33 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        Edit.setWindowTitle(_translate("Edit", "Edit", None))
        self.groupBox_2.setTitle(_translate("Edit", "Misc", None))
        self.checkBox_3.setText(_translate("Edit", "Auto brackets", None))
        self.checkBox_2.setText(_translate("Edit", "Remove trailing spaces while editing", None))
        self.groupBox_3.setTitle(_translate("Edit", "Text Cursor", None))
        self.checkBox_5.setText(_translate("Edit", "Smart home and smart end", None))
        self.groupBox_4.setTitle(_translate("Edit", "Auto Completion", None))
        self.checkBox_6.setText(_translate("Edit", "Enable auto completion", None))
        self.label.setText(_translate("Edit", "Minimal word length to complete:", None))

