# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/codeeditor/symbols.ui'
#
# Created: Sat Oct 18 10:31:41 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SymbolsDock(object):
    def setupUi(self, SymbolsDock):
        SymbolsDock.setObjectName("SymbolsDock")
        SymbolsDock.resize(330, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewSymbols = QtWidgets.QTreeView(self.dockWidgetContents)
        self.tableViewSymbols.setAlternatingRowColors(True)
        self.tableViewSymbols.setUniformRowHeights(True)
        self.tableViewSymbols.setHeaderHidden(True)
        self.tableViewSymbols.setObjectName("tableViewSymbols")
        self.verticalLayout.addWidget(self.tableViewSymbols)
        SymbolsDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionNewFolder = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName("actionNewFolder")
        self.actionNewFromTemplate = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName("actionNewFromTemplate")
        self.actionDelete = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNewProject = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("project-development-new-template")
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionCloseProject = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/project-development-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName("actionCloseProject")
        self.actionOpenProject = QtWidgets.QAction(SymbolsDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/project-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionProperties = QtWidgets.QAction(SymbolsDock)
        self.actionProperties.setObjectName("actionProperties")
        self.actionRefresh = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionOpen = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenSystemEditor = QtWidgets.QAction(SymbolsDock)
        self.actionOpenSystemEditor.setObjectName("actionOpenSystemEditor")
        self.actionRename = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionOrderByName = QtWidgets.QAction(SymbolsDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName("actionOrderByName")
        self.actionOrderBySize = QtWidgets.QAction(SymbolsDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName("actionOrderBySize")
        self.actionOrderByDate = QtWidgets.QAction(SymbolsDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName("actionOrderByDate")
        self.actionOrderByType = QtWidgets.QAction(SymbolsDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName("actionOrderByType")
        self.actionOrderDescending = QtWidgets.QAction(SymbolsDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName("actionOrderDescending")
        self.actionOrderFoldersFirst = QtWidgets.QAction(SymbolsDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName("actionOrderFoldersFirst")
        self.actionSetInTerminal = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("utilities-terminal")
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName("actionSetInTerminal")
        self.actionRemove = QtWidgets.QAction(SymbolsDock)
        self.actionRemove.setObjectName("actionRemove")
        self.actionProjectBundles = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("bundle-item-bundle")
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName("actionProjectBundles")
        self.actionBashInit = QtWidgets.QAction(SymbolsDock)
        self.actionBashInit.setObjectName("actionBashInit")
        self.actionCopy = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSelectRelatedBundles = QtWidgets.QAction(SymbolsDock)
        self.actionSelectRelatedBundles.setObjectName("actionSelectRelatedBundles")
        self.actionGoDown = QtWidgets.QAction(SymbolsDock)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.actionGoDown.setIcon(icon)
        self.actionGoDown.setObjectName("actionGoDown")

        self.retranslateUi(SymbolsDock)
        QtCore.QMetaObject.connectSlotsByName(SymbolsDock)

    def retranslateUi(self, SymbolsDock):
        _translate = QtCore.QCoreApplication.translate
        SymbolsDock.setWindowTitle(_translate("SymbolsDock", "Symbols"))
        self.actionNewFile.setText(_translate("SymbolsDock", "File"))
        self.actionNewFolder.setText(_translate("SymbolsDock", "Folder"))
        self.actionNewFromTemplate.setText(_translate("SymbolsDock", "From Template"))
        self.actionNewFromTemplate.setToolTip(_translate("SymbolsDock", "From Template"))
        self.actionDelete.setText(_translate("SymbolsDock", "Delete"))
        self.actionNewProject.setText(_translate("SymbolsDock", "Project"))
        self.actionCloseProject.setText(_translate("SymbolsDock", "Close"))
        self.actionOpenProject.setText(_translate("SymbolsDock", "Open"))
        self.actionProperties.setText(_translate("SymbolsDock", "Properties"))
        self.actionRefresh.setText(_translate("SymbolsDock", "Refresh"))
        self.actionRefresh.setShortcut(_translate("SymbolsDock", "F5"))
        self.actionOpen.setText(_translate("SymbolsDock", "Open"))
        self.actionOpenSystemEditor.setText(_translate("SymbolsDock", "System Editor"))
        self.actionRename.setText(_translate("SymbolsDock", "Rename"))
        self.actionRename.setToolTip(_translate("SymbolsDock", "Rename"))
        self.actionRename.setShortcut(_translate("SymbolsDock", "F2"))
        self.actionOrderByName.setText(_translate("SymbolsDock", "By Name"))
        self.actionOrderBySize.setText(_translate("SymbolsDock", "By Size"))
        self.actionOrderByDate.setText(_translate("SymbolsDock", "By Date"))
        self.actionOrderByType.setText(_translate("SymbolsDock", "By Type"))
        self.actionOrderDescending.setText(_translate("SymbolsDock", "Descending"))
        self.actionOrderFoldersFirst.setText(_translate("SymbolsDock", "Folders First"))
        self.actionSetInTerminal.setText(_translate("SymbolsDock", "Set In Terminal"))
        self.actionRemove.setText(_translate("SymbolsDock", "Remove"))
        self.actionProjectBundles.setText(_translate("SymbolsDock", "Project Bundles"))
        self.actionProjectBundles.setToolTip(_translate("SymbolsDock", "Bundles inside this project"))
        self.actionBashInit.setText(_translate("SymbolsDock", "Bash Init"))
        self.actionCopy.setText(_translate("SymbolsDock", "&Copy"))
        self.actionCopy.setShortcut(_translate("SymbolsDock", "Ctrl+C"))
        self.actionCut.setText(_translate("SymbolsDock", "Cu&t"))
        self.actionCut.setShortcut(_translate("SymbolsDock", "Ctrl+X"))
        self.actionPaste.setText(_translate("SymbolsDock", "&Paste"))
        self.actionPaste.setShortcut(_translate("SymbolsDock", "Ctrl+V"))
        self.actionSelectRelatedBundles.setText(_translate("SymbolsDock", "Select Related Bundles"))
        self.actionSelectRelatedBundles.setToolTip(_translate("SymbolsDock", "Choose bundles related to this project"))
        self.actionGoDown.setText(_translate("SymbolsDock", "Go Down"))

