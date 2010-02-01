

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
        self.center()
        QMetaObject.connectSlotsByName(self)
        
    def setup_actions(self):
        self.actionQuit = QAction(_(u"&Quit"), self)
        self.actionQuit.setObjectName("actionQuit")
    
    def setup_menus(self):
        menubar = QMenuBar(self)
        self.file_menu = QMenu(_("&File"))
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