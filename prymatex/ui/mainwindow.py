# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/mainwindow.ui'
#
# Created: Fri Jun 28 09:26:33 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(801, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitTabWidget = SplitTabWidget(self.centralwidget)
        self.splitTabWidget.setObjectName(_fromUtf8("splitTabWidget"))
        self.verticalLayout.addWidget(self.splitTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuRecentFiles = QtGui.QMenu(self.menuFile)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-open-recent.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuRecentFiles.setIcon(icon)
        self.menuRecentFiles.setObjectName(_fromUtf8("menuRecentFiles"))
        self.menuNew = QtGui.QMenu(self.menuFile)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuNew.setIcon(icon1)
        self.menuNew.setObjectName(_fromUtf8("menuNew"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuPanels = QtGui.QMenu(self.menuView)
        self.menuPanels.setObjectName(_fromUtf8("menuPanels"))
        self.menuNavigation = QtGui.QMenu(self.menubar)
        self.menuNavigation.setObjectName(_fromUtf8("menuNavigation"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuBundles = QtGui.QMenu(self.menubar)
        self.menuBundles.setObjectName(_fromUtf8("menuBundles"))
        self.menuBundleEditor = QtGui.QMenu(self.menuBundles)
        self.menuBundleEditor.setObjectName(_fromUtf8("menuBundleEditor"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        MainWindow.setMenuBar(self.menubar)
        self.actionNewEditor = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("tab-new"))
        self.actionNewEditor.setIcon(icon)
        self.actionNewEditor.setObjectName(_fromUtf8("actionNewEditor"))
        self.actionOpen = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save"))
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save-as"))
        self.actionSaveAs.setIcon(icon)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionSaveAll = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save-all"))
        self.actionSaveAll.setIcon(icon)
        self.actionSaveAll.setObjectName(_fromUtf8("actionSaveAll"))
        self.actionClose = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("tab-close"))
        self.actionClose.setIcon(icon)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionCloseOthers = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("tab-close-other"))
        self.actionCloseOthers.setIcon(icon)
        self.actionCloseOthers.setObjectName(_fromUtf8("actionCloseOthers"))
        self.actionQuit = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionUndo = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-undo"))
        self.actionUndo.setIcon(icon)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-redo"))
        self.actionRedo.setIcon(icon)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.actionCopy = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-copy"))
        self.actionCopy.setIcon(icon)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionCut = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-cut"))
        self.actionCut.setIcon(icon)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-paste"))
        self.actionPaste.setIcon(icon)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSettings = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("configure"))
        self.actionSettings.setIcon(icon)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionFullscreen = QtGui.QAction(MainWindow)
        self.actionFullscreen.setCheckable(True)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-fullscreen"))
        self.actionFullscreen.setIcon(icon)
        self.actionFullscreen.setObjectName(_fromUtf8("actionFullscreen"))
        self.actionShowMenus = QtGui.QAction(MainWindow)
        self.actionShowMenus.setCheckable(True)
        self.actionShowMenus.setObjectName(_fromUtf8("actionShowMenus"))
        self.actionNextTab = QtGui.QAction(MainWindow)
        self.actionNextTab.setObjectName(_fromUtf8("actionNextTab"))
        self.actionPreviousTab = QtGui.QAction(MainWindow)
        self.actionPreviousTab.setObjectName(_fromUtf8("actionPreviousTab"))
        self.actionReportBug = QtGui.QAction(MainWindow)
        self.actionReportBug.setObjectName(_fromUtf8("actionReportBug"))
        self.actionTranslatePrymatex = QtGui.QAction(MainWindow)
        self.actionTranslatePrymatex.setObjectName(_fromUtf8("actionTranslatePrymatex"))
        self.actionProjectHomepage = QtGui.QAction(MainWindow)
        self.actionProjectHomepage.setObjectName(_fromUtf8("actionProjectHomepage"))
        self.actionTakeScreenshot = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("ksnapshot"))
        self.actionTakeScreenshot.setIcon(icon)
        self.actionTakeScreenshot.setObjectName(_fromUtf8("actionTakeScreenshot"))
        self.actionAbout = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("help-about"))
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAboutQt = QtGui.QAction(MainWindow)
        self.actionAboutQt.setObjectName(_fromUtf8("actionAboutQt"))
        self.actionNewFromTemplate = QtGui.QAction(MainWindow)
        self.actionNewFromTemplate.setEnabled(True)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionReadDocumentation = QtGui.QAction(MainWindow)
        self.actionReadDocumentation.setObjectName(_fromUtf8("actionReadDocumentation"))
        self.actionCloseAll = QtGui.QAction(MainWindow)
        self.actionCloseAll.setObjectName(_fromUtf8("actionCloseAll"))
        self.actionShowStatus = QtGui.QAction(MainWindow)
        self.actionShowStatus.setCheckable(True)
        self.actionShowStatus.setObjectName(_fromUtf8("actionShowStatus"))
        self.actionOpenAllRecentFiles = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open-recent"))
        self.actionOpenAllRecentFiles.setIcon(icon)
        self.actionOpenAllRecentFiles.setObjectName(_fromUtf8("actionOpenAllRecentFiles"))
        self.actionRemoveAllRecentFiles = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-clear"))
        self.actionRemoveAllRecentFiles.setIcon(icon)
        self.actionRemoveAllRecentFiles.setObjectName(_fromUtf8("actionRemoveAllRecentFiles"))
        self.actionShowBundleEditor = QtGui.QAction(MainWindow)
        self.actionShowBundleEditor.setObjectName(_fromUtf8("actionShowBundleEditor"))
        self.actionEditCommands = QtGui.QAction(MainWindow)
        self.actionEditCommands.setObjectName(_fromUtf8("actionEditCommands"))
        self.actionEditLanguages = QtGui.QAction(MainWindow)
        self.actionEditLanguages.setObjectName(_fromUtf8("actionEditLanguages"))
        self.actionEditSnippets = QtGui.QAction(MainWindow)
        self.actionEditSnippets.setObjectName(_fromUtf8("actionEditSnippets"))
        self.actionReloadBundles = QtGui.QAction(MainWindow)
        self.actionReloadBundles.setObjectName(_fromUtf8("actionReloadBundles"))
        self.actionSelectTab = QtGui.QAction(MainWindow)
        self.actionSelectTab.setObjectName(_fromUtf8("actionSelectTab"))
        self.actionNewProject = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-development-new-template"))
        self.actionNewProject.setIcon(icon)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionDelete = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-delete"))
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionSwitchProfile = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("system-switch-user"))
        self.actionSwitchProfile.setIcon(icon)
        self.actionSwitchProfile.setObjectName(_fromUtf8("actionSwitchProfile"))
        self.actionImportProject = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-open"))
        self.actionImportProject.setIcon(icon)
        self.actionImportProject.setObjectName(_fromUtf8("actionImportProject"))
        self.actionLastEditLocation = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-first-view"))
        self.actionLastEditLocation.setIcon(icon)
        self.actionLastEditLocation.setObjectName(_fromUtf8("actionLastEditLocation"))
        self.actionLocationBack = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-previous-view"))
        self.actionLocationBack.setIcon(icon)
        self.actionLocationBack.setObjectName(_fromUtf8("actionLocationBack"))
        self.actionLocationForward = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-next-view"))
        self.actionLocationForward.setIcon(icon)
        self.actionLocationForward.setObjectName(_fromUtf8("actionLocationForward"))
        self.actionJumpToTabWindow = QtGui.QAction(MainWindow)
        self.actionJumpToTabWindow.setObjectName(_fromUtf8("actionJumpToTabWindow"))
        self.menuRecentFiles.addAction(self.actionOpenAllRecentFiles)
        self.menuRecentFiles.addAction(self.actionRemoveAllRecentFiles)
        self.menuNew.addAction(self.actionNewEditor)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionNewFromTemplate)
        self.menuNew.addAction(self.actionNewProject)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuRecentFiles.menuAction())
        self.menuFile.addAction(self.actionImportProject)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionSaveAll)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionCloseAll)
        self.menuFile.addAction(self.actionCloseOthers)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSwitchProfile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.menuPanels.menuAction())
        self.menuNavigation.addAction(self.actionNextTab)
        self.menuNavigation.addAction(self.actionPreviousTab)
        self.menuNavigation.addAction(self.actionSelectTab)
        self.menuNavigation.addAction(self.actionJumpToTabWindow)
        self.menuNavigation.addSeparator()
        self.menuNavigation.addAction(self.actionLastEditLocation)
        self.menuNavigation.addAction(self.actionLocationBack)
        self.menuNavigation.addAction(self.actionLocationForward)
        self.menuHelp.addAction(self.actionReportBug)
        self.menuHelp.addAction(self.actionTranslatePrymatex)
        self.menuHelp.addAction(self.actionProjectHomepage)
        self.menuHelp.addAction(self.actionReadDocumentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionTakeScreenshot)
        self.menuHelp.addAction(self.actionAboutQt)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuBundleEditor.addAction(self.actionShowBundleEditor)
        self.menuBundleEditor.addSeparator()
        self.menuBundleEditor.addAction(self.actionEditCommands)
        self.menuBundleEditor.addAction(self.actionEditLanguages)
        self.menuBundleEditor.addAction(self.actionEditSnippets)
        self.menuBundleEditor.addSeparator()
        self.menuBundleEditor.addAction(self.actionReloadBundles)
        self.menuBundles.addAction(self.menuBundleEditor.menuAction())
        self.menuBundles.addSeparator()
        self.menuPreferences.addAction(self.actionShowMenus)
        self.menuPreferences.addAction(self.actionShowStatus)
        self.menuPreferences.addSeparator()
        self.menuPreferences.addAction(self.actionFullscreen)
        self.menuPreferences.addSeparator()
        self.menuPreferences.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuNavigation.menuAction())
        self.menubar.addAction(self.menuBundles.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRecentFiles.setTitle(QtGui.QApplication.translate("MainWindow", "&Recent Files", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNew.setTitle(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPanels.setTitle(QtGui.QApplication.translate("MainWindow", "Panels", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNavigation.setTitle(QtGui.QApplication.translate("MainWindow", "&Navigation", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBundles.setTitle(QtGui.QApplication.translate("MainWindow", "&Bundles", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBundleEditor.setTitle(QtGui.QApplication.translate("MainWindow", "Bundle &Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "&Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewEditor.setText(QtGui.QApplication.translate("MainWindow", "&Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewEditor.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAll.setText(QtGui.QApplication.translate("MainWindow", "Save All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAll.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseOthers.setText(QtGui.QApplication.translate("MainWindow", "Close Others", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseOthers.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("MainWindow", "&Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("MainWindow", "&Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setToolTip(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cu&t", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setToolTip(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setToolTip(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFullscreen.setText(QtGui.QApplication.translate("MainWindow", "Fullscreen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFullscreen.setShortcut(QtGui.QApplication.translate("MainWindow", "F11", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowMenus.setText(QtGui.QApplication.translate("MainWindow", "Show Menus", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowMenus.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+M", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNextTab.setText(QtGui.QApplication.translate("MainWindow", "N&ext Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNextTab.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+PgDown", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreviousTab.setText(QtGui.QApplication.translate("MainWindow", "P&revious Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreviousTab.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+PgUp", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReportBug.setText(QtGui.QApplication.translate("MainWindow", "Report &Bug", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTranslatePrymatex.setText(QtGui.QApplication.translate("MainWindow", "&Translate Prymatex", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProjectHomepage.setText(QtGui.QApplication.translate("MainWindow", "Project &Homepage", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTakeScreenshot.setText(QtGui.QApplication.translate("MainWindow", "Take &Screenshot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutQt.setText(QtGui.QApplication.translate("MainWindow", "About &Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFromTemplate.setText(QtGui.QApplication.translate("MainWindow", "From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFromTemplate.setToolTip(QtGui.QApplication.translate("MainWindow", "From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFromTemplate.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReadDocumentation.setText(QtGui.QApplication.translate("MainWindow", "Read &Documentation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseAll.setText(QtGui.QApplication.translate("MainWindow", "Close All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowStatus.setText(QtGui.QApplication.translate("MainWindow", "Show Status", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenAllRecentFiles.setText(QtGui.QApplication.translate("MainWindow", "Open All Recent Files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemoveAllRecentFiles.setText(QtGui.QApplication.translate("MainWindow", "Remove All Recent Files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowBundleEditor.setText(QtGui.QApplication.translate("MainWindow", "Show Bundle &Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowBundleEditor.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+Ctrl+Alt+B", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditCommands.setText(QtGui.QApplication.translate("MainWindow", "Edit &Commands", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditCommands.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+Ctrl+Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditLanguages.setText(QtGui.QApplication.translate("MainWindow", "Edit &Languages", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditLanguages.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+Ctrl+Alt+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditSnippets.setText(QtGui.QApplication.translate("MainWindow", "Edit &Snippets", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditSnippets.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+Ctrl+Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReloadBundles.setText(QtGui.QApplication.translate("MainWindow", "Reload &Bundles", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectTab.setText(QtGui.QApplication.translate("MainWindow", "&Select Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectTab.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewProject.setText(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewProject.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSwitchProfile.setText(QtGui.QApplication.translate("MainWindow", "Switch Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImportProject.setText(QtGui.QApplication.translate("MainWindow", "Import Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLastEditLocation.setText(QtGui.QApplication.translate("MainWindow", "Last Edit Location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLastEditLocation.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocationBack.setText(QtGui.QApplication.translate("MainWindow", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocationBack.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+Left", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocationForward.setText(QtGui.QApplication.translate("MainWindow", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocationForward.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+Right", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJumpToTabWindow.setText(QtGui.QApplication.translate("MainWindow", "Jump To Tab Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJumpToTabWindow.setShortcut(QtGui.QApplication.translate("MainWindow", "F12", None, QtGui.QApplication.UnicodeUTF8))

from prymatex.widgets.splitter import SplitTabWidget
