# encoding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.tabwidget import PMXTabWidget 
from prymatex.gui.statusbar import PMXStatusBar

def createAction(object, caption, 
                 shortcut = None, # QKeySequence
                 name = None,
                 do_i18n = True): # Name, 
    '''
    @param object: Objeto
    @param name: Nombre de la propiedad
    @param caption: Texto de la acción a ser i18nalizdo
    @param shortcut: Texto del atajo a ser i18nalizdo
    '''
    caption = do_i18n and _(caption) or caption
    action = QAction(_(caption), object)
    if not name:
        name = caption.replace(' ', '')
        name = name.replace('&', '')
        #print name
    actionName = 'action' + name
    action.setObjectName(actionName)
    if shortcut:
        action.setShortcut(_(shortcut))
    setattr(object, actionName, action )
    return action

def addActionsToMenu(menu, *actions):
    '''
    Helper for mass menu action creation
    Usage:
    addActionsToMenu(menu,
                     ("&Open", "Ctrl+O", "actionFOpen", {do_i18n = False}),
                     (pos1, pos2, pos3, {x = 2}),
                     None,
                     ()
    )
    '''
    for action_params in actions:
        parent = menu.parent()
        assert parent is not None
        if not action_params:
            menu.addSeparator()
        elif type(action_params) is QMenu:
            menu.addMenu(action_params)
        else:
            kwargs = {}
            if isinstance(action_params[-1], dict):
                largs = action_params[:-1]
                kwargs.update(action_params[-1])
            else:
                largs = action_params
            menu.addAction(createAction(parent, *largs, **kwargs))
            
            

class PMXMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))
        
        self.setup_menus()
        self.setup_actions()
        
        self.setup_toolbars()
        self.setup_gui()
        self.center()
        QMetaObject.connectSlotsByName(self)
        
        self.edior_tabs.currentWidget().setFocus(Qt.TabFocusReason)
    
    def setup_gui(self):
        self.edior_tabs = PMXTabWidget(self)
        self.setCentralWidget(self.edior_tabs)
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
        )
        
        addActionsToMenu(self.view_menu,
                                ("&Full Screen", Qt.Key_F11),
                                ("&Show Menus", "Ctrl+M"),
        )
        
        addActionsToMenu(self.window_menu,
                                ("&Next Tab", Qt.CTRL + Qt.Key_PageDown),
                                ("&Previous Tab", Qt.CTRL + Qt.Key_PageUp),
                                None,
                                self.panes_submenu,
                                None,
        )
        
        app_name = qApp.instance().applicationName()
        addActionsToMenu(self.help_menu, 
                         (_("&About %s", app_name), {'name': 'AboutApp', 'do_i18n': False,}),
                         ("&AboutQt",),
                         None,
                         ("Report &Bug", ),
                         ("Project &Homepage", ),
                         (_("&Translate %s", app_name), {'do_i18n': False}),
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
        
        self.window_menu = QMenu(_("&Window"), self)
        self.window_menu.windowActionGroup = MenuActionGroup(self.window_menu)
        menubar.addMenu(self.window_menu)
        
        # Panes
        self.panes_submenu = QMenu(_("&Panes"), self)
        
        self.help_menu = QMenu(_("&Help"), self)
        menubar.addMenu(self.help_menu)
        
        self.setMenuBar(menubar)
    
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
        #self.edior_tabs.addTab(QTextEdit(), "New Tab %d" % self.counter)
        #self.counter += 1
        self.edior_tabs.appendEmptyTab()
    
    @pyqtSignature('')
    def on_actionClose_triggered(self):
        index = self.edior_tabs.currentIndex()
        self.edior_tabs.closeTab(index)
        self.edior_tabs.currentWidget().setFocus(Qt.TabFocusReason)

    
    @pyqtSignature('')    
    def on_actionNextTab_triggered(self):
        
        curr = self.edior_tabs.currentIndex()
        count = self.edior_tabs.count()
        
        if curr < count -1:
            prox = curr +1
        else:
            prox = 0
        self.edior_tabs.setCurrentIndex(prox)
        self.edior_tabs.currentWidget().setFocus(Qt.TabFocusReason)
        
    @pyqtSignature('')
    def on_actionPreviousTab_triggered(self):
        curr = self.edior_tabs.currentIndex()
        count = self.edior_tabs.count()
        
        if curr > 0:
            prox = curr -1
        else:
            prox = count -1
        self.edior_tabs.setCurrentIndex(prox)
        self.edior_tabs.currentWidget().setFocus(Qt.TabFocusReason)
        
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
            self.edior_tabs.openLocalFile(path)
    
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