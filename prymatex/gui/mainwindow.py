#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import itertools
from string import Template

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from prymatex.ui.mainwindow import Ui_MainWindow
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.editor.codeedit import PMXCodeEditor
from prymatex.gui import utils


class PMXMainWindow(QtGui.QMainWindow, Ui_MainWindow, PMXObject):
    '''Prymatex main window'''
    ##########################################################
    # Signals
    ##########################################################
    newFileCreated = pyqtSignal(str)
    
    ##########################################################
    # Settings
    ##########################################################
    SETTINGS_GROUP = 'MainWindow'
    
    windowTitleTemplate = pmxConfigPorperty(default = "$PMX_APP_NAME")
    
    @pmxConfigPorperty(default = True)
    def showMenuBar(self, value):
        self._showMenuBar = value
        self.menuBar().setShown(value)
    
    # Constructor
    def __init__(self):
        '''
        The main window
        @param parent: The QObject parent, in this case it should be the QApp
        @param files_to_open: The set of files to be opened when the window
                              is shown in the screen.
        '''
        super(PMXMainWindow, self).__init__()
        
        # Initialize graphical elements
        self.setupUi(self)
        
        self.setupDockers()
        self.setupDialogs()
        self.setupMenu()
        self.setupStatusBar()
        
        self.addEditor(PMXCodeEditor(self))
        
        # Connect Signals
        self.splitTabWidget.tabWindowChanged.connect(self.setCurrentEditor)
        #self.statusbar.syntaxChanged.connect(self.setEditorSyntax)
        self.dialogNewFromTemplate.newFileCreated.connect(self.newFileFromTemplate)
        self.application.fileManager.fileHistoryChanged.connect(self._update_file_history)
        utils.centerWidget(self, scale = (0.9, 0.8))
        self.configure()
     
    def addEditor(self, editor):
        self.splitTabWidget.addTab(editor)
        self.setCurrentEditor(editor) 
    
    def setupStatusBar(self):
        from prymatex.gui.statusbar import PMXStatusBar
        self.setStatusBar(PMXStatusBar(self))
        self.statusBar().hide()
        
    def setupDockers(self):
        '''
        Basic panels, dock objects. More docks should be available via plugins
        '''
        from prymatex.gui.dockers.fstree import PMXFileSystemDock
        from prymatex.gui.dockers.project import PMXProjectDock
        from prymatex.gui.dockers.symbols import PMXSymboldListDock
        from prymatex.gui.dockers.browser import PMXBrowserDock
        from prymatex.gui.dockers.console import PMXConsoleDock
        from prymatex.gui.dockers.logger import QtLogHandler, PMXLoggerDock
        
        self.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        self.paneFileSystem = PMXFileSystemDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneFileSystem)
        self.menuPanels.addAction(self.paneFileSystem.toggleViewAction())
        self.paneFileSystem.hide()
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.menuPanels.addAction(self.paneProject.toggleViewAction())
        self.paneProject.hide()
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.menuPanels.addAction(self.paneSymbolList.toggleViewAction())
        self.paneSymbolList.hide()
        
        self.paneBrowser = PMXBrowserDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneBrowser)
        self.menuPanels.addAction(self.paneBrowser.toggleViewAction())
        self.paneBrowser.hide()
        
        self.paneConsole = PMXConsoleDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneConsole)
        self.menuPanels.addAction(self.paneConsole.toggleViewAction())
        self.paneConsole.hide()
        
        #Logging Sub-Window setup
        qthandler = QtLogHandler()
        self.logger.addHandler(qthandler)
        self.paneLogging = PMXLoggerDock(qthandler, self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneLogging)
        self.menuPanels.addAction(self.paneLogging.toggleViewAction())
        self.paneLogging.hide()
    
    def setupDialogs(self):
        from prymatex.gui.filterdlg import PMXFilterDialog
        from prymatex.gui.dialogs import PMXNewFromTemplateDialog
        from prymatex.gui.support.bundleselector import PMXBundleItemSelector
        
        # Create dialogs
        self.dialogNewFromTemplate = PMXNewFromTemplateDialog(self)
        self.dialogFilter = PMXFilterDialog(self)
        self.actionGroupTabs = PMXTabActionGroup(self) # Tab handling
        self.bundleItemSelector = PMXBundleItemSelector(self)
        
    def setupMenu(self):
        #Recent files
        self._update_file_history()
        
        #Bundles Menu
        name_order = lambda b1, b2: cmp(b1.name, b2.name)
        for bundle in sorted(self.application.supportManager.getAllBundles(), name_order):
            menu = self.application.supportManager.buildBundleMenu(bundle, self)
            if menu is not None:
                self.menuBundles.addMenu(menu)
        #Connect
        self.application.supportManager.bundleItemTriggered.connect(lambda item: self.currentEditor.insertBundleItem(item))

    def _update_file_history(self):
        menu = self.actionOpen_Recent.menu()
        if menu is None:
            menu = QtGui.QMenu(self)
            self.actionOpen_Recent.setMenu(menu)
        else:
            menu.clear()
        for file in self.application.fileManager.fileHistory:
            action = QtGui.QAction(file, self)
            receiver = lambda file = QtCore.QFile(file): self.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(action)
    #====================================================================
    # Bundle Items
    #====================================================================
    def setEditorSyntax(self, syntax):
        editor = self.currentEditor
        if editor is not None:
            editor.setSyntax(syntax)
    

    @QtCore.pyqtSlot()
    def on_actionSelect_Bundle_Item_triggered(self):
        editor = self.currentEditor
        scope = editor.getCurrentScope()
        items = self.application.supportManager.getActionItems(scope)
        item = self.bundleItemSelector.select(items)
        if item is not None:
            self.currentEditor.insertBundleItem(item)

    #===========================================================================
    # Auto Connects
    #===========================================================================    

    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        #self.application.getEditor()
        self.addEditor(PMXCodeEditor(self))
        
    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)


    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QApplication.quit()
    

    @QtCore.pyqtSlot()
    def on_actionNext_Tab_triggered(self):
        self.tabWidget.focusNextTab()
        

    @QtCore.pyqtSlot()
    def on_actionPrevious_Tab_triggered(self):
        self.tabWidget.focusPrevTab()

    @QtCore.pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, check):
        if not check and self.isFullScreen():
            self.showNormal()
        elif check:
            self.showFullScreen()
    
    @QtCore.pyqtSlot(bool)
    def on_actionShow_Menus_toggled(self, state):
        menubar = self.menuBar()
        if state:
            menubar.show()
        else:
            menubar.hide()
        
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        '''
        Opens one or more files
        '''
        #TODO: El directory puede ser dependiente del current editor o del file manager
        files = self.application.fileManager.getOpenFiles()
        for file in files:
            self.openFile(file)
        
    @QtCore.pyqtSlot()
    def on_actionShow_Bundle_Editor_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.exec_()

    def openFile(self, fileInfo):
        #self.application.getEditorForFile(file)
        editor = PMXCodeEditor(self)
        self.addEditor(editor)
        editor.open(fileInfo)

    def openUrl(self, url):
        if isinstance(url, (str, unicode)):
            url = QtCore.QUrl(url)
        source = url.queryItemValue('url')
        if source:
            source = QtCore.QUrl(source)
            editor = self.openFile(source.path())
            line = url.queryItemValue('line')
            if line:
                editor.codeEdit.goToLine(int(line))
            column = url.queryItemValue('column')
            if column:
                editor.codeEdit.goToColumn(int(column))
        
    @QtCore.pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        qApp.aboutQt()
    
        
    @QtCore.pyqtSlot()
    def on_actionAbout_this_application_triggered(self):
        QMessageBox.information(self, self.trUtf8("About Prymatex"), 
                                self.trUtf8("<h3>Prymatex</h3>"
                                "<p>A general purpouse Text Editor</p>")
                                )
        
    @QtCore.pyqtSlot()
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
        
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        fileInfo = self.currentEditor.fileInfo or self.application.fileManager.getSaveFile(title = "Save file")
        if fileInfo is not None:
            self.currentEditor.save(fileInfo)
        
    @QtCore.pyqtSlot()
    def on_actionSave_As_triggered(self):
        fileInfo = self.application.fileManager.getSaveFile(title = "Save file")
        if fileInfo is not None:
            self.currentEditor.save(fileInfo)
        
    @QtCore.pyqtSlot()
    def on_actionSaveAll_triggered(self):
        for i in range(0, self.tabWidgetEditors.count()):
            if not self.tabWidgetEditors.widget(i).reqquest_save():
                #self.statusBar().showMessage(self.trUtf8("Not all documents were saved"), 1000)
                break
        
    @QtCore.pyqtSlot()
    def on_actionTake_Screenshot_triggered(self):
        self.takeScreenShot()
    
    #TODO: use new stlye in signals and slots
    @pyqtSignature('takeScreenShot()')
    def takeScreenShot(self):
        pxm = QPixmap.grabWindow(self.winId())
        format = 'png'
        from datetime import datetime
        now = datetime.now()
        name = now.strftime('sshot-%Y-%m-%d-%H_%M_%S') + '.' + format
        pxm.save(name, format)
        #self.statusBar().showMessage("Screenshot saved as <a>%s</a>" % name)
        
    @QtCore.pyqtSlot()
    def on_actionZoom_In_triggered(self):
        self.currentEditorWidget.codeEdit.zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoom_Out_triggered(self):
        self.currentEditorWidget.codeEdit.zoomOut()
        
    @QtCore.pyqtSlot()
    def on_actionFilter_Through_Command_triggered(self):
        self.dialogFilter.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionClose_Others_triggered(self):
        count = self.tabWidgetEditors.count()
        index = self.tabWidgetEditors.currentIndex()
        widgets = []
        
        for i in range(0, index) + range(index+1, count):
            widgets.append(self.tabWidgetEditors.widget(i))
        for w in widgets:
            i = self.tabWidgetEditors.indexOf(w)
            if not self.tabWidgetEditors.closeTab(i):
                return
        
    @QtCore.pyqtSlot()     
    def on_actionMove_Tab_Left_triggered(self):
        self.tabWidget.moveTabLeft()
        
    @QtCore.pyqtSlot()
    def on_actionMove_Tab_Right_triggered(self):
        self.tabWidget.moveTabRight()
    
    #===========================================================================
    # Dumb code :/
    #===========================================================================
        
    @QtCore.pyqtSlot()
    def on_actionPreferences_triggered(self):
        self.application.configDialog.exec_()
    
        
    @QtCore.pyqtSlot()
    def on_actionPaste_As_New_triggered(self):
        text = qApp.instance().clipboard().text()
        if text:
            editor = self.addEmptyEditor()
            editor.appendPlainText(text)
        else:
            self.mainWindow.statusBar().showMessage(self.trUtf8("Nothing to paste."))
        
    @QtCore.pyqtSlot()
    def on_actionGo_To_Line_triggered(self):
        self.currentEditorWidget.goToLine()
        
    @QtCore.pyqtSlot()
    def on_actionGo_To_File_triggered(self):
        '''
        Triggers 
        '''
        self.tabWidget.chooseFileDlg.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        print "MainWindow::find"
        self.currentEditorWidget.showFindWidget()
        
    @QtCore.pyqtSlot()
    def on_actionFind_Replace_triggered(self):
        print "MainWindow::replace"
        self.currentEditorWidget.showReplaceWidget()
    
    def setCurrentEditor(self, editor):
        
        self.currentEditor = editor
        
        #Update status bar
        #self.statusBar().updateStatus(editorWidget.codeEdit.status)
        #self.statusBar().updateSyntax(editorWidget.codeEdit.syntax)
        
        #Update window title
        template = Template(self.windowTitleTemplate)
        
        self.setWindowTitle(template.safe_substitute(
            **editor.buildEnvironment(self.application.supportManager.buildEnvironment())
        ))
        self.currentEditor.setFocus(QtCore.Qt.MouseFocusReason)
    
    def closeEvent(self, event):
        #unsaved = self.tabWidget.unsavedCounter
        #if unsaved:
        #    close_msg = self.trUtf8("There are %s unsaved document in this window.<br>"
        #                            "Close anyway?")
        #    response = QMessageBox.question(self, self.trUtf8("Sure to close?"), 
        #                     unicode(close_msg) % unsaved, 
        #                     buttons=QMessageBox.Ok | QMessageBox.Cancel, 
        #                     defaultButton=QMessageBox.Ok)
        #    if response == QMessageBox.Cancel:
        #        event.ignore()
        
        event.accept()
        self.debug("Closing window")
        
    #===========================================================
    # Templates
    #===========================================================
    def newFileFromTemplate(self, path):
        self.openFile(path, auto_focus=True)
        
    @QtCore.pyqtSlot()
    def on_actionNew_from_template_triggered(self):
        self.dialogNewFromTemplate.exec_()
    
    #============================================================
    # Bookmarks
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToggle_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.toggleBookmark(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionNext_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.bookmarkNext(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionPrevious_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.bookmarkPrevious(editor.textCursor().block().blockNumber() + 1)
        
    @QtCore.pyqtSlot()
    def on_actionRemove_All_Bookmarks_triggered(self):
        editor = self.currentEditor
        editor.removeBookmarks()

class PMXTabActionGroup(QActionGroup):
    '''
    This calss stores some information realted
    '''
    def __init__(self, parent):
        QActionGroup.__init__(self, parent)
        self.menus = []
        # TODO: Translate this shorcuts, but not really nesseary, are they?
        self.shortcuts = [ QKeySequence("Alt+%s" % i)  for i in range(10) ]

    def addAction(self, action):
        QActionGroup.addAction(self, action)
        for m in self.menus:
            m.addAction(action)
        self.updateShortcuts()
       
    def updateShortcuts(self):
        for action, shortcut in itertools.izip(self.actions(), self.shortcuts):
            action.setShortcut(shortcut)

    def removeAction(self, action):
        QActionGroup.removeAction(self, action)
        for m in self.menus:
            m.removeAction(action)
        self.updateShortcuts()
        
    def addMenu(self, menu):
        if not menu in self.menus:
            self.menus.append(menu)
            for action in self.actions():
                menu.addAction(action)
