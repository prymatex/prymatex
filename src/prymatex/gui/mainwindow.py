# encoding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.tabwidget import PMXTabWidget 
from prymatex.gui.statusbar import PMXStatusBar
from prymatex.gui.panes.fspane import FSPane
from prymatex.gui.utils import addActionsToMenu

class PMXMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))
        
        self.setup_menus()
        self.setup_actions()
        self.setup_panes()
        self.setup_toolbars()
        self.setup_gui()
        self.center()
        QMetaObject.connectSlotsByName(self)
        
        self.tabWidgetEditors.currentWidget().setFocus(Qt.TabFocusReason)
        
        self.pane = FSPane(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.pane)
    
    def setup_gui(self):
        self.tabWidgetEditors = PMXTabWidget(self)
        self.setCentralWidget(self.tabWidgetEditors)
        status_bar = PMXStatusBar(self)
        self.setStatusBar(status_bar)
        
    
    def setup_actions(self):
        addActionsToMenu(self.file_menu,
                                   ("New", "Ctrl+N", {'name': "NewTab"}),
                                   ("&Open...", "Ctrl+O", {'name':'FileOpen'}),
                                   ("&Save", "Ctrl+S"),
                                   ("Save &As", "Ctrl+Shift+S"),
                                   ("Save &All", "Ctrl+Alt+S"),
                                   None,
                                   ("&Reload", "Ctrl+R"),
                                   ("&Close", "Ctrl+W"),
                                   ("Close &Others", "Ctrl+Shift+W"),
                                   None,
                                   ("&Quit", "Ctrl+Q"),
        )
        
        addActionsToMenu(self.edit_menu,
                        ("Un&do", "Ctrl+Z"),
                        ("&Redo", "Ctrl+Shift+Z"),
                        None,
                        ("&Copy", "Ctrl+C"),
                        ("C&ut", "Ctrl+X"),
                        ("&Paste", "Ctrl+V"),
                        ("Paste As &New", "Ctrl+Shift+V"),
                        
        )
        
        addActionsToMenu(self.settings_menu,
                        ("Show Line &Numbers", "F10"),
                         None,
                        ('Preferences', ),
                         
                        )
        
        
        addActionsToMenu(self.view_menu,
                                ("&Full Screen", "F11"),
                                ("&Show Menus", "Ctrl+M"),
                                None,
                                ("Zoom &In", "Ctrl+Plus"),
                                ("Zoom &Out", "Ctrl+Minus"),
                                None,
                                ("Focus Editor", "F12"),
        )
        
        
        
        addActionsToMenu(self.window_menu,
                                ("&Next Tab", "Ctrl+PageDown"),
                                ("&Previous Tab", "Ctrl+PageUp"),
                                None,
                                ("Move Tab &Left",  "Ctrl+Shift+PageUp"),
                                ("Move Tab &Right", "Ctrl+Shift+PageDown"),
                                None,
                                self.panes_submenu,
                                
        )
        
        app_name = qApp.instance().applicationName()
        addActionsToMenu(self.help_menu, 
                         (_("&About %s", app_name), {'name': 'AboutApp', 'do_i18n': False,}),
                         ("&AboutQt",),
                         None,
                         ("Report &Bug", ),
                         ("Project &Homepage", ),
                         (_("&Translate %s", app_name), {'do_i18n': False}),
                         None,
                         ('&Take Screenshot', 'Ctrl+8'),
        )
#        self.help_menu.addActions([
#                                createAction(self, _("&About %s") % app_name, 
#                                             name = 'AboutApp', do_i18n = False),
#                                createAction(self, _("&About Qt")),
#                                   
#        ])
        
        
    
    def setup_menus(self):
        menubar = QMenuBar(self)
        self.file_menu = QMenu(_("&File"), self)
        menubar.addMenu(self.file_menu)
        
        self.edit_menu = QMenu(_("&Edit"), self)
        menubar.addMenu(self.edit_menu)
        
        self.view_menu = QMenu(_("&View"), self)
        menubar.addMenu(self.view_menu)
        
        self.bundle_menu = QMenu(_("&Bundle"), self)
        menubar.addMenu(self.bundle_menu)
        
        self.tools_menu = QMenu(_("&Tools"), self)
        menubar.addMenu(self.tools_menu)
        
        self.settings_menu = QMenu(_("&Settings"), self)
        menubar.addMenu(self.settings_menu)
        
        self.window_menu = QMenu(_("&Window"), self)
        self.window_menu.windowActionGroup = MenuActionGroup(self.window_menu)
        menubar.addMenu(self.window_menu)
        
        # Panes
        self.panes_submenu = QMenu(_("&Panes"), self)
        
        self.help_menu = QMenu(_("&Help"), self)
        menubar.addMenu(self.help_menu)
        
        self.setMenuBar(menubar)
    
    def setup_panes(self):
        actions = \
        addActionsToMenu(self.panes_submenu, 
                         ('Filesystem', {'checkable': True}),
                         ('Text Search', {'checkable': True}),
                         ('Session', {'checkable': True}),
                         )
        print actions
        
    
    def setup_toolbars(self):
        pass 
    
    def center(self):
        
        dsk_geo = qApp.instance().desktop().availableGeometry()
        dwidth, dheight = dsk_geo.width(), dsk_geo.height() 
        width = dwidth * 0.7
        height = dheight * 0.67
        x0 = (dwidth - width) / 2 
        y0 = (dheight - height) / 2
        self.setGeometry(x0,y0,width,height)
        
        
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
            
    @pyqtSignature('')
    def on_actionShowMenus_triggered(self):
        menubar = self.menuBar()
        if menubar.isHidden():
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
    def on_actionProjectHomepage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
    
    @pyqtSignature('')
    def on_actionSave_triggered(self):
        print "actionSave"
    
    @pyqtSignature('')
    def on_actionSaveAll_triggered(self):
        print "actionSaveAll"
    
    @pyqtSignature('')
    def on_actionTakeScreenshot_triggered(self):
        QTimer.singleShot()
        pxm = QPixmap.grabWindow(self.winId())
        format = 'png'
        from datetime import datetime
        now = datetime.now()
        #initialPath = QDir.currentPath() + "/untitled." + format

#        fileName = QFileDialog.getSaveFileName(self, "Save As",
#                initialPath,
#                "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
#        if fileName:
#            pxm.save(fileName, format)
        name = now.strftime('sshot-%Y-%m-%d-%H_%M_%S') + '.' + format
        pxm.save(name, format)
        
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

    
class MenuActionGroup(QActionGroup):
    def __init__(self, parent):
        assert isinstance(parent, QMenu)
        QActionGroup.__init__(self, parent)
    
    def addAction(self, action):
        QActionGroup.addAction(self, action)
        self.parent().addAction(action)
    
    def removeAction(self, action):
        QActionGroup.removeAction(self, action)
        self.parent().removeAction(action)
        