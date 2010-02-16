# encoding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.tabwidget import PMXTabWidget , PMWTabsMenu
from prymatex.gui.statusbar import PMXStatusBar
from prymatex.gui.panes.fspane import FSPane
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence
from prymatex.gui.mixins.common import CenterWidget
from prymatex.gui.editor import PMXTextEdit
from prymatex.config.configdialog import PMXConfigDialog
from prymatex.gui.panes.outputpanel import PMXOutputDock
from prymatex.gui.panes.project import PMXProjectDock
from prymatex.gui.panes.symbols import PMXSymboldListDock
from prymatex.gui.panes.bundles import PMXBundleEditorDock


class PMXMainWindow(QMainWindow, CenterWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))
        
        
        self.setup_panes()
        self.setup_menus()
        self.setup_actions()
        self.setup_gui()
        self.setup_toolbars()
        
        self.center()
        
        self.dialogConfig = PMXConfigDialog(self)
        
        QMetaObject.connectSlotsByName(self)
        
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        self.actionShowFSPane.setChecked(True)
        
    
    def setup_gui(self):
        self.tabWidgetEditors = PMXTabWidget(self)
        self.setCentralWidget(self.tabWidgetEditors)
        status_bar = PMXStatusBar(self)
        self.setStatusBar(status_bar)
        
    
    def setup_actions(self):
        
        #=======================================================================
        # File Menu
        #=======================================================================
        
        self.actionNewTab = QAction(_("New"), self)
        self.actionNewTab.setObjectName("actionNewTab")
        self.actionNewTab.setShortcut(text_to_KeySequence("Ctrl+N"))
        self.file_menu.addAction(self.actionNewTab)
        self.addAction(self.actionNewTab)
        
        self.actionFileOpen = QAction(_("&Open"), self)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.actionFileOpen.setShortcut(text_to_KeySequence("Ctrl+O"))
        self.file_menu.addAction(self.actionFileOpen)
        self.addAction(self.actionFileOpen)
        
        self.actionSave = QAction(_("&Save"), self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut(text_to_KeySequence("Ctrl+S"))
        self.file_menu.addAction(self.actionSave)
        self.addAction(self.actionSave)
        
        self.actionSaveAs = QAction(_("Save &As"), self)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionSaveAs.setShortcut(text_to_KeySequence("Ctrl+Shift+S"))
        self.file_menu.addAction(self.actionSaveAs)
        self.addAction(self.actionSaveAs)
        
        self.actionSaveAll = QAction(_("Save A&ll"), self)
        self.actionSaveAll.setObjectName("actionSaveAll")
        self.actionSaveAll.setShortcut(text_to_KeySequence("Ctrl+Alt+S"))
        self.file_menu.addAction(self.actionSaveAll)
        self.addAction(self.actionSaveAll)
        
        self.file_menu.addSeparator()
        
        self.actionReload = QAction(_("&Reload"), self)
        self.actionReload.setObjectName("actionReload")
        self.actionReload.setShortcut(text_to_KeySequence("F5"))
        self.file_menu.addAction(self.actionReload)
        self.addAction(self.actionReload)
        
        self.actionClose = QAction(_("&Close"), self)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.setShortcut(text_to_KeySequence("Ctrl+W"))
        self.file_menu.addAction(self.actionClose)
        self.addAction(self.actionClose)
        
        self.actionCloseOthers = QAction(_("Close &Others"), self)
        self.actionCloseOthers.setObjectName("actionCloseOthers")
        self.actionCloseOthers.setShortcut(text_to_KeySequence("Ctrl+Shift+W"))
        self.file_menu.addAction(self.actionCloseOthers)
        self.addAction(self.actionCloseOthers)
        
        self.file_menu.addSeparator()
        
        self.actionClose = QAction(_("&Quit"), self)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.setShortcut(text_to_KeySequence("Ctrl+Q"))
        self.file_menu.addAction(self.actionClose)
        self.addAction(self.actionClose)
        
        #=======================================================================
        # Edit Menu
        #=======================================================================
        
        self.actionUndo = QAction(_("Un&do"), self)
        self.actionUndo.setObjectName("actionUndo")
        self.actionUndo.setShortcut(text_to_KeySequence("Ctrl+Z"))
        self.edit_menu.addAction(self.actionUndo)
        self.addAction(self.actionUndo)
        
        self.actionRedo = QAction(_("&Redo"), self)
        self.actionRedo.setObjectName("actionRedo")
        self.actionRedo.setShortcut(text_to_KeySequence("Ctrl+Shift+Z"))
        self.edit_menu.addAction(self.actionRedo)
        self.addAction(self.actionRedo)
        
        self.edit_menu.addSeparator()
        
        self.actionCopy = QAction(_("&Copy"), self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCopy.setShortcut(text_to_KeySequence("Ctrl+C"))
        self.edit_menu.addAction(self.actionCopy)
        self.addAction(self.actionCopy)
        
        self.actionCut = QAction(_("C&ut"), self)
        self.actionCut.setObjectName("actionCut")
        self.actionCut.setShortcut(text_to_KeySequence("Ctrl+X"))
        self.edit_menu.addAction(self.actionCut)
        self.addAction(self.actionCut)
        
        self.actionPaste = QAction(_("&Paste"), self)
        self.actionPaste.setObjectName("actionPaste")
        self.actionPaste.setShortcut(text_to_KeySequence("Ctrl+V"))
        self.edit_menu.addAction(self.actionPaste)
        self.addAction(self.actionPaste)
        
        self.actionPasteAsNew = QAction(_("Paste As &New"), self)
        self.actionPasteAsNew.setObjectName("actionPasteAsNew")
        self.actionPasteAsNew.setShortcut("")
        self.edit_menu.addAction(self.actionPasteAsNew)
        self.addAction(self.actionPasteAsNew)
        
        self.edit_menu.addSeparator()
        
        self.actionFind = QAction(_("&Find"), self)
        self.actionFind.setObjectName("actionFind")
        self.actionFind.setShortcut(text_to_KeySequence("Ctrl+F"))
        self.edit_menu.addAction(self.actionFind)
        self.addAction(self.actionFind)
        
        
        self.actionFindReplace = QAction(_("Find/&Replace"), self)
        self.actionFindReplace.setObjectName("actionFindReplace")
        self.actionFindReplace.setShortcut(text_to_KeySequence("Ctrl+R"))
        self.edit_menu.addAction(self.actionFindReplace)
        self.addAction(self.actionFindReplace)
        
        
        self.actionPreferences = QAction(_("&Preferences"), self)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionPreferences.setShortcut(text_to_KeySequence("Ctrl+Shift+P"))
        self.edit_menu.addAction(self.actionPreferences)
        self.addAction(self.actionPreferences)
        
        
        
        #=======================================================================
        # View Menu
        #=======================================================================
        
        self.actionFullScreen = QAction(_("&Full Screen"), self)
        self.actionFullScreen.setObjectName("actionFullScreen")
        self.actionFullScreen.setShortcut(text_to_KeySequence("F11"))
        self.actionFullScreen.setCheckable(True)
        self.view_menu.addAction(self.actionFullScreen)
        self.addAction(self.actionFullScreen)
        
        self.actionShowMenus = QAction(_("&Show Menus"), self)
        self.actionShowMenus.setObjectName("actionShowMenus")
        self.actionShowMenus.setShortcut(text_to_KeySequence("Ctrl+M"))
        self.actionShowMenus.setCheckable(True)
        self.actionShowMenus.setChecked(True)
        self.view_menu.addAction(self.actionShowMenus)
        self.addAction(self.actionShowMenus)
        
        self.view_menu.addSeparator()
        
        self.actionZoomIn = QAction(_("Zoom &In"), self)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomIn.setShortcut(text_to_KeySequence("Ctrl+Plus"))
        self.view_menu.addAction(self.actionZoomIn)
        self.addAction(self.actionZoomIn)
        
        self.actionZoomOut = QAction(_("Zoom &Out"), self)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionZoomOut.setShortcut(text_to_KeySequence("Ctrl+Minus"))
        self.view_menu.addAction(self.actionZoomOut)
        self.addAction(self.actionZoomOut)
        
        self.view_menu.addSeparator()
        
        self.actionFocusEditor = QAction(_("Focus &Editor"), self)
        self.actionFocusEditor.setObjectName("actionFocusEditor")
        self.actionFocusEditor.setShortcut(text_to_KeySequence("F12"))
        self.view_menu.addAction(self.actionFocusEditor)
        self.addAction(self.actionFocusEditor)
        
        self.actionShowLineNumbers = QAction(_("Show Line &Numbers"), self)
        self.actionShowLineNumbers.setObjectName("actionShowLineNumbers")
        self.actionShowLineNumbers.setShortcut(text_to_KeySequence("F10"))
        self.actionShowLineNumbers.setCheckable(True)
        self.view_menu.addAction(self.actionShowLineNumbers)
        self.addAction(self.actionShowLineNumbers)
        
        self.view_menu.addSeparator()
        
        self.actionShowFSPane = PMXDockAction(_("Show File System Panel"),
                                              _("Hide File System Panel"),
                                              self.paneFileSystem, self)
        self.actionShowFSPane.setObjectName("actionShowFSPane")
        self.actionShowFSPane.setShortcut(text_to_KeySequence("F8"))
        self.view_menu.addAction(self.actionShowFSPane)
        self.addAction(self.actionShowFSPane)
        
        self.actionShowOutputPane = PMXDockAction(_("Show Output Panel"),
                                                  _("Hide Output Panel"),
                                                  self.paneOutput, self)
        self.actionShowOutputPane.setObjectName("actionShowOutputPane")
        self.actionShowOutputPane.setShortcut(text_to_KeySequence("F7"))
        self.view_menu.addAction(self.actionShowOutputPane)
        self.addAction(self.actionShowOutputPane)
        
        self.actionShowProjectPanel = PMXDockAction(_("Show Project Panel"),
                                                    _("Hide Project Panel"), 
                                                    self.paneProject, self)
        self.actionShowProjectPanel.setObjectName("actionShowProjectPanel")
        self.actionShowProjectPanel.setShortcut(text_to_KeySequence("F9"))
        self.view_menu.addAction(self.actionShowProjectPanel)
        self.addAction(self.actionShowProjectPanel)
        
        self.actionShowSymbolListPane = PMXDockAction(_("Show Symbol List Panel"),
                                                _("Hide Symbol List Panel"), 
                                                self.paneSymbolList, self)
        self.actionShowSymbolListPane.setObjectName("actionShowSymbolListPane")
        self.actionShowSymbolListPane.setShortcut(text_to_KeySequence("F6"))
        self.view_menu.addAction(self.actionShowSymbolListPane)
        self.addAction(self.actionShowSymbolListPane)
        
        self.view_menu.addSeparator()
        self.actionShowCurrentScope = QAction(_("Show current scope"), self)
        self.actionShowCurrentScope.setObjectName("actionShowCurrentScope")
        self.actionShowCurrentScope.setShortcut(text_to_KeySequence("Alt+S"))
        self.view_menu.addAction(self.actionShowCurrentScope)
        #self.addAction(self.actionShowCurrentScope)
         
        #=======================================================================
        # Navigation Menu
        #=======================================================================
        
        # Bookmarks
        self.actionToogleBookmark = QAction(_("Toggle &Bookmark"), self)
        self.actionToogleBookmark.setObjectName("actionToogleBookmark")
        self.actionToogleBookmark.setShortcut(text_to_KeySequence("Ctrl+B"))
        self.menuNavigation.addAction(self.actionToogleBookmark)
        
        self.actionGoToNextBookmark = QAction(_("&Next Bookmark"), self)
        self.actionGoToNextBookmark.setObjectName("actionGoToNextBookmark")
        self.actionGoToNextBookmark.setShortcut(text_to_KeySequence("F2"))
        self.menuNavigation.addAction(self.actionGoToNextBookmark)
        
        self.actionGoToPreviousBookmark = QAction(_("&Previous Bookmark"), self)
        self.actionGoToPreviousBookmark.setObjectName("actionGoToPreviousBookmark")
        self.actionGoToPreviousBookmark.setShortcut(text_to_KeySequence("Ctrl+F2"))
        self.menuNavigation.addAction(self.actionGoToPreviousBookmark)
        
        self.actionRemoveAllBookmarks = QAction(_("&Remove All Bookmarks"), self)
        self.actionRemoveAllBookmarks.setObjectName("actionRemoveAllBookmarks")
        self.actionRemoveAllBookmarks.setShortcut(text_to_KeySequence("Ctrl+Shift+F2"))
        self.menuNavigation.addAction(self.actionRemoveAllBookmarks)
        
        
        self.menuNavigation.addSeparator()
        
        self.actionNexTab = QAction(_("&Next Tab"), self)
        self.actionNexTab.setObjectName("actionNexTab")
        self.actionNexTab.setShortcut(text_to_KeySequence("Ctrl+PageDown"))
        self.menuNavigation.addAction(self.actionNexTab)
        self.addAction(self.actionNexTab)
        
        self.actionPreviousTab = QAction(_("&Previous Tab"), self)
        self.actionPreviousTab.setObjectName("actionPreviousTab")
        self.actionPreviousTab.setShortcut(text_to_KeySequence("Ctrl+PageUp"))
        self.menuNavigation.addAction(self.actionPreviousTab)
        self.addAction(self.actionPreviousTab)
        
        self.actionMoveTabLeft = QAction(_("Move Tab &Left"), self)
        self.actionMoveTabLeft.setObjectName("actionMoveTabLeft")
        self.actionMoveTabLeft.setShortcut(text_to_KeySequence("Ctrl+Shift+PageUp"))
        self.menuNavigation.addAction(self.actionMoveTabLeft)
        self.addAction(self.actionMoveTabLeft)
        
        self.actionMoveTabRight = QAction(_("Move Tab &Right"), self)
        self.actionMoveTabRight.setObjectName("actionMoveTabRight")
        self.actionMoveTabRight.setShortcut(text_to_KeySequence("Ctrl+Shift+PageDown"))
        self.menuNavigation.addAction(self.actionMoveTabRight)
        self.addAction(self.actionMoveTabRight)
        
        self.menuNavigation.addSeparator()
        
        self.menuPanes = PMWTabsMenu(_("Panes"), self) 
        self.menuNavigation.addMenu(self.menuPanes)
        
        self.menuNavigation.addSeparator()
        # Gotos
        
        self.actionGoHeaderSource = QAction(_("Go to &Header/Source"), self)
        self.actionGoHeaderSource.setObjectName("actionGoHeaderSource")
        self.actionGoHeaderSource.setShortcut(text_to_KeySequence("Ctrl+F3"))
        self.menuNavigation.addAction(self.actionGoHeaderSource)
        self.addAction(self.actionGoHeaderSource)
        
        self.actionGoToFile = QAction(_("Go to &File"), self)
        self.actionGoToFile.setObjectName("actionGoToFile")
        #self.actionGoToFile.setShortcut("")
        self.menuNavigation.addAction(self.actionGoToFile)
        self.addAction(self.actionGoToFile)
        
        self.actionGoToSymbol = QAction(_("Go to &Symbol"), self)
        self.actionGoToSymbol.setObjectName("actionGoToSymbol")
        self.actionGoToSymbol.setShortcut(text_to_KeySequence("Ctrl+Shift+G"))
        self.menuNavigation.addAction(self.actionGoToSymbol)
        self.addAction(self.actionGoToSymbol)
        
        self.actionGoToMatchingBracket = QAction(_("Go to Matching &Bracket"), self)
        self.actionGoToMatchingBracket.setObjectName("actionGoToMatchingBracket")
        self.actionGoToMatchingBracket.setShortcut(text_to_KeySequence("Ctrl+B"))
        self.menuNavigation.addAction(self.actionGoToMatchingBracket)
        self.addAction(self.actionGoToMatchingBracket)
        
        self.actionGoToLine = QAction(_("Go To Line"), self)
        self.actionGoToLine.setObjectName("actionGoToLine")
        self.actionGoToLine.setShortcut(text_to_KeySequence("Ctrl+G"))
        self.menuNavigation.addAction(self.actionGoToLine)
        self.addAction(self.actionGoToLine)
        
                
        #=======================================================================
        # Run Script
        #=======================================================================
        
        self.actionRunScript = QAction(_("Run Script"), self)
        self.actionRunScript.setObjectName("actionRunScript")
        self.actionRunScript.setShortcut(text_to_KeySequence("Alt+R"))
        self.tools_menu.addAction(self.actionRunScript)
        self.addAction(self.actionRunScript)
        
        self.actionOpenCommandPrompt = QAction(_("Open Terminal"), self)
        self.actionOpenCommandPrompt.setObjectName("actionOpenCommandPrompt")
        self.actionOpenCommandPrompt.setShortcut(text_to_KeySequence("F4"))
        self.tools_menu.addAction(self.actionOpenCommandPrompt)
        
        self.actionOpenFileManager = QAction(_("Open File Manager"), self)
        self.actionOpenFileManager.setObjectName("actionOpenFileManager")
        self.actionOpenFileManager.setShortcut(text_to_KeySequence("F6"))
        self.tools_menu.addAction(self.actionOpenFileManager)
        
        
        #=======================================================================
        # Help Menu
        #=======================================================================
        app_name = qApp.instance().applicationName()
        
        self.actionReportBug = QAction(_("Report &Bug"), self)
        self.actionReportBug.setObjectName("actionReportBug")
        #self.actionReportBug.setShortcut(text_to_KeySequence(""))
        self.help_menu.addAction(self.actionReportBug)
        self.addAction(self.actionReportBug)
        
        
        self.actionTranslateApp = QAction(_("Translate %s", app_name), self)
        self.actionTranslateApp.setObjectName("actionTranslateApp")
        #self.actionTranslateApp.setShortcut(text_to_KeySequence(""))
        self.help_menu.addAction(self.actionTranslateApp)
        self.addAction(self.actionTranslateApp)
        
        self.actionProjectHomePage = QAction(_("Project &Homepage"), self)
        self.actionProjectHomePage.setObjectName("actionProjectHomePage")
        #self.actionProjectHomePage.setShortcut("")
        self.help_menu.addAction(self.actionProjectHomePage)
        self.addAction(self.actionProjectHomePage)
        
        self.actionTakeScreenshot = QAction(_("&Take Screenshot"), self)
        self.actionTakeScreenshot.setObjectName("actionTakeScreenshot")
        self.actionTakeScreenshot.setShortcut(text_to_KeySequence("Ctrl+Print"))
        self.help_menu.addAction(self.actionTakeScreenshot)
        self.addAction(self.actionTakeScreenshot)
        
        self.help_menu.addSeparator()
        self.actionAboutQt = QAction(_("About &Qt"), self)
        self.actionAboutQt.setObjectName("actionAboutQt")
        #self.actionAboutQt.setShortcut("")
        self.help_menu.addAction(self.actionAboutQt)
        self.addAction(self.actionAboutQt)
        
        self.actionAboutApp = QAction(_("&About %s", app_name), self)
        self.actionAboutApp.setObjectName("actionAboutApp")
        #self.actionAboutApp.setShortcut()
        self.help_menu.addAction(self.actionAboutApp)
        self.addAction(self.actionAboutApp)
        
        #=======================================================================
        # Bundles menus
        #=======================================================================
        
        self.actionBundleEditor = PMXDockAction(_("Show &Bundle Editor"),
                                                _("Hide &Bundle Editor"),
                                                  self.paneBundleEditor, 
                                                  self)
        self.actionBundleEditor.setObjectName("actionBundleEditor")
        self.actionBundleEditor.setShortcut(text_to_KeySequence("Ctrl+Shift+B"))
        self.bundle_menu.addAction(self.actionBundleEditor)
        self.addAction(self.actionBundleEditor)
        
        
        
        self.actionActivateBundle = QAction(_("Select Bundle Item..."), self)
        self.actionActivateBundle.setObjectName("actionActivateBundle")
        self.actionActivateBundle.setShortcut(text_to_KeySequence("Ctrl+Alt+T"))
        self.bundle_menu.addAction(self.actionActivateBundle)
        
        #=======================================================================
        # Configuración 
        #=======================================================================
        
        
        self.menuConvertCase = QMenu(_("&Convert"), self)
        self.menuText.addMenu(self.menuConvertCase)
        
        self.actionConvertUpercase = QAction(_("to Uppercase"), self)
        self.actionConvertUpercase.setObjectName("actionConvertUpercase")
        #self.actionConvertUpercase.setShortcut("")
        self.menuConvertCase.addAction(self.actionConvertUpercase)
        self.addAction(self.actionConvertUpercase)
        
        self.actionConvertLowercase = QAction(_("to &Lowercase"), self)
        self.actionConvertLowercase.setObjectName("actionConvertLowercase")
        #self.actionConvertLowercase.setShortcut("")
        self.menuConvertCase.addAction(self.actionConvertLowercase)
        self.addAction(self.actionConvertLowercase)
        
        self.actionConvertTitleCase = QAction(_("to &Titlecase"), self)
        self.actionConvertTitleCase.setObjectName("actionConvertTitleCase")
        #self.actionConvertTitleCase.setShortcut("")
        self.menuConvertCase.addAction(self.actionConvertTitleCase)
        self.addAction(self.actionConvertTitleCase)
        
        self.actionConvertInvertCase = QAction(_("to Invert case"), self)
        self.actionConvertInvertCase.setObjectName("actionConvertInvertCase")
        #self.actionConvertInvertCase.setShortcut("")
        self.menuConvertCase.addAction(self.actionConvertInvertCase)
        self.addAction(self.actionConvertInvertCase)
        
        self.actionConvertTranspose = QAction(_("Transpose"), self)
        self.actionConvertTranspose.setObjectName("actionConvertTranspose")
        #self.actionConvertTranspose.setShortcut("")
        self.menuConvertCase.addAction(self.actionConvertTranspose)
        self.addAction(self.actionConvertTranspose)
        
        self.menuText.addSeparator()
        
        self.actionShiftLeft = QAction(_("Shift Left"), self)
        self.actionShiftLeft.setObjectName("actionShiftLeft")
        #self.actionShiftLeft.setShortcut("")
        self.menuText.addAction(self.actionShiftLeft)
        self.addAction(self.actionShiftLeft)
        
        self.actionShiftRight = QAction(_("Shift Right"), self)
        self.actionShiftRight.setObjectName("actionShiftRight")
        #self.actionShiftRight.setShortcut("")
        self.menuText.addAction(self.actionShiftRight)
        self.addAction(self.actionShiftRight)
        
        self.menuText.addSeparator()
        
        self.actionTabToSpaces = QAction(_("Tab to spaces"), self)
        self.actionTabToSpaces.setObjectName("actionTabToSpaces")
        #self.actionTabToSpaces.setShortcut("")
        self.menuText.addAction(self.actionTabToSpaces)
        self.addAction(self.actionTabToSpaces)
        
        self.actionSpacesToTabs = QAction(_("Spaces to tabs"), self)
        self.actionSpacesToTabs.setObjectName("actionSpacesToTabs")
        #self.actionSpacesToTabs.setShortcut("")
        self.menuText.addAction(self.actionSpacesToTabs)
        self.addAction(self.actionSpacesToTabs)
        
        self.menuText.addSeparator()
        
        self.actionFilterThroughCommand = QAction(_("Filter through command"), self)
        self.actionFilterThroughCommand.setObjectName("actionFilterThroughCommand")
        #self.actionFilterThroughCommand.setShortcut("")
        self.menuText.addAction(self.actionFilterThroughCommand)
        self.addAction(self.actionFilterThroughCommand)
        
        self.actionRunSelection = QAction(_("Run Selection"), self)
        self.actionRunSelection.setObjectName("actionRunSelection")
        #self.actionRunSelection.setShortcut("")
        self.menuText.addAction(self.actionRunSelection)
        self.addAction(self.actionRunSelection)
    
    def setup_menus(self):
        
        menubar = QMenuBar(self)
        
        self.file_menu = QMenu(_("&File"), self)
        menubar.addMenu(self.file_menu)
        
        self.edit_menu = QMenu(_("&Edit"), self)
        menubar.addMenu(self.edit_menu)
        
        self.view_menu = QMenu(_("&View"), self)
        menubar.addMenu(self.view_menu)
        
        self.menuText = QMenu(_("&Text"), self)
        menubar.addMenu(self.menuText)
        
        self.tools_menu = QMenu(_("&Tools"), self)
        menubar.addMenu(self.tools_menu)
        
        self.menuNavigation = QMenu(_("&Navigation"), self)
        menubar.addMenu(self.menuNavigation)
        
        self.bundle_menu = QMenu(_("&Bundle"), self)
        menubar.addMenu(self.bundle_menu)
        
        self.help_menu = QMenu(_("&Help"), self)
        menubar.addMenu(self.help_menu)
        
        self.setMenuBar(menubar)
    
    def setup_panes(self):
        
        self.paneFileSystem = FSPane(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.paneFileSystem)
        self.paneFileSystem.hide()
        
        self.paneOutput = PMXOutputDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneOutput)
        self.paneOutput.hide()
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.paneProject.hide()
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.paneSymbolList.hide()
        
        self.paneBundleEditor = PMXBundleEditorDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneBundleEditor)
        self.paneBundleEditor.hide()
        
    
    def setup_toolbars(self):
        #raise NotImplementedError("Do we need them?")
        pass
    
        
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    counter = 0
    
    @pyqtSignature('')
    def on_actionNewTab_triggered(self):
        #self.tabWidgetEditors.addTab(QTextEdit(), "New Tab %d" % self.counter)
        #self.counter += 1
        self.tabWidgetEditors.appendEmptyTab()
    
    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.tabWidgetEditors.currentIndex()
        self.tabWidgetEditors.closeTab(index)
        if self.tabWidgetEditors.count():
            self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNextTab_triggered(self):
        
        curr = self.tabWidgetEditors.currentIndex()
        count = self.tabWidgetEditors.count()
        
        if curr < count -1:
            prox = curr +1
        else:
            prox = 0
        self.tabWidgetEditors.setCurrentIndex(prox)
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
    @pyqtSignature('')
    def on_actionPreviousTab_triggered(self):
        curr = self.tabWidgetEditors.currentIndex()
        count = self.tabWidgetEditors.count()
        
        if curr > 0:
            prox = curr -1
        else:
            prox = count -1
        self.tabWidgetEditors.setCurrentIndex(prox)
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
    @pyqtSignature('')
    def on_actionAboutApp_triggered(self):
        QMessageBox.about(self, _("About"), _("""
        <h3>Prymatex Text Editor</h3>
        <p>(c) 2010 Xurix</p>
        <p><h4>Authors:</h4>
        <ul>
            <li>D3f0</li>
            <li>diegomvh</li>
            <li>locurask</li>
        </ul>
        <a href="">Homepage</a>
        <p>Version %s</p>
        </p>
        """, qApp.instance().applicationVersion()))
        
    @pyqtSignature('')
    def on_actionFullScreen_triggered(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    
    #@pyqtSignature('toggled(bool)')
    def on_actionShowMenus_toggled(self, state):
        print "Toggle", state
        menubar = self.menuBar()
        if state:
            menubar.show()
        else:
            menubar.hide()
        
            
    @pyqtSignature('')
    def on_actionFileOpen_triggered(self):
        fs = QFileDialog.getOpenFileNames()
        if not fs:
            return
        for path in fs:
            self.tabWidgetEditors.openLocalFile(path)
    
    @pyqtSignature('')
    def on_actionAboutQt_triggered(self):
        qApp.aboutQt()
    
    @pyqtSignature('')
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
    
    @property
    def current_editor(self):
        editor = self.tabWidgetEditors.currentWidget()
        if isinstance(editor, PMXTextEdit):
            return editor
        
    @pyqtSignature('')
    def on_actionSave_triggered(self):
        self.current_editor.save()
    
    @pyqtSignature('')
    def on_actionSaveAs_triggered(self):
        self.current_editor.save(save_as = True)
        
    @pyqtSignature('')
    def on_actionSaveAll_triggered(self):
        for i in range(0, self.tabWidgetEditors.count()):
            if not self.tabWidgetEditors.widget(i).save():
                self.statusBar().showMessage(_("Not all documents were saved"), 1000)
                break
    
    @pyqtSignature('')
    def on_actionTakeScreenshot_triggered(self):
        QTimer.singleShot(1000, self, SLOT('takeScreenShot()'))
        
    @pyqtSignature('takeScreenShot()')
    def takeScreenShot(self):
        pxm = QPixmap.grabWindow(self.winId())
        format = 'png'
        from datetime import datetime
        now = datetime.now()
        name = now.strftime('sshot-%Y-%m-%d-%H_%M_%S') + '.' + format
        pxm.save(name, format)
        self.statusBar().showMessage("Screenshot saved as %s" % name)
        
    @pyqtSignature('')
    def on_actionZoomIn_triggered(self):
        self.tabWidgetEditors.currentWidget().zoomIn()
    
    @pyqtSignature('')
    def on_actionZoomOut_triggered(self):
        self.tabWidgetEditors.currentWidget().zoomOut()
    
    @pyqtSignature('')
    def on_actionFocusEditor_triggered(self):
        # Siempre debería haber una ventana de edición
        try:
            self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        except Exception:
            pass
    
    
    @pyqtSignature('')
    def on_actionCloseOthers_triggered(self):
        count = self.tabWidgetEditors.count()
        index = self.tabWidgetEditors.currentIndex()
        widgets = []
        
        for i in range(0, index) + range(index+1, count):
            widgets.append(self.tabWidgetEditors.widget(i))
        for w in widgets:
            i = self.tabWidgetEditors.indexOf(w)
            if not self.tabWidgetEditors.closeTab(i):
                return
            
#                return
#        for i in range(index+1, count):
#            if not self.tabWidgetEditors.closeTab(i):
#                return
    @pyqtSignature('')
    def on_actionMoveTabLeft_triggered(self):
        if self.tabWidgetEditors.count() == 1:
            return
        count = self.tabWidgetEditors.count()
        index = self.tabWidgetEditors.currentIndex()
        text = self.tabWidgetEditors.tabText(index)       
        widget = self.tabWidgetEditors.currentWidget()
        self.tabWidgetEditors.removeTab(index)
        index -= 1
        if index < 0:
            index = count
        self.tabWidgetEditors.insertTab(index, widget, text)
        self.tabWidgetEditors.setCurrentWidget(widget)
    
    @pyqtSignature('')    
    def on_actionMoveTabRight_triggered(self):
        if self.tabWidgetEditors.count() == 1:
            return
        count = self.tabWidgetEditors.count()
        index = self.tabWidgetEditors.currentIndex()
        text = self.tabWidgetEditors.tabText(index)       
        widget = self.tabWidgetEditors.currentWidget()
        self.tabWidgetEditors.removeTab(index)
        index += 1
        if index >= count:
            index = 0
        self.tabWidgetEditors.insertTab(index, widget, text)
        self.tabWidgetEditors.setCurrentWidget(widget)
    
    #===========================================================================
    # Dumb code :/
    #===========================================================================
    
    @pyqtSignature('')
    def on_actionPreferences_triggered(self):
        self.dialogConfig.exec_()
    
    def notifyCursorChange(self, editor, row, col):
        ''' Called by editors '''
        if editor == self.tabWidgetEditors.currentWidget():
            self.statusBar().updateCursorPos(col, row)
        
    def on_actionShowLineNumbers_toggled(self, check):
        print "Line", check
    

    @pyqtSignature('')
    def on_actionGoToLine_triggered(self):
        
        editor = self.tabWidgetEditors.currentWidget()
        editor.showGoToLineDialog()
        
    @pyqtSignature('')
    def on_actionShowCurrentScope_triggered(self):
        scope = self.tabWidgetEditors.currentWidget().getCurrentScope()
        self.statusBar().showMessage(scope)
        

class PMXDockAction(QAction):
    '''
    Hides or shows a dock wheater the action is activated or deactivated
    respectively.
    '''
    def __init__(self, text_show, text_hide, dock, parent):
        '''
        @param text_show: Text to show when the dock is hidden
        @param text_hide: Text to show when the dock is shown
        @param dock: Dock widget
        @param parent: Parent QObject
        '''
        text = dock.isHidden() and text_show or text_hide
        QAction.__init__(self, text, parent)
        self.setCheckable(True)
        self.connect(self, SIGNAL("toggled(bool)"), self.toggleDock)
        
        self.connect(dock, SIGNAL("widgetShown(bool)"), self.checkCrossButtonHide)
        
        self.dock = dock
        self.text_show, self.text_hide = text_show, text_hide
    
    def toggleDock(self, check):
        if check:
            if self.dock.isHidden():
                self.dock.show()
            self.setText(self.text_hide)
        else:
            if not self.dock.isHidden():
                self.dock.hide()
            self.setText(self.text_show)
    
    def checkCrossButtonHide(self, dockShown):
        if not dockShown:
            if self.isChecked():
                self.setChecked(False)
