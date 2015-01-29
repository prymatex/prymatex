# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/process.ui'
#
# Created: Thu Jan 29 12:30:37 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExternalProcessDock(object):
    def setupUi(self, ExternalProcessDock):
        ExternalProcessDock.setObjectName("ExternalProcessDock")
        ExternalProcessDock.resize(330, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewExternalProcess = QtWidgets.QTreeView(self.dockWidgetContents)
        self.tableViewExternalProcess.setAlternatingRowColors(True)
        self.tableViewExternalProcess.setUniformRowHeights(True)
        self.tableViewExternalProcess.setHeaderHidden(True)
        self.tableViewExternalProcess.setObjectName("tableViewExternalProcess")
        self.verticalLayout.addWidget(self.tableViewExternalProcess)
        ExternalProcessDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionNewFolder = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName("actionNewFolder")
        self.actionNewFromTemplate = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName("actionNewFromTemplate")
        self.actionDelete = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNewProject = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionCloseProject = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/project-development-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName("actionCloseProject")
        self.actionOpenProject = QtWidgets.QAction(ExternalProcessDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/project-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionProperties = QtWidgets.QAction(ExternalProcessDock)
        self.actionProperties.setObjectName("actionProperties")
        self.actionRefresh = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionOpen = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenSystemEditor = QtWidgets.QAction(ExternalProcessDock)
        self.actionOpenSystemEditor.setObjectName("actionOpenSystemEditor")
        self.actionRename = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionOrderByName = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName("actionOrderByName")
        self.actionOrderBySize = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName("actionOrderBySize")
        self.actionOrderByDate = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName("actionOrderByDate")
        self.actionOrderByType = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName("actionOrderByType")
        self.actionOrderDescending = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName("actionOrderDescending")
        self.actionOrderFoldersFirst = QtWidgets.QAction(ExternalProcessDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName("actionOrderFoldersFirst")
        self.actionSetInTerminal = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("utilities-terminal")
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName("actionSetInTerminal")
        self.actionRemove = QtWidgets.QAction(ExternalProcessDock)
        self.actionRemove.setObjectName("actionRemove")
        self.actionProjectBundles = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("bundle-item-bundle")
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName("actionProjectBundles")
        self.actionBashInit = QtWidgets.QAction(ExternalProcessDock)
        self.actionBashInit.setObjectName("actionBashInit")
        self.actionCopy = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSelectRelatedBundles = QtWidgets.QAction(ExternalProcessDock)
        self.actionSelectRelatedBundles.setObjectName("actionSelectRelatedBundles")
        self.actionGoDown = QtWidgets.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.actionGoDown.setIcon(icon)
        self.actionGoDown.setObjectName("actionGoDown")

        self.retranslateUi(ExternalProcessDock)
        QtCore.QMetaObject.connectSlotsByName(ExternalProcessDock)

    def retranslateUi(self, ExternalProcessDock):
        _translate = QtCore.QCoreApplication.translate
        ExternalProcessDock.setWindowTitle(_translate("ExternalProcessDock", "Process"))
        self.actionNewFile.setText(_translate("ExternalProcessDock", "File"))
        self.actionNewFolder.setText(_translate("ExternalProcessDock", "Folder"))
        self.actionNewFromTemplate.setText(_translate("ExternalProcessDock", "From Template"))
        self.actionNewFromTemplate.setToolTip(_translate("ExternalProcessDock", "From Template"))
        self.actionDelete.setText(_translate("ExternalProcessDock", "Delete"))
        self.actionNewProject.setText(_translate("ExternalProcessDock", "Project"))
        self.actionCloseProject.setText(_translate("ExternalProcessDock", "Close"))
        self.actionOpenProject.setText(_translate("ExternalProcessDock", "Open"))
        self.actionProperties.setText(_translate("ExternalProcessDock", "Properties"))
        self.actionRefresh.setText(_translate("ExternalProcessDock", "Refresh"))
        self.actionRefresh.setShortcut(_translate("ExternalProcessDock", "F5"))
        self.actionOpen.setText(_translate("ExternalProcessDock", "Open"))
        self.actionOpenSystemEditor.setText(_translate("ExternalProcessDock", "System Editor"))
        self.actionRename.setText(_translate("ExternalProcessDock", "Rename"))
        self.actionRename.setToolTip(_translate("ExternalProcessDock", "Rename"))
        self.actionRename.setShortcut(_translate("ExternalProcessDock", "F2"))
        self.actionOrderByName.setText(_translate("ExternalProcessDock", "By Name"))
        self.actionOrderBySize.setText(_translate("ExternalProcessDock", "By Size"))
        self.actionOrderByDate.setText(_translate("ExternalProcessDock", "By Date"))
        self.actionOrderByType.setText(_translate("ExternalProcessDock", "By Type"))
        self.actionOrderDescending.setText(_translate("ExternalProcessDock", "Descending"))
        self.actionOrderFoldersFirst.setText(_translate("ExternalProcessDock", "Folders First"))
        self.actionSetInTerminal.setText(_translate("ExternalProcessDock", "Set In Terminal"))
        self.actionRemove.setText(_translate("ExternalProcessDock", "Remove"))
        self.actionProjectBundles.setText(_translate("ExternalProcessDock", "Project Bundles"))
        self.actionProjectBundles.setToolTip(_translate("ExternalProcessDock", "Bundles inside this project"))
        self.actionBashInit.setText(_translate("ExternalProcessDock", "Bash Init"))
        self.actionCopy.setText(_translate("ExternalProcessDock", "&Copy"))
        self.actionCopy.setShortcut(_translate("ExternalProcessDock", "Ctrl+C"))
        self.actionCut.setText(_translate("ExternalProcessDock", "Cu&t"))
        self.actionCut.setShortcut(_translate("ExternalProcessDock", "Ctrl+X"))
        self.actionPaste.setText(_translate("ExternalProcessDock", "&Paste"))
        self.actionPaste.setShortcut(_translate("ExternalProcessDock", "Ctrl+V"))
        self.actionSelectRelatedBundles.setText(_translate("ExternalProcessDock", "Select Related Bundles"))
        self.actionSelectRelatedBundles.setToolTip(_translate("ExternalProcessDock", "Choose bundles related to this project"))
        self.actionGoDown.setText(_translate("ExternalProcessDock", "Go Down"))

