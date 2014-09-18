# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/filesystem.ui'
#
# Created: Thu Sep 18 10:12:00 2014
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

class Ui_FileSystemDock(object):
    def setupUi(self, FileSystemDock):
        FileSystemDock.setObjectName(_fromUtf8("FileSystemDock"))
        FileSystemDock.resize(330, 484)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        self.buttonsLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonBack = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonBack.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-previous"))
        self.pushButtonBack.setIcon(icon)
        self.pushButtonBack.setFlat(True)
        self.pushButtonBack.setObjectName(_fromUtf8("pushButtonBack"))
        self.buttonsLayout.addWidget(self.pushButtonBack)
        self.pushButtonFoward = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonFoward.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-next"))
        self.pushButtonFoward.setIcon(icon)
        self.pushButtonFoward.setFlat(True)
        self.pushButtonFoward.setObjectName(_fromUtf8("pushButtonFoward"))
        self.buttonsLayout.addWidget(self.pushButtonFoward)
        self.pushButtonUp = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonUp.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-up"))
        self.pushButtonUp.setIcon(icon)
        self.pushButtonUp.setFlat(True)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.buttonsLayout.addWidget(self.pushButtonUp)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.buttonsLayout.addWidget(self.line)
        self.pushButtonSync = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("sync"))
        self.pushButtonSync.setIcon(icon)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setFlat(True)
        self.pushButtonSync.setObjectName(_fromUtf8("pushButtonSync"))
        self.buttonsLayout.addWidget(self.pushButtonSync)
        self.pushButtonCollapseAll = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCollapseAll.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCollapseAll.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("collapse-all"))
        self.pushButtonCollapseAll.setIcon(icon)
        self.pushButtonCollapseAll.setFlat(True)
        self.pushButtonCollapseAll.setObjectName(_fromUtf8("pushButtonCollapseAll"))
        self.buttonsLayout.addWidget(self.pushButtonCollapseAll)
        self.pushButtonCustomFilters = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCustomFilters.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCustomFilters.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("custom-filters"))
        self.pushButtonCustomFilters.setIcon(icon)
        self.pushButtonCustomFilters.setFlat(True)
        self.pushButtonCustomFilters.setObjectName(_fromUtf8("pushButtonCustomFilters"))
        self.buttonsLayout.addWidget(self.pushButtonCustomFilters)
        self.pushButtonOptions = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonOptions.setMaximumSize(QtCore.QSize(45, 24))
        self.pushButtonOptions.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("options"))
        self.pushButtonOptions.setIcon(icon)
        self.pushButtonOptions.setFlat(True)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.buttonsLayout.addWidget(self.pushButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.comboBoxLocation = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLocation.sizePolicy().hasHeightForWidth())
        self.comboBoxLocation.setSizePolicy(sizePolicy)
        self.comboBoxLocation.setEditable(True)
        self.comboBoxLocation.setObjectName(_fromUtf8("comboBoxLocation"))
        self.verticalLayout.addWidget(self.comboBoxLocation)
        self.treeViewFileSystem = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewFileSystem.setObjectName(_fromUtf8("treeViewFileSystem"))
        self.verticalLayout.addWidget(self.treeViewFileSystem)
        FileSystemDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder-new"))
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/run-build-file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-delete"))
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionOrderByName = QtGui.QAction(FileSystemDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName(_fromUtf8("actionOrderByName"))
        self.actionOrderBySize = QtGui.QAction(FileSystemDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName(_fromUtf8("actionOrderBySize"))
        self.actionOrderByDate = QtGui.QAction(FileSystemDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName(_fromUtf8("actionOrderByDate"))
        self.actionOrderByType = QtGui.QAction(FileSystemDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName(_fromUtf8("actionOrderByType"))
        self.actionOrderDescending = QtGui.QAction(FileSystemDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName(_fromUtf8("actionOrderDescending"))
        self.actionOrderFoldersFirst = QtGui.QAction(FileSystemDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName(_fromUtf8("actionOrderFoldersFirst"))
        self.actionOpen = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpenSystemEditor = QtGui.QAction(FileSystemDock)
        self.actionOpenSystemEditor.setObjectName(_fromUtf8("actionOpenSystemEditor"))
        self.actionOpenDefaultEditor = QtGui.QAction(FileSystemDock)
        self.actionOpenDefaultEditor.setObjectName(_fromUtf8("actionOpenDefaultEditor"))
        self.actionRename = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-rename"))
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        self.actionConvertIntoProject = QtGui.QAction(FileSystemDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConvertIntoProject.setIcon(icon1)
        self.actionConvertIntoProject.setObjectName(_fromUtf8("actionConvertIntoProject"))
        self.actionSetInTerminal = QtGui.QAction(FileSystemDock)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/apps/utilities-terminal.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetInTerminal.setIcon(icon2)
        self.actionSetInTerminal.setObjectName(_fromUtf8("actionSetInTerminal"))
        self.actionCut = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-cut"))
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionCopy = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-copy"))
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-paste"))
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))

        self.retranslateUi(FileSystemDock)
        QtCore.QMetaObject.connectSlotsByName(FileSystemDock)

    def retranslateUi(self, FileSystemDock):
        FileSystemDock.setWindowTitle(_translate("FileSystemDock", "File System", None))
        self.pushButtonBack.setToolTip(_translate("FileSystemDock", "Go previous place", None))
        self.pushButtonFoward.setToolTip(_translate("FileSystemDock", "Go next place", None))
        self.pushButtonUp.setToolTip(_translate("FileSystemDock", "Go up one level", None))
        self.pushButtonSync.setToolTip(_translate("FileSystemDock", "Sync folder with current editor file path", None))
        self.comboBoxLocation.setToolTip(_translate("FileSystemDock", "Folders", None))
        self.actionNewFile.setText(_translate("FileSystemDock", "File", None))
        self.actionNewFolder.setText(_translate("FileSystemDock", "Folder", None))
        self.actionNewFromTemplate.setText(_translate("FileSystemDock", "File From Template", None))
        self.actionNewFromTemplate.setToolTip(_translate("FileSystemDock", "File From Template", None))
        self.actionDelete.setText(_translate("FileSystemDock", "Delete", None))
        self.actionOrderByName.setText(_translate("FileSystemDock", "By Name", None))
        self.actionOrderBySize.setText(_translate("FileSystemDock", "By Size", None))
        self.actionOrderByDate.setText(_translate("FileSystemDock", "By Date", None))
        self.actionOrderByType.setText(_translate("FileSystemDock", "By Type", None))
        self.actionOrderDescending.setText(_translate("FileSystemDock", "Descending", None))
        self.actionOrderFoldersFirst.setText(_translate("FileSystemDock", "Folders First", None))
        self.actionOpen.setText(_translate("FileSystemDock", "Open", None))
        self.actionOpenSystemEditor.setText(_translate("FileSystemDock", "System Editor", None))
        self.actionOpenDefaultEditor.setText(_translate("FileSystemDock", "Default Editor", None))
        self.actionRename.setText(_translate("FileSystemDock", "Rename", None))
        self.actionRename.setToolTip(_translate("FileSystemDock", "Rename", None))
        self.actionRename.setShortcut(_translate("FileSystemDock", "F2", None))
        self.actionConvertIntoProject.setText(_translate("FileSystemDock", "Convert Into Project", None))
        self.actionConvertIntoProject.setToolTip(_translate("FileSystemDock", "Convert current directory into project", None))
        self.actionSetInTerminal.setText(_translate("FileSystemDock", "Set In Terminal", None))
        self.actionCut.setText(_translate("FileSystemDock", "Cu&t", None))
        self.actionCut.setShortcut(_translate("FileSystemDock", "Ctrl+X", None))
        self.actionCopy.setText(_translate("FileSystemDock", "&Copy", None))
        self.actionCopy.setShortcut(_translate("FileSystemDock", "Ctrl+C", None))
        self.actionPaste.setText(_translate("FileSystemDock", "&Paste", None))
        self.actionPaste.setShortcut(_translate("FileSystemDock", "Ctrl+V", None))

