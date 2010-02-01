

from PyQt4.QtGui import QMainWindow

from prymatex.lib.i18n import ugettext as _

class PMXMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(_(u"Prymatex Text Editor"))
        self.setup_actions()
        self.setup_menus()
        self.setup_toolbars()
        
    def setup_actions(self):
        pass
    
    def setup_menus(self):
        pass
    
    def setup_toolbars(self):
        pass 