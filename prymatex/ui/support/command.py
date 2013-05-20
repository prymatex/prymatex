# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/support/command.ui'
#
# Created: Tue May 14 21:59:15 2013
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

class Ui_Command(object):
    def setupUi(self, Command):
        Command.setObjectName(_fromUtf8("Command"))
        Command.resize(361, 331)
        self.formLayout_2 = QtGui.QFormLayout(Command)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(Command)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboBoxBeforeRunning = QtGui.QComboBox(Command)
        self.comboBoxBeforeRunning.setObjectName(_fromUtf8("comboBoxBeforeRunning"))
        self.horizontalLayout_2.addWidget(self.comboBoxBeforeRunning)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonOptions = QtGui.QPushButton(Command)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.horizontalLayout_2.addWidget(self.pushButtonOptions)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(Command)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.command = QtGui.QPlainTextEdit(Command)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName(_fromUtf8("command"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.command)
        self.label_3 = QtGui.QLabel(Command)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
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
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtGui.QLabel(Command)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxOutput = QtGui.QComboBox(Command)
        self.comboBoxOutput.setObjectName(_fromUtf8("comboBoxOutput"))
        self.horizontalLayout_3.addWidget(self.comboBoxOutput)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.formLayout_2.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(Command)
        QtCore.QMetaObject.connectSlotsByName(Command)

    def retranslateUi(self, Command):
        Command.setWindowTitle(_translate("Command", "Form", None))
        self.label.setText(_translate("Command", "Save:", None))
        self.pushButtonOptions.setText(_translate("Command", "Options", None))
        self.label_2.setText(_translate("Command", "Command(s):", None))
        self.label_3.setText(_translate("Command", "Input:", None))
        self.labelInputOption.setText(_translate("Command", "or", None))
        self.label_4.setText(_translate("Command", "Output:", None))

