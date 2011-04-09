# -*- coding: utf-8 -*-
import itertools
import logging
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from prymatex.bundles import PMXBundle, PMXMenuNode
from prymatex.gui.editor.codeedit import PMXCodeEdit
from prymatex.gui.filterdlg import PMXFilterDialog
from prymatex.gui.mixins.common import CenterWidget
from prymatex.gui.panes.bundles import PMXBundleEditorDock
from prymatex.gui.panes.fspane import PMXFSPaneDock
from prymatex.gui.panes.outputpanel import PMXOutputDock
from prymatex.gui.panes.project import PMXProjectDock
from prymatex.gui.panes.symbols import PMXSymboldListDock
from prymatex.gui.panes.browser import PMXBrowserPaneDock
from prymatex.gui.tabwidget import PMXTabWidget, PMXTabsMenu
from prymatex.gui.ui_mainwindow import Ui_MainWindow
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.editor import PMXEditorWidget
from prymatex.gui.dialogs import NewFromTemplateDialog
from prymatex.core.exceptions import FileDoesNotExistError
from prymatex.core.base import PMXObject

#from prymatex.config.configdialog import PMXConfigDialog

logger = logging.getLogger(__name__)

class PMXMainWindow(QMainWindow, Ui_MainWindow, CenterWidget, PMXObject):
    '''
    Prymatex main window, it holds a currentEditor property which
    grants access to the focused editor.
    '''

    def __init__(self, files_to_open):
        '''
        The main window
        @param parent: The QObject parent, in this case it should be the QApp
        @param files_to_open: The set of files to be opened when the window
                              is shown in the screen.
        '''
        super(PMXMainWindow, self).__init__()
        # Initialize graphical elements
        self.setupUi(self)
        
        self.setWindowTitle(self.trUtf8(u"Prymatex Text Editor"))

        #Conectar tabs con status y status con tabs
        #self.statusbar.syntaxMenu.syntaxChange.connect(self.tabWidgetEditors.on_syntax_change)
        #self.tabWidgetEditors.currentEditorChange.connect(self.statusbar.syntaxMenu.on_current_editor_changed)
        
        self.actionGroupTabs = PMXTabActionGroup(self) # Tab handling
        self.NewFromTemplateDialog = NewFromTemplateDialog(self)
        
        self.NewFromTemplateDialog.newFileCreated.connect(self.newFileFromTemplate)
        
        #self.tabWidget = PMXTabWidget(self)
        #self.setCentralWidget( self.tabWidget )
        
        #self.tabWidgetEditors.buttonTabList.setMenu(self.menuPanes)
        #self.actionGroupTabs.addMenu(self.menuPanes)
        
        self.setup_panes()
        self.setup_logging()
        
        #self.setup_menus()
        #self.setup_actions()
        
        #self.setup_toolbars()
        
        self.center()
        
        # Una vez centrada la ventana caramos los menues
        self.addBundlesToMenu()
        
        #self.dialogConfig = PMXConfigDialog(self)
        self.dialogFilter = PMXFilterDialog(self)
        #self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        #self.actionShowFSPane.setChecked(True)
        self.prevent_menu_lock()
        
        for file in files_to_open:
            print "Opening file", file
            self.openFile(file)
    
    def setup_logging(self):
        '''
        Logging Sub-Window setup
        TODO: Fix speed issues when a big amount of events is presented
        '''
        from logwidget import LogDockWidget
        self.log_dock_widget = LogDockWidget(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock_widget)
        self.log_dock_widget.action = self.actionShow_Log_Window

    def prevent_menu_lock(self):
        '''
        Inspects the MainWindow definition and add the actions itself.
        If menubar is hidden (Ctrl+M), actions will be available.
        Maybe we will need to filter something, right now I don't belive
        it'll be nesseary.
        '''
        action_names = filter(lambda name: name.startswith('action'), dir(self))
        for action in map(lambda name: getattr(self, name), action_names):
            if isinstance(action, QAction):
                self.addAction(action)
    
    def setup_panes(self):
        '''
        Basic panels, dock objects. More docks should be available via plugins
        '''
        self.paneFileSystem = PMXFSPaneDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneFileSystem)
        self.paneFileSystem.hide()
        self.paneFileSystem.associateAction(self.actionShow_File_System_Pane,
                                            self.trUtf8("Show Filesystem Panel"),
                                            self.trUtf8("Hide Filesystem Panel"))
        
        self.paneOutput = PMXOutputDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneOutput)
        self.paneOutput.hide()
        self.paneOutput.associateAction(self.actionShow_Output,
                                        self.trUtf8("Show Output"),
                                        self.trUtf8("Hide Output"))
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.paneProject.hide()
        self.paneProject.associateAction(self.actionShow_Project_Dock,
                                         self.trUtf8("Show Project"),
                                         self.trUtf8("Hide Project"))
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.paneSymbolList.hide()
        
        
        self.paneBundleEditor = PMXBundleEditorDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneBundleEditor)
        self.paneBundleEditor.hide()
        
        self.paneBrowser = PMXBrowserPaneDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneBrowser)
        self.paneBrowser.hide()
        self.paneBrowser.associateAction(self.actionShow_Browser_Dock,
                                         self.trUtf8("Show Browser"),
                                         self.trUtf8("Hide Browser"))
        
    #====================================================================
    # Bundle Items
    #====================================================================
    def menuBundleItemActionTriggered(self, item):
        self.currentEditor.insertBundleItem(item)
        
    def addMenuItem(self, parent_menu, item):
        if isinstance(item, PMXMenuNode):
            menu = QMenu(item.name, parent_menu)
            parent_menu.addMenu(menu)
            for _, i in item.iteritems():
                self.addMenuItem(menu, i)
        elif item == PMXMenuNode.MENU_SPACE:
            parent_menu.addSeparator()
        elif item != None and item.name:
            action = QAction(item.buildMenuTextEntry(), self)
            receiver = lambda item = item: self.menuBundleItemActionTriggered(item)
            self.connect(action, SIGNAL('triggered()'), receiver)
            parent_menu.addAction(action)
            
    def addBundlesToMenu(self):
        name_order = lambda b1, b2: cmp(b1.name, b2.name)
        
        used = []
        BANNED_ACCEL = ' \t'
        def get_name_with_accel(name):
            
            for index, char in enumerate(name):
                if char in BANNED_ACCEL:
                    continue
                char = char.lower()
                # Not so nice
                #return name[0:index] + '&' + name[index:]
                if not char in used:
                    used.append(char)
                    new_name = name[0:index] + '&' + name[index:]
                    return new_name
            return name        
        
        for bundle in sorted(PMXBundle.BUNDLES.values(), name_order):
            
            menu = QMenu(get_name_with_accel(bundle.name), self)
            
            self.menuBundles.addMenu(menu)
            if bundle.mainMenu != None:
                for _, item in bundle.mainMenu.iteritems():
                    self.addMenuItem(menu, item)  
    
    #====================================================================
    # Command outputs
    #====================================================================
    def showHtml(self, string, **kwargs):
        self.paneBrowser.setHtml(string, kwargs['command'])
        self.paneBrowser.show()
    
    def showTooltip(self, string, **kwargs):
        cursor = self.currentEditor.textCursor()
        point = self.currentEditor.viewport().mapToGlobal(self.currentEditor.cursorRect(cursor).bottomRight())
        QToolTip.showText(point, string.strip(), self.currentEditor)
    
    def createNewDocument(self, string, **kwargs):
        print "Nuevo documento", string
            
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    counter = 0
    
    #===========================================================================
    # Shortcuts
    #===========================================================================
    
    @property
    def currentTabWidget(self):
        ''' Shortcut to the current editor (bypass layoutManager) '''
        #return self.centralWidget()
        return self.tabWidget

    # TODO: Fix, just grep and replace
    @property
    def current_editor(self):
        return self.current_editor_widget.codeEdit
    currentEditor = current_editor # Alias

    @property
    def current_editor_widget(self):
        return self.currentTabWidget.currentWidget()
    currentEditorWidget = current_editor_widget
    
    @pyqtSignature('')
    def on_actionNewTab_triggered(self):
        self.tabWidget.appendEmptyTab()

    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNext_Tab_triggered(self):
        self.tabWidget.focusNextTab()
        

        
    @pyqtSignature('')
    def on_actionPrevious_Tab_triggered(self):
        self.tabWidget.focusPrevTab()
        
    @pyqtSignature('')
    def on_actionAboutApp_triggered(self):
        QMessageBox.about(self, self.trUtf8("About"), self.trUtf8("""
        <h3>Prymatex Text Editor</h3>
        <p>(c) 2010 Xurix</p>
        <p><h4>Authors:</h4>
        <ul>
            <li>D3f0</li>
            <li>diegomvh</li>
            <li>locurask</li>
        </ul>
        <a href="http://d3f0.github.com/prymatex">Homepage</a>
        <p>Version %s</p>
        </p>
        """, qApp.instance().applicationVersion()))
        
    @pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, check):
        if not check and self.isFullScreen():
            self.showNormal()
        elif check:
            self.showFullScreen()
    
    
    @pyqtSlot(bool)
    def on_actionShow_Menus_toggled(self, state):
        print "Toggle", state
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
        start_directory = qApp.instance().startDirectory()
        files_to_open = QFileDialog.getOpenFileNames(self, self.trUtf8("Select Files to Open"),
                                            start_directory)
        
        for path in files_to_open:
            self.openFile(path, auto_focus = True)
            
    
    def openUrl(self, url):
        if isinstance(url, (str, unicode)):
            url = QUrl(url)
        source = url.queryItemValue('url')
        if source:
            source = QUrl(source)
            editor = self.openFile(source.path())
            line = url.queryItemValue('line')
            if line:
                editor.codeEdit.goToLine(int(line))
            column = url.queryItemValue('column')
            if column:
                editor.codeEdit.goToColumn(int(column))
            
    def openFile(self, path, auto_focus = False):
        '''
        Opens a file or focus its editor
        '''
        file_manager = qApp.instance().file_manager
        try:
            pmx_file = file_manager.openFile(path)
        except FileDoesNotExistError, e:
            QMessageBox.critical(self, "File not found", "%s" % e, QMessageBox.Ok)
            return
        if not pmx_file in self.tabWidget:
            try:
                editor = PMXEditorWidget.editorFactory(pmx_file)
            except Exception, e:
                from prymatex.gui.emergency import PMXTraceBackDialog
                PMXTraceBackDialog(e).exec_()
                #del pmx_file
                return 
            self.tabWidget.addTab(editor)
        else:
            editor = self.tabWidget[pmx_file]
        self.tabWidget.focusEditor(editor)
        return editor
    
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
        self.current_editor_widget.request_save()
    
    @pyqtSignature('')
    def on_actionSave_As_triggered(self):
        self.current_editor_widget.request_save(save_as = True)
        
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
        self.current_editor_widget.zoomIn()
    
    @pyqtSignature('')
    def on_actionZoom_Out_triggered(self):
        self.current_editor_widget.zoomOut()
    
    @pyqtSignature('')
    def on_actionFocus_Editor_triggered(self):
        # Siempre debería haber una ventana de edición
        try:
            self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        except Exception:
            pass
    
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
            editor = self.tabWidgetEditors.appendEmptyTab()
            editor.appendPlainText(text)
        else:
            self.mainwindow.statusbar.showMessage(self.trUtf8("Nothing to paste."))
          

    @pyqtSignature('')
    def on_actionGo_To_Line_triggered(self):
        #editor = self.tabWidgetEditors.currentWidget()
        #editor.showGoToLineDialog()
        self.current_editor.gotolineWidget.show()

    @pyqtSignature('')
    def on_actionGo_To_File_triggered(self):
        '''
        Triggers 
        '''
        self.tabWidget.chooseFileDlg.exec_()
    
    @pyqtSignature('')
    def on_actionShow_Current_Scope_triggered(self):
        scope = self.currentEditor.getCurrentScope()
        self.statusBar().showMessage("%s" % (scope))
        
    @pyqtSignature('')
    def on_actionTo_iNVERT_cASE_triggered(self):
        def to_title(s):
            return unicode(s).swapcase()
        self.current_editor.replaceCursorText(to_title)
        
    @pyqtSignature('')
    def on_actionTo_lowercase_triggered(self):
        def to_lower(s):
            return unicode(s).lower()
        self.current_editor.replaceCursorText(to_lower)
        
    @pyqtSignature('')
    def on_actionTo_TitleCase_triggered(self):
        def to_title(s):
            return unicode(s).title()
        self.current_editor.replaceCursorText(to_title)
        
    @pyqtSignature('')
    def on_actionTranspose_triggered(self):
        def transpose(s):
            s = list(unicode(s))
            l = len(s)
            for i in range(len(s)/2):
                s[i], s[l-i-1] = s[l-i-1], s[i],
            return ''.join(s)
        
        self.current_editor.replaceCursorText(transpose)
        
    @pyqtSignature('')
    def on_actionTo_UPPERCASE_triggered(self):
        def to_upper(s):
            return unicode(s).upper()
        self.current_editor.replaceCursorText(to_upper)
        
    @pyqtSignature('')
    def on_actionFind_triggered(self):
        self.current_editor.actionFind.trigger()
        
    @pyqtSignature('')
    def on_actionFind_Replace_triggered(self):
        self.current_editor.actionReplace.trigger()
    
    #===========================================================
    # Templates
    #===========================================================
    def newFileFromTemplate(self, path):
        self.openFile(path, auto_focus=True)
    
    @pyqtSignature('')
    def on_actionNew_from_template_triggered(self):
        self.NewFromTemplateDialog.exec_()
    
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
            