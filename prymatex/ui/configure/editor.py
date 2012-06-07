# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/editor.ui'
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

class Ui_EditorWidget(object):
    def setupUi(self, EditorWidget):
        EditorWidget.setObjectName(_fromUtf8("EditorWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(EditorWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelDefaultSyntax = QtGui.QLabel(EditorWidget)
        self.labelDefaultSyntax.setObjectName(_fromUtf8("labelDefaultSyntax"))
        self.horizontalLayout.addWidget(self.labelDefaultSyntax)
        self.comboBoxDefaultSyntax = QtGui.QComboBox(EditorWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxDefaultSyntax.sizePolicy().hasHeightForWidth())
        self.comboBoxDefaultSyntax.setSizePolicy(sizePolicy)
        self.comboBoxDefaultSyntax.setObjectName(_fromUtf8("comboBoxDefaultSyntax"))
        self.horizontalLayout.addWidget(self.comboBoxDefaultSyntax)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBoxHighlight = QtGui.QCheckBox(EditorWidget)
        self.checkBoxHighlight.setObjectName(_fromUtf8("checkBoxHighlight"))
        self.verticalLayout.addWidget(self.checkBoxHighlight)
        self.groupBox = QtGui.QGroupBox(EditorWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxLineNumbers = QtGui.QCheckBox(self.groupBox)
        self.checkBoxLineNumbers.setObjectName(_fromUtf8("checkBoxLineNumbers"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBoxLineNumbers)
        self.checkBoxBookmarks = QtGui.QCheckBox(self.groupBox)
        self.checkBoxBookmarks.setObjectName(_fromUtf8("checkBoxBookmarks"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBoxBookmarks)
        self.checkBoxFolding = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFolding.setObjectName(_fromUtf8("checkBoxFolding"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBoxFolding)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(EditorWidget)
        QtCore.QMetaObject.connectSlotsByName(EditorWidget)

    def retranslateUi(self, EditorWidget):
        EditorWidget.setWindowTitle(_('Editor'))
        self.labelDefaultSyntax.setText(_('Default Syntax'))
        self.checkBoxHighlight.setText(_('Highlight current line'))
        self.groupBox.setTitle(_('Gutter'))
        self.checkBoxLineNumbers.setText(_('Show Line Numbers'))
        self.checkBoxBookmarks.setText(_('Show Bookmarks'))
        self.checkBoxFolding.setText(_('Show Folding'))

