# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/files.ui'
#
# Created: Fri Jun 28 09:26:37 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        Files.setWindowTitle(QtGui.QApplication.translate("Files", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Files", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Files", "File history:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Files", "File format", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEncoding.setText(QtGui.QApplication.translate("Files", "Encoding:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEndOfLine.setText(QtGui.QApplication.translate("Files", "End of line:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Files", "Automatic end of line detection", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Files", "Automatic cleanups", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("Files", "Remove trailing spaces", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("Files", "Append newline at end of file on save", None, QtGui.QApplication.UnicodeUTF8))

