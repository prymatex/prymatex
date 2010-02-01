

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from prymatex.lib.i18n import ugettext as _

class PMXMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))
        self.setup_actions()
        self.setup_menus()
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
        self.actionQuit = QAction(_(u"&Quit"), self)
        self.actionQuit.setObjectName("actionQuit")
        
        
        self.actionNewTab = QAction(_("New &tab"), self)
        self.actionNewTab.setObjectName("actionNewTab")
        self.actionNewTab.setShortcut(QKeySequence("Ctrl+N"))
    
    def setup_menus(self):
        menubar = QMenuBar(self)
        self.file_menu = QMenu(_("&File"))
        
        self.file_menu.addAction(self.actionNewTab)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.actionQuit)
        
        menubar.addMenu(self.file_menu)
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