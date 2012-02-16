# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/editor.ui'
#
# Created: Thu Feb 16 14:56:59 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EditorWidget(object):
    def setupUi(self, EditorWidget):
        EditorWidget.setObjectName(_fromUtf8("EditorWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(EditorWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_4 = QtGui.QCheckBox(EditorWidget)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.verticalLayout.addWidget(self.checkBox_4)
        self.groupBox = QtGui.QGroupBox(EditorWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox_2)
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_3)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(EditorWidget)
        QtCore.QMetaObject.connectSlotsByName(EditorWidget)

    def retranslateUi(self, EditorWidget):
        EditorWidget.setWindowTitle(_('Editor'))
        self.checkBox_4.setText(_('Highlight current line'))
        self.groupBox.setTitle(_('Gutter'))
        self.checkBox.setText(_('Show Line Numbers'))
        self.checkBox_2.setText(_('Show Bookmarks'))
        self.checkBox_3.setText(_('Show Folding'))

