# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/codeeditor/bookmarks.ui'
#
# Created: Mon Jan 26 19:54:12 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookmarksDock(object):
    def setupUi(self, BookmarksDock):
        BookmarksDock.setObjectName("BookmarksDock")
        BookmarksDock.resize(330, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewBookmarks = QtWidgets.QTreeView(self.dockWidgetContents)
        self.tableViewBookmarks.setAlternatingRowColors(True)
        self.tableViewBookmarks.setUniformRowHeights(True)
        self.tableViewBookmarks.setHeaderHidden(True)
        self.tableViewBookmarks.setObjectName("tableViewBookmarks")
        self.verticalLayout.addWidget(self.tableViewBookmarks)
        BookmarksDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionNewFolder = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName("actionNewFolder")
        self.actionNewFromTemplate = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName("actionNewFromTemplate")
        self.actionDelete = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNewProject = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionCloseProject = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/project-development-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName("actionCloseProject")
        self.actionOpenProject = QtWidgets.QAction(BookmarksDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/project-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionProperties = QtWidgets.QAction(BookmarksDock)
        self.actionProperties.setObjectName("actionProperties")
        self.actionRefresh = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionOpen = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenSystemEditor = QtWidgets.QAction(BookmarksDock)
        self.actionOpenSystemEditor.setObjectName("actionOpenSystemEditor")
        self.actionRename = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionOrderByName = QtWidgets.QAction(BookmarksDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName("actionOrderByName")
        self.actionOrderBySize = QtWidgets.QAction(BookmarksDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName("actionOrderBySize")
        self.actionOrderByDate = QtWidgets.QAction(BookmarksDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName("actionOrderByDate")
        self.actionOrderByType = QtWidgets.QAction(BookmarksDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName("actionOrderByType")
        self.actionOrderDescending = QtWidgets.QAction(BookmarksDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName("actionOrderDescending")
        self.actionOrderFoldersFirst = QtWidgets.QAction(BookmarksDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName("actionOrderFoldersFirst")
        self.actionSetInTerminal = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("utilities-terminal")
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName("actionSetInTerminal")
        self.actionRemove = QtWidgets.QAction(BookmarksDock)
        self.actionRemove.setObjectName("actionRemove")
        self.actionProjectBundles = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("bundle-item-bundle")
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName("actionProjectBundles")
        self.actionBashInit = QtWidgets.QAction(BookmarksDock)
        self.actionBashInit.setObjectName("actionBashInit")
        self.actionCopy = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSelectRelatedBundles = QtWidgets.QAction(BookmarksDock)
        self.actionSelectRelatedBundles.setObjectName("actionSelectRelatedBundles")
        self.actionGoDown = QtWidgets.QAction(BookmarksDock)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.actionGoDown.setIcon(icon)
        self.actionGoDown.setObjectName("actionGoDown")

        self.retranslateUi(BookmarksDock)
        QtCore.QMetaObject.connectSlotsByName(BookmarksDock)

    def retranslateUi(self, BookmarksDock):
        _translate = QtCore.QCoreApplication.translate
        BookmarksDock.setWindowTitle(_translate("BookmarksDock", "Bookmarks"))
        self.actionNewFile.setText(_translate("BookmarksDock", "File"))
        self.actionNewFolder.setText(_translate("BookmarksDock", "Folder"))
        self.actionNewFromTemplate.setText(_translate("BookmarksDock", "From Template"))
        self.actionNewFromTemplate.setToolTip(_translate("BookmarksDock", "From Template"))
        self.actionDelete.setText(_translate("BookmarksDock", "Delete"))
        self.actionNewProject.setText(_translate("BookmarksDock", "Project"))
        self.actionCloseProject.setText(_translate("BookmarksDock", "Close"))
        self.actionOpenProject.setText(_translate("BookmarksDock", "Open"))
        self.actionProperties.setText(_translate("BookmarksDock", "Properties"))
        self.actionRefresh.setText(_translate("BookmarksDock", "Refresh"))
        self.actionRefresh.setShortcut(_translate("BookmarksDock", "F5"))
        self.actionOpen.setText(_translate("BookmarksDock", "Open"))
        self.actionOpenSystemEditor.setText(_translate("BookmarksDock", "System Editor"))
        self.actionRename.setText(_translate("BookmarksDock", "Rename"))
        self.actionRename.setToolTip(_translate("BookmarksDock", "Rename"))
        self.actionRename.setShortcut(_translate("BookmarksDock", "F2"))
        self.actionOrderByName.setText(_translate("BookmarksDock", "By Name"))
        self.actionOrderBySize.setText(_translate("BookmarksDock", "By Size"))
        self.actionOrderByDate.setText(_translate("BookmarksDock", "By Date"))
        self.actionOrderByType.setText(_translate("BookmarksDock", "By Type"))
        self.actionOrderDescending.setText(_translate("BookmarksDock", "Descending"))
        self.actionOrderFoldersFirst.setText(_translate("BookmarksDock", "Folders First"))
        self.actionSetInTerminal.setText(_translate("BookmarksDock", "Set In Terminal"))
        self.actionRemove.setText(_translate("BookmarksDock", "Remove"))
        self.actionProjectBundles.setText(_translate("BookmarksDock", "Project Bundles"))
        self.actionProjectBundles.setToolTip(_translate("BookmarksDock", "Bundles inside this project"))
        self.actionBashInit.setText(_translate("BookmarksDock", "Bash Init"))
        self.actionCopy.setText(_translate("BookmarksDock", "&Copy"))
        self.actionCopy.setShortcut(_translate("BookmarksDock", "Ctrl+C"))
        self.actionCut.setText(_translate("BookmarksDock", "Cu&t"))
        self.actionCut.setShortcut(_translate("BookmarksDock", "Ctrl+X"))
        self.actionPaste.setText(_translate("BookmarksDock", "&Paste"))
        self.actionPaste.setShortcut(_translate("BookmarksDock", "Ctrl+V"))
        self.actionSelectRelatedBundles.setText(_translate("BookmarksDock", "Select Related Bundles"))
        self.actionSelectRelatedBundles.setToolTip(_translate("BookmarksDock", "Choose bundles related to this project"))
        self.actionGoDown.setText(_translate("BookmarksDock", "Go Down"))

