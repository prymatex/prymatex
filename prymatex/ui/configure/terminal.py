# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/terminal.ui'
#
# Created: Thu Jan 24 13:52:49 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Terminal(object):
    def setupUi(self, Terminal):
        Terminal.setObjectName(_fromUtf8("Terminal"))
        Terminal.resize(533, 268)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Terminal)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBoxFont = QtGui.QGroupBox(Terminal)
        self.groupBoxFont.setObjectName(_fromUtf8("groupBoxFont"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBoxFont)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setMargin(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxFontName = QtGui.QFontComboBox(self.groupBoxFont)
        self.comboBoxFontName.setFontFilters(QtGui.QFontComboBox.MonospacedFonts)
        self.comboBoxFontName.setObjectName(_fromUtf8("comboBoxFontName"))
        self.horizontalLayout_3.addWidget(self.comboBoxFontName)
        self.spinBoxFontSize = QtGui.QSpinBox(self.groupBoxFont)
        self.spinBoxFontSize.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxFontSize.setMinimum(7)
        self.spinBoxFontSize.setObjectName(_fromUtf8("spinBoxFontSize"))
        self.horizontalLayout_3.addWidget(self.spinBoxFontSize)
        self.checkBoxFontAntialias = QtGui.QCheckBox(self.groupBoxFont)
        self.checkBoxFontAntialias.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBoxFontAntialias.setObjectName(_fromUtf8("checkBoxFontAntialias"))
        self.horizontalLayout_3.addWidget(self.checkBoxFontAntialias)
        self.verticalLayout_2.addWidget(self.groupBoxFont)
        self.groupBox = QtGui.QGroupBox(Terminal)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBoxScheme = QtGui.QComboBox(self.groupBox)
        self.comboBoxScheme.setObjectName(_fromUtf8("comboBoxScheme"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxScheme)
        self.checkBoxEditorTheme = QtGui.QCheckBox(self.groupBox)
        self.checkBoxEditorTheme.setObjectName(_fromUtf8("checkBoxEditorTheme"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.checkBoxEditorTheme)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Terminal)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.spinBoxBufferSize = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxBufferSize.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spinBoxBufferSize.setObjectName(_fromUtf8("spinBoxBufferSize"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBoxBufferSize)
        self.checkBoxSynchronize = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxSynchronize.setObjectName(_fromUtf8("checkBoxSynchronize"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.checkBoxSynchronize)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Terminal)
        QtCore.QMetaObject.connectSlotsByName(Terminal)

    def retranslateUi(self, Terminal):
        Terminal.setWindowTitle(_('Terminal'))
        self.groupBoxFont.setTitle(_('Font'))
        self.checkBoxFontAntialias.setText(_('Anti alias'))
        self.groupBox.setTitle(_('Appearance'))
        self.label.setText(_('Color scheme:'))
        self.checkBoxEditorTheme.setText(_('Use editor theme when possible'))
        self.groupBox_2.setTitle(_('Behavior'))
        self.label_3.setText(_('Buffer:'))
        self.checkBoxSynchronize.setText(_('Automatically synchronize the terminal with the current editor when possible'))

