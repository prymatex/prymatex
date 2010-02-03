# encoding: utf-8
from PyQt4.QtGui import QApplication, QIcon


class PMXApplication(QApplication):
    def __init__(self, arguments):
        
        QApplication.__init__(self, arguments)
        
        self.setApplicationName("Prymatex Text Editor")
        self.setApplicationVersion("0.1") # hg stuff?
        self.setOrganizationDomain("org")
        self.setOrganizationName("Xurix")
        
        self.projectUrl = 'http://code.google.com/p/prymatex'
        
        from prymatex.resmgr import resource_manager
        self.__res_mngr = resource_manager
        
        self.setWindowIcon(self.res_mngr.getIcon('Prymatex_Logo.png'))
        
        from prymatex.gui.mainwindow import PMXMainWindow
        self.main_window = PMXMainWindow()
        self.main_window.show()
        
    @property
    def res_mngr(self):
        return self.__res_mngr
    
    def getThemePath(self):
        #TODO: Get something from the config
        pass
    
    
        