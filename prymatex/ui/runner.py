# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/runner.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PMXRunnerWidget(object):
    def setupUi(self, PMXRunnerWidget):
        PMXRunnerWidget.setObjectName(_fromUtf8("PMXRunnerWidget"))
        PMXRunnerWidget.resize(534, 487)
        PMXRunnerWidget.setWindowTitle(_('Runner'))
        PMXRunnerWidget.setStyleSheet(_fromUtf8("QTextEdit#textOutput {\n"
"  border: 1px solid #CCC;\n"
"  /*padding: 4px;*/\n"
"  margin: 4px;\n"
"  background: rgba(23, 23, 23, 23);\n"
"}\n"
"\n"
"QLabel#heading {\n"
"    font-weight: bold;\n"
"    margin: 10px;\n"
"    font-size: 18pt;\n"
"}\n"
"QComboBox {\n"
"    color: red;\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(PMXRunnerWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.heading = QtGui.QLabel(PMXRunnerWidget)
        self.heading.setStyleSheet(_fromUtf8(""))
        self.heading.setText(_('TextLabel'))
        self.heading.setObjectName(_fromUtf8("heading"))
        self.horizontalLayout.addWidget(self.heading)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(PMXRunnerWidget)
        self.comboBox.setToolTip(_('Theme'))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, _('Dark'))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, _('Clean'))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, _('Mac'))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(3, _('Xplode'))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(4, _('Galactic'))
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtGui.QPushButton(PMXRunnerWidget)
        self.pushButton_2.setText(_('Copy to Clipboard'))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(PMXRunnerWidget)
        self.pushButton.setText(_('Paste to...'))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textOutput = QtGui.QTextEdit(PMXRunnerWidget)
        self.textOutput.setObjectName(_fromUtf8("textOutput"))
        self.verticalLayout.addWidget(self.textOutput)

        self.retranslateUi(PMXRunnerWidget)
        QtCore.QMetaObject.connectSlotsByName(PMXRunnerWidget)

    def retranslateUi(self, PMXRunnerWidget):
        pass

