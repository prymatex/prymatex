# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/edit.ui'
#
# Created: Thu Sep 18 10:11:59 2014
#      by: PyQt4 UI code generator 4.10.4
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
        Edit.resize(385, 375)
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
        self.checkBoxAutoBrackets = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxAutoBrackets.setObjectName(_fromUtf8("checkBoxAutoBrackets"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBoxAutoBrackets)
        self.checkBoxRemoveTrailingSpaces = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxRemoveTrailingSpaces.setObjectName(_fromUtf8("checkBoxRemoveTrailingSpaces"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBoxRemoveTrailingSpaces)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_5 = QtGui.QGroupBox(Edit)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.formLayout_4 = QtGui.QFormLayout(self.groupBox_5)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setMargin(6)
        self.formLayout_4.setSpacing(2)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.radioButtonTabulators = QtGui.QRadioButton(self.groupBox_5)
        self.radioButtonTabulators.setObjectName(_fromUtf8("radioButtonTabulators"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.radioButtonTabulators)
        self.radioButtonSpaces = QtGui.QRadioButton(self.groupBox_5)
        self.radioButtonSpaces.setObjectName(_fromUtf8("radioButtonSpaces"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.radioButtonSpaces)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.groupBox_5)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBoxTabWidth = QtGui.QSpinBox(self.groupBox_5)
        self.spinBoxTabWidth.setMinimum(2)
        self.spinBoxTabWidth.setMaximum(20)
        self.spinBoxTabWidth.setProperty("value", 4)
        self.spinBoxTabWidth.setObjectName(_fromUtf8("spinBoxTabWidth"))
        self.horizontalLayout.addWidget(self.spinBoxTabWidth)
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_4 = QtGui.QLabel(self.groupBox_5)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spinBoxIndentationWidth = QtGui.QSpinBox(self.groupBox_5)
        self.spinBoxIndentationWidth.setMinimum(2)
        self.spinBoxIndentationWidth.setMaximum(20)
        self.spinBoxIndentationWidth.setProperty("value", 4)
        self.spinBoxIndentationWidth.setObjectName(_fromUtf8("spinBoxIndentationWidth"))
        self.horizontalLayout_3.addWidget(self.spinBoxIndentationWidth)
        self.formLayout_4.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.checkBoxAdjustIndentationOnPaste = QtGui.QCheckBox(self.groupBox_5)
        self.checkBoxAdjustIndentationOnPaste.setObjectName(_fromUtf8("checkBoxAdjustIndentationOnPaste"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.SpanningRole, self.checkBoxAdjustIndentationOnPaste)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_3 = QtGui.QGroupBox(Edit)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.checkBoxSmartHomeSmartEnd = QtGui.QCheckBox(self.groupBox_3)
        self.checkBoxSmartHomeSmartEnd.setObjectName(_fromUtf8("checkBoxSmartHomeSmartEnd"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBoxSmartHomeSmartEnd)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(Edit)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.checkBoxEnableAutoCompletion = QtGui.QCheckBox(self.groupBox_4)
        self.checkBoxEnableAutoCompletion.setObjectName(_fromUtf8("checkBoxEnableAutoCompletion"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBoxEnableAutoCompletion)
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.spinBoxWordLengthToComplete = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxWordLengthToComplete.setMinimum(3)
        self.spinBoxWordLengthToComplete.setMaximum(10)
        self.spinBoxWordLengthToComplete.setObjectName(_fromUtf8("spinBoxWordLengthToComplete"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxWordLengthToComplete)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem2 = QtGui.QSpacerItem(17, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Edit)
        QtCore.QMetaObject.connectSlotsByName(Edit)

    def retranslateUi(self, Edit):
        Edit.setWindowTitle(_translate("Edit", "Edit", None))
        self.groupBox_2.setTitle(_translate("Edit", "Misc", None))
        self.checkBoxAutoBrackets.setText(_translate("Edit", "Auto brackets", None))
        self.checkBoxRemoveTrailingSpaces.setText(_translate("Edit", "Remove trailing spaces while editing", None))
        self.groupBox_5.setTitle(_translate("Edit", "Indentation", None))
        self.radioButtonTabulators.setText(_translate("Edit", "Tabulators", None))
        self.radioButtonSpaces.setText(_translate("Edit", "Spaces", None))
        self.label_2.setText(_translate("Edit", "Tab width:", None))
        self.label_4.setText(_translate("Edit", "Indentation width:", None))
        self.checkBoxAdjustIndentationOnPaste.setText(_translate("Edit", "Adjust indentation of code pasted from the clipboard", None))
        self.groupBox_3.setTitle(_translate("Edit", "Text Cursor", None))
        self.checkBoxSmartHomeSmartEnd.setText(_translate("Edit", "Smart home and smart end", None))
        self.groupBox_4.setTitle(_translate("Edit", "Auto Completion", None))
        self.checkBoxEnableAutoCompletion.setText(_translate("Edit", "Enable auto completion", None))
        self.label.setText(_translate("Edit", "Minimal word length to complete:", None))

