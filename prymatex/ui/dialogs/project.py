# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dialogs/project.ui'
#
# Created: Thu Dec 11 08:36:23 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectDialog(object):
    def setupUi(self, ProjectDialog):
        ProjectDialog.setObjectName("ProjectDialog")
        ProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        ProjectDialog.resize(600, 443)
        ProjectDialog.setMinimumSize(QtCore.QSize(600, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(ProjectDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label1 = QtWidgets.QLabel(ProjectDialog)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.line_2 = QtWidgets.QFrame(ProjectDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.lineProjectName = QtWidgets.QLineEdit(ProjectDialog)
        self.lineProjectName.setObjectName("lineProjectName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineProjectName)
        self.checkBoxUseDefaultLocation = QtWidgets.QCheckBox(ProjectDialog)
        self.checkBoxUseDefaultLocation.setChecked(True)
        self.checkBoxUseDefaultLocation.setObjectName("checkBoxUseDefaultLocation")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.checkBoxUseDefaultLocation)
        self.label2 = QtWidgets.QLabel(ProjectDialog)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineLocation = QtWidgets.QLineEdit(ProjectDialog)
        self.lineLocation.setEnabled(False)
        self.lineLocation.setObjectName("lineLocation")
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtWidgets.QPushButton(ProjectDialog)
        self.buttonChoose.setEnabled(False)
        icon = QtGui.QIcon.fromTheme("folder")
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName("buttonChoose")
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label = QtWidgets.QLabel(ProjectDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label)
        self.textDescription = QtWidgets.QTextEdit(ProjectDialog)
        self.textDescription.setObjectName("textDescription")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textDescription)
        self.line = QtWidgets.QFrame(ProjectDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.line)
        self.label3 = QtWidgets.QLabel(ProjectDialog)
        self.label3.setObjectName("label3")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label3)
        self.comboBoxKeywords = QtWidgets.QComboBox(ProjectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxKeywords.sizePolicy().hasHeightForWidth())
        self.comboBoxKeywords.setSizePolicy(sizePolicy)
        self.comboBoxKeywords.setEditable(True)
        self.comboBoxKeywords.setObjectName("comboBoxKeywords")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.comboBoxKeywords)
        self.label_3 = QtWidgets.QLabel(ProjectDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtWidgets.QComboBox(ProjectDialog)
        self.comboBoxLicence.setObjectName("comboBoxLicence")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.comboBoxLicence)
        self.checkBoxUseTemplate = QtWidgets.QCheckBox(ProjectDialog)
        self.checkBoxUseTemplate.setObjectName("checkBoxUseTemplate")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.checkBoxUseTemplate)
        self.label_2 = QtWidgets.QLabel(ProjectDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxTemplate = QtWidgets.QComboBox(ProjectDialog)
        self.comboBoxTemplate.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTemplate.sizePolicy().hasHeightForWidth())
        self.comboBoxTemplate.setSizePolicy(sizePolicy)
        self.comboBoxTemplate.setObjectName("comboBoxTemplate")
        self.horizontalLayout_3.addWidget(self.comboBoxTemplate)
        self.buttonEnvironment = QtWidgets.QPushButton(ProjectDialog)
        self.buttonEnvironment.setEnabled(False)
        self.buttonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonEnvironment.setText("")
        icon = QtGui.QIcon.fromTheme("code-variable")
        self.buttonEnvironment.setIcon(icon)
        self.buttonEnvironment.setObjectName("buttonEnvironment")
        self.horizontalLayout_3.addWidget(self.buttonEnvironment)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtWidgets.QPushButton(ProjectDialog)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName("buttonCreate")
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtWidgets.QPushButton(ProjectDialog)
        icon = QtGui.QIcon.fromTheme("dialog-cancel")
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProjectDialog)
        self.buttonCancel.clicked.connect(ProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectDialog)
        ProjectDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        ProjectDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, ProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label1.setText(_translate("ProjectDialog", "Name:"))
        self.checkBoxUseDefaultLocation.setText(_translate("ProjectDialog", "Use default location"))
        self.label2.setText(_translate("ProjectDialog", "Location:"))
        self.buttonChoose.setText(_translate("ProjectDialog", "Ch&oose"))
        self.label.setText(_translate("ProjectDialog", "Description:"))
        self.label3.setText(_translate("ProjectDialog", "Keywords:"))
        self.label_3.setText(_translate("ProjectDialog", "Licence:"))
        self.checkBoxUseTemplate.setText(_translate("ProjectDialog", "Use template"))
        self.label_2.setText(_translate("ProjectDialog", "Template:"))
        self.buttonCreate.setText(_translate("ProjectDialog", "&Create"))
        self.buttonCancel.setText(_translate("ProjectDialog", "C&ancel"))

