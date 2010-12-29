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
from prymatex.gui.tabwidget import PMXTabWidget , PMWTabsMenu
from prymatex.gui.panes.fspane import PMXFSPaneDock
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence
from layoutmanager import PMXLayoutManager
from prymatex.gui.mixins.common import CenterWidget
from prymatex.config.configdialog import PMXConfigDialog
from prymatex.gui.panes.outputpanel import PMXOutputDock
from prymatex.gui.panes.project import PMXProjectDock
from prymatex.gui.panes.symbols import PMXSymboldListDock
from prymatex.gui.panes.bundles import PMXBundleEditorDock
from prymatex.gui.ui_mainwindow import Ui_MainWindow
from prymatex.gui.filterdlg import PMXFilterDialog

import itertools
import logging
from prymatex.lib.textmate.bundle import TMMenuNode, MENU_SPACE
logger = logging.getLogger(__name__)

class PMXMainWindow(QMainWindow, Ui_MainWindow, CenterWidget):

    
    def __init__(self):
        QMainWindow.__init__(self)
        # Initialize graphical elements
        self.setupUi(self)
        
        self.setWindowTitle(self.trUtf8(u"Prymatex Text Editor"))

        #Conectar tabs con status y status con tabs
        #self.statusbar.syntaxMenu.syntaxChange.connect(self.tabWidgetEditors.on_syntax_change)
        #self.tabWidgetEditors.currentEditorChange.connect(self.statusbar.syntaxMenu.on_current_editor_changed)
        
        self.actionGroupTabs = PMXTabActionGroup(self) # Tab handling
        
        self.layoutManager = PMXLayoutManager(self)
        self.setCentralWidget(self.layoutManager)
        #self.setCentralWidget(self.tabWidgetEditors)
        #self.tabWidgetEditors.buttonTabList.setMenu(self.menuPanes)
        #self.actionGroupTabs.addMenu(self.menuPanes)
        
        self.setup_panes()
        self.setup_logging()
        
        #self.setup_menus()
        #self.setup_actions()
        
        #self.setup_toolbars()
        
        self.center()
        
        # Una vez centrada la ventana caramos los mnues
        from prymatex.lib.textmate.bundle import TM_BUNDLES
        self.add_bundles_to_menu(TM_BUNDLES)
        
        self.dialogConfig = PMXConfigDialog(self)
        self.dialogFilter = PMXFilterDialog(self)
        #self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        #self.actionShowFSPane.setChecked(True)
        self.prevent_menu_lock()


    
    def setup_logging(self):
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
                                            _("Show Filesystem Panel"),
                                            _("Hide Filesystem Panel"))
        
        
        self.paneOutput = PMXOutputDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneOutput)
        self.paneOutput.hide()
        self.paneOutput.associateAction(self.actionShow_Output,
                                        _("Show Output"),
                                        _("Hide output"))
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneProject)
        self.paneProject.hide()
        self.paneProject.associateAction(self.actionShow_Project_Dock,
                                         _("Show Project"),
                                         _("Hide project"))
        
        self.paneSymbolList = PMXSymboldListDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.paneSymbolList)
        self.paneSymbolList.hide()
        
        
        self.paneBundleEditor = PMXBundleEditorDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paneBundleEditor)
        self.paneBundleEditor.hide()
        
    def setup_toolbars(self):
        #raise NotImplementedError("Do we need them?")
        pass
    
    
    def add_menu_item(self, parent_menu, item):
        if isinstance(item, TMMenuNode):
            menu = QMenu(item.name)
            parent_menu.addMenu(menu)
            for _, i in item.iteritems():
                self.add_menu_item(menu, i)
        elif item == MENU_SPACE:
            parent_menu.addSeparator()
        elif item and item.name:
            action = QAction(item.name, self)
            parent_menu.addAction(action)
            
    def add_bundles_to_menu(self, bundles):
        names = sorted(bundles.keys())
        #assert isinstance(bundles, TMMenuNode), "No me pasaste bundles"
        for name in names:
            menu = QMenu(name, self)
            self.menuBundles.addMenu(menu)
            bundle = bundles[name]
            for _, item in bundle.menu.iteritems():
                self.add_menu_item(menu, item)  
                
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    counter = 0
    
    #===========================================================================
    # Shortcuts
    #===========================================================================
    
    @property
    def currentTabWidget(self):
        ''' Shortcut to the current editor (bypass layoutManager) '''
        return self.layoutManager.currentTabWidget
    
    @property
    def currentEditor(self):
        return self.currentTabWidget.currentWidget()
    
    @pyqtSignature('')
    def on_actionNewTab_triggered(self):
        self.currentTabWidget.appendEmptyTab()

    
    
    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.currentTabWidget.currentIndex()
        self.currentTabWidget.closeTab(index)
        if self.currentTabWidget.count():
            self.currentTabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNext_Tab_triggered(self):
        self.currentTabWidget.focusNextTab()
        

        
    @pyqtSignature('')
    def on_actionPrevious_Tab_triggered(self):
        self.currentTabWidget.focusPrevTab()
        
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
        fs = QFileDialog.getOpenFileNames(self, _("Select Files to Open"),
                                            qApp.instance().startDirectory())
        if not fs:
            return
        for path in fs:
            #PMXCodeEdit.get
            self.currentTabWidget.openFile(path)
            #self.tabWidgetEditors.openLocalFile(path)
    
    @pyqtSignature('')
    def on_actionAboutQt_triggered(self):
        qApp.aboutQt()
    
    @pyqtSignature('')
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
    
    @property
    def editor(self):
        '''
        Current Editor
        '''
        self.layoutManager.currentEditor()
        #return self.tabWidgetEditors.currentWidget()
        
    @pyqtSignature('')
    def on_actionSave_triggered(self):
        self.currentEditor.save()
    
    @pyqtSignature('')
    def on_actionSaveAs_triggered(self):
        self.currentEditor.save(save_as = True)
        
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
    def on_actionZoom_In_triggered(self):
        self.currentEditor.zoomIn()
        
    
    @pyqtSignature('')
    def on_actionZoom_Out_triggered(self):
        self.currentEditor.zoomOut()
    
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
            self.mainwindow.statusbar.showMessage(_("Nothing to paste."))
          

    @pyqtSignature('')
    def on_actionGo_To_Line_triggered(self):
        editor = self.tabWidgetEditors.currentWidget()
        editor.showGoToLineDialog()
        
    @pyqtSignature('')
    def on_actionShow_Current_Scope_triggered(self):
        scope = self.tabWidgetEditors.currentWidget().get_current_scope()
        folding = self.tabWidgetEditors.currentWidget().get_current_folding()
        self.statusBar().showMessage("%d - %s" % (folding, scope))
        
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
        self.currentEditor.actionFind.trigger()
        
    @pyqtSignature('')
    def on_actionFind_Replace_triggered(self):
        self.currentEditor.actionReplace.trigger()
    

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
            