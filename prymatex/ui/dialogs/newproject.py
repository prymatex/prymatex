# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dialogs/newproject.ui'
#
# Created: Wed May 27 08:01:34 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        NewProjectDialog.setObjectName("NewProjectDialog")
        NewProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        NewProjectDialog.resize(600, 443)
        NewProjectDialog.setMinimumSize(QtCore.QSize(600, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(NewProjectDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label1 = QtWidgets.QLabel(NewProjectDialog)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.lineEditName = QtWidgets.QLineEdit(NewProjectDialog)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.label2 = QtWidgets.QLabel(NewProjectDialog)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEditFolder = QtWidgets.QLineEdit(NewProjectDialog)
        self.lineEditFolder.setEnabled(False)
        self.lineEditFolder.setObjectName("lineEditFolder")
        self.horizontalLayout_5.addWidget(self.lineEditFolder)
        self.pushButtonChooseFolder = QtWidgets.QPushButton(NewProjectDialog)
        self.pushButtonChooseFolder.setObjectName("pushButtonChooseFolder")
        self.horizontalLayout_5.addWidget(self.pushButtonChooseFolder)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_4 = QtWidgets.QLabel(NewProjectDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEditFile = QtWidgets.QLineEdit(NewProjectDialog)
        self.lineEditFile.setEnabled(False)
        self.lineEditFile.setObjectName("lineEditFile")
        self.horizontalLayout_6.addWidget(self.lineEditFile)
        self.pushButtonChooseFile = QtWidgets.QPushButton(NewProjectDialog)
        self.pushButtonChooseFile.setObjectName("pushButtonChooseFile")
        self.horizontalLayout_6.addWidget(self.pushButtonChooseFile)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.line_2 = QtWidgets.QFrame(NewProjectDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.label = QtWidgets.QLabel(NewProjectDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label)
        self.textEditDescription = QtWidgets.QTextEdit(NewProjectDialog)
        self.textEditDescription.setObjectName("textEditDescription")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.textEditDescription)
        self.label3 = QtWidgets.QLabel(NewProjectDialog)
        self.label3.setObjectName("label3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label3)
        self.comboBoxKeywords = QtWidgets.QComboBox(NewProjectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxKeywords.sizePolicy().hasHeightForWidth())
        self.comboBoxKeywords.setSizePolicy(sizePolicy)
        self.comboBoxKeywords.setEditable(True)
        self.comboBoxKeywords.setObjectName("comboBoxKeywords")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.comboBoxKeywords)
        self.label_3 = QtWidgets.QLabel(NewProjectDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtWidgets.QComboBox(NewProjectDialog)
        self.comboBoxLicence.setObjectName("comboBoxLicence")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.comboBoxLicence)
        self.line = QtWidgets.QFrame(NewProjectDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.line)
        self.checkBoxUseTemplate = QtWidgets.QCheckBox(NewProjectDialog)
        self.checkBoxUseTemplate.setObjectName("checkBoxUseTemplate")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.checkBoxUseTemplate)
        self.label_2 = QtWidgets.QLabel(NewProjectDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxTemplate = QtWidgets.QComboBox(NewProjectDialog)
        self.comboBoxTemplate.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTemplate.sizePolicy().hasHeightForWidth())
        self.comboBoxTemplate.setSizePolicy(sizePolicy)
        self.comboBoxTemplate.setObjectName("comboBoxTemplate")
        self.horizontalLayout_3.addWidget(self.comboBoxTemplate)
        self.pushButtonEnvironment = QtWidgets.QPushButton(NewProjectDialog)
        self.pushButtonEnvironment.setEnabled(False)
        self.pushButtonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.pushButtonEnvironment.setText("")
        self.pushButtonEnvironment.setObjectName("pushButtonEnvironment")
        self.horizontalLayout_3.addWidget(self.pushButtonEnvironment)
        self.formLayout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBoxUseSourceFolder = QtWidgets.QCheckBox(NewProjectDialog)
        self.checkBoxUseSourceFolder.setChecked(True)
        self.checkBoxUseSourceFolder.setObjectName("checkBoxUseSourceFolder")
        self.horizontalLayout_2.addWidget(self.checkBoxUseSourceFolder)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCreate = QtWidgets.QPushButton(NewProjectDialog)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.pushButtonCreate.setIcon(icon)
        self.pushButtonCreate.setObjectName("pushButtonCreate")
        self.horizontalLayout.addWidget(self.pushButtonCreate)
        self.pushButtonCancel = QtWidgets.QPushButton(NewProjectDialog)
        icon = QtGui.QIcon.fromTheme("dialog-cancel")
        self.pushButtonCancel.setIcon(icon)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewProjectDialog)
        self.pushButtonCancel.clicked.connect(NewProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialog)
        NewProjectDialog.setTabOrder(self.lineEditFolder, self.pushButtonChooseFolder)
        NewProjectDialog.setTabOrder(self.pushButtonChooseFolder, self.pushButtonCreate)

    def retranslateUi(self, NewProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label1.setText(_translate("NewProjectDialog", "Name:"))
        self.label2.setText(_translate("NewProjectDialog", "Folder:"))
        self.pushButtonChooseFolder.setText(_translate("NewProjectDialog", "Ch&oose"))
        self.label_4.setText(_translate("NewProjectDialog", "File:"))
        self.pushButtonChooseFile.setText(_translate("NewProjectDialog", "Ch&oose"))
        self.label.setText(_translate("NewProjectDialog", "Description:"))
        self.label3.setText(_translate("NewProjectDialog", "Keywords:"))
        self.label_3.setText(_translate("NewProjectDialog", "Licence:"))
        self.checkBoxUseTemplate.setText(_translate("NewProjectDialog", "Use template"))
        self.label_2.setText(_translate("NewProjectDialog", "Template:"))
        self.checkBoxUseSourceFolder.setText(_translate("NewProjectDialog", "Use source folder"))
        self.pushButtonCreate.setText(_translate("NewProjectDialog", "&Create"))
        self.pushButtonCancel.setText(_translate("NewProjectDialog", "C&ancel"))

