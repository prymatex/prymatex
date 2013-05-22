# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/files.ui'
#
# Created: Wed May 22 20:00:20 2013
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

class Ui_Files(object):
    def setupUi(self, Files):
        Files.setObjectName(_fromUtf8("Files"))
        Files.resize(272, 281)
        self.verticalLayout = QtGui.QVBoxLayout(Files)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(Files)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.spinBox = QtGui.QSpinBox(self.groupBox_3)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(40)
        self.spinBox.setSingleStep(5)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(Files)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.labelEncoding = QtGui.QLabel(self.groupBox)
        self.labelEncoding.setObjectName(_fromUtf8("labelEncoding"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelEncoding)
        self.comboBoxEncoding = QtGui.QComboBox(self.groupBox)
        self.comboBoxEncoding.setObjectName(_fromUtf8("comboBoxEncoding"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.labelEndOfLine = QtGui.QLabel(self.groupBox)
        self.labelEndOfLine.setObjectName(_fromUtf8("labelEndOfLine"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelEndOfLine)
        self.comboBoxEndOfLine = QtGui.QComboBox(self.groupBox)
        self.comboBoxEndOfLine.setObjectName(_fromUtf8("comboBoxEndOfLine"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxEndOfLine)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.SpanningRole, self.checkBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Files)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox_2)
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBox_3)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Files)
        QtCore.QMetaObject.connectSlotsByName(Files)

    def retranslateUi(self, Files):
        Files.setWindowTitle(_translate("Files", "Files", None))
        self.groupBox_3.setTitle(_translate("Files", "Source", None))
        self.label.setText(_translate("Files", "File history:", None))
        self.groupBox.setTitle(_translate("Files", "File format", None))
        self.labelEncoding.setText(_translate("Files", "Encoding:", None))
        self.labelEndOfLine.setText(_translate("Files", "End of line:", None))
        self.checkBox.setText(_translate("Files", "Automatic end of line detection", None))
        self.groupBox_2.setTitle(_translate("Files", "Automatic cleanups", None))
        self.checkBox_2.setText(_translate("Files", "Remove trailing spaces", None))
        self.checkBox_3.setText(_translate("Files", "Append newline at end of file on save", None))

