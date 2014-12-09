# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/projects.ui'
#
# Created: Tue Dec  9 12:44:20 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectsDock(object):
    def setupUi(self, ProjectsDock):
        ProjectsDock.setObjectName("ProjectsDock")
        ProjectsDock.resize(330, 484)
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
        self.pushButtonGoPrevious.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setObjectName("pushButtonGoPrevious")
        self.buttonsLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonGoNext.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme("go-next")
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setObjectName("pushButtonGoNext")
        self.buttonsLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonGoUp = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonGoUp.setMaximumSize(QtCore.QSize(24, 24))
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
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme("sync")
        self.pushButtonSync.setIcon(icon)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setObjectName("pushButtonSync")
        self.buttonsLayout.addWidget(self.pushButtonSync)
        self.pushButtonCollapseAll = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonCollapseAll.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCollapseAll.setText("")
        icon = QtGui.QIcon.fromTheme("collapse-all")
        self.pushButtonCollapseAll.setIcon(icon)
        self.pushButtonCollapseAll.setObjectName("pushButtonCollapseAll")
        self.buttonsLayout.addWidget(self.pushButtonCollapseAll)
        self.pushButtonCustomFilters = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonCustomFilters.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCustomFilters.setText("")
        icon = QtGui.QIcon.fromTheme("custom-filters")
        self.pushButtonCustomFilters.setIcon(icon)
        self.pushButtonCustomFilters.setObjectName("pushButtonCustomFilters")
        self.buttonsLayout.addWidget(self.pushButtonCustomFilters)
        self.toolButtonOptions = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("options")
        self.toolButtonOptions.setIcon(icon)
        self.toolButtonOptions.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButtonOptions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonOptions.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonOptions.setObjectName("toolButtonOptions")
        self.buttonsLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.treeViewProjects = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewProjects.setUniformRowHeights(True)
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setObjectName("treeViewProjects")
        self.verticalLayout.addWidget(self.treeViewProjects)
        ProjectsDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionNewFolder = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName("actionNewFolder")
        self.actionNewFromTemplate = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName("actionNewFromTemplate")
        self.actionDelete = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNewProject = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionCloseProject = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/project-development-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName("actionCloseProject")
        self.actionOpenProject = QtWidgets.QAction(ProjectsDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/project-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionProperties = QtWidgets.QAction(ProjectsDock)
        self.actionProperties.setObjectName("actionProperties")
        self.actionRefresh = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionOpen = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenSystemEditor = QtWidgets.QAction(ProjectsDock)
        self.actionOpenSystemEditor.setObjectName("actionOpenSystemEditor")
        self.actionRename = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionOrderByName = QtWidgets.QAction(ProjectsDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName("actionOrderByName")
        self.actionOrderBySize = QtWidgets.QAction(ProjectsDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName("actionOrderBySize")
        self.actionOrderByDate = QtWidgets.QAction(ProjectsDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName("actionOrderByDate")
        self.actionOrderByType = QtWidgets.QAction(ProjectsDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName("actionOrderByType")
        self.actionOrderDescending = QtWidgets.QAction(ProjectsDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName("actionOrderDescending")
        self.actionOrderFoldersFirst = QtWidgets.QAction(ProjectsDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName("actionOrderFoldersFirst")
        self.actionSetInTerminal = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("utilities-terminal")
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName("actionSetInTerminal")
        self.actionRemove = QtWidgets.QAction(ProjectsDock)
        self.actionRemove.setObjectName("actionRemove")
        self.actionProjectBundles = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("bundle-item-bundle")
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName("actionProjectBundles")
        self.actionBashInit = QtWidgets.QAction(ProjectsDock)
        self.actionBashInit.setObjectName("actionBashInit")
        self.actionCopy = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSelectRelatedBundles = QtWidgets.QAction(ProjectsDock)
        self.actionSelectRelatedBundles.setObjectName("actionSelectRelatedBundles")
        self.actionGoDown = QtWidgets.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.actionGoDown.setIcon(icon)
        self.actionGoDown.setObjectName("actionGoDown")

        self.retranslateUi(ProjectsDock)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDock)

    def retranslateUi(self, ProjectsDock):
        _translate = QtCore.QCoreApplication.translate
        ProjectsDock.setWindowTitle(_translate("ProjectsDock", "Projects"))
        self.pushButtonGoPrevious.setToolTip(_translate("ProjectsDock", "Go previous place"))
        self.pushButtonGoNext.setToolTip(_translate("ProjectsDock", "Go next place"))
        self.pushButtonGoUp.setToolTip(_translate("ProjectsDock", "Go up one level"))
        self.pushButtonSync.setToolTip(_translate("ProjectsDock", "Sync folder with current editor file path"))
        self.actionNewFile.setText(_translate("ProjectsDock", "File"))
        self.actionNewFolder.setText(_translate("ProjectsDock", "Folder"))
        self.actionNewFromTemplate.setText(_translate("ProjectsDock", "From Template"))
        self.actionNewFromTemplate.setToolTip(_translate("ProjectsDock", "From Template"))
        self.actionDelete.setText(_translate("ProjectsDock", "Delete"))
        self.actionNewProject.setText(_translate("ProjectsDock", "Project"))
        self.actionCloseProject.setText(_translate("ProjectsDock", "Close"))
        self.actionOpenProject.setText(_translate("ProjectsDock", "Open"))
        self.actionProperties.setText(_translate("ProjectsDock", "Properties"))
        self.actionRefresh.setText(_translate("ProjectsDock", "Refresh"))
        self.actionRefresh.setShortcut(_translate("ProjectsDock", "F5"))
        self.actionOpen.setText(_translate("ProjectsDock", "Open"))
        self.actionOpenSystemEditor.setText(_translate("ProjectsDock", "System Editor"))
        self.actionRename.setText(_translate("ProjectsDock", "Rename"))
        self.actionRename.setToolTip(_translate("ProjectsDock", "Rename"))
        self.actionRename.setShortcut(_translate("ProjectsDock", "F2"))
        self.actionOrderByName.setText(_translate("ProjectsDock", "By Name"))
        self.actionOrderBySize.setText(_translate("ProjectsDock", "By Size"))
        self.actionOrderByDate.setText(_translate("ProjectsDock", "By Date"))
        self.actionOrderByType.setText(_translate("ProjectsDock", "By Type"))
        self.actionOrderDescending.setText(_translate("ProjectsDock", "Descending"))
        self.actionOrderFoldersFirst.setText(_translate("ProjectsDock", "Folders First"))
        self.actionSetInTerminal.setText(_translate("ProjectsDock", "Set In Terminal"))
        self.actionRemove.setText(_translate("ProjectsDock", "Remove"))
        self.actionProjectBundles.setText(_translate("ProjectsDock", "Project Bundles"))
        self.actionProjectBundles.setToolTip(_translate("ProjectsDock", "Bundles inside this project"))
        self.actionBashInit.setText(_translate("ProjectsDock", "Bash Init"))
        self.actionCopy.setText(_translate("ProjectsDock", "&Copy"))
        self.actionCopy.setShortcut(_translate("ProjectsDock", "Ctrl+C"))
        self.actionCut.setText(_translate("ProjectsDock", "Cu&t"))
        self.actionCut.setShortcut(_translate("ProjectsDock", "Ctrl+X"))
        self.actionPaste.setText(_translate("ProjectsDock", "&Paste"))
        self.actionPaste.setShortcut(_translate("ProjectsDock", "Ctrl+V"))
        self.actionSelectRelatedBundles.setText(_translate("ProjectsDock", "Select Related Bundles"))
        self.actionSelectRelatedBundles.setToolTip(_translate("ProjectsDock", "Choose bundles related to this project"))
        self.actionGoDown.setText(_translate("ProjectsDock", "Go Down"))

