# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/command.ui'
#
# Created: Wed May 27 08:01:32 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Command(object):
    def setupUi(self, Command):
        Command.setObjectName("Command")
        Command.resize(409, 246)
        self.formLayout_2 = QtWidgets.QFormLayout(Command)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(Command)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.command = QtWidgets.QPlainTextEdit(Command)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName("command")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.command)
        self.label_3 = QtWidgets.QLabel(Command)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxInput = QtWidgets.QComboBox(Command)
        self.comboBoxInput.setObjectName("comboBoxInput")
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.labelInputOption = QtWidgets.QLabel(Command)
        self.labelInputOption.setObjectName("labelInputOption")
        self.horizontalLayout.addWidget(self.labelInputOption)
        self.comboBoxFallbackInput = QtWidgets.QComboBox(Command)
        self.comboBoxFallbackInput.setObjectName("comboBoxFallbackInput")
        self.horizontalLayout.addWidget(self.comboBoxFallbackInput)
        self.label_5 = QtWidgets.QLabel(Command)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.comboBoxInputFormat = QtWidgets.QComboBox(Command)
        self.comboBoxInputFormat.setObjectName("comboBoxInputFormat")
        self.horizontalLayout.addWidget(self.comboBoxInputFormat)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout_2.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(Command)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxOutputLocation = QtWidgets.QComboBox(Command)
        self.comboBoxOutputLocation.setObjectName("comboBoxOutputLocation")
        self.horizontalLayout_3.addWidget(self.comboBoxOutputLocation)
        self.label_6 = QtWidgets.QLabel(Command)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboBoxOutputFormat = QtWidgets.QComboBox(Command)
        self.comboBoxOutputFormat.setObjectName("comboBoxOutputFormat")
        self.horizontalLayout_3.addWidget(self.comboBoxOutputFormat)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.formLayout_2.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBoxOutputCaret = QtWidgets.QComboBox(Command)
        self.comboBoxOutputCaret.setObjectName("comboBoxOutputCaret")
        self.horizontalLayout_4.addWidget(self.comboBoxOutputCaret)
        self.checkBoxAutoScrollOutput = QtWidgets.QCheckBox(Command)
        self.checkBoxAutoScrollOutput.setObjectName("checkBoxAutoScrollOutput")
        self.horizontalLayout_4.addWidget(self.checkBoxAutoScrollOutput)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.formLayout_2.setLayout(7, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_7 = QtWidgets.QLabel(Command)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEditPattern = QtWidgets.QLineEdit(Command)
        self.lineEditPattern.setObjectName("lineEditPattern")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditPattern)
        self.label_8 = QtWidgets.QLabel(Command)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBoxBeforeRunning = QtWidgets.QComboBox(Command)
        self.comboBoxBeforeRunning.setObjectName("comboBoxBeforeRunning")
        self.horizontalLayout_2.addWidget(self.comboBoxBeforeRunning)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(Command)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)

        self.retranslateUi(Command)
        QtCore.QMetaObject.connectSlotsByName(Command)

    def retranslateUi(self, Command):
        _translate = QtCore.QCoreApplication.translate
        Command.setWindowTitle(_translate("Command", "Form"))
        self.label_2.setText(_translate("Command", "Command:"))
        self.label_3.setText(_translate("Command", "Input:"))
        self.labelInputOption.setText(_translate("Command", "or"))
        self.label_5.setText(_translate("Command", "format"))
        self.label_4.setText(_translate("Command", "Output:"))
        self.label_6.setText(_translate("Command", "format"))
        self.checkBoxAutoScrollOutput.setText(_translate("Command", "Scroll for new output"))
        self.label_7.setText(_translate("Command", "Caret:"))
        self.label_8.setText(_translate("Command", "Match:"))
        self.label.setText(_translate("Command", "Save:"))

