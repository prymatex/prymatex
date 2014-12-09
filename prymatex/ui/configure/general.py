# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/general.ui'
#
# Created: Tue Dec  9 16:01:56 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName("General")
        General.resize(506, 274)
        self.verticalLayout = QtWidgets.QVBoxLayout(General)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(General)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.comboBoxQtStyle = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxQtStyle.setObjectName("comboBoxQtStyle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxQtStyle)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxQtStyleSheet = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxQtStyleSheet.setObjectName("comboBoxQtStyleSheet")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBoxQtStyleSheet)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.comboBoxIconTheme = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxIconTheme.setObjectName("comboBoxIconTheme")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBoxIconTheme)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(General)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxAskAboutExternalDeletions = QtWidgets.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxAskAboutExternalDeletions.setFont(font)
        self.checkBoxAskAboutExternalDeletions.setObjectName("checkBoxAskAboutExternalDeletions")
        self.verticalLayout_2.addWidget(self.checkBoxAskAboutExternalDeletions)
        self.checkBoxAskAboutExternalChanges = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBoxAskAboutExternalChanges.setObjectName("checkBoxAskAboutExternalChanges")
        self.verticalLayout_2.addWidget(self.checkBoxAskAboutExternalChanges)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        _translate = QtCore.QCoreApplication.translate
        General.setWindowTitle(_translate("General", "General"))
        self.groupBox_2.setTitle(_translate("General", "Interface"))
        self.label_2.setText(_translate("General", "Qt style:"))
        self.label_3.setText(_translate("General", "Qt stylesheet:"))
        self.label_4.setText(_translate("General", "Icon theme:"))
        self.groupBox_3.setTitle(_translate("General", "External actions"))
        self.checkBoxAskAboutExternalDeletions.setText(_translate("General", "Ask about external file deletions? or remove editor"))
        self.checkBoxAskAboutExternalChanges.setText(_translate("General", "Ask about external file changes? or replace editor content"))

