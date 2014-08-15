# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/general.ui'
#
# Created: Fri Aug 15 10:26:59 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName(_fromUtf8("General"))
        General.resize(506, 274)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(General)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
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
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBoxIconTheme = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxIconTheme.setObjectName(_fromUtf8("comboBoxIconTheme"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxIconTheme)
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
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(_translate("General", "General", None))
        self.groupBox_2.setTitle(_translate("General", "Interface", None))
        self.label_2.setText(_translate("General", "Qt style:", None))
        self.label_3.setText(_translate("General", "Qt stylesheet:", None))
        self.label_4.setText(_translate("General", "Icon theme:", None))
        self.groupBox_3.setTitle(_translate("General", "External actions", None))
        self.checkBoxAskAboutExternalDeletions.setText(_translate("General", "Ask about external file deletions? or remove editor", None))
        self.checkBoxAskAboutExternalChanges.setText(_translate("General", "Ask about external file changes? or replace editor content", None))

