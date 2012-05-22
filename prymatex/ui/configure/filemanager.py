# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/filemanager.ui'
#
# Created: Tue Feb 14 15:51:26 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FileManagerDialog(object):
    def setupUi(self, FileManagerDialog):
        FileManagerDialog.setObjectName(_fromUtf8("FileManagerDialog"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileManagerDialog.setWindowIcon(icon)
        self.formLayout = QtGui.QFormLayout(FileManagerDialog)
        self.formLayout.setMargin(0)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(FileManagerDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBoxSaveWhenFocusIsLost = QtGui.QCheckBox(FileManagerDialog)
        self.checkBoxSaveWhenFocusIsLost.setObjectName(_fromUtf8("checkBoxSaveWhenFocusIsLost"))
        self.verticalLayout.addWidget(self.checkBoxSaveWhenFocusIsLost)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBoxSaveEvery = QtGui.QCheckBox(FileManagerDialog)
        self.checkBoxSaveEvery.setObjectName(_fromUtf8("checkBoxSaveEvery"))
        self.horizontalLayout.addWidget(self.checkBoxSaveEvery)
        self.spinBoxSavePeriod = QtGui.QSpinBox(FileManagerDialog)
        self.spinBoxSavePeriod.setEnabled(False)
        self.spinBoxSavePeriod.setMinimum(1)
        self.spinBoxSavePeriod.setMaximum(120)
        self.spinBoxSavePeriod.setObjectName(_fromUtf8("spinBoxSavePeriod"))
        self.horizontalLayout.addWidget(self.spinBoxSavePeriod)
        self.label_2 = QtGui.QLabel(FileManagerDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.verticalLayout)
        self.label_3 = QtGui.QLabel(FileManagerDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxEncoding = QtGui.QComboBox(FileManagerDialog)
        self.comboBoxEncoding.setObjectName(_fromUtf8("comboBoxEncoding"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxEncoding)
        self.label_4 = QtGui.QLabel(FileManagerDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBoxLineEnding = QtGui.QComboBox(FileManagerDialog)
        self.comboBoxLineEnding.setObjectName(_fromUtf8("comboBoxLineEnding"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxLineEnding)

        self.retranslateUi(FileManagerDialog)
        QtCore.QObject.connect(self.checkBoxSaveEvery, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.spinBoxSavePeriod.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(FileManagerDialog)

    def retranslateUi(self, FileManagerDialog):
        FileManagerDialog.setWindowTitle(_('File Manager'))
        self.label.setText(_('Save when'))
        self.checkBoxSaveWhenFocusIsLost.setText(_('Focus is Lost'))
        self.checkBoxSaveEvery.setText(_('Perform Backups every'))
        self.label_2.setText(_('minutes'))
        self.label_3.setText(_('Encoding'))
        self.label_4.setText(_('Line Ending'))

from prymatex import resources_rc
