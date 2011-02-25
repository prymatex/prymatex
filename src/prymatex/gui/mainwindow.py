# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.gui.editor.base import PMXCodeEdit

if __name__ == "__main__":
    import sys
    from os.path import join
    sys.path.append(join('..', '..'))
    
    
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.tabwidget import PMXTabWidget , PMXTabsMenu
from prymatex.gui.panes.fspane import PMXFSPaneDock
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence

from prymatex.gui.mixins.common import CenterWidget
#from prymatex.config.configdialog import PMXConfigDialog
from prymatex.gui.panes.outputpanel import PMXOutputDock
from prymatex.gui.panes.project import PMXProjectDock
from prymatex.gui.panes.symbols import PMXSymboldListDock
from prymatex.gui.panes.bundles import PMXBundleEditorDock
from prymatex.gui.ui_mainwindow import Ui_MainWindow
from prymatex.gui.filterdlg import PMXFilterDialog

import itertools
import logging
from prymatex.bundles.base import PMXMenuNode
logger = logging.getLogger(__name__)

class PMXMainWindow(QMainWindow, Ui_MainWindow, CenterWidget):
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
        tabWidget = PMXTabWidget(self)
        self.setCentralWidget( tabWidget )
        #self.tabWidgetEditors.buttonTabList.setMenu(self.menuPanes)
        #self.actionGroupTabs.addMenu(self.menuPanes)
        
        self.setup_panes()
        self.setup_logging()
        
        #self.setup_menus()
        #self.setup_actions()
        
        #self.setup_toolbars()
        
        self.center()
        
        # Una vez centrada la ventana caramos los mnues
        self.addBundlesToMenu()
        
        #self.dialogConfig = PMXConfigDialog(self)
        self.dialogFilter = PMXFilterDialog(self)
        #self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        #self.actionShowFSPane.setChecked(True)
        self.prevent_menu_lock()
    
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
                                        self.trUtf8("Hide output"))
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.paneProject.hide()
        self.paneProject.associateAction(self.actionShow_Project_Dock,
                                         self.trUtf8("Show Project"),
                                         self.trUtf8("Hide project"))
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.paneSymbolList.hide()
        
        
        self.paneBundleEditor = PMXBundleEditorDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneBundleEditor)
        self.paneBundleEditor.hide()
        
    def setup_toolbars(self):
        #raise NotImplementedError("Do we need them?")
        pass
    
    def insertBundleItem(self, item):
        if not item.ready():
            item.compile()
        self.currentEditor.insertBundleItem(item.clone())
        
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
            #shortcut = item.getKeySequence()
            #if shortcut != None:
            #    action.setShortcut(shortcut)
            receiver = lambda item = item: self.insertBundleItem(item)
            self.connect(action, SIGNAL('triggered()'), receiver)
            parent_menu.addAction(action)
            
    def addBundlesToMenu(self):
        from prymatex.bundles.base import PMXBundle
        #assert isinstance(bundles, TMMenuNode), "No me pasaste bundles"
        for bundle in PMXBundle.BUNDLES.values():
            menu = QMenu(bundle.name, self)
            self.menuBundles.addMenu(menu)
            if bundle.mainMenu != None:
                for _, item in bundle.mainMenu.iteritems():
                    self.addMenuItem(menu, item)  
                
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    counter = 0
    
    #===========================================================================
    # Shortcuts
    #===========================================================================
    
    @property
    def currentTabWidget(self):
        ''' Shortcut to the current editor (bypass layoutManager) '''
        return self.centralWidget()

    # TODO: Fix, just grep and replace
    @property
    def current_editor(self):
        #return self.currentTabWidget.currentWidget() # Old layout manager code
        editor_widget = self.currentTabWidget.currentWidget()
        return editor_widget.codeEdit
        
    currentEditor = current_editor

    @pyqtSignature('')
    def on_actionNewTab_triggered(self):
        self.centralWidget().appendEmptyTab()

    
    
    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.centralWidget().currentIndex()
        self.centralWidget().closeTab(index)
        if self.centralWidget().count():
            self.centralWidget().currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNext_Tab_triggered(self):
        self.centralWidget().focusNextTab()
        

        
    @pyqtSignature('')
    def on_actionPrevious_Tab_triggered(self):
        self.centralWidget().focusPrevTab()
        
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
        <a href="">Homepage</a>
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
        #qApp.instance().startDirectory()
        fs = QFileDialog.getOpenFileNames(self, self.trUtf8("Select Files to Open"),
                                            qApp.instance().startDirectory())
        if not fs:
            return
        for path in fs:
            self.centralWidget().openFile(path)
    
    @pyqtSignature('')
    def on_actionAboutQt_triggered(self):
        qApp.aboutQt()
    
    @pyqtSignature('')
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
    
       
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
                self.statusBar().showMessage(self.trUtf8("Not all documents were saved"), 1000)
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
    def on_actionZoom_In_triggered(self):
        self.current_editor.zoomIn()
        
    
    @pyqtSignature('')
    def on_actionZoom_Out_triggered(self):
        self.current_editor.zoomOut()
    
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
        self.tab_widget_mediator.moveTabLeft()
    
    @pyqtSignature('')    
    def on_actionMove_Tab_Right_triggered(self):
        self.tab_widget_mediator.moveTabRight()
    
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
        self.centralWidget().chooseFileDlg.exec_()
    
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
            