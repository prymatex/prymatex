# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/resource.ui'
#
# Created: Thu Dec 11 08:36:23 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResouceWidget(object):
    def setupUi(self, ResouceWidget):
        ResouceWidget.setObjectName("ResouceWidget")
        ResouceWidget.resize(574, 392)
        self.verticalLayout = QtWidgets.QVBoxLayout(ResouceWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.labelPath = QtWidgets.QLabel(ResouceWidget)
        self.labelPath.setObjectName("labelPath")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelPath)
        self.labelType = QtWidgets.QLabel(ResouceWidget)
        self.labelType.setObjectName("labelType")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelType)
        self.labelLocation = QtWidgets.QLabel(ResouceWidget)
        self.labelLocation.setObjectName("labelLocation")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelLocation)
        self.labelLastModified = QtWidgets.QLabel(ResouceWidget)
        self.labelLastModified.setObjectName("labelLastModified")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelLastModified)
        self.textLabelPath = QtWidgets.QLabel(ResouceWidget)
        self.textLabelPath.setText("")
        self.textLabelPath.setObjectName("textLabelPath")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.textLabelPath)
        self.textLabelType = QtWidgets.QLabel(ResouceWidget)
        self.textLabelType.setText("")
        self.textLabelType.setObjectName("textLabelType")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textLabelType)
        self.textLabelLocation = QtWidgets.QLabel(ResouceWidget)
        self.textLabelLocation.setText("")
        self.textLabelLocation.setObjectName("textLabelLocation")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.textLabelLocation)
        self.textLabelLastModified = QtWidgets.QLabel(ResouceWidget)
        self.textLabelLastModified.setText("")
        self.textLabelLastModified.setObjectName("textLabelLastModified")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textLabelLastModified)
        self.labelSize = QtWidgets.QLabel(ResouceWidget)
        self.labelSize.setObjectName("labelSize")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelSize)
        self.textLabelSize = QtWidgets.QLabel(ResouceWidget)
        self.textLabelSize.setText("")
        self.textLabelSize.setObjectName("textLabelSize")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textLabelSize)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(ResouceWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.groupBox_3 = QtWidgets.QGroupBox(ResouceWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidgetPermissions = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidgetPermissions.setObjectName("tableWidgetPermissions")
        self.tableWidgetPermissions.setColumnCount(3)
        self.tableWidgetPermissions.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPermissions.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.tableWidgetPermissions.setItem(2, 2, item)
        self.verticalLayout_2.addWidget(self.tableWidgetPermissions)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(ResouceWidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setContentsMargins(6, 6, 6, 6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radioButton_2)
        self.comboBoxEncoding = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxEncoding.setEnabled(False)
        self.comboBoxEncoding.setObjectName("comboBoxEncoding")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ResouceWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.comboBoxEndOfLine_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxEndOfLine_2.setEnabled(False)
        self.comboBoxEndOfLine_2.setObjectName("comboBoxEndOfLine_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxEndOfLine_2)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radioButton_4)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.radioButton_3)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ResouceWidget)
        QtCore.QMetaObject.connectSlotsByName(ResouceWidget)

    def retranslateUi(self, ResouceWidget):
        _translate = QtCore.QCoreApplication.translate
        ResouceWidget.setWindowTitle(_translate("ResouceWidget", "Resource"))
        self.labelPath.setText(_translate("ResouceWidget", "Path:"))
        self.labelType.setText(_translate("ResouceWidget", "Type:"))
        self.labelLocation.setText(_translate("ResouceWidget", "Location:"))
        self.labelLastModified.setText(_translate("ResouceWidget", "Last modified:"))
        self.labelSize.setText(_translate("ResouceWidget", "Size:"))
        self.groupBox_3.setTitle(_translate("ResouceWidget", "Permissions"))
        item = self.tableWidgetPermissions.verticalHeaderItem(0)
        item.setText(_translate("ResouceWidget", "Owner"))
        item = self.tableWidgetPermissions.verticalHeaderItem(1)
        item.setText(_translate("ResouceWidget", "Group"))
        item = self.tableWidgetPermissions.verticalHeaderItem(2)
        item.setText(_translate("ResouceWidget", "Other"))
        item = self.tableWidgetPermissions.horizontalHeaderItem(0)
        item.setText(_translate("ResouceWidget", "Read"))
        item = self.tableWidgetPermissions.horizontalHeaderItem(1)
        item.setText(_translate("ResouceWidget", "Write"))
        item = self.tableWidgetPermissions.horizontalHeaderItem(2)
        item.setText(_translate("ResouceWidget", "Execute"))
        __sortingEnabled = self.tableWidgetPermissions.isSortingEnabled()
        self.tableWidgetPermissions.setSortingEnabled(False)
        self.tableWidgetPermissions.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("ResouceWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Note:</span> Removing de executable flag on a folder will cause its children to become unreadable</p></body></html>"))
        self.groupBox.setTitle(_translate("ResouceWidget", "Text file encoding"))
        self.radioButton.setText(_translate("ResouceWidget", "Inherited"))
        self.radioButton_2.setText(_translate("ResouceWidget", "Other:"))
        self.groupBox_2.setTitle(_translate("ResouceWidget", "Text file end of line"))
        self.radioButton_4.setText(_translate("ResouceWidget", "Other"))
        self.radioButton_3.setText(_translate("ResouceWidget", "Inherited"))

