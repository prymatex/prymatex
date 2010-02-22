# -*- coding: utf-8 -*-
# encoding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.tabwidget import PMXTabWidget , PMWTabsMenu
from prymatex.gui.statusbar import PMXStatusBar
from prymatex.gui.panes.fspane import PMXFSPaneDock
from prymatex.gui.utils import addActionsToMenu, text_to_KeySequence
from prymatex.gui.mixins.common import CenterWidget
from prymatex.gui.editor import PMXTextEdit
from prymatex.config.configdialog import PMXConfigDialog
from prymatex.gui.panes.outputpanel import PMXOutputDock
from prymatex.gui.panes.project import PMXProjectDock
from prymatex.gui.panes.symbols import PMXSymboldListDock
from prymatex.gui.panes.bundles import PMXBundleEditorDock
from prymatex.gui.ui_mainwindow import Ui_MainWindow
import itertools
import logging
logger = logging.getLogger(__name__)

class PMXMainWindow(QMainWindow, Ui_MainWindow, CenterWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))

        self.actionGroupTabs = PMXTabActionGroup(self) # Tab handling
        self.setupUi(self)
        self.setCentralWidget(self.tabWidgetEditors)
        self.tabWidgetEditors.buttonTabList.setMenu(self.menuPanes)
        self.actionGroupTabs.addMenu(self.menuPanes)
        #self.setup_panes()
        #self.setup_menus()
        #self.setup_actions()
        
        #self.setup_toolbars()
        
        self.center()
        
        self.dialogConfig = PMXConfigDialog(self)
        
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        #self.actionShowFSPane.setChecked(True)
        self.prevent_menu_lock()

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
        
        self.paneFileSystem = PMXFSPaneDock(self)
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
        logger.info("New")
        self.tabWidgetEditors.appendEmptyTab()
    
    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.tabWidgetEditors.currentIndex()
        self.tabWidgetEditors.closeTab(index)
        if self.tabWidgetEditors.count():
            self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNext_Tab_triggered(self):
        
        curr = self.tabWidgetEditors.currentIndex()
        count = self.tabWidgetEditors.count()
        
        if curr < count -1:
            prox = curr +1
        else:
            prox = 0
        self.tabWidgetEditors.setCurrentIndex(prox)
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
    @pyqtSignature('')
    def on_actionPrevious_Tab_triggered(self):
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
        
    @pyqtSlot(bool)
    def on_actionFullScreen_triggered(self):
        if self.isFullScreen():
            self.showNormal()
        else:
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
        return self.tabWidgetEditors.currentWidget()
        
        
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
    def on_actionZoom_In_triggered(self):
        self.tabWidgetEditors.currentWidget().zoomIn()
    
    @pyqtSignature('')
    def on_actionZoom_Out_triggered(self):
        self.tabWidgetEditors.currentWidget().zoomOut()
    
    @pyqtSignature('')
    def on_actionFocus_Editor_triggered(self):
        # Siempre debería haber una ventana de edición
        try:
            self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        except Exception:
            pass
    
    
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
            
#                return
#        for i in range(index+1, count):
#            if not self.tabWidgetEditors.closeTab(i):
#                return
    @pyqtSignature('')
    def on_actionMove_Tab_Left_triggered(self):
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
    def on_actionMove_Tab_Right_triggered(self):
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
        
    def on_actionShow_Line_Numbers_toggled(self, check):
        print "Line", check
    

    @pyqtSignature('')
    def on_actionGo_To_Line_triggered(self):
        
        editor = self.tabWidgetEditors.currentWidget()
        editor.showGoToLineDialog()
        
    @pyqtSignature('')
    def on_actionShow_Current_Scope_triggered(self):
        scope = self.tabWidgetEditors.currentWidget().getCurrentScope()
        self.statusBar().showMessage(scope)
        
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


def associateQActionWithDock(qAction, dockWidget, showText, hiddenText):
    pass

class PMXActionDockConnector(QObject):
    '''
    A wrapper for QActions that watches a widget hide/show events
    and sets the QAction to checked
    '''
    def __init__(self, action, widget, show_text, hide_text):
        assert action.isCeckable(), "%s is not checkable!" % action
        self.action = action
        self.widget = widget
        self.show_text, self.hide_text = show_text, hide_text
        text = widget.isHidden() and show_text or hide_text
        self.action.setText(text)
        self.connect(self.action, SIGNAL("toggled(bool)"), self.toggleDock)
        self.connect(self.widget, SIGNAL("widgetShown(bool)"), self.checkCrossButtonHide) 
    
    def toggleDock(self, check):
        if check:
            if self.widget.isHidden():
                self.widget.show()
            self.action.setText(self.hide_text)
        else:
            if not self.widget.isHidden():
                self.widget.hide()
            self.action.setText(self.text_show)
    
    def checkCrossButtonHide(self, dockShown):
        if not dockShown:
            if self.action.isChecked():
                self.action.setChecked(False)

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

class __PMWTabsMenu(QMenu):
    '''
    A menu that keeps only one action active
    '''
    def __init__(self, caption, parent):
        QMenu.__init__(self, caption, parent)
        self.actionGroup = QActionGroup(self)
        self.shortcuts = []
        for i in range(1, 10):
            self.shortcuts.append(text_to_KeySequence("Alt+%d" % i))


    def addAction(self, action):
        QMenu.addAction(self, action)
        self.actionGroup.addAction(action)
        self.updateShortcuts()

    def removeAction(self, action):
        QMenu.removeAction(self, action)
        self.actionGroup.removeAction(action)
        self.updateShortcuts()



                
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
            