# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/codeeditor/newstatus.ui'
#
# Created: Fri Dec 12 12:19:07 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CodeEditorStatus(object):
    def setupUi(self, CodeEditorStatus):
        CodeEditorStatus.setObjectName("CodeEditorStatus")
        CodeEditorStatus.resize(1100, 230)
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
        self.comboBoxInput = QtWidgets.QComboBox(self.widgetCommand)
        self.comboBoxInput.setObjectName("comboBoxInput")
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.line_4 = QtWidgets.QFrame(self.widgetCommand)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.comboBoxOutput = QtWidgets.QComboBox(self.widgetCommand)
        self.comboBoxOutput.setObjectName("comboBoxOutput")
        self.horizontalLayout.addWidget(self.comboBoxOutput)
        self.comboBoxCommand = QtWidgets.QComboBox(self.widgetCommand)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxCommand.sizePolicy().hasHeightForWidth())
        self.comboBoxCommand.setSizePolicy(sizePolicy)
        self.comboBoxCommand.setEditable(True)
        self.comboBoxCommand.setObjectName("comboBoxCommand")
        self.horizontalLayout.addWidget(self.comboBoxCommand)
        self.pushButtonCommandClose = QtWidgets.QPushButton(self.widgetCommand)
        self.pushButtonCommandClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonCommandClose.setIcon(icon)
        self.pushButtonCommandClose.setObjectName("pushButtonCommandClose")
        self.horizontalLayout.addWidget(self.pushButtonCommandClose)
        self.verticalLayout.addWidget(self.widgetCommand)
        self.widgetFind = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetFind.setObjectName("widgetFind")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widgetFind)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonFindRegularExrepssion = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("regular-expression")
        self.pushButtonFindRegularExrepssion.setIcon(icon)
        self.pushButtonFindRegularExrepssion.setCheckable(True)
        self.pushButtonFindRegularExrepssion.setObjectName("pushButtonFindRegularExrepssion")
        self.horizontalLayout_5.addWidget(self.pushButtonFindRegularExrepssion)
        self.pushButtonFindCaseSensitive = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("case-sensitive")
        self.pushButtonFindCaseSensitive.setIcon(icon)
        self.pushButtonFindCaseSensitive.setCheckable(True)
        self.pushButtonFindCaseSensitive.setObjectName("pushButtonFindCaseSensitive")
        self.horizontalLayout_5.addWidget(self.pushButtonFindCaseSensitive)
        self.pushButtonFindWholeWord = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("whole-word")
        self.pushButtonFindWholeWord.setIcon(icon)
        self.pushButtonFindWholeWord.setCheckable(True)
        self.pushButtonFindWholeWord.setObjectName("pushButtonFindWholeWord")
        self.horizontalLayout_5.addWidget(self.pushButtonFindWholeWord)
        self.line = QtWidgets.QFrame(self.widgetFind)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.pushButtonFindWrap = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("wrap")
        self.pushButtonFindWrap.setIcon(icon)
        self.pushButtonFindWrap.setCheckable(True)
        self.pushButtonFindWrap.setObjectName("pushButtonFindWrap")
        self.horizontalLayout_5.addWidget(self.pushButtonFindWrap)
        self.pushButtonFindInSelection = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("selection")
        self.pushButtonFindInSelection.setIcon(icon)
        self.pushButtonFindInSelection.setCheckable(True)
        self.pushButtonFindInSelection.setObjectName("pushButtonFindInSelection")
        self.horizontalLayout_5.addWidget(self.pushButtonFindInSelection)
        self.line_2 = QtWidgets.QFrame(self.widgetFind)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)
        self.pushButtonFindHighlightMatches = QtWidgets.QPushButton(self.widgetFind)
        icon = QtGui.QIcon.fromTheme("highlight-matches")
        self.pushButtonFindHighlightMatches.setIcon(icon)
        self.pushButtonFindHighlightMatches.setCheckable(True)
        self.pushButtonFindHighlightMatches.setObjectName("pushButtonFindHighlightMatches")
        self.horizontalLayout_5.addWidget(self.pushButtonFindHighlightMatches)
        self.comboBoxFind = QtWidgets.QComboBox(self.widgetFind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFind.sizePolicy().hasHeightForWidth())
        self.comboBoxFind.setSizePolicy(sizePolicy)
        self.comboBoxFind.setEditable(True)
        self.comboBoxFind.setObjectName("comboBoxFind")
        self.horizontalLayout_5.addWidget(self.comboBoxFind)
        self.pushButtonFindFind = QtWidgets.QPushButton(self.widgetFind)
        self.pushButtonFindFind.setObjectName("pushButtonFindFind")
        self.horizontalLayout_5.addWidget(self.pushButtonFindFind)
        self.pushButtonFindPrev = QtWidgets.QPushButton(self.widgetFind)
        self.pushButtonFindPrev.setObjectName("pushButtonFindPrev")
        self.horizontalLayout_5.addWidget(self.pushButtonFindPrev)
        self.pushButtonFindAll = QtWidgets.QPushButton(self.widgetFind)
        self.pushButtonFindAll.setObjectName("pushButtonFindAll")
        self.horizontalLayout_5.addWidget(self.pushButtonFindAll)
        self.pushButtonFindClose = QtWidgets.QPushButton(self.widgetFind)
        self.pushButtonFindClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonFindClose.setIcon(icon)
        self.pushButtonFindClose.setObjectName("pushButtonFindClose")
        self.horizontalLayout_5.addWidget(self.pushButtonFindClose)
        self.verticalLayout.addWidget(self.widgetFind)
        self.widgetReplace = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetReplace.setObjectName("widgetReplace")
        self.gridLayout = QtWidgets.QGridLayout(self.widgetReplace)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFindMode_2 = QtWidgets.QLabel(self.widgetReplace)
        self.labelFindMode_2.setObjectName("labelFindMode_2")
        self.gridLayout.addWidget(self.labelFindMode_2, 1, 6, 1, 1)
        self.pushButtonReplaceWrap = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("wrap")
        self.pushButtonReplaceWrap.setIcon(icon)
        self.pushButtonReplaceWrap.setCheckable(True)
        self.pushButtonReplaceWrap.setObjectName("pushButtonReplaceWrap")
        self.gridLayout.addWidget(self.pushButtonReplaceWrap, 0, 4, 1, 1)
        self.pushButtonReplaceFind = QtWidgets.QPushButton(self.widgetReplace)
        self.pushButtonReplaceFind.setObjectName("pushButtonReplaceFind")
        self.gridLayout.addWidget(self.pushButtonReplaceFind, 0, 8, 1, 1)
        self.pushButtonReplaceInSelection = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("selection")
        self.pushButtonReplaceInSelection.setIcon(icon)
        self.pushButtonReplaceInSelection.setCheckable(True)
        self.pushButtonReplaceInSelection.setObjectName("pushButtonReplaceInSelection")
        self.gridLayout.addWidget(self.pushButtonReplaceInSelection, 0, 5, 1, 1)
        self.labelFindMode_3 = QtWidgets.QLabel(self.widgetReplace)
        self.labelFindMode_3.setObjectName("labelFindMode_3")
        self.gridLayout.addWidget(self.labelFindMode_3, 0, 6, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.widgetReplace)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 3, 1, 1)
        self.comboBoxReplaceWhat = QtWidgets.QComboBox(self.widgetReplace)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxReplaceWhat.sizePolicy().hasHeightForWidth())
        self.comboBoxReplaceWhat.setSizePolicy(sizePolicy)
        self.comboBoxReplaceWhat.setEditable(True)
        self.comboBoxReplaceWhat.setObjectName("comboBoxReplaceWhat")
        self.gridLayout.addWidget(self.comboBoxReplaceWhat, 0, 7, 1, 1)
        self.pushButtonReplaceWholeWord = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("whole-word")
        self.pushButtonReplaceWholeWord.setIcon(icon)
        self.pushButtonReplaceWholeWord.setCheckable(True)
        self.pushButtonReplaceWholeWord.setObjectName("pushButtonReplaceWholeWord")
        self.gridLayout.addWidget(self.pushButtonReplaceWholeWord, 0, 2, 1, 1)
        self.pushButtonReplaceCaseSensitive = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("case-sensitive")
        self.pushButtonReplaceCaseSensitive.setIcon(icon)
        self.pushButtonReplaceCaseSensitive.setCheckable(True)
        self.pushButtonReplaceCaseSensitive.setObjectName("pushButtonReplaceCaseSensitive")
        self.gridLayout.addWidget(self.pushButtonReplaceCaseSensitive, 0, 1, 1, 1)
        self.pushButtonFindReplaceClose = QtWidgets.QPushButton(self.widgetReplace)
        self.pushButtonFindReplaceClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonFindReplaceClose.setIcon(icon)
        self.pushButtonFindReplaceClose.setObjectName("pushButtonFindReplaceClose")
        self.gridLayout.addWidget(self.pushButtonFindReplaceClose, 0, 12, 1, 1)
        self.pushButtonReplaceHighlightMatches = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("highlight-matches")
        self.pushButtonReplaceHighlightMatches.setIcon(icon)
        self.pushButtonReplaceHighlightMatches.setCheckable(True)
        self.pushButtonReplaceHighlightMatches.setObjectName("pushButtonReplaceHighlightMatches")
        self.gridLayout.addWidget(self.pushButtonReplaceHighlightMatches, 1, 4, 1, 1)
        self.pushButtonReplaceRegularExpression = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("regular-expression")
        self.pushButtonReplaceRegularExpression.setIcon(icon)
        self.pushButtonReplaceRegularExpression.setCheckable(True)
        self.pushButtonReplaceRegularExpression.setObjectName("pushButtonReplaceRegularExpression")
        self.gridLayout.addWidget(self.pushButtonReplaceRegularExpression, 0, 0, 1, 1)
        self.comboBoxReplaceWith = QtWidgets.QComboBox(self.widgetReplace)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxReplaceWith.sizePolicy().hasHeightForWidth())
        self.comboBoxReplaceWith.setSizePolicy(sizePolicy)
        self.comboBoxReplaceWith.setEditable(True)
        self.comboBoxReplaceWith.setObjectName("comboBoxReplaceWith")
        self.gridLayout.addWidget(self.comboBoxReplaceWith, 1, 7, 1, 1)
        self.pushButtonReplacePreserveCase = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("preserve-case")
        self.pushButtonReplacePreserveCase.setIcon(icon)
        self.pushButtonReplacePreserveCase.setCheckable(True)
        self.pushButtonReplacePreserveCase.setObjectName("pushButtonReplacePreserveCase")
        self.gridLayout.addWidget(self.pushButtonReplacePreserveCase, 1, 0, 1, 1)
        self.pushButtonReplaceReplaceAll = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("replace-all")
        self.pushButtonReplaceReplaceAll.setIcon(icon)
        self.pushButtonReplaceReplaceAll.setObjectName("pushButtonReplaceReplaceAll")
        self.gridLayout.addWidget(self.pushButtonReplaceReplaceAll, 1, 9, 1, 1)
        self.pushButtonReplaceReplace = QtWidgets.QPushButton(self.widgetReplace)
        icon = QtGui.QIcon.fromTheme("replace")
        self.pushButtonReplaceReplace.setIcon(icon)
        self.pushButtonReplaceReplace.setObjectName("pushButtonReplaceReplace")
        self.gridLayout.addWidget(self.pushButtonReplaceReplace, 0, 9, 1, 1)
        self.pushButtonReplaceFindAll = QtWidgets.QPushButton(self.widgetReplace)
        self.pushButtonReplaceFindAll.setObjectName("pushButtonReplaceFindAll")
        self.gridLayout.addWidget(self.pushButtonReplaceFindAll, 1, 8, 1, 1)
        self.verticalLayout.addWidget(self.widgetReplace)
        self.widgetFindInFiles = QtWidgets.QWidget(CodeEditorStatus)
        self.widgetFindInFiles.setObjectName("widgetFindInFiles")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widgetFindInFiles)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonFindInFilesClose = QtWidgets.QPushButton(self.widgetFindInFiles)
        self.pushButtonFindInFilesClose.setText("")
        icon = QtGui.QIcon.fromTheme("close")
        self.pushButtonFindInFilesClose.setIcon(icon)
        self.pushButtonFindInFilesClose.setObjectName("pushButtonFindInFilesClose")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesClose, 0, 9, 1, 1)
        self.pushButtonFindInFilesUseEditor = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("use-editor")
        self.pushButtonFindInFilesUseEditor.setIcon(icon)
        self.pushButtonFindInFilesUseEditor.setCheckable(True)
        self.pushButtonFindInFilesUseEditor.setObjectName("pushButtonFindInFilesUseEditor")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesUseEditor, 0, 4, 1, 1)
        self.labelFindMode_6 = QtWidgets.QLabel(self.widgetFindInFiles)
        self.labelFindMode_6.setObjectName("labelFindMode_6")
        self.gridLayout_2.addWidget(self.labelFindMode_6, 2, 5, 1, 1)
        self.labelFindMode_5 = QtWidgets.QLabel(self.widgetFindInFiles)
        self.labelFindMode_5.setObjectName("labelFindMode_5")
        self.gridLayout_2.addWidget(self.labelFindMode_5, 0, 5, 1, 1)
        self.labelFindMode_4 = QtWidgets.QLabel(self.widgetFindInFiles)
        self.labelFindMode_4.setObjectName("labelFindMode_4")
        self.gridLayout_2.addWidget(self.labelFindMode_4, 1, 5, 1, 1)
        self.pushButtonFindInFilesWholeWord = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("whole-word")
        self.pushButtonFindInFilesWholeWord.setIcon(icon)
        self.pushButtonFindInFilesWholeWord.setCheckable(True)
        self.pushButtonFindInFilesWholeWord.setObjectName("pushButtonFindInFilesWholeWord")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesWholeWord, 0, 2, 1, 1)
        self.comboBoxFindInFilesReplace = QtWidgets.QComboBox(self.widgetFindInFiles)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFindInFilesReplace.sizePolicy().hasHeightForWidth())
        self.comboBoxFindInFilesReplace.setSizePolicy(sizePolicy)
        self.comboBoxFindInFilesReplace.setEditable(True)
        self.comboBoxFindInFilesReplace.setObjectName("comboBoxFindInFilesReplace")
        self.gridLayout_2.addWidget(self.comboBoxFindInFilesReplace, 2, 6, 1, 1)
        self.comboBoxFindInFilesWhat = QtWidgets.QComboBox(self.widgetFindInFiles)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFindInFilesWhat.sizePolicy().hasHeightForWidth())
        self.comboBoxFindInFilesWhat.setSizePolicy(sizePolicy)
        self.comboBoxFindInFilesWhat.setEditable(True)
        self.comboBoxFindInFilesWhat.setObjectName("comboBoxFindInFilesWhat")
        self.gridLayout_2.addWidget(self.comboBoxFindInFilesWhat, 0, 6, 1, 1)
        self.pushButtonFindInFilesRegularExpression = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("regular-expression")
        self.pushButtonFindInFilesRegularExpression.setIcon(icon)
        self.pushButtonFindInFilesRegularExpression.setCheckable(True)
        self.pushButtonFindInFilesRegularExpression.setObjectName("pushButtonFindInFilesRegularExpression")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesRegularExpression, 0, 0, 1, 1)
        self.pushButtonFindInFilesShowContext = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("show-context")
        self.pushButtonFindInFilesShowContext.setIcon(icon)
        self.pushButtonFindInFilesShowContext.setCheckable(True)
        self.pushButtonFindInFilesShowContext.setObjectName("pushButtonFindInFilesShowContext")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesShowContext, 0, 3, 1, 1)
        self.pushButtonFindInFilesCaseSensitive = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("case-sensitive")
        self.pushButtonFindInFilesCaseSensitive.setIcon(icon)
        self.pushButtonFindInFilesCaseSensitive.setCheckable(True)
        self.pushButtonFindInFilesCaseSensitive.setObjectName("pushButtonFindInFilesCaseSensitive")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesCaseSensitive, 0, 1, 1, 1)
        self.comboBoxFindInFilesWhere = QtWidgets.QComboBox(self.widgetFindInFiles)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFindInFilesWhere.sizePolicy().hasHeightForWidth())
        self.comboBoxFindInFilesWhere.setSizePolicy(sizePolicy)
        self.comboBoxFindInFilesWhere.setEditable(True)
        self.comboBoxFindInFilesWhere.setObjectName("comboBoxFindInFilesWhere")
        self.gridLayout_2.addWidget(self.comboBoxFindInFilesWhere, 1, 6, 1, 1)
        self.pushButtonFindInFilesFind = QtWidgets.QPushButton(self.widgetFindInFiles)
        self.pushButtonFindInFilesFind.setObjectName("pushButtonFindInFilesFind")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesFind, 0, 7, 1, 1)
        self.pushButtonFindInFilesReplace = QtWidgets.QPushButton(self.widgetFindInFiles)
        icon = QtGui.QIcon.fromTheme("replace")
        self.pushButtonFindInFilesReplace.setIcon(icon)
        self.pushButtonFindInFilesReplace.setObjectName("pushButtonFindInFilesReplace")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesReplace, 2, 7, 1, 1)
        self.pushButtonFindInFilesWhere = QtWidgets.QPushButton(self.widgetFindInFiles)
        self.pushButtonFindInFilesWhere.setObjectName("pushButtonFindInFilesWhere")
        self.gridLayout_2.addWidget(self.pushButtonFindInFilesWhere, 1, 7, 1, 1)
        self.verticalLayout.addWidget(self.widgetFindInFiles)
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
        self.line_5 = QtWidgets.QFrame(self.widgetStatus)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_2.addWidget(self.line_5)
        self.labelContent = QtWidgets.QLabel(self.widgetStatus)
        self.labelContent.setMaximumSize(QtCore.QSize(350, 16777215))
        self.labelContent.setObjectName("labelContent")
        self.horizontalLayout_2.addWidget(self.labelContent)
        self.line_6 = QtWidgets.QFrame(self.widgetStatus)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_2.addWidget(self.line_6)
        self.labelStatus = QtWidgets.QLabel(self.widgetStatus)
        self.labelStatus.setMaximumSize(QtCore.QSize(150, 16777215))
        self.labelStatus.setObjectName("labelStatus")
        self.horizontalLayout_2.addWidget(self.labelStatus)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.toolButtonMenuBundles = QtWidgets.QToolButton(self.widgetStatus)
        icon = QtGui.QIcon.fromTheme("menu-bundles")
        self.toolButtonMenuBundles.setIcon(icon)
        self.toolButtonMenuBundles.setObjectName("toolButtonMenuBundles")
        self.horizontalLayout_2.addWidget(self.toolButtonMenuBundles)
        self.comboBoxSyntaxes = QtWidgets.QComboBox(self.widgetStatus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSyntaxes.sizePolicy().hasHeightForWidth())
        self.comboBoxSyntaxes.setSizePolicy(sizePolicy)
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
        self.pushButtonCommandClose.pressed.connect(self.widgetCommand.hide)
        self.pushButtonFindClose.pressed.connect(self.widgetFind.hide)
        self.pushButtonFindReplaceClose.pressed.connect(self.widgetReplace.hide)
        self.pushButtonFindInFilesClose.pressed.connect(self.widgetFindInFiles.hide)
        QtCore.QMetaObject.connectSlotsByName(CodeEditorStatus)

    def retranslateUi(self, CodeEditorStatus):
        _translate = QtCore.QCoreApplication.translate
        CodeEditorStatus.setWindowTitle(_translate("CodeEditorStatus", "Form"))
        self.pushButtonFindRegularExrepssion.setToolTip(_translate("CodeEditorStatus", "Regular expression"))
        self.pushButtonFindCaseSensitive.setToolTip(_translate("CodeEditorStatus", "Case sensitive"))
        self.pushButtonFindWholeWord.setToolTip(_translate("CodeEditorStatus", "Whole word"))
        self.pushButtonFindWrap.setToolTip(_translate("CodeEditorStatus", "Wrap"))
        self.pushButtonFindInSelection.setToolTip(_translate("CodeEditorStatus", "In selection"))
        self.pushButtonFindHighlightMatches.setToolTip(_translate("CodeEditorStatus", "Highlight matches"))
        self.pushButtonFindFind.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>"))
        self.pushButtonFindFind.setText(_translate("CodeEditorStatus", "Find"))
        self.pushButtonFindPrev.setText(_translate("CodeEditorStatus", "Find Prev"))
        self.pushButtonFindAll.setText(_translate("CodeEditorStatus", "Find All"))
        self.labelFindMode_2.setText(_translate("CodeEditorStatus", "With:"))
        self.pushButtonReplaceWrap.setToolTip(_translate("CodeEditorStatus", "Wrap"))
        self.pushButtonReplaceFind.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>"))
        self.pushButtonReplaceFind.setText(_translate("CodeEditorStatus", "Find"))
        self.pushButtonReplaceInSelection.setToolTip(_translate("CodeEditorStatus", "In selection"))
        self.labelFindMode_3.setText(_translate("CodeEditorStatus", "What:"))
        self.pushButtonReplaceWholeWord.setToolTip(_translate("CodeEditorStatus", "Whole word"))
        self.pushButtonReplaceCaseSensitive.setToolTip(_translate("CodeEditorStatus", "Case sensitive"))
        self.pushButtonReplaceHighlightMatches.setToolTip(_translate("CodeEditorStatus", "Highlight matches"))
        self.pushButtonReplaceRegularExpression.setToolTip(_translate("CodeEditorStatus", "Regular expression"))
        self.pushButtonReplacePreserveCase.setToolTip(_translate("CodeEditorStatus", "Preserve case"))
        self.pushButtonReplaceReplaceAll.setText(_translate("CodeEditorStatus", "Replace &All"))
        self.pushButtonReplaceReplace.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>"))
        self.pushButtonReplaceReplace.setText(_translate("CodeEditorStatus", "Replace"))
        self.pushButtonReplaceFindAll.setText(_translate("CodeEditorStatus", "Find All"))
        self.pushButtonFindInFilesUseEditor.setToolTip(_translate("CodeEditorStatus", "Use editor"))
        self.labelFindMode_6.setText(_translate("CodeEditorStatus", "Replace:"))
        self.labelFindMode_5.setText(_translate("CodeEditorStatus", "What:"))
        self.labelFindMode_4.setText(_translate("CodeEditorStatus", "Where:"))
        self.pushButtonFindInFilesWholeWord.setToolTip(_translate("CodeEditorStatus", "Whole word"))
        self.pushButtonFindInFilesRegularExpression.setToolTip(_translate("CodeEditorStatus", "Regular expression"))
        self.pushButtonFindInFilesShowContext.setToolTip(_translate("CodeEditorStatus", "Show context"))
        self.pushButtonFindInFilesCaseSensitive.setToolTip(_translate("CodeEditorStatus", "Case sensitive"))
        self.pushButtonFindInFilesFind.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>"))
        self.pushButtonFindInFilesFind.setText(_translate("CodeEditorStatus", "Find"))
        self.pushButtonFindInFilesReplace.setToolTip(_translate("CodeEditorStatus", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>"))
        self.pushButtonFindInFilesReplace.setText(_translate("CodeEditorStatus", "Replace"))
        self.pushButtonFindInFilesWhere.setText(_translate("CodeEditorStatus", "..."))
        self.labelPosition.setText(_translate("CodeEditorStatus", "Position"))
        self.labelContent.setText(_translate("CodeEditorStatus", "Content"))
        self.labelStatus.setText(_translate("CodeEditorStatus", "Status"))

