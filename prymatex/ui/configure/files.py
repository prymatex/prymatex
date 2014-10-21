# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/files.ui'
#
# Created: Tue Oct 21 18:29:52 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Files(object):
    def setupUi(self, Files):
        Files.setObjectName("Files")
        Files.resize(272, 281)
        self.verticalLayout = QtWidgets.QVBoxLayout(Files)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Files)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(40)
        self.spinBox.setSingleStep(5)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(Files)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setContentsMargins(6, 6, 6, 6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelEncoding = QtWidgets.QLabel(self.groupBox)
        self.labelEncoding.setObjectName("labelEncoding")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelEncoding)
        self.comboBoxEncoding = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxEncoding.setObjectName("comboBoxEncoding")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.labelEndOfLine = QtWidgets.QLabel(self.groupBox)
        self.labelEndOfLine.setObjectName("labelEndOfLine")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelEndOfLine)
        self.comboBoxEndOfLine = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxEndOfLine.setObjectName("comboBoxEndOfLine")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxEndOfLine)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.checkBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Files)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox_3)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Files)
        QtCore.QMetaObject.connectSlotsByName(Files)

    def retranslateUi(self, Files):
        _translate = QtCore.QCoreApplication.translate
        Files.setWindowTitle(_translate("Files", "Files"))
        self.groupBox_3.setTitle(_translate("Files", "Source"))
        self.label.setText(_translate("Files", "File history:"))
        self.groupBox.setTitle(_translate("Files", "File format"))
        self.labelEncoding.setText(_translate("Files", "Encoding:"))
        self.labelEndOfLine.setText(_translate("Files", "End of line:"))
        self.checkBox.setText(_translate("Files", "Automatic end of line detection"))
        self.groupBox_2.setTitle(_translate("Files", "Automatic cleanups"))
        self.checkBox_2.setText(_translate("Files", "Remove trailing spaces"))
        self.checkBox_3.setText(_translate("Files", "Append newline at end of file on save"))

