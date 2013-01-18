# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/general.ui'
#
# Created: Thu Jan 17 19:51:02 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName(_fromUtf8("General"))
        General.resize(506, 274)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(General)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.comboBoxQtStyle = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxQtStyle.setObjectName(_fromUtf8("comboBoxQtStyle"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxQtStyle)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxQtStyleSheet = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxQtStyleSheet.setObjectName(_fromUtf8("comboBoxQtStyleSheet"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxQtStyleSheet)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(General)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBoxAskAboutExternalDeletions = QtGui.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxAskAboutExternalDeletions.setFont(font)
        self.checkBoxAskAboutExternalDeletions.setObjectName(_fromUtf8("checkBoxAskAboutExternalDeletions"))
        self.verticalLayout_2.addWidget(self.checkBoxAskAboutExternalDeletions)
        self.checkBoxAskAboutExternalChanges = QtGui.QCheckBox(self.groupBox_3)
        self.checkBoxAskAboutExternalChanges.setObjectName(_fromUtf8("checkBoxAskAboutExternalChanges"))
        self.verticalLayout_2.addWidget(self.checkBoxAskAboutExternalChanges)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(General)
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
        self.labelLineEnding = QtGui.QLabel(self.groupBox)
        self.labelLineEnding.setObjectName(_fromUtf8("labelLineEnding"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLineEnding)
        self.comboBoxLineEnding = QtGui.QComboBox(self.groupBox)
        self.comboBoxLineEnding.setObjectName(_fromUtf8("comboBoxLineEnding"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxLineEnding)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(_('General'))
        self.groupBox_2.setTitle(_('Interface'))
        self.label_2.setText(_('Qt style:'))
        self.label_3.setText(_('Qt style sheet:'))
        self.groupBox_3.setTitle(_('External actions'))
        self.checkBoxAskAboutExternalDeletions.setText(_('Ask about external file deletions? or remove editor'))
        self.checkBoxAskAboutExternalChanges.setText(_('Ask about external file changes? or replace editor content'))
        self.groupBox.setTitle(_('Files'))
        self.labelEncoding.setText(_('Encoding'))
        self.labelLineEnding.setText(_('Line Ending'))

