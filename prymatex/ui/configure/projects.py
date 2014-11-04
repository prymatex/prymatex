# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/projects.ui'
#
# Created: Tue Nov  4 08:31:38 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Projects(object):
    def setupUi(self, Projects):
        Projects.setObjectName("Projects")
        Projects.resize(272, 281)
        self.verticalLayout = QtWidgets.QVBoxLayout(Projects)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Projects)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineLocation_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineLocation_2.setEnabled(False)
        self.lineLocation_2.setObjectName("lineLocation_2")
        self.horizontalLayout_6.addWidget(self.lineLocation_2)
        self.buttonChoose_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.buttonChoose_2.setEnabled(False)
        icon = QtGui.QIcon.fromTheme("folder")
        self.buttonChoose_2.setIcon(icon)
        self.buttonChoose_2.setObjectName("buttonChoose_2")
        self.horizontalLayout_6.addWidget(self.buttonChoose_2)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBoxLicence.setObjectName("comboBoxLicence")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxLicence)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Projects)
        QtCore.QMetaObject.connectSlotsByName(Projects)

    def retranslateUi(self, Projects):
        _translate = QtCore.QCoreApplication.translate
        Projects.setWindowTitle(_translate("Projects", "Projects"))
        self.groupBox_3.setTitle(_translate("Projects", "Defaults"))
        self.label.setText(_translate("Projects", "Location:"))
        self.buttonChoose_2.setText(_translate("Projects", "Ch&oose"))
        self.label_3.setText(_translate("Projects", "Licence:"))

