# encoding: utf-8
from PyQt4.QtGui import QApplication, QMessageBox
from PyQt4.QtCore import SIGNAL

from os.path import join, exists
from os import getpid, unlink
from prymatex.lib.exceptions import AlreadyRunningError

class PMXApplication(QApplication):
     
    def __init__(self, arguments):
        
        QApplication.__init__(self, arguments)
        from prymatex.resmgr import resource_manager
        self.__res_mngr = resource_manager
        
        self.setApplicationName("Prymatex Text Editor")
        self.setApplicationVersion("0.1") # hg stuff?
        self.setOrganizationDomain("org")
        self.setOrganizationName("Xurix")
        self.projectUrl = 'http://code.google.com/p/prymatex'
        
        self.setWindowIcon(self.res_mngr.getIcon('Prymatex_Logo.png'))
        
        self.check_single_instance()
        
        from prymatex.gui.mainwindow import PMXMainWindow
        self.main_window = PMXMainWindow()
        self.main_window.show()
        
        self.connect(self, SIGNAL('aboutToQuit()'), self.cleanup)
    
    @property
    def lock_filename(self):
        return join(self.res_mngr.path, 'LOCK') 
    
    
    
    def cleanup(self):
        try:
            unlink(self.lock_filename)
        except:
            pass
        
    
    @property
    def config(self):
        #TODO: Implementar
        pass
        
    @property
    def res_mngr(self):
        return self.__res_mngr
    
    
    def check_single_instance(self):
        '''
        Intenta trabajar con una sola instancia
        '''
        
        from prymatex.lib import os
        if exists(self.lock_filename):
            f = open(self.lock_filename)
            pid = int(f.read())
            f.close()
            print "Esta?", pid in os.pid_proc_dict()
            if pid in os.pid_proc_dict():
                from prymatex.lib.i18n import ugettext as _
                print "PID Existente"
                QMessageBox.critical(None, _('Application Already Running'),
                                     _('''%s seems to be runnig. Please
                                     close the other instance.''', self.applicationName()),
                                     QMessageBox.Ok)
                raise AlreadyRunningError(pid)
            
        else:
            f = open(self.lock_filename, 'w')
            f.write('%s' % getpid())
            f.close()
        