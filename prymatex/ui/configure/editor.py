# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/editor.ui'
#
# Created: Fri Jan 11 10:55:13 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName(_fromUtf8("Editor"))
        Editor.resize(415, 351)
        self.verticalLayout = QtGui.QVBoxLayout(Editor)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(Editor)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setMargin(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelDefaultSyntax = QtGui.QLabel(self.groupBox_2)
        self.labelDefaultSyntax.setObjectName(_fromUtf8("labelDefaultSyntax"))
        self.horizontalLayout.addWidget(self.labelDefaultSyntax)
        self.comboBoxDefaultSyntax = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxDefaultSyntax.sizePolicy().hasHeightForWidth())
        self.comboBoxDefaultSyntax.setSizePolicy(sizePolicy)
        self.comboBoxDefaultSyntax.setObjectName(_fromUtf8("comboBoxDefaultSyntax"))
        self.horizontalLayout.addWidget(self.comboBoxDefaultSyntax)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.checkBoxHighlightCurrenLine = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxHighlightCurrenLine.setObjectName(_fromUtf8("checkBoxHighlightCurrenLine"))
        self.verticalLayout_3.addWidget(self.checkBoxHighlightCurrenLine)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.checkBoxShowMarginLine = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxShowMarginLine.setMaximumSize(QtCore.QSize(130, 16777215))
        self.checkBoxShowMarginLine.setObjectName(_fromUtf8("checkBoxShowMarginLine"))
        self.horizontalLayout_2.addWidget(self.checkBoxShowMarginLine)
        self.spinBoxMarginLineSpace = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxMarginLineSpace.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxMarginLineSpace.setObjectName(_fromUtf8("spinBoxMarginLineSpace"))
        self.horizontalLayout_2.addWidget(self.spinBoxMarginLineSpace)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.checkBoxShowTabSpaces = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxShowTabSpaces.setObjectName(_fromUtf8("checkBoxShowTabSpaces"))
        self.verticalLayout_3.addWidget(self.checkBoxShowTabSpaces)
        self.checkBoxShowLineParagraph = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxShowLineParagraph.setObjectName(_fromUtf8("checkBoxShowLineParagraph"))
        self.verticalLayout_3.addWidget(self.checkBoxShowLineParagraph)
        self.checkBoxWrapLines = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxWrapLines.setObjectName(_fromUtf8("checkBoxWrapLines"))
        self.verticalLayout_3.addWidget(self.checkBoxWrapLines)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(Editor)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBoxLineNumbers = QtGui.QCheckBox(self.groupBox)
        self.checkBoxLineNumbers.setObjectName(_fromUtf8("checkBoxLineNumbers"))
        self.verticalLayout_2.addWidget(self.checkBoxLineNumbers)
        self.checkBoxBookmarks = QtGui.QCheckBox(self.groupBox)
        self.checkBoxBookmarks.setObjectName(_fromUtf8("checkBoxBookmarks"))
        self.verticalLayout_2.addWidget(self.checkBoxBookmarks)
        self.checkBoxFolding = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFolding.setObjectName(_fromUtf8("checkBoxFolding"))
        self.verticalLayout_2.addWidget(self.checkBoxFolding)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        Editor.setWindowTitle(_('Editor'))
        self.groupBox_2.setTitle(_('Source'))
        self.labelDefaultSyntax.setText(_('Default syntax'))
        self.checkBoxHighlightCurrenLine.setText(_('Highlight current line'))
        self.checkBoxShowMarginLine.setText(_('Show margin line after'))
        self.checkBoxShowTabSpaces.setText(_('Show tabs and spaces'))
        self.checkBoxShowLineParagraph.setText(_('Show line and paragraph'))
        self.checkBoxWrapLines.setText(_('Wrap lines'))
        self.groupBox.setTitle(_('Gutter'))
        self.checkBoxLineNumbers.setText(_('Show line numbers'))
        self.checkBoxBookmarks.setText(_('Show bookmarks'))
        self.checkBoxFolding.setText(_('Show folding'))

