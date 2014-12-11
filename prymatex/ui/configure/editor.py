# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/editor.ui'
#
# Created: Wed Dec 10 16:51:31 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(415, 352)
        self.verticalLayout = QtWidgets.QVBoxLayout(Editor)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Editor)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelDefaultSyntax = QtWidgets.QLabel(self.groupBox_2)
        self.labelDefaultSyntax.setObjectName("labelDefaultSyntax")
        self.horizontalLayout.addWidget(self.labelDefaultSyntax)
        self.comboBoxDefaultSyntax = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxDefaultSyntax.sizePolicy().hasHeightForWidth())
        self.comboBoxDefaultSyntax.setSizePolicy(sizePolicy)
        self.comboBoxDefaultSyntax.setObjectName("comboBoxDefaultSyntax")
        self.horizontalLayout.addWidget(self.comboBoxDefaultSyntax)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.checkBoxHighlightCurrenLine = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxHighlightCurrenLine.setObjectName("checkBoxHighlightCurrenLine")
        self.verticalLayout_3.addWidget(self.checkBoxHighlightCurrenLine)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBoxShowMarginLine = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxShowMarginLine.setMaximumSize(QtCore.QSize(130, 16777215))
        self.checkBoxShowMarginLine.setObjectName("checkBoxShowMarginLine")
        self.horizontalLayout_2.addWidget(self.checkBoxShowMarginLine)
        self.spinBoxMarginLineSpace = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBoxMarginLineSpace.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxMarginLineSpace.setMinimum(60)
        self.spinBoxMarginLineSpace.setMaximum(100)
        self.spinBoxMarginLineSpace.setProperty("value", 80)
        self.spinBoxMarginLineSpace.setObjectName("spinBoxMarginLineSpace")
        self.horizontalLayout_2.addWidget(self.spinBoxMarginLineSpace)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.checkBoxShowIndentGuide = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxShowIndentGuide.setObjectName("checkBoxShowIndentGuide")
        self.verticalLayout_3.addWidget(self.checkBoxShowIndentGuide)
        self.checkBoxShowTabSpaces = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxShowTabSpaces.setObjectName("checkBoxShowTabSpaces")
        self.verticalLayout_3.addWidget(self.checkBoxShowTabSpaces)
        self.checkBoxShowLineParagraph = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxShowLineParagraph.setObjectName("checkBoxShowLineParagraph")
        self.verticalLayout_3.addWidget(self.checkBoxShowLineParagraph)
        self.checkBoxWrapLines = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxWrapLines.setObjectName("checkBoxWrapLines")
        self.verticalLayout_3.addWidget(self.checkBoxWrapLines)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Editor)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxLineNumbers = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxLineNumbers.setObjectName("checkBoxLineNumbers")
        self.verticalLayout_2.addWidget(self.checkBoxLineNumbers)
        self.checkBoxBookmarks = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxBookmarks.setObjectName("checkBoxBookmarks")
        self.verticalLayout_2.addWidget(self.checkBoxBookmarks)
        self.checkBoxFolding = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxFolding.setObjectName("checkBoxFolding")
        self.verticalLayout_2.addWidget(self.checkBoxFolding)
        self.checkBoxSelection = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxSelection.setObjectName("checkBoxSelection")
        self.verticalLayout_2.addWidget(self.checkBoxSelection)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        _translate = QtCore.QCoreApplication.translate
        Editor.setWindowTitle(_translate("Editor", "Editor"))
        self.groupBox_2.setTitle(_translate("Editor", "Source"))
        self.labelDefaultSyntax.setText(_translate("Editor", "Default syntax:"))
        self.checkBoxHighlightCurrenLine.setText(_translate("Editor", "Highlight current line"))
        self.checkBoxShowMarginLine.setText(_translate("Editor", "Show margin line after"))
        self.checkBoxShowIndentGuide.setText(_translate("Editor", "Show indent guides"))
        self.checkBoxShowTabSpaces.setText(_translate("Editor", "Show tabs and spaces"))
        self.checkBoxShowLineParagraph.setText(_translate("Editor", "Show line and paragraph"))
        self.checkBoxWrapLines.setText(_translate("Editor", "Wrap lines"))
        self.groupBox.setTitle(_translate("Editor", "Gutters"))
        self.checkBoxLineNumbers.setText(_translate("Editor", "Show line numbers"))
        self.checkBoxBookmarks.setText(_translate("Editor", "Show bookmarks"))
        self.checkBoxFolding.setText(_translate("Editor", "Show folding"))
        self.checkBoxSelection.setText(_translate("Editor", "Show selected text"))

