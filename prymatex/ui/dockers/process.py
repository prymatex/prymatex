# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/process.ui'
#
# Created: Thu Sep 18 10:11:59 2014
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

class Ui_ExternalProcessDock(object):
    def setupUi(self, ExternalProcessDock):
        ExternalProcessDock.setObjectName(_fromUtf8("ExternalProcessDock"))
        ExternalProcessDock.resize(330, 484)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewExternalProcess = QtGui.QTreeView(self.dockWidgetContents)
        self.tableViewExternalProcess.setAlternatingRowColors(True)
        self.tableViewExternalProcess.setUniformRowHeights(True)
        self.tableViewExternalProcess.setHeaderHidden(True)
        self.tableViewExternalProcess.setObjectName(_fromUtf8("tableViewExternalProcess"))
        self.verticalLayout.addWidget(self.tableViewExternalProcess)
        ExternalProcessDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder-new"))
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-delete"))
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionNewProject = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-development-new-template"))
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionCloseProject = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName(_fromUtf8("actionCloseProject"))
        self.actionOpenProject = QtGui.QAction(ExternalProcessDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName(_fromUtf8("actionOpenProject"))
        self.actionProperties = QtGui.QAction(ExternalProcessDock)
        self.actionProperties.setObjectName(_fromUtf8("actionProperties"))
        self.actionRefresh = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-refresh"))
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionOpen = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpenSystemEditor = QtGui.QAction(ExternalProcessDock)
        self.actionOpenSystemEditor.setObjectName(_fromUtf8("actionOpenSystemEditor"))
        self.actionRename = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-rename"))
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        self.actionOrderByName = QtGui.QAction(ExternalProcessDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName(_fromUtf8("actionOrderByName"))
        self.actionOrderBySize = QtGui.QAction(ExternalProcessDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName(_fromUtf8("actionOrderBySize"))
        self.actionOrderByDate = QtGui.QAction(ExternalProcessDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName(_fromUtf8("actionOrderByDate"))
        self.actionOrderByType = QtGui.QAction(ExternalProcessDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName(_fromUtf8("actionOrderByType"))
        self.actionOrderDescending = QtGui.QAction(ExternalProcessDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName(_fromUtf8("actionOrderDescending"))
        self.actionOrderFoldersFirst = QtGui.QAction(ExternalProcessDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName(_fromUtf8("actionOrderFoldersFirst"))
        self.actionSetInTerminal = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("utilities-terminal"))
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName(_fromUtf8("actionSetInTerminal"))
        self.actionRemove = QtGui.QAction(ExternalProcessDock)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
        self.actionProjectBundles = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("bundle-item-bundle"))
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName(_fromUtf8("actionProjectBundles"))
        self.actionBashInit = QtGui.QAction(ExternalProcessDock)
        self.actionBashInit.setObjectName(_fromUtf8("actionBashInit"))
        self.actionCopy = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-copy"))
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionCut = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-cut"))
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-paste"))
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSelectRelatedBundles = QtGui.QAction(ExternalProcessDock)
        self.actionSelectRelatedBundles.setObjectName(_fromUtf8("actionSelectRelatedBundles"))
        self.actionGoDown = QtGui.QAction(ExternalProcessDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-down"))
        self.actionGoDown.setIcon(icon)
        self.actionGoDown.setObjectName(_fromUtf8("actionGoDown"))

        self.retranslateUi(ExternalProcessDock)
        QtCore.QMetaObject.connectSlotsByName(ExternalProcessDock)

    def retranslateUi(self, ExternalProcessDock):
        ExternalProcessDock.setWindowTitle(_translate("ExternalProcessDock", "External Process", None))
        self.actionNewFile.setText(_translate("ExternalProcessDock", "File", None))
        self.actionNewFolder.setText(_translate("ExternalProcessDock", "Folder", None))
        self.actionNewFromTemplate.setText(_translate("ExternalProcessDock", "From Template", None))
        self.actionNewFromTemplate.setToolTip(_translate("ExternalProcessDock", "From Template", None))
        self.actionDelete.setText(_translate("ExternalProcessDock", "Delete", None))
        self.actionNewProject.setText(_translate("ExternalProcessDock", "Project", None))
        self.actionCloseProject.setText(_translate("ExternalProcessDock", "Close", None))
        self.actionOpenProject.setText(_translate("ExternalProcessDock", "Open", None))
        self.actionProperties.setText(_translate("ExternalProcessDock", "Properties", None))
        self.actionRefresh.setText(_translate("ExternalProcessDock", "Refresh", None))
        self.actionRefresh.setShortcut(_translate("ExternalProcessDock", "F5", None))
        self.actionOpen.setText(_translate("ExternalProcessDock", "Open", None))
        self.actionOpenSystemEditor.setText(_translate("ExternalProcessDock", "System Editor", None))
        self.actionRename.setText(_translate("ExternalProcessDock", "Rename", None))
        self.actionRename.setToolTip(_translate("ExternalProcessDock", "Rename", None))
        self.actionRename.setShortcut(_translate("ExternalProcessDock", "F2", None))
        self.actionOrderByName.setText(_translate("ExternalProcessDock", "By Name", None))
        self.actionOrderBySize.setText(_translate("ExternalProcessDock", "By Size", None))
        self.actionOrderByDate.setText(_translate("ExternalProcessDock", "By Date", None))
        self.actionOrderByType.setText(_translate("ExternalProcessDock", "By Type", None))
        self.actionOrderDescending.setText(_translate("ExternalProcessDock", "Descending", None))
        self.actionOrderFoldersFirst.setText(_translate("ExternalProcessDock", "Folders First", None))
        self.actionSetInTerminal.setText(_translate("ExternalProcessDock", "Set In Terminal", None))
        self.actionRemove.setText(_translate("ExternalProcessDock", "Remove", None))
        self.actionProjectBundles.setText(_translate("ExternalProcessDock", "Project Bundles", None))
        self.actionProjectBundles.setToolTip(_translate("ExternalProcessDock", "Bundles inside this project", None))
        self.actionBashInit.setText(_translate("ExternalProcessDock", "Bash Init", None))
        self.actionCopy.setText(_translate("ExternalProcessDock", "&Copy", None))
        self.actionCopy.setShortcut(_translate("ExternalProcessDock", "Ctrl+C", None))
        self.actionCut.setText(_translate("ExternalProcessDock", "Cu&t", None))
        self.actionCut.setShortcut(_translate("ExternalProcessDock", "Ctrl+X", None))
        self.actionPaste.setText(_translate("ExternalProcessDock", "&Paste", None))
        self.actionPaste.setShortcut(_translate("ExternalProcessDock", "Ctrl+V", None))
        self.actionSelectRelatedBundles.setText(_translate("ExternalProcessDock", "Select Related Bundles", None))
        self.actionSelectRelatedBundles.setToolTip(_translate("ExternalProcessDock", "Choose bundles related to this project", None))
        self.actionGoDown.setText(_translate("ExternalProcessDock", "Go Down", None))

