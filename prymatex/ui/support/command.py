# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/command.ui'
#
# Created: Thu Sep 18 09:56:55 2014
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

class Ui_Command(object):
    def setupUi(self, Command):
        Command.setObjectName(_fromUtf8("Command"))
        Command.resize(421, 317)
        self.formLayout_2 = QtGui.QFormLayout(Command)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(Command)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.command = QtGui.QPlainTextEdit(Command)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName(_fromUtf8("command"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.command)
        self.label_3 = QtGui.QLabel(Command)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBoxInput = QtGui.QComboBox(Command)
        self.comboBoxInput.setObjectName(_fromUtf8("comboBoxInput"))
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.labelInputOption = QtGui.QLabel(Command)
        self.labelInputOption.setObjectName(_fromUtf8("labelInputOption"))
        self.horizontalLayout.addWidget(self.labelInputOption)
        self.comboBoxFallbackInput = QtGui.QComboBox(Command)
        self.comboBoxFallbackInput.setObjectName(_fromUtf8("comboBoxFallbackInput"))
        self.horizontalLayout.addWidget(self.comboBoxFallbackInput)
        self.label_5 = QtGui.QLabel(Command)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        self.comboBoxInputFormat = QtGui.QComboBox(Command)
        self.comboBoxInputFormat.setObjectName(_fromUtf8("comboBoxInputFormat"))
        self.horizontalLayout.addWidget(self.comboBoxInputFormat)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout_2.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtGui.QLabel(Command)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxOutputLocation = QtGui.QComboBox(Command)
        self.comboBoxOutputLocation.setObjectName(_fromUtf8("comboBoxOutputLocation"))
        self.horizontalLayout_3.addWidget(self.comboBoxOutputLocation)
        self.label_6 = QtGui.QLabel(Command)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboBoxOutputFormat = QtGui.QComboBox(Command)
        self.comboBoxOutputFormat.setObjectName(_fromUtf8("comboBoxOutputFormat"))
        self.horizontalLayout_3.addWidget(self.comboBoxOutputFormat)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.formLayout_2.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.comboBoxOutputCaret = QtGui.QComboBox(Command)
        self.comboBoxOutputCaret.setObjectName(_fromUtf8("comboBoxOutputCaret"))
        self.horizontalLayout_4.addWidget(self.comboBoxOutputCaret)
        self.checkBoxAutoScrollOutput = QtGui.QCheckBox(Command)
        self.checkBoxAutoScrollOutput.setObjectName(_fromUtf8("checkBoxAutoScrollOutput"))
        self.horizontalLayout_4.addWidget(self.checkBoxAutoScrollOutput)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.formLayout_2.setLayout(7, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_7 = QtGui.QLabel(Command)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEditPattern = QtGui.QLineEdit(Command)
        self.lineEditPattern.setObjectName(_fromUtf8("lineEditPattern"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditPattern)
        self.label_8 = QtGui.QLabel(Command)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_8)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboBoxBeforeRunning = QtGui.QComboBox(Command)
        self.comboBoxBeforeRunning.setObjectName(_fromUtf8("comboBoxBeforeRunning"))
        self.horizontalLayout_2.addWidget(self.comboBoxBeforeRunning)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label = QtGui.QLabel(Command)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)

        self.retranslateUi(Command)
        QtCore.QMetaObject.connectSlotsByName(Command)

    def retranslateUi(self, Command):
        Command.setWindowTitle(_translate("Command", "Form", None))
        self.label_2.setText(_translate("Command", "Command:", None))
        self.label_3.setText(_translate("Command", "Input:", None))
        self.labelInputOption.setText(_translate("Command", "or", None))
        self.label_5.setText(_translate("Command", "format", None))
        self.label_4.setText(_translate("Command", "Output:", None))
        self.label_6.setText(_translate("Command", "format", None))
        self.checkBoxAutoScrollOutput.setText(_translate("Command", "Scroll for new output", None))
        self.label_7.setText(_translate("Command", "Caret:", None))
        self.label_8.setText(_translate("Command", "Match:", None))
        self.label.setText(_translate("Command", "Save:", None))

