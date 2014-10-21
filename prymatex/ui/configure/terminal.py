# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/terminal.ui'
#
# Created: Tue Oct 21 18:29:51 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Terminal(object):
    def setupUi(self, Terminal):
        Terminal.setObjectName("Terminal")
        Terminal.resize(533, 268)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Terminal)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBoxFont = QtWidgets.QGroupBox(Terminal)
        self.groupBoxFont.setObjectName("groupBoxFont")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxFont)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fontComboBoxName = QtWidgets.QFontComboBox(self.groupBoxFont)
        self.fontComboBoxName.setFontFilters(QtWidgets.QFontComboBox.MonospacedFonts)
        self.fontComboBoxName.setObjectName("fontComboBoxName")
        self.horizontalLayout_3.addWidget(self.fontComboBoxName)
        self.spinBoxFontSize = QtWidgets.QSpinBox(self.groupBoxFont)
        self.spinBoxFontSize.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxFontSize.setMinimum(7)
        self.spinBoxFontSize.setObjectName("spinBoxFontSize")
        self.horizontalLayout_3.addWidget(self.spinBoxFontSize)
        self.checkBoxAntialias = QtWidgets.QCheckBox(self.groupBoxFont)
        self.checkBoxAntialias.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBoxAntialias.setObjectName("checkBoxAntialias")
        self.horizontalLayout_3.addWidget(self.checkBoxAntialias)
        self.verticalLayout_2.addWidget(self.groupBoxFont)
        self.groupBox = QtWidgets.QGroupBox(Terminal)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBoxScheme = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxScheme.setObjectName("comboBoxScheme")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBoxScheme)
        self.checkBoxEditorTheme = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxEditorTheme.setObjectName("checkBoxEditorTheme")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.checkBoxEditorTheme)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Terminal)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(6, 6, 6, 6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBoxBufferSize = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBoxBufferSize.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spinBoxBufferSize.setMinimum(10)
        self.spinBoxBufferSize.setMaximum(1000)
        self.spinBoxBufferSize.setSingleStep(10)
        self.spinBoxBufferSize.setObjectName("spinBoxBufferSize")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBoxBufferSize)
        self.checkBoxSynchronize = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxSynchronize.setObjectName("checkBoxSynchronize")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.checkBoxSynchronize)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Terminal)
        QtCore.QMetaObject.connectSlotsByName(Terminal)

    def retranslateUi(self, Terminal):
        _translate = QtCore.QCoreApplication.translate
        Terminal.setWindowTitle(_translate("Terminal", "Terminal"))
        self.groupBoxFont.setTitle(_translate("Terminal", "Font"))
        self.checkBoxAntialias.setText(_translate("Terminal", "Anti alias"))
        self.groupBox.setTitle(_translate("Terminal", "Appearance"))
        self.label.setText(_translate("Terminal", "Color scheme:"))
        self.checkBoxEditorTheme.setText(_translate("Terminal", "Use editor theme when possible"))
        self.groupBox_2.setTitle(_translate("Terminal", "Behavior"))
        self.label_3.setText(_translate("Terminal", "Buffer:"))
        self.checkBoxSynchronize.setText(_translate("Terminal", "Automatically synchronize the terminal with the current editor when possible"))

