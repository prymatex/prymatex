# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/project.ui'
#
# Created: Sat Oct 18 10:31:43 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Project(object):
    def setupUi(self, Project):
        Project.setObjectName("Project")
        Project.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(Project)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.label1 = QtWidgets.QLabel(Project)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.lineProjectName = QtWidgets.QLineEdit(Project)
        self.lineProjectName.setObjectName("lineProjectName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineProjectName)
        self.label = QtWidgets.QLabel(Project)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.textDescription = QtWidgets.QTextEdit(Project)
        self.textDescription.setObjectName("textDescription")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textDescription)
        self.label3 = QtWidgets.QLabel(Project)
        self.label3.setObjectName("label3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)
        self.comboBoxKeywords = QtWidgets.QComboBox(Project)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxKeywords.sizePolicy().hasHeightForWidth())
        self.comboBoxKeywords.setSizePolicy(sizePolicy)
        self.comboBoxKeywords.setEditable(True)
        self.comboBoxKeywords.setObjectName("comboBoxKeywords")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBoxKeywords)
        self.label_3 = QtWidgets.QLabel(Project)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtWidgets.QComboBox(Project)
        self.comboBoxLicence.setObjectName("comboBoxLicence")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBoxLicence)
        self.label2 = QtWidgets.QLabel(Project)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.textLabelLocation = QtWidgets.QLabel(Project)
        self.textLabelLocation.setText("")
        self.textLabelLocation.setObjectName("textLabelLocation")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textLabelLocation)

        self.retranslateUi(Project)
        QtCore.QMetaObject.connectSlotsByName(Project)

    def retranslateUi(self, Project):
        _translate = QtCore.QCoreApplication.translate
        Project.setWindowTitle(_translate("Project", "Form"))
        self.label1.setText(_translate("Project", "Name:"))
        self.label.setText(_translate("Project", "Description:"))
        self.label3.setText(_translate("Project", "Keywords:"))
        self.label_3.setText(_translate("Project", "Licence:"))
        self.label2.setText(_translate("Project", "Location:"))

