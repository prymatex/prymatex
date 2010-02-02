# encoding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pprint import pformat
from prymatex.lib.i18n import ugettext as _

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
        print name
    actionName = 'action' + name
    action.setObjectName(actionName)
    if shortcut:
        action.setShortcut(_(shortcut))
    setattr(object, actionName, action )
    return action

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
        self.edior_tabs = QTabWidget()
        self.edior_tabs.addTab(QTextEdit(), "Hello world")
        self.setCentralWidget(self.edior_tabs)
        
    
    def setup_actions(self):
        self.file_menu.addActions([
                                   createAction(self, "New Tab", "Ctrl+N"),
                                   createAction(self, "&Close Tab", "Ctrl+W"),
                                   createAction(self, "&Quit", "Ctrl+Q"),
        ])
        
        self.edit_menu.addActions( [
                              createAction(self, "&Copy", "Ctrl+C"),
                              createAction(self, "C&ut", "Ctrl+X"),
                              createAction(self, "&Paste", "Ctrl+V"),
        ])
        
        self.view_menu.addActions([
                                createAction(self, "&Full Screen", Qt.Key_F11),
                                createAction(self, "&Show Menus", "Ctrl+M"),
                                   
        ])
        
        self.window_menu.addActions([
                                createAction(self, "&Next Tab", Qt.CTRL + Qt.Key_PageDown),
                                createAction(self, "&Previous Tab", Qt.CTRL + Qt.Key_PageUp),
                                
        ])
        
        app_name = qApp.instance().applicationName()
        self.help_menu.addActions([
                                createAction(self, _("&About %s") % app_name, 
                                             name = 'AboutApp', do_i18n = False),
                                createAction(self, _("&About Qt")),
                                   
        ])
        
        
    
    def setup_menus(self):
        menubar = QMenuBar(self)
        self.file_menu = QMenu(_("&File"), self)
        menubar.addMenu(self.file_menu)
        
        self.edit_menu = QMenu(_("&Edit"), self)
        menubar.addMenu(self.edit_menu)
        
        self.view_menu = QMenu(_("&View"), self)
        menubar.addMenu(self.view_menu)
        
        self.window_menu = QMenu(_("&Window"), self)
        menubar.addMenu(self.window_menu)
        
        self.help_menu = QMenu(_("&Help"), self)
        menubar.addMenu(self.help_menu)
        
        self.setMenuBar(menubar)
    
    def setup_toolbars(self):
        pass 
    
    def center(self):
        #TODO: Make this real
        self.setGeometry(10,10,500,460)
        
        
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    counter = 0
    
    @pyqtSignature('')
    def on_actionNewTab_triggered(self):
        self.edior_tabs.addTab(QTextEdit(), "New Tab %d" % self.counter)
        self.counter += 1
    
    @pyqtSignature('')
    def on_actionCloseTab_triggered(self):
        #self.edior_tabs.currentWidget()
        self.edior_tabs.removeTab(self.edior_tabs.currentIndex())
    
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
        </p>
        """))
        
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