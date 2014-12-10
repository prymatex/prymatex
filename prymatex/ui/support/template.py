# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/template.ui'
#
# Created: Wed Dec 10 13:43:27 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Template(object):
    def setupUi(self, Template):
        Template.setObjectName("Template")
        Template.resize(361, 237)
        self.formLayout_2 = QtWidgets.QFormLayout(Template)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(Template)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditExtension = QtWidgets.QLineEdit(Template)
        self.lineEditExtension.setObjectName("lineEditExtension")
        self.horizontalLayout_2.addWidget(self.lineEditExtension)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(Template)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.command = QtWidgets.QPlainTextEdit(Template)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName("command")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.command)
        self.label_4 = QtWidgets.QLabel(Template)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxOutput = QtWidgets.QComboBox(Template)
        self.comboBoxOutput.setObjectName("comboBoxOutput")
        self.horizontalLayout_3.addWidget(self.comboBoxOutput)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(Template)
        QtCore.QMetaObject.connectSlotsByName(Template)

    def retranslateUi(self, Template):
        _translate = QtCore.QCoreApplication.translate
        Template.setWindowTitle(_translate("Template", "Form"))
        self.label.setText(_translate("Template", "Extension:"))
        self.label_2.setText(_translate("Template", "Command(s):"))
        self.label_4.setText(_translate("Template", "Output:"))

