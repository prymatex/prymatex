# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dialogs/filter.ui'
#
# Created: Wed Dec 10 16:51:29 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName("FilterDialog")
        FilterDialog.resize(486, 314)
        self.gridLayout = QtWidgets.QGridLayout(FilterDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(FilterDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(FilterDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout.addWidget(self.radioButton_4)
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout.addWidget(self.radioButton_5)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(FilterDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 88, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 2)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        _translate = QtCore.QCoreApplication.translate
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Dialog"))
        self.groupBox.setTitle(_translate("FilterDialog", "Filter type"))
        self.radioButton.setText(_translate("FilterDialog", "Include only"))
        self.radioButton_2.setText(_translate("FilterDialog", "Exclude all"))
        self.groupBox_2.setTitle(_translate("FilterDialog", "Applies to"))
        self.radioButton_3.setText(_translate("FilterDialog", "Files"))
        self.radioButton_4.setText(_translate("FilterDialog", "Folders"))
        self.radioButton_5.setText(_translate("FilterDialog", "Files and folders"))
        self.checkBox.setText(_translate("FilterDialog", "All children (recursive)"))
        self.groupBox_3.setTitle(_translate("FilterDialog", "File and folders attributes"))
        self.comboBox.setItemText(0, _translate("FilterDialog", "Name"))
        self.comboBox.setItemText(1, _translate("FilterDialog", "Project relative path"))
        self.comboBox.setItemText(2, _translate("FilterDialog", "Location"))
        self.comboBox.setItemText(3, _translate("FilterDialog", "Last modified"))
        self.comboBox.setItemText(4, _translate("FilterDialog", "File length"))
        self.comboBox.setItemText(5, _translate("FilterDialog", "Read only"))
        self.comboBox.setItemText(6, _translate("FilterDialog", "Symbolic link"))

