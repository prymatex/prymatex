# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/filemanager.ui'
#
# Created: Wed Jan 23 09:31:01 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FileManager(object):
    def setupUi(self, FileManager):
        FileManager.setObjectName(_fromUtf8("FileManager"))
        FileManager.resize(468, 564)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileManager.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(FileManager)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(FileManager)
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
        self.groupBox_2 = QtGui.QGroupBox(FileManager)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(FileManager)
        QtCore.QMetaObject.connectSlotsByName(FileManager)

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle(_('File Manager'))
        self.groupBox.setTitle(_('File format'))
        self.labelEncoding.setText(_('Encoding:'))
        self.labelEndOfLine.setText(_('End of line:'))
        self.checkBox.setText(_('Automatic end of line detection'))
        self.groupBox_2.setTitle(_('Automatic cleanups'))
        self.checkBox_3.setText(_('Append newline at end of file on save'))
        self.checkBox_2.setText(_('Remove trailing spaces'))

