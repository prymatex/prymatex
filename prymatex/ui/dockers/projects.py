# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/dockers/projects.ui'
#
# Created: Tue Jul 30 11:12:01 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProjectsDock(object):
    def setupUi(self, ProjectsDock):
        ProjectsDock.setObjectName(_fromUtf8("ProjectsDock"))
        ProjectsDock.resize(330, 484)
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
        self.pushButtonSync = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder-sync"))
        self.pushButtonSync.setIcon(icon)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setFlat(True)
        self.pushButtonSync.setObjectName(_fromUtf8("pushButtonSync"))
        self.buttonsLayout.addWidget(self.pushButtonSync)
        self.pushButtonCollapseAll = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCollapseAll.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCollapseAll.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-list-tree"))
        self.pushButtonCollapseAll.setIcon(icon)
        self.pushButtonCollapseAll.setFlat(True)
        self.pushButtonCollapseAll.setObjectName(_fromUtf8("pushButtonCollapseAll"))
        self.buttonsLayout.addWidget(self.pushButtonCollapseAll)
        self.pushButtonCustomFilters = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCustomFilters.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCustomFilters.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-filter"))
        self.pushButtonCustomFilters.setIcon(icon)
        self.pushButtonCustomFilters.setFlat(True)
        self.pushButtonCustomFilters.setObjectName(_fromUtf8("pushButtonCustomFilters"))
        self.buttonsLayout.addWidget(self.pushButtonCustomFilters)
        self.pushButtonOptions = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonOptions.setMaximumSize(QtCore.QSize(45, 24))
        self.pushButtonOptions.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("configure"))
        self.pushButtonOptions.setIcon(icon)
        self.pushButtonOptions.setFlat(True)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.buttonsLayout.addWidget(self.pushButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.treeViewProjects = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewProjects.setUniformRowHeights(True)
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setObjectName(_fromUtf8("treeViewProjects"))
        self.verticalLayout.addWidget(self.treeViewProjects)
        ProjectsDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder-new"))
        self.actionNewFolder.setIcon(icon)
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-delete"))
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionNewProject = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-development-new-template"))
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionCloseProject = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon)
        self.actionCloseProject.setObjectName(_fromUtf8("actionCloseProject"))
        self.actionOpenProject = QtGui.QAction(ProjectsDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionOpenProject.setObjectName(_fromUtf8("actionOpenProject"))
        self.actionProperties = QtGui.QAction(ProjectsDock)
        self.actionProperties.setObjectName(_fromUtf8("actionProperties"))
        self.actionRefresh = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-refresh"))
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionOpen = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpenSystemEditor = QtGui.QAction(ProjectsDock)
        self.actionOpenSystemEditor.setObjectName(_fromUtf8("actionOpenSystemEditor"))
        self.actionRename = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-rename"))
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        self.actionOrderByName = QtGui.QAction(ProjectsDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName(_fromUtf8("actionOrderByName"))
        self.actionOrderBySize = QtGui.QAction(ProjectsDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName(_fromUtf8("actionOrderBySize"))
        self.actionOrderByDate = QtGui.QAction(ProjectsDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName(_fromUtf8("actionOrderByDate"))
        self.actionOrderByType = QtGui.QAction(ProjectsDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName(_fromUtf8("actionOrderByType"))
        self.actionOrderDescending = QtGui.QAction(ProjectsDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName(_fromUtf8("actionOrderDescending"))
        self.actionOrderFoldersFirst = QtGui.QAction(ProjectsDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName(_fromUtf8("actionOrderFoldersFirst"))
        self.actionSetInTerminal = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("utilities-terminal"))
        self.actionSetInTerminal.setIcon(icon)
        self.actionSetInTerminal.setObjectName(_fromUtf8("actionSetInTerminal"))
        self.actionRemove = QtGui.QAction(ProjectsDock)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
        self.actionProjectBundles = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("bundle-item-bundle"))
        self.actionProjectBundles.setIcon(icon)
        self.actionProjectBundles.setObjectName(_fromUtf8("actionProjectBundles"))
        self.actionBashInit = QtGui.QAction(ProjectsDock)
        self.actionBashInit.setObjectName(_fromUtf8("actionBashInit"))
        self.actionCopy = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-copy"))
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionCut = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-cut"))
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-paste"))
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSelectRelatedBundles = QtGui.QAction(ProjectsDock)
        self.actionSelectRelatedBundles.setObjectName(_fromUtf8("actionSelectRelatedBundles"))

        self.retranslateUi(ProjectsDock)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDock)

    def retranslateUi(self, ProjectsDock):
        ProjectsDock.setWindowTitle(QtGui.QApplication.translate("ProjectsDock", "Projects", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSync.setToolTip(QtGui.QApplication.translate("ProjectsDock", "Sync folder with current editor file path", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setText(QtGui.QApplication.translate("ProjectsDock", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFolder.setText(QtGui.QApplication.translate("ProjectsDock", "Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFromTemplate.setText(QtGui.QApplication.translate("ProjectsDock", "From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFromTemplate.setToolTip(QtGui.QApplication.translate("ProjectsDock", "From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("ProjectsDock", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewProject.setText(QtGui.QApplication.translate("ProjectsDock", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProject.setText(QtGui.QApplication.translate("ProjectsDock", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProject.setText(QtGui.QApplication.translate("ProjectsDock", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setText(QtGui.QApplication.translate("ProjectsDock", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("ProjectsDock", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setShortcut(QtGui.QApplication.translate("ProjectsDock", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("ProjectsDock", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenSystemEditor.setText(QtGui.QApplication.translate("ProjectsDock", "System Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRename.setText(QtGui.QApplication.translate("ProjectsDock", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRename.setToolTip(QtGui.QApplication.translate("ProjectsDock", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRename.setShortcut(QtGui.QApplication.translate("ProjectsDock", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderByName.setText(QtGui.QApplication.translate("ProjectsDock", "By Name", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderBySize.setText(QtGui.QApplication.translate("ProjectsDock", "By Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderByDate.setText(QtGui.QApplication.translate("ProjectsDock", "By Date", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderByType.setText(QtGui.QApplication.translate("ProjectsDock", "By Type", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderDescending.setText(QtGui.QApplication.translate("ProjectsDock", "Descending", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOrderFoldersFirst.setText(QtGui.QApplication.translate("ProjectsDock", "Folders First", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetInTerminal.setText(QtGui.QApplication.translate("ProjectsDock", "Set In Terminal", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove.setText(QtGui.QApplication.translate("ProjectsDock", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProjectBundles.setText(QtGui.QApplication.translate("ProjectsDock", "Project Bundles", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProjectBundles.setToolTip(QtGui.QApplication.translate("ProjectsDock", "Bundles inside this project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBashInit.setText(QtGui.QApplication.translate("ProjectsDock", "Bash Init", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("ProjectsDock", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("ProjectsDock", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("ProjectsDock", "Cu&t", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("ProjectsDock", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("ProjectsDock", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("ProjectsDock", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectRelatedBundles.setText(QtGui.QApplication.translate("ProjectsDock", "Select Related Bundles", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectRelatedBundles.setToolTip(QtGui.QApplication.translate("ProjectsDock", "Choose bundles related to this project", None, QtGui.QApplication.UnicodeUTF8))

