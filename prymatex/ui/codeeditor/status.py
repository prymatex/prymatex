# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/codeeditor/status.ui'
#
# Created: Thu Sep 18 09:56:56 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CodeEditorStatus(object):
    def setupUi(self, CodeEditorStatus):
        CodeEditorStatus.setObjectName(_fromUtf8("CodeEditorStatus"))
        CodeEditorStatus.resize(686, 246)
        self.verticalLayout = QtGui.QVBoxLayout(CodeEditorStatus)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetCommand = QtGui.QWidget(CodeEditorStatus)
        self.widgetCommand.setObjectName(_fromUtf8("widgetCommand"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widgetCommand)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonCommandClose = QtGui.QPushButton(self.widgetCommand)
        self.pushButtonCommandClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("close"))
        self.pushButtonCommandClose.setIcon(icon)
        self.pushButtonCommandClose.setFlat(True)
        self.pushButtonCommandClose.setObjectName(_fromUtf8("pushButtonCommandClose"))
        self.horizontalLayout.addWidget(self.pushButtonCommandClose)
        self.label = QtGui.QLabel(self.widgetCommand)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxCommand = QtGui.QComboBox(self.widgetCommand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxCommand.sizePolicy().hasHeightForWidth())
        self.comboBoxCommand.setSizePolicy(sizePolicy)
        self.comboBoxCommand.setEditable(True)
        self.comboBoxCommand.setObjectName(_fromUtf8("comboBoxCommand"))
        self.horizontalLayout.addWidget(self.comboBoxCommand)
        self.label_2 = QtGui.QLabel(self.widgetCommand)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBoxInput = QtGui.QComboBox(self.widgetCommand)
        self.comboBoxInput.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBoxInput.setObjectName(_fromUtf8("comboBoxInput"))
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.label_3 = QtGui.QLabel(self.widgetCommand)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBoxOutput = QtGui.QComboBox(self.widgetCommand)
        self.comboBoxOutput.setMaximumSize(QtCore.QSize(160, 16777215))
        self.comboBoxOutput.setObjectName(_fromUtf8("comboBoxOutput"))
        self.horizontalLayout.addWidget(self.comboBoxOutput)
        self.verticalLayout.addWidget(self.widgetCommand)
        self.widgetGoToLine = QtGui.QWidget(CodeEditorStatus)
        self.widgetGoToLine.setObjectName(_fromUtf8("widgetGoToLine"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widgetGoToLine)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonGoToLineClose = QtGui.QPushButton(self.widgetGoToLine)
        self.pushButtonGoToLineClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("close"))
        self.pushButtonGoToLineClose.setIcon(icon)
        self.pushButtonGoToLineClose.setFlat(True)
        self.pushButtonGoToLineClose.setObjectName(_fromUtf8("pushButtonGoToLineClose"))
        self.horizontalLayout_3.addWidget(self.pushButtonGoToLineClose)
        self.labelGoToLine = QtGui.QLabel(self.widgetGoToLine)
        self.labelGoToLine.setObjectName(_fromUtf8("labelGoToLine"))
        self.horizontalLayout_3.addWidget(self.labelGoToLine)
        self.spinBoxGoToLine = QtGui.QSpinBox(self.widgetGoToLine)
        self.spinBoxGoToLine.setMinimum(1)
        self.spinBoxGoToLine.setMaximum(999999999)
        self.spinBoxGoToLine.setObjectName(_fromUtf8("spinBoxGoToLine"))
        self.horizontalLayout_3.addWidget(self.spinBoxGoToLine)
        spacerItem = QtGui.QSpacerItem(154, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widgetGoToLine)
        self.widgetIFind = QtGui.QWidget(CodeEditorStatus)
        self.widgetIFind.setObjectName(_fromUtf8("widgetIFind"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widgetIFind)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pushButtonIFindClose = QtGui.QPushButton(self.widgetIFind)
        self.pushButtonIFindClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("close"))
        self.pushButtonIFindClose.setIcon(icon)
        self.pushButtonIFindClose.setFlat(True)
        self.pushButtonIFindClose.setObjectName(_fromUtf8("pushButtonIFindClose"))
        self.horizontalLayout_5.addWidget(self.pushButtonIFindClose)
        self.labelIFind = QtGui.QLabel(self.widgetIFind)
        self.labelIFind.setObjectName(_fromUtf8("labelIFind"))
        self.horizontalLayout_5.addWidget(self.labelIFind)
        self.lineEditIFind = QtGui.QLineEdit(self.widgetIFind)
        self.lineEditIFind.setObjectName(_fromUtf8("lineEditIFind"))
        self.horizontalLayout_5.addWidget(self.lineEditIFind)
        self.pushButtonIFindNext = QtGui.QPushButton(self.widgetIFind)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-down"))
        self.pushButtonIFindNext.setIcon(icon)
        self.pushButtonIFindNext.setObjectName(_fromUtf8("pushButtonIFindNext"))
        self.horizontalLayout_5.addWidget(self.pushButtonIFindNext)
        self.pushButtonIFindPrevious = QtGui.QPushButton(self.widgetIFind)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-up"))
        self.pushButtonIFindPrevious.setIcon(icon)
        self.pushButtonIFindPrevious.setObjectName(_fromUtf8("pushButtonIFindPrevious"))
        self.horizontalLayout_5.addWidget(self.pushButtonIFindPrevious)
        self.checkBoxIFindCaseSensitively = QtGui.QCheckBox(self.widgetIFind)
        self.checkBoxIFindCaseSensitively.setObjectName(_fromUtf8("checkBoxIFindCaseSensitively"))
        self.horizontalLayout_5.addWidget(self.checkBoxIFindCaseSensitively)
        spacerItem1 = QtGui.QSpacerItem(155, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widgetIFind)
        self.widgetFindReplace = QtGui.QWidget(CodeEditorStatus)
        self.widgetFindReplace.setObjectName(_fromUtf8("widgetFindReplace"))
        self.gridLayout = QtGui.QGridLayout(self.widgetFindReplace)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonFindReplaceClose = QtGui.QPushButton(self.widgetFindReplace)
        self.pushButtonFindReplaceClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("close"))
        self.pushButtonFindReplaceClose.setIcon(icon)
        self.pushButtonFindReplaceClose.setFlat(True)
        self.pushButtonFindReplaceClose.setObjectName(_fromUtf8("pushButtonFindReplaceClose"))
        self.gridLayout.addWidget(self.pushButtonFindReplaceClose, 0, 0, 1, 1)
        self.labelFind = QtGui.QLabel(self.widgetFindReplace)
        self.labelFind.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFind.setObjectName(_fromUtf8("labelFind"))
        self.gridLayout.addWidget(self.labelFind, 0, 1, 1, 1)
        self.labelReplace = QtGui.QLabel(self.widgetFindReplace)
        self.labelReplace.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelReplace.setObjectName(_fromUtf8("labelReplace"))
        self.gridLayout.addWidget(self.labelReplace, 1, 1, 1, 1)
        self.lineEditFind = QtGui.QLineEdit(self.widgetFindReplace)
        self.lineEditFind.setObjectName(_fromUtf8("lineEditFind"))
        self.gridLayout.addWidget(self.lineEditFind, 0, 2, 1, 1)
        self.lineEditReplace = QtGui.QLineEdit(self.widgetFindReplace)
        self.lineEditReplace.setObjectName(_fromUtf8("lineEditReplace"))
        self.gridLayout.addWidget(self.lineEditReplace, 1, 2, 1, 1)
        self.pushButtonReplace = QtGui.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("replace"))
        self.pushButtonReplace.setIcon(icon)
        self.pushButtonReplace.setObjectName(_fromUtf8("pushButtonReplace"))
        self.gridLayout.addWidget(self.pushButtonReplace, 1, 3, 1, 1)
        self.pushButtonReplaceAll = QtGui.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("replace-all"))
        self.pushButtonReplaceAll.setIcon(icon)
        self.pushButtonReplaceAll.setObjectName(_fromUtf8("pushButtonReplaceAll"))
        self.gridLayout.addWidget(self.pushButtonReplaceAll, 1, 4, 1, 1)
        self.pushButtonFindPrevious = QtGui.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-up"))
        self.pushButtonFindPrevious.setIcon(icon)
        self.pushButtonFindPrevious.setObjectName(_fromUtf8("pushButtonFindPrevious"))
        self.gridLayout.addWidget(self.pushButtonFindPrevious, 0, 4, 1, 1)
        self.pushButtonFindNext = QtGui.QPushButton(self.widgetFindReplace)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-down"))
        self.pushButtonFindNext.setIcon(icon)
        self.pushButtonFindNext.setObjectName(_fromUtf8("pushButtonFindNext"))
        self.gridLayout.addWidget(self.pushButtonFindNext, 0, 3, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.widgetFindReplace)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.labelFindMode = QtGui.QLabel(self.groupBox)
        self.labelFindMode.setObjectName(_fromUtf8("labelFindMode"))
        self.horizontalLayout_6.addWidget(self.labelFindMode)
        self.comboBoxFindMode = QtGui.QComboBox(self.groupBox)
        self.comboBoxFindMode.setObjectName(_fromUtf8("comboBoxFindMode"))
        self.horizontalLayout_6.addWidget(self.comboBoxFindMode)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.checkBoxFindCaseSensitively = QtGui.QCheckBox(self.groupBox)
        self.checkBoxFindCaseSensitively.setObjectName(_fromUtf8("checkBoxFindCaseSensitively"))
        self.horizontalLayout_6.addWidget(self.checkBoxFindCaseSensitively)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.pushButtonFindAll = QtGui.QPushButton(self.groupBox)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("find-all"))
        self.pushButtonFindAll.setIcon(icon)
        self.pushButtonFindAll.setObjectName(_fromUtf8("pushButtonFindAll"))
        self.horizontalLayout_6.addWidget(self.pushButtonFindAll)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 5)
        self.verticalLayout.addWidget(self.widgetFindReplace)
        self.widgetStatus = QtGui.QWidget(CodeEditorStatus)
        self.widgetStatus.setObjectName(_fromUtf8("widgetStatus"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widgetStatus)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelPosition = QtGui.QLabel(self.widgetStatus)
        self.labelPosition.setMaximumSize(QtCore.QSize(300, 16777215))
        self.labelPosition.setObjectName(_fromUtf8("labelPosition"))
        self.horizontalLayout_2.addWidget(self.labelPosition)
        self.line = QtGui.QFrame(self.widgetStatus)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        self.labelContent = QtGui.QLabel(self.widgetStatus)
        self.labelContent.setMaximumSize(QtCore.QSize(350, 16777215))
        self.labelContent.setObjectName(_fromUtf8("labelContent"))
        self.horizontalLayout_2.addWidget(self.labelContent)
        self.line_2 = QtGui.QFrame(self.widgetStatus)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_2.addWidget(self.line_2)
        self.labelStatus = QtGui.QLabel(self.widgetStatus)
        self.labelStatus.setMaximumSize(QtCore.QSize(150, 16777215))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.horizontalLayout_2.addWidget(self.labelStatus)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.toolButtonMenuBundle = QtGui.QToolButton(self.widgetStatus)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("bundle-item-bundle"))
        self.toolButtonMenuBundle.setIcon(icon)
        self.toolButtonMenuBundle.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonMenuBundle.setAutoRaise(True)
        self.toolButtonMenuBundle.setObjectName(_fromUtf8("toolButtonMenuBundle"))
        self.horizontalLayout_2.addWidget(self.toolButtonMenuBundle)
        self.comboBoxSyntaxes = QtGui.QComboBox(self.widgetStatus)
        self.comboBoxSyntaxes.setObjectName(_fromUtf8("comboBoxSyntaxes"))
        self.horizontalLayout_2.addWidget(self.comboBoxSyntaxes)
        self.comboBoxSymbols = QtGui.QComboBox(self.widgetStatus)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSymbols.sizePolicy().hasHeightForWidth())
        self.comboBoxSymbols.setSizePolicy(sizePolicy)
        self.comboBoxSymbols.setObjectName(_fromUtf8("comboBoxSymbols"))
        self.horizontalLayout_2.addWidget(self.comboBoxSymbols)
        self.verticalLayout.addWidget(self.widgetStatus)

        self.retranslateUi(CodeEditorStatus)
        QtCore.QMetaObject.connectSlotsByName(CodeEditorStatus)

    def retranslateUi(self, CodeEditorStatus):
        CodeEditorStatus.setWindowTitle(_translate("CodeEditorStatus", "Form", None))
        self.label.setText(_translate("CodeEditorStatus", "Command:", None))
        self.label_2.setText(_translate("CodeEditorStatus", "Input:", None))
        self.label_3.setText(_translate("CodeEditorStatus", "Output:", None))
        self.labelGoToLine.setText(_translate("CodeEditorStatus", "Go to line:", None))
        self.labelIFind.setText(_translate("CodeEditorStatus", "Find:", None))
        self.pushButtonIFindNext.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>", None))
        self.pushButtonIFindNext.setText(_translate("CodeEditorStatus", "Next", None))
        self.pushButtonIFindPrevious.setText(_translate("CodeEditorStatus", "Previous", None))
        self.checkBoxIFindCaseSensitively.setText(_translate("CodeEditorStatus", "Case Sensitively", None))
        self.labelFind.setText(_translate("CodeEditorStatus", "Find:", None))
        self.labelReplace.setText(_translate("CodeEditorStatus", "Replace:", None))
        self.pushButtonReplace.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>", None))
        self.pushButtonReplace.setText(_translate("CodeEditorStatus", "Replace", None))
        self.pushButtonReplaceAll.setText(_translate("CodeEditorStatus", "Replace &All", None))
        self.pushButtonFindPrevious.setText(_translate("CodeEditorStatus", "Previous", None))
        self.pushButtonFindNext.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>", None))
        self.pushButtonFindNext.setText(_translate("CodeEditorStatus", "Next", None))
        self.labelFindMode.setText(_translate("CodeEditorStatus", "Mode:", None))
        self.checkBoxFindCaseSensitively.setText(_translate("CodeEditorStatus", "Case Sensitively", None))
        self.checkBox.setText(_translate("CodeEditorStatus", "Selection Only", None))
        self.pushButtonFindAll.setText(_translate("CodeEditorStatus", "Find All", None))
        self.labelPosition.setText(_translate("CodeEditorStatus", "Position", None))
        self.labelContent.setText(_translate("CodeEditorStatus", "Content", None))
        self.labelStatus.setText(_translate("CodeEditorStatus", "Status", None))

