# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/codeeditor/status.ui'
#
# Created: Wed Dec 10 16:51:30 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CodeEditorStatus(object):
    def setupUi(self, CodeEditorStatus):
        CodeEditorStatus.setObjectName("CodeEditorStatus")
        CodeEditorStatus.resize(686, 246)
        self.verticalLayout = QtWidgets.QVBoxLayout(CodeEditorStatus)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetCommand = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetCommand.setObjectName("widgetCommand")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetCommand)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonCommandClose = QtWidgets.QPushButton(self.widgetCommand)
        self.pushButtonCommandClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonCommandClose.setIcon(icon)
        self.pushButtonCommandClose.setFlat(True)
        self.pushButtonCommandClose.setObjectName("pushButtonCommandClose")
        self.horizontalLayout.addWidget(self.pushButtonCommandClose)
        self.label = QtWidgets.QLabel(self.widgetCommand)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxCommand = QtWidgets.QComboBox(self.widgetCommand)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxCommand.sizePolicy().hasHeightForWidth())
        self.comboBoxCommand.setSizePolicy(sizePolicy)
        self.comboBoxCommand.setEditable(True)
        self.comboBoxCommand.setObjectName("comboBoxCommand")
        self.horizontalLayout.addWidget(self.comboBoxCommand)
        self.label_2 = QtWidgets.QLabel(self.widgetCommand)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBoxInput = QtWidgets.QComboBox(self.widgetCommand)
        self.comboBoxInput.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBoxInput.setObjectName("comboBoxInput")
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.label_3 = QtWidgets.QLabel(self.widgetCommand)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBoxOutput = QtWidgets.QComboBox(self.widgetCommand)
        self.comboBoxOutput.setMaximumSize(QtCore.QSize(160, 16777215))
        self.comboBoxOutput.setObjectName("comboBoxOutput")
        self.horizontalLayout.addWidget(self.comboBoxOutput)
        self.verticalLayout.addWidget(self.widgetCommand)
        self.widgetGoToLine = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetGoToLine.setObjectName("widgetGoToLine")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetGoToLine)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonGoToLineClose = QtWidgets.QPushButton(self.widgetGoToLine)
        self.pushButtonGoToLineClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonGoToLineClose.setIcon(icon)
        self.pushButtonGoToLineClose.setFlat(True)
        self.pushButtonGoToLineClose.setObjectName("pushButtonGoToLineClose")
        self.horizontalLayout_3.addWidget(self.pushButtonGoToLineClose)
        self.labelGoToLine = QtWidgets.QLabel(self.widgetGoToLine)
        self.labelGoToLine.setObjectName("labelGoToLine")
        self.horizontalLayout_3.addWidget(self.labelGoToLine)
        self.spinBoxGoToLine = QtWidgets.QSpinBox(self.widgetGoToLine)
        self.spinBoxGoToLine.setMinimum(1)
        self.spinBoxGoToLine.setMaximum(999999999)
        self.spinBoxGoToLine.setObjectName("spinBoxGoToLine")
        self.horizontalLayout_3.addWidget(self.spinBoxGoToLine)
        spacerItem = QtWidgets.QSpacerItem(154, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widgetGoToLine)
        self.widgetIFind = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetIFind.setObjectName("widgetIFind")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widgetIFind)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonIFindClose = QtWidgets.QPushButton(self.widgetIFind)
        self.pushButtonIFindClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonIFindClose.setIcon(icon)
        self.pushButtonIFindClose.setFlat(True)
        self.pushButtonIFindClose.setObjectName("pushButtonIFindClose")
        self.horizontalLayout_5.addWidget(self.pushButtonIFindClose)
        self.labelIFind = QtWidgets.QLabel(self.widgetIFind)
        self.labelIFind.setObjectName("labelIFind")
        self.horizontalLayout_5.addWidget(self.labelIFind)
        self.lineEditIFind = QtWidgets.QLineEdit(self.widgetIFind)
        self.lineEditIFind.setObjectName("lineEditIFind")
        self.horizontalLayout_5.addWidget(self.lineEditIFind)
        self.pushButtonIFindNext = QtWidgets.QPushButton(self.widgetIFind)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.pushButtonIFindNext.setIcon(icon)
        self.pushButtonIFindNext.setObjectName("pushButtonIFindNext")
        self.horizontalLayout_5.addWidget(self.pushButtonIFindNext)
        self.pushButtonIFindPrevious = QtWidgets.QPushButton(self.widgetIFind)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.pushButtonIFindPrevious.setIcon(icon)
        self.pushButtonIFindPrevious.setObjectName("pushButtonIFindPrevious")
        self.horizontalLayout_5.addWidget(self.pushButtonIFindPrevious)
        self.checkBoxIFindCaseSensitively = QtWidgets.QCheckBox(self.widgetIFind)
        self.checkBoxIFindCaseSensitively.setObjectName("checkBoxIFindCaseSensitively")
        self.horizontalLayout_5.addWidget(self.checkBoxIFindCaseSensitively)
        spacerItem1 = QtWidgets.QSpacerItem(155, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widgetIFind)
        self.widgetFindReplace = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetFindReplace.setObjectName("widgetFindReplace")
        self.gridLayout = QtWidgets.QGridLayout(self.widgetFindReplace)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonFindReplaceClose = QtWidgets.QPushButton(self.widgetFindReplace)
        self.pushButtonFindReplaceClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonFindReplaceClose.setIcon(icon)
        self.pushButtonFindReplaceClose.setFlat(True)
        self.pushButtonFindReplaceClose.setObjectName("pushButtonFindReplaceClose")
        self.gridLayout.addWidget(self.pushButtonFindReplaceClose, 0, 0, 1, 1)
        self.labelFind = QtWidgets.QLabel(self.widgetFindReplace)
        self.labelFind.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFind.setObjectName("labelFind")
        self.gridLayout.addWidget(self.labelFind, 0, 1, 1, 1)
        self.labelReplace = QtWidgets.QLabel(self.widgetFindReplace)
        self.labelReplace.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelReplace.setObjectName("labelReplace")
        self.gridLayout.addWidget(self.labelReplace, 1, 1, 1, 1)
        self.lineEditFind = QtWidgets.QLineEdit(self.widgetFindReplace)
        self.lineEditFind.setObjectName("lineEditFind")
        self.gridLayout.addWidget(self.lineEditFind, 0, 2, 1, 1)
        self.lineEditReplace = QtWidgets.QLineEdit(self.widgetFindReplace)
        self.lineEditReplace.setObjectName("lineEditReplace")
        self.gridLayout.addWidget(self.lineEditReplace, 1, 2, 1, 1)
        self.pushButtonReplace = QtWidgets.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme("replace")
        self.pushButtonReplace.setIcon(icon)
        self.pushButtonReplace.setObjectName("pushButtonReplace")
        self.gridLayout.addWidget(self.pushButtonReplace, 1, 3, 1, 1)
        self.pushButtonReplaceAll = QtWidgets.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme("replace-all")
        self.pushButtonReplaceAll.setIcon(icon)
        self.pushButtonReplaceAll.setObjectName("pushButtonReplaceAll")
        self.gridLayout.addWidget(self.pushButtonReplaceAll, 1, 4, 1, 1)
        self.pushButtonFindPrevious = QtWidgets.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.pushButtonFindPrevious.setIcon(icon)
        self.pushButtonFindPrevious.setObjectName("pushButtonFindPrevious")
        self.gridLayout.addWidget(self.pushButtonFindPrevious, 0, 4, 1, 1)
        self.pushButtonFindNext = QtWidgets.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.pushButtonFindNext.setIcon(icon)
        self.pushButtonFindNext.setObjectName("pushButtonFindNext")
        self.gridLayout.addWidget(self.pushButtonFindNext, 0, 3, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.widgetFindReplace)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelFindMode = QtWidgets.QLabel(self.groupBox)
        self.labelFindMode.setObjectName("labelFindMode")
        self.horizontalLayout_6.addWidget(self.labelFindMode)
        self.comboBoxFindMode = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxFindMode.setObjectName("comboBoxFindMode")
        self.horizontalLayout_6.addWidget(self.comboBoxFindMode)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.checkBoxFindCaseSensitively = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxFindCaseSensitively.setObjectName("checkBoxFindCaseSensitively")
        self.horizontalLayout_6.addWidget(self.checkBoxFindCaseSensitively)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.pushButtonFindAll = QtWidgets.QPushButton(self.groupBox)
        icon = QtGui.QIcon.fromTheme("find-all")
        self.pushButtonFindAll.setIcon(icon)
        self.pushButtonFindAll.setObjectName("pushButtonFindAll")
        self.horizontalLayout_6.addWidget(self.pushButtonFindAll)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 5)
        self.verticalLayout.addWidget(self.widgetFindReplace)
        self.widgetStatus = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetStatus.setObjectName("widgetStatus")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widgetStatus)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelPosition = QtWidgets.QLabel(self.widgetStatus)
        self.labelPosition.setMaximumSize(QtCore.QSize(300, 16777215))
        self.labelPosition.setObjectName("labelPosition")
        self.horizontalLayout_2.addWidget(self.labelPosition)
        self.line = QtWidgets.QFrame(self.widgetStatus)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.labelContent = QtWidgets.QLabel(self.widgetStatus)
        self.labelContent.setMaximumSize(QtCore.QSize(350, 16777215))
        self.labelContent.setObjectName("labelContent")
        self.horizontalLayout_2.addWidget(self.labelContent)
        self.line_2 = QtWidgets.QFrame(self.widgetStatus)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.labelStatus = QtWidgets.QLabel(self.widgetStatus)
        self.labelStatus.setMaximumSize(QtCore.QSize(150, 16777215))
        self.labelStatus.setObjectName("labelStatus")
        self.horizontalLayout_2.addWidget(self.labelStatus)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.toolButtonMenuBundle = QtWidgets.QToolButton(self.widgetStatus)
        icon = QtGui.QIcon.fromTheme("bundle-item-bundle")
        self.toolButtonMenuBundle.setIcon(icon)
        self.toolButtonMenuBundle.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButtonMenuBundle.setAutoRaise(True)
        self.toolButtonMenuBundle.setObjectName("toolButtonMenuBundle")
        self.horizontalLayout_2.addWidget(self.toolButtonMenuBundle)
        self.comboBoxSyntaxes = QtWidgets.QComboBox(self.widgetStatus)
        self.comboBoxSyntaxes.setObjectName("comboBoxSyntaxes")
        self.horizontalLayout_2.addWidget(self.comboBoxSyntaxes)
        self.comboBoxSymbols = QtWidgets.QComboBox(self.widgetStatus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSymbols.sizePolicy().hasHeightForWidth())
        self.comboBoxSymbols.setSizePolicy(sizePolicy)
        self.comboBoxSymbols.setObjectName("comboBoxSymbols")
        self.horizontalLayout_2.addWidget(self.comboBoxSymbols)
        self.verticalLayout.addWidget(self.widgetStatus)

        self.retranslateUi(CodeEditorStatus)
        QtCore.QMetaObject.connectSlotsByName(CodeEditorStatus)

    def retranslateUi(self, CodeEditorStatus):
        _translate = QtCore.QCoreApplication.translate
        CodeEditorStatus.setWindowTitle(_translate("CodeEditorStatus", "Form"))
        self.label.setText(_translate("CodeEditorStatus", "Command:"))
        self.label_2.setText(_translate("CodeEditorStatus", "Input:"))
        self.label_3.setText(_translate("CodeEditorStatus", "Output:"))
        self.labelGoToLine.setText(_translate("CodeEditorStatus", "Go to line:"))
        self.labelIFind.setText(_translate("CodeEditorStatus", "Find:"))
        self.pushButtonIFindNext.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>"))
        self.pushButtonIFindNext.setText(_translate("CodeEditorStatus", "Next"))
        self.pushButtonIFindPrevious.setText(_translate("CodeEditorStatus", "Previous"))
        self.checkBoxIFindCaseSensitively.setText(_translate("CodeEditorStatus", "Case Sensitively"))
        self.labelFind.setText(_translate("CodeEditorStatus", "Find:"))
        self.labelReplace.setText(_translate("CodeEditorStatus", "Replace:"))
        self.pushButtonReplace.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>"))
        self.pushButtonReplace.setText(_translate("CodeEditorStatus", "Replace"))
        self.pushButtonReplaceAll.setText(_translate("CodeEditorStatus", "Replace &All"))
        self.pushButtonFindPrevious.setText(_translate("CodeEditorStatus", "Previous"))
        self.pushButtonFindNext.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>"))
        self.pushButtonFindNext.setText(_translate("CodeEditorStatus", "Next"))
        self.labelFindMode.setText(_translate("CodeEditorStatus", "Mode:"))
        self.checkBoxFindCaseSensitively.setText(_translate("CodeEditorStatus", "Case Sensitively"))
        self.checkBox.setText(_translate("CodeEditorStatus", "Selection Only"))
        self.pushButtonFindAll.setText(_translate("CodeEditorStatus", "Find All"))
        self.labelPosition.setText(_translate("CodeEditorStatus", "Position"))
        self.labelContent.setText(_translate("CodeEditorStatus", "Content"))
        self.labelStatus.setText(_translate("CodeEditorStatus", "Status"))

