# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/general.ui'
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
        General.setWindowTitle(QtGui.QApplication.translate("General", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("General", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("General", "Qt style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("General", "Qt style sheet:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("General", "External actions", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAskAboutExternalDeletions.setText(QtGui.QApplication.translate("General", "Ask about external file deletions? or remove editor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAskAboutExternalChanges.setText(QtGui.QApplication.translate("General", "Ask about external file changes? or replace editor content", None, QtGui.QApplication.UnicodeUTF8))

