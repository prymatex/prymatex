# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/dragcommand.ui'
#
# Created: Mon Oct 27 12:36:56 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DragCommand(object):
    def setupUi(self, DragCommand):
        DragCommand.setObjectName("DragCommand")
        DragCommand.resize(361, 237)
        self.formLayout_2 = QtWidgets.QFormLayout(DragCommand)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(DragCommand)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditExtensions = QtWidgets.QLineEdit(DragCommand)
        self.lineEditExtensions.setObjectName("lineEditExtensions")
        self.horizontalLayout_2.addWidget(self.lineEditExtensions)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(DragCommand)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.command = QtWidgets.QPlainTextEdit(DragCommand)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName("command")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.command)
        self.label_4 = QtWidgets.QLabel(DragCommand)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxOutput = QtWidgets.QComboBox(DragCommand)
        self.comboBoxOutput.setObjectName("comboBoxOutput")
        self.horizontalLayout_3.addWidget(self.comboBoxOutput)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(DragCommand)
        QtCore.QMetaObject.connectSlotsByName(DragCommand)

    def retranslateUi(self, DragCommand):
        _translate = QtCore.QCoreApplication.translate
        DragCommand.setWindowTitle(_translate("DragCommand", "Form"))
        self.label.setText(_translate("DragCommand", "File Types:"))
        self.label_2.setText(_translate("DragCommand", "Command(s):"))
        self.label_4.setText(_translate("DragCommand", "Output:"))

