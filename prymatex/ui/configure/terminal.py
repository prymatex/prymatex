# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/terminal.ui'
#
# Created: Thu Jun  7 06:28:45 2012
#      by: PyQt4 UI code generator 4.9.1
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
        Terminal.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Terminal)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(Terminal)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineFont = QtGui.QLineEdit(self.groupBox_2)
        self.lineFont.setReadOnly(True)
        self.lineFont.setObjectName(_fromUtf8("lineFont"))
        self.horizontalLayout.addWidget(self.lineFont)
        self.pushButtonChangeFont = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonChangeFont.setObjectName(_fromUtf8("pushButtonChangeFont"))
        self.horizontalLayout.addWidget(self.pushButtonChangeFont)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(Terminal)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboColorScheme = QtGui.QComboBox(self.groupBox)
        self.comboColorScheme.setObjectName(_fromUtf8("comboColorScheme"))
        self.gridLayout.addWidget(self.comboColorScheme, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboScrollBar = QtGui.QComboBox(self.groupBox)
        self.comboScrollBar.setObjectName(_fromUtf8("comboScrollBar"))
        self.gridLayout.addWidget(self.comboScrollBar, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Terminal)
        QtCore.QMetaObject.connectSlotsByName(Terminal)

    def retranslateUi(self, Terminal):
        Terminal.setWindowTitle(_('Terminal'))
        self.groupBox_2.setTitle(_('Font'))
        self.pushButtonChangeFont.setText(_('&Change'))
        self.groupBox.setTitle(_('Appearance'))
        self.label.setText(_('Color Scheme'))
        self.label_2.setText(_('Scroll'))

