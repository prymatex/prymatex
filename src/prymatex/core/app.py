# -*- coding: utf-8 -*-
# encoding: utf-8
from PyQt4.QtGui import QApplication, QMessageBox, QSplashScreen, QPixmap, QIcon
from PyQt4.QtCore import SIGNAL, QEvent

from os.path import join, exists, isdir, isabs

from os import getpid, unlink, getcwd
from os.path import dirname, abspath
from prymatex.lib import deco

from logging import getLogger
logger = getLogger(__name__)

# ipdb handling
import sys
sys_excepthook = sys.excepthook
class PMXApplication(QApplication):
    '''
    The application instance.
    There can't be two apps running simultaneously, since configuration issues
    may occur.
    The application loads the TM Bundles and Themes.
    '''
    
    __config = None
    __res_mngr = None
    __logger = None
    
    #@printtime
    @deco.logtime
    def __init__(self, args, logger = None):
        '''
        Inicialización de la aplicación.
        '''
        QApplication.__init__(self, args)
        # Logger setup
        self.setup_logging() 
        
        from prymatex.optargs import parser
        self.__options, files_to_open = parser.parse_args(args[1:])
        
        # Some init's
        self.init_application_params()
        self.init_config()
        self.init_resources()
        self.res_mngr.loadStyleSheet()
        
        self.__untitled_counter = 0
        
        self.splash = QSplashScreen(QPixmap(":/images/resources/prymatex/Prymatex_Splash.svg"))
        self.splash.show()
        
        self.setWindowIcon(QIcon(":/resources/icons/Prymatex_Logo.png"))
        
        self.check_single_instance()
        
        #Settings
        #TODO: Settings
        
        # Bundles and Stuff
        self.load_textmate_stuff()
        
        self.connect(self, SIGNAL('aboutToQuit()'), self.cleanup)
        self.connect(self, SIGNAL('aboutToQuit()'), self.save_config)
        
        # Creates the GUI
        self.createWindows(files_to_open)
        
        # TODO: Fix
        if not self.options.ipdb_excepthook:
            sys.excepthook = sys_excepthook
        else:
            import ipdb
    
    def load_textmate_stuff(self):
        self.load_texmate_themes()
        self.load_texmate_bundles()
    
    
    @property
    def options(self):
        ''' These options are defined in
        prymatex.optargs and are hold by the
        application instance '''
        return self.__options
        
    
    def createWindows(self, files_to_open):
        '''
        Creates the windows
        '''
        from prymatex.gui.mainwindow import PMXMainWindow
        self.windows = []
        first_window = PMXMainWindow( files_to_open )
        self.splash.finish(first_window)
        first_window.show()
        self.windows.append(first_window)   # Could it be possible to hold it in
                                            # its childrens?
        
        self.connect(first_window, SIGNAL("destroyed(QObject)"), self.destroyWindow)
    
    def destroyWindow(self, qobject):
        pass
    @property
    def logger(self):
        return self.__logger
    
    @logger.setter
    def logger(self, logger):
        from  logging import RootLogger
        assert isinstance(logger, RootLogger)
        self.__logger = logger
        logger.info("Logger set in the application instance")
    
    def setup_logging(self):
        import logging
        
        logger = logging.getLogger("")
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler("messages.log")
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        
        
        # create formatter and add it to the handlers
        formatter = logging.Formatter()#"%(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        from prymatex.gui.logwidget import handler as qth
        logger.addHandler(qth)
        logger.info("Application startup")
        self.logger = logger
    
    def init_application_params(self):
        from prymatex import version
        self.setApplicationName(version.__doc__)
        self.setApplicationVersion(version.__version__) # hg stuff?
        self.setOrganizationDomain("org")
        self.projectUrl = version.__url__    
    
    @property
    def lock_filename(self):
        return join(self.res_mngr.path, 'LOCK') 
    
    def cleanup(self):
        try:
            unlink(self.lock_filename)
        except:
            pass
    
    def save_config(self):
        self.logger.info("Save config")
        self.config.save()
        self.logger.info("Config saved")
    
    def init_resources(self):
        if not self.__res_mngr:
            from prymatex.resmgr import ResourceManager
            self.__res_mngr = ResourceManager()
        
    def init_config(self):
        if not self.__config:
            from prymatex.core.config import settings
            self.__config = settings
            
    @property
    def config(self):
        '''
        Retorna un objeto que soporta xxx.yyy.zzz
        y que puede propagar señales ante edición.
        '''
        return self.__config
        
    @property
    def res_mngr(self):
        '''
        Retorna el administrador de recursos
        '''
        return self.__res_mngr
    
    def load_texmate_themes(self):
        '''
        Load textmate Bundles and Themes
        '''
        from prymatex.bundles import load_prymatex_themes
        from prymatex.lib.i18n import ugettext as _
        
        self.splash.showMessage(_("Loading themes..."))
        themes = load_prymatex_themes(self.config.PMX_THEMES_PATH)
        
        self.splash.showMessage(_("%d themes loaded", themes))
        QApplication.processEvents()
    
    # Decorador para imprimir cuanto tarda
    @deco.logtime
    def load_texmate_bundles(self):
        from prymatex.bundles import load_prymatex_bundles
        from prymatex.lib.i18n import ugettext as _
        bundles = 0
        splash = self.splash
        def before_load_callback(counter, total, name):
            progress = (float(counter) / total) * 100
            splash.showMessage(_("Loading bundle %s\n%4d of %4d (%.d%%)", 
                                 name, counter, total, progress))
            QApplication.processEvents()
            
        self.splash.showMessage(_("Loading bundles..."))
        bundles += load_prymatex_bundles(before_load_callback)
        #Cargar bundles de usuario
        #for dirname in self.config.PMX_BUNDLES_PATH:
        #    self.splash.showMessage(_("Loading bundles..."))
        #    if isdir(dirname):
        #        if not isabs(dirname):
        #            dirname = join(getcwd(), dirname) 
        #        
        #    else:
        #        self.logger.warning("The theme dir does not exist")
                
        QApplication.processEvents()
        
    def check_single_instance(self):
        '''
        Intenta trabajar con una sola instancia
        '''
        from prymatex.lib import os
        if exists(self.lock_filename):
            f = open(self.lock_filename)
            pid = int(f.read())
            f.close()
            self.logger.info("Checking for another instance: %s", 
                        pid in os.pid_proc_dict()
                        )
            if pid in os.pid_proc_dict():
                from prymatex.lib.i18n import ugettext as _
                self.logger.warning("Another app running")
                QMessageBox.critical(None, _('Application Already Running'),
                                     _('''%s seems to be runnig. Please
                                     close the other instance.''', self.applicationName()),
                                     QMessageBox.Ok)
                from prymatex.lib.exceptions import AlreadyRunningError
                raise AlreadyRunningError(pid)
            
        else:
            f = open(self.lock_filename, 'w')
            f.write('%s' % getpid())
            f.close()
            
    def startDirectory(self):
        '''
        Returns the start dir
        '''
        if self.options.startdir and exists(self.options.startdir):
            return abspath(self.options.startdir)
        else:
            from prymatex.lib.os import get_homedir
            return get_homedir()

    def notify(self, receiver, event):
        '''
    	Notify with propagation for customEvent
    	'''
        if event.type() > QEvent.User:
            w = receiver
            while(w):
                # DEBUG
                #print ('Type of w is %s', type(w))
                if is_sip_wrapped(w):
                    res = w.customEvent(event)
                    if res and event.isAccepted():
                        return res
                    elif w.receivers(event.signal) != 0:    
                        w.emit(event.signal, event.source, *event.largs)
                w = w.parent()
        return super(PMXApplication, self).notify(receiver, event)

def is_sip_wrapped(instance):
    try:
        instance.sender()
    except RuntimeError:
        return False
    return True
    
import res_rc #@UnresolvedImport @UnusedImport
