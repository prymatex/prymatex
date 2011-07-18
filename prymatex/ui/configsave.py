# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configsave.ui'
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

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName(_fromUtf8("Save"))
        Save.setEnabled(True)
        Save.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/document-save-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Save.setWindowIcon(icon)
        self.formLayout = QtGui.QFormLayout(Save)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Save)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label)
        self.lineBackupPrefix = QtGui.QLineEdit(Save)
        self.lineBackupPrefix.setEnabled(False)
        self.lineBackupPrefix.setObjectName(_fromUtf8("lineBackupPrefix"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineBackupPrefix)
        self.label_2 = QtGui.QLabel(Save)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.label_2)
        self.lineBackupPostfix = QtGui.QLineEdit(Save)
        self.lineBackupPostfix.setEnabled(False)
        self.lineBackupPostfix.setObjectName(_fromUtf8("lineBackupPostfix"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.lineBackupPostfix)
        self.label_3 = QtGui.QLabel(Save)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboEncodings = QtGui.QComboBox(Save)
        self.comboEncodings.setObjectName(_fromUtf8("comboEncodings"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.comboEncodings)
        self.label_4 = QtGui.QLabel(Save)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBox = QtGui.QComboBox(Save)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.checkBox = QtGui.QCheckBox(Save)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.checkBox_3 = QtGui.QCheckBox(Save)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.checkBox_3)
        self.checkAutoSave = QtGui.QCheckBox(Save)
        self.checkAutoSave.setObjectName(_fromUtf8("checkAutoSave"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkAutoSave)
        self.spinSaveInterval = QtGui.QSpinBox(Save)
        self.spinSaveInterval.setEnabled(False)
        self.spinSaveInterval.setMaximum(120)
        self.spinSaveInterval.setObjectName(_fromUtf8("spinSaveInterval"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinSaveInterval)
        self.checkBox_4 = QtGui.QCheckBox(Save)
        self.checkBox_4.setEnabled(True)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.checkBox_4)

        self.retranslateUi(Save)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.spinSaveInterval.setEnabled)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lineBackupPrefix.setEnabled)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lineBackupPostfix.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        Save.setWindowTitle(_('Save'))
        self.label.setText(_('Backup prefix'))
        self.lineBackupPrefix.setText(_('.'))
        self.label_2.setText(_('Backup postfix'))
        self.lineBackupPostfix.setText(_('~'))
        self.label_3.setText(_('Default encoding'))
        self.label_4.setText(_('Line Ending'))
        self.comboBox.setItemText(0, _('LF (recommended)'))
        self.comboBox.setItemText(1, _('CR + LF'))
        self.checkBox.setText(_('Use for existing files as well'))
        self.checkBox_3.setText(_('Use for existing files as well'))
        self.checkAutoSave.setText(_('Automaitcally save'))
        self.spinSaveInterval.setSuffix(_(' mins'))
        self.spinSaveInterval.setPrefix(_('every '))
        self.checkBox_4.setText(_('Save when focus is lost'))

