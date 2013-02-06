# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/dialogs/filter.ui'
#
# Created: Wed Feb  6 11:06:59 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName(_fromUtf8("FilterDialog"))
        FilterDialog.resize(486, 314)
        self.gridLayout = QtGui.QGridLayout(FilterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(FilterDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(FilterDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.verticalLayout.addWidget(self.radioButton_3)
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.verticalLayout.addWidget(self.radioButton_4)
        self.radioButton_5 = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        self.verticalLayout.addWidget(self.radioButton_5)
        self.checkBox = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(FilterDialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.comboBox = QtGui.QComboBox(self.groupBox_3)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 88, 23))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 2)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        FilterDialog.setWindowTitle(_('Dialog'))
        self.groupBox.setTitle(_('Filter type'))
        self.radioButton.setText(_('Include only'))
        self.radioButton_2.setText(_('Exclude all'))
        self.groupBox_2.setTitle(_('Applies to'))
        self.radioButton_3.setText(_('Files'))
        self.radioButton_4.setText(_('Folders'))
        self.radioButton_5.setText(_('Files and folders'))
        self.checkBox.setText(_('All children (recursive)'))
        self.groupBox_3.setTitle(_('File and folders attributes'))
        self.comboBox.setItemText(0, _('Name'))
        self.comboBox.setItemText(1, _('Project relative path'))
        self.comboBox.setItemText(2, _('Location'))
        self.comboBox.setItemText(3, _('Last modified'))
        self.comboBox.setItemText(4, _('File length'))
        self.comboBox.setItemText(5, _('Read only'))
        self.comboBox.setItemText(6, _('Symbolic link'))

