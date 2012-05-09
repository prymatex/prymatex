# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\ui\configure\terminal.ui'
#
# Created: Wed May 09 07:32:31 2012
#      by: PyQt4 UI code generator 4.8.2
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
        self.verticalLayout = QtGui.QVBoxLayout(Terminal)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Terminal)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboColorScheme = QtGui.QComboBox(Terminal)
        self.comboColorScheme.setObjectName(_fromUtf8("comboColorScheme"))
        self.gridLayout.addWidget(self.comboColorScheme, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Terminal)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboScrollBar = QtGui.QComboBox(Terminal)
        self.comboScrollBar.setObjectName(_fromUtf8("comboScrollBar"))
        self.gridLayout.addWidget(self.comboScrollBar, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Terminal)
        QtCore.QMetaObject.connectSlotsByName(Terminal)

    def retranslateUi(self, Terminal):
        Terminal.setWindowTitle(_('Terminal'))
        self.label.setText(_('Color Scheme'))
        self.label_2.setText(_('Scroll'))

