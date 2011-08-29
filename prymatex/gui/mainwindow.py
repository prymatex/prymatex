#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import itertools
from string import Template

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from prymatex.ui.mainwindow import Ui_MainWindow

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.editor.codeedit import PMXCodeEdit
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence
from prymatex.gui.editor.editorwidget import PMXEditorWidget
from prymatex.core.exceptions import FileDoesNotExistError
from prymatex.core.base import PMXWidget
from prymatex.core.config import pmxConfigPorperty
from prymatex.core.exceptions import FileNotSupported

class PMXMainWindow(QtGui.QMainWindow, Ui_MainWindow, PMXWidget):
    '''
    Prymatex main window, it holds a currentEditor property which
    grants access to the focused editor.
    '''
    newFileCreated = pyqtSignal(str)
    
    class Meta:
        settings = 'MainWindow'
    
    # Settings
    windowTitleTemplate = pmxConfigPorperty(default = "$APPNAME")
    
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
        
        self.addEmptyEditor()
        
        # Connect Signals
        self.splitTabWidget.tabWindowChanged.connect(self.setCurrentEditor)
        self.statusbar.syntaxChanged.connect(self.setEditorSyntax)
        self.dialogNewFromTemplate.newFileCreated.connect(self.newFileFromTemplate)
        self.pmxApp.fileManager.fileHistoryChanged.connect(self._update_file_history)
        
        self.configure()
        self.center()
    
    #Deprecate tabWidget
    @property
    def tabWidget(self):
        return self.splitTabWidget
    
    #TODO: Crear un methodo para instanciar editor widgets y agregarlos a una lista de editores activos
    def addEmptyEditor(self):
        empty_file = self.pmxApp.fileManager.getEmptyFile()
        editorWidget = PMXEditorWidget(empty_file, parent = self)
        self.tabWidget.addTab(editorWidget, empty_file.fileName())
        self.currentEditorWidget = editorWidget
        
    def setupDockers(self):
        '''
        Basic panels, dock objects. More docks should be available via plugins
        '''
        from prymatex.gui.dockers.fstree import PMXFSPaneDock
        from prymatex.gui.dockers.project import PMXProjectDock
        from prymatex.gui.dockers.symbols import PMXSymboldListDock
        from prymatex.gui.dockers.browser import PMXBrowserPaneDock
        from prymatex.gui.dockers.console import PMXConsoleDock
        from prymatex.gui.logwidget import QtLogHandler, LogDockWidget
        
        self.paneFileSystem = PMXFSPaneDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneFileSystem)    
        self.paneFileSystem.associateAction(self.actionShow_File_System_Pane,
                                            self.trUtf8("Show Filesystem Panel"),
                                            self.trUtf8("Hide Filesystem Panel"))
        self.paneFileSystem.hide()
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.paneProject.hide()
        self.paneProject.associateAction(self.actionShow_Project_Dock,
                                         self.trUtf8("Show Project"),
                                         self.trUtf8("Hide Project"))
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.paneSymbolList.hide()
        
        self.paneBrowser = PMXBrowserPaneDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneBrowser)
        self.paneBrowser.hide()
        self.paneBrowser.associateAction(self.actionShow_Browser_Dock,
                                         self.trUtf8("Show Browser"),
                                         self.trUtf8("Hide Browser"))
        
        self.paneConsole = PMXConsoleDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneConsole)
        self.paneConsole.hide()
        self.paneConsole.associateAction(self.actionShow_Terminal_Dock,
                                         self.trUtf8("Show Terminal"),
                                         self.trUtf8("Hide Terminal"))
        
        #Logging Sub-Window setup
        qthandler = QtLogHandler()
        self.logger.addHandler(qthandler)
        self.paneLogging = LogDockWidget(qthandler, self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneLogging)
        self.paneLogging.action = self.actionShow_Log_Window
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
        for bundle in sorted(self.pmxApp.supportManager.getAllBundles(), name_order):
            menu = self.pmxApp.supportManager.buildBundleMenu(bundle, self)
            if menu is not None:
                self.menuBundles.addMenu(menu)
        #Connect
        self.pmxApp.supportManager.bundleItemTriggered.connect(lambda item: self.currentEditor.insertBundleItem(item))

    def _update_file_history(self):
        menu = self.actionOpen_Recent.menu()
        if menu is None:
            menu = QtGui.QMenu(self)
            self.actionOpen_Recent.setMenu(menu)
        for file in self.pmxApp.fileManager.fileHistory:
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
    
    @pyqtSignature('')
    def on_actionSelect_Bundle_Item_triggered(self):
        editor = self.currentEditor
        scope = editor.getCurrentScope()
        items = self.pmxApp.supportManager.getActionItems(scope)
        item = self.bundleItemSelector.select(items)
        if item is not None:
            self.currentEditor.insertBundleItem(item)

    #===========================================================================
    # Shortcuts
    #===========================================================================
    @property
    def currentEditor(self):
        widget = self.currentEditorWidget
        if widget != None:
            return widget.codeEdit

    #===========================================================================
    # Auto Connects
    #===========================================================================    
    @pyqtSignature('')
    def on_actionNew_triggered(self):
        self.addEmptyEditor()

    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    @pyqtSignature('')    
    def on_actionNext_Tab_triggered(self):
        self.tabWidget.focusNextTab()
        
    @pyqtSignature('')
    def on_actionPrevious_Tab_triggered(self):
        self.tabWidget.focusPrevTab()
        
    @pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, check):
        if not check and self.isFullScreen():
            self.showNormal()
        elif check:
            self.showFullScreen()
    
    @pyqtSlot(bool)
    def on_actionShow_Menus_toggled(self, state):
        menubar = self.menuBar()
        if state:
            menubar.show()
        else:
            menubar.hide()
        
    @pyqtSignature('')
    def on_actionOpen_triggered(self):
        '''
        Opens one or more files
        '''
        #TODO: El directory puede ser dependiente del current editor o del file manager
        files = self.pmxApp.fileManager.getOpenFiles()
        focus = len(files) == 1
        for file in files:
            self.openFile(file, focus)
    
    @pyqtSignature('')
    def on_actionShow_Bundle_Editor_triggered(self):
        #TODO: mejorar esto
        self.pmxApp.bundleEditor.exec_()

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
            
    def openFile(self, file, focus = False):
        '''
        Opens a file
        @return: editor widget or None if it can't make it
        
        editor = PMXEditorWidget(file)
        icon = fileManager.getFileIcon(file)
        self.tabWidget.addTab(editor, file.fileName())
        self.tabWidget.setActiveIcon(editor, icon)
        return editor
        '''
        pass
    
    @pyqtSignature('')
    def on_actionAbout_Qt_triggered(self):
        qApp.aboutQt()
    
    @pyqtSignature('')
    def on_actionAbout_this_application_triggered(self):
        QMessageBox.information(self, self.trUtf8("About Prymatex"), 
                                self.trUtf8("<h3>Prymatex</h3>"
                                "<p>A general purpouse Text Editor</p>")
                                )
    
    @pyqtSignature('')
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)

    @pyqtSignature('')
    def on_actionSave_triggered(self):
        self.currentEditorWidget.request_save()
    
    @pyqtSignature('')
    def on_actionSave_As_triggered(self):
        self.currentEditorWidget.request_save(save_as = True)
        
    @pyqtSignature('')
    def on_actionSaveAll_triggered(self):
        for i in range(0, self.tabWidgetEditors.count()):
            if not self.tabWidgetEditors.widget(i).reqquest_save():
                #self.statusBar().showMessage(self.trUtf8("Not all documents were saved"), 1000)
                break
    
    def on_actionTake_Screenshot_triggered(self):
        self.takeScreenShot()
        
    @pyqtSignature('takeScreenShot()')
    def takeScreenShot(self):
        pxm = QPixmap.grabWindow(self.winId())
        format = 'png'
        from datetime import datetime
        now = datetime.now()
        name = now.strftime('sshot-%Y-%m-%d-%H_%M_%S') + '.' + format
        pxm.save(name, format)
        self.statusBar().showMessage("Screenshot saved as <a>%s</a>" % name)
        
    @pyqtSignature('')
    def on_actionZoom_In_triggered(self):
        self.currentEditorWidget.codeEdit.zoomIn()
    
    @pyqtSignature('')
    def on_actionZoom_Out_triggered(self):
        self.currentEditorWidget.codeEdit.zoomOut()

    @pyqtSignature('')
    def on_actionFilter_Through_Command_triggered(self):
        self.dialogFilter.exec_()
    
    @pyqtSignature('')
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
            
    @pyqtSignature('')
    def on_actionMove_Tab_Left_triggered(self):
        self.tabWidget.moveTabLeft()
    
    @pyqtSignature('')    
    def on_actionMove_Tab_Right_triggered(self):
        self.tabWidget.moveTabRight()
    
    #===========================================================================
    # Dumb code :/
    #===========================================================================
    @pyqtSignature('')
    def on_actionPreferences_triggered(self):
        qApp.instance().configdialog.exec_()
    
    def notifyCursorChange(self, editor, row, col):
        ''' Called by editors '''
        if editor == self.tabWidgetEditors.currentWidget():
            self.statusBar().updateCursorPos(col, row)
        
    def on_actionShow_Line_Numbers_toggled(self, check):
        print "Line", check

    @pyqtSlot()
    def on_actionPaste_As_New_triggered(self):
        text = qApp.instance().clipboard().text()
        if text:
            editor = self.addEmptyEditor()
            editor.appendPlainText(text)
        else:
            self.mainWindow.statusbar.showMessage(self.trUtf8("Nothing to paste."))

    @pyqtSignature('')
    def on_actionGo_To_Line_triggered(self):
        self.currentEditorWidget.goToLine()

    @pyqtSignature('')
    def on_actionGo_To_File_triggered(self):
        '''
        Triggers 
        '''
        self.tabWidget.chooseFileDlg.exec_()
    
    @pyqtSignature('')
    def on_actionFind_triggered(self):
        print "MainWindow::find"
        self.currentEditorWidget.showFindWidget()
        
    @pyqtSignature('')
    def on_actionFind_Replace_triggered(self):
        print "MainWindow::replace"
        self.currentEditorWidget.showReplaceWidget()
    
    def setCurrentEditor(self, editorWidget):
        
        self.currentEditorWidget = editorWidget
        
        #Update status bar
        self.statusBar().updateStatus(editorWidget.codeEdit.status)
        self.statusBar().updateSyntax(editorWidget.codeEdit.syntax)
        
        #Update window title
        template = Template(self.windowTitleTemplate)
        
        extra_attrs = self.pmxApp.supportManager.buildEnvironment()
        s = template.safe_substitute(APPNAME = "Prymatex",
                                     FILE = editorWidget.file.filename,
                                     PROJECT = 'No project',
                                     **extra_attrs)
        self.setWindowTitle(s)
    
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
    
    @pyqtSignature('')
    def on_actionNew_from_template_triggered(self):
        self.dialogNewFromTemplate.exec_()
    
    #============================================================
    # Bookmarks
    #============================================================
    @pyqtSignature('')
    def on_actionToggle_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.toggleBookmark(editor.textCursor().block().blockNumber() + 1)
    
    @pyqtSignature('')
    def on_actionNext_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.bookmarkNext(editor.textCursor().block().blockNumber() + 1)

    @pyqtSignature('')
    def on_actionPrevious_Bookmark_triggered(self):
        editor = self.currentEditor
        editor.bookmarkPrevious(editor.textCursor().block().blockNumber() + 1)
    
    @pyqtSignature('')
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
