# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/editordragcommand.ui'
#
# Created: Sun Jul 17 21:59:52 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DragCommand(object):
    def setupUi(self, DragCommand):
        DragCommand.setObjectName(_fromUtf8("DragCommand"))
        DragCommand.resize(361, 237)
        self.formLayout_2 = QtGui.QFormLayout(DragCommand)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(DragCommand)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditExtensions = QtGui.QLineEdit(DragCommand)
        self.lineEditExtensions.setObjectName(_fromUtf8("lineEditExtensions"))
        self.horizontalLayout_2.addWidget(self.lineEditExtensions)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(DragCommand)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.command = QtGui.QPlainTextEdit(DragCommand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.command.sizePolicy().hasHeightForWidth())
        self.command.setSizePolicy(sizePolicy)
        self.command.setObjectName(_fromUtf8("command"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.command)
        self.label_4 = QtGui.QLabel(DragCommand)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxOutput = QtGui.QComboBox(DragCommand)
        self.comboBoxOutput.setObjectName(_fromUtf8("comboBoxOutput"))
        self.horizontalLayout_3.addWidget(self.comboBoxOutput)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(DragCommand)
        QtCore.QMetaObject.connectSlotsByName(DragCommand)

    def retranslateUi(self, DragCommand):
        DragCommand.setWindowTitle(_('Form'))
        self.label.setText(_('File Types:'))
        self.label_2.setText(_('Command(s):'))
        self.label_4.setText(_('Output:'))

