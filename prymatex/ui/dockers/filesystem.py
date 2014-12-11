# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/filesystem.ui'
#
# Created: Wed Dec 10 16:51:32 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileSystemDock(object):
    def setupUi(self, FileSystemDock):
        FileSystemDock.setObjectName("FileSystemDock")
        FileSystemDock.resize(347, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName("buttonsLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonGoPrevious = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setObjectName("pushButtonGoPrevious")
        self.buttonsLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setObjectName("pushButtonGoNext")
        self.buttonsLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonGoUp = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.pushButtonGoUp.setIcon(icon)
        self.pushButtonGoUp.setObjectName("pushButtonGoUp")
        self.buttonsLayout.addWidget(self.pushButtonGoUp)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.buttonsLayout.addWidget(self.line)
        self.pushButtonSync = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("sync")
        self.pushButtonSync.setIcon(icon)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setObjectName("pushButtonSync")
        self.buttonsLayout.addWidget(self.pushButtonSync)
        self.pushButtonCollapse = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonCollapse.setText("")
        icon = QtGui.QIcon.fromTheme("collapse")
        self.pushButtonCollapse.setIcon(icon)
        self.pushButtonCollapse.setObjectName("pushButtonCollapse")
        self.buttonsLayout.addWidget(self.pushButtonCollapse)
        self.pushButtonFilter = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonFilter.setText("")
        icon = QtGui.QIcon.fromTheme("filter")
        self.pushButtonFilter.setIcon(icon)
        self.pushButtonFilter.setObjectName("pushButtonFilter")
        self.buttonsLayout.addWidget(self.pushButtonFilter)
        self.toolButtonOptions = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("options")
        self.toolButtonOptions.setIcon(icon)
        self.toolButtonOptions.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButtonOptions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonOptions.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonOptions.setObjectName("toolButtonOptions")
        self.buttonsLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.comboBoxLocation = QtWidgets.QComboBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLocation.sizePolicy().hasHeightForWidth())
        self.comboBoxLocation.setSizePolicy(sizePolicy)
        self.comboBoxLocation.setEditable(True)
        self.comboBoxLocation.setObjectName("comboBoxLocation")
        self.verticalLayout.addWidget(self.comboBoxLocation)
        self.treeViewFileSystem = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewFileSystem.setObjectName("treeViewFileSystem")
        self.verticalLayout.addWidget(self.treeViewFileSystem)
        FileSystemDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionNewFolder = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName("actionNewFolder")
        self.actionNewFromTemplate = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/run-build-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName("actionNewFromTemplate")
        self.actionDelete = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionOrderByName = QtWidgets.QAction(FileSystemDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName("actionOrderByName")
        self.actionOrderBySize = QtWidgets.QAction(FileSystemDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName("actionOrderBySize")
        self.actionOrderByDate = QtWidgets.QAction(FileSystemDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName("actionOrderByDate")
        self.actionOrderByType = QtWidgets.QAction(FileSystemDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName("actionOrderByType")
        self.actionOrderDescending = QtWidgets.QAction(FileSystemDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName("actionOrderDescending")
        self.actionOrderFoldersFirst = QtWidgets.QAction(FileSystemDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName("actionOrderFoldersFirst")
        self.actionOpen = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenSystemEditor = QtWidgets.QAction(FileSystemDock)
        self.actionOpenSystemEditor.setObjectName("actionOpenSystemEditor")
        self.actionOpenDefaultEditor = QtWidgets.QAction(FileSystemDock)
        self.actionOpenDefaultEditor.setObjectName("actionOpenDefaultEditor")
        self.actionRename = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionConvertIntoProject = QtWidgets.QAction(FileSystemDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConvertIntoProject.setIcon(icon1)
        self.actionConvertIntoProject.setObjectName("actionConvertIntoProject")
        self.actionSetInTerminal = QtWidgets.QAction(FileSystemDock)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/apps/utilities-terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetInTerminal.setIcon(icon2)
        self.actionSetInTerminal.setObjectName("actionSetInTerminal")
        self.actionCut = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(FileSystemDock)
        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName("actionPaste")

        self.retranslateUi(FileSystemDock)
        QtCore.QMetaObject.connectSlotsByName(FileSystemDock)

    def retranslateUi(self, FileSystemDock):
        _translate = QtCore.QCoreApplication.translate
        FileSystemDock.setWindowTitle(_translate("FileSystemDock", "Files"))
        self.pushButtonGoPrevious.setToolTip(_translate("FileSystemDock", "Go previous place"))
        self.pushButtonGoNext.setToolTip(_translate("FileSystemDock", "Go next place"))
        self.pushButtonGoUp.setToolTip(_translate("FileSystemDock", "Go up one level"))
        self.pushButtonSync.setToolTip(_translate("FileSystemDock", "Sync folder with current editor file path"))
        self.comboBoxLocation.setToolTip(_translate("FileSystemDock", "Folders"))
        self.actionNewFile.setText(_translate("FileSystemDock", "File"))
        self.actionNewFolder.setText(_translate("FileSystemDock", "Folder"))
        self.actionNewFromTemplate.setText(_translate("FileSystemDock", "File From Template"))
        self.actionNewFromTemplate.setToolTip(_translate("FileSystemDock", "File From Template"))
        self.actionDelete.setText(_translate("FileSystemDock", "Delete"))
        self.actionOrderByName.setText(_translate("FileSystemDock", "By Name"))
        self.actionOrderBySize.setText(_translate("FileSystemDock", "By Size"))
        self.actionOrderByDate.setText(_translate("FileSystemDock", "By Date"))
        self.actionOrderByType.setText(_translate("FileSystemDock", "By Type"))
        self.actionOrderDescending.setText(_translate("FileSystemDock", "Descending"))
        self.actionOrderFoldersFirst.setText(_translate("FileSystemDock", "Folders First"))
        self.actionOpen.setText(_translate("FileSystemDock", "Open"))
        self.actionOpenSystemEditor.setText(_translate("FileSystemDock", "System Editor"))
        self.actionOpenDefaultEditor.setText(_translate("FileSystemDock", "Default Editor"))
        self.actionRename.setText(_translate("FileSystemDock", "Rename"))
        self.actionRename.setToolTip(_translate("FileSystemDock", "Rename"))
        self.actionRename.setShortcut(_translate("FileSystemDock", "F2"))
        self.actionConvertIntoProject.setText(_translate("FileSystemDock", "Convert Into Project"))
        self.actionConvertIntoProject.setToolTip(_translate("FileSystemDock", "Convert current directory into project"))
        self.actionSetInTerminal.setText(_translate("FileSystemDock", "Set In Terminal"))
        self.actionCut.setText(_translate("FileSystemDock", "Cu&t"))
        self.actionCut.setShortcut(_translate("FileSystemDock", "Ctrl+X"))
        self.actionCopy.setText(_translate("FileSystemDock", "&Copy"))
        self.actionCopy.setShortcut(_translate("FileSystemDock", "Ctrl+C"))
        self.actionPaste.setText(_translate("FileSystemDock", "&Paste"))
        self.actionPaste.setShortcut(_translate("FileSystemDock", "Ctrl+V"))

