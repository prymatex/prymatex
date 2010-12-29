# -*- coding: utf-8 -*-
# encoding: utf-8
from PyQt4.QtGui import QApplication, QMessageBox, QSplashScreen, QPixmap, QIcon
from PyQt4.QtCore import SIGNAL, QEvent

from os.path import join, exists, isdir, isabs

from os import getpid, unlink, getcwd
from os.path import dirname, abspath
from prymatex.lib.deco import printtime, logtime

from optparse import OptionParser

BASE_PATH = dirname(__file__)

def infinite_generator(initial = 0):
    ''' A simple integer generator for unique
    endless sequences, such as "Untitled %d" files and such
    '''
    while True:
        yield initial
        initial += 1 

class PMXApplication(QApplication):
    '''
    The application instance.
    It's loaded only one time for every application instance, so some counters
    and shared data that need to be correctly updaded upon close are held here.
    '''
    
    __config = None
    __res_mngr = None
    __logger = None
    
    #@printtime
    @logtime
    def __init__(self, arguments, logger = None):
        '''
        Inicialización de la aplicación.
        '''
        QApplication.__init__(self, arguments)
        # Logger setup
        self.setup_logging()
        from prymatex.optargs import parser
        self.options, args = parser.parse_args(arguments) # Options are readonly
        files_to_open = args[1:]
        
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
        
        # Settings
        
        
        # Bundles and Stuff
        self.load_texmate_themes()
        self.load_texmate_bundles()
        
        from prymatex.gui.mainwindow import PMXMainWindow
        self.main_window = PMXMainWindow()
        self.splash.finish(self.main_window)
        self.main_window.show()
        
        self.connect(self, SIGNAL('aboutToQuit()'), self.cleanup)
        self.connect(self, SIGNAL('aboutToQuit()'), self.save_config)
    
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
        
    
    def parse_args(self, args):
        '''
        Parse command line arguments through optparse library.
        
        This parsing could halt the application.
        '''
        parser = OptionParser(version = self.applicationVersion(),
                                description = self.applicationName(), 
                                prog = 'prymatex', 
                                epilog = "")
    
        parser.add_option('-s', '--session', dest="session",
                          help="Name of the session")
        parser.add_option('-l', '--last', dest="last",
                          help="Load last session")
        
        opts, files = parser.parse_args(argv)
    
    @property
    def untitled_counter(self):
        '''
        Returns current untitled counter value.
        '''
        return self.__untitled_counter
    
    def get_inc_untitled_counter(self):
        '''
        Gets the untitled counter
        '''
        v = self.__untitled_counter
        self.__untitled_counter += 1
        return v
        
    def _get_current_editor(self):
        '''
        Shortcut al editor actual
        '''
        return self.main_window.tabWidgetEditors.currentWidget()
        
    
    current_editor = property(_get_current_editor)
    
    def init_application_params(self):
        import prymatex
        self.setApplicationName(prymatex.PRODUCT_NAME)
        self.setApplicationVersion(prymatex.VERSION) # hg stuff?
        self.setOrganizationDomain("org")
        self.projectUrl = prymatex.PROJECT_HOME    
    
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
            self.__res_mngr = ResourceManager(BASE_PATH)
        
    def init_config(self):
        if not self.__config:
            from prymatex.config import settings
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
    
    def deferred_load_texmate_bundles(self):
        '''
        Crea una lista de los paths abslutos de donde se cargan
        bundles y lanza un hilo para cargarlos.
        '''
        from prymatex.lib.textmate.loader import PMXBundleLoaderThread
        
        path_list = []
        for dirname in self.config.TEXTMATE_BUNDLES_PATHS:
            if isdir(dirname):
                if not isabs(dirname):
                    dirname = join(getcwd(), dirname)
                path_list.append(dirname)
        self.bundle_thread = PMXBundleLoaderThread(path_list, self)
        self.bundle_thread.start()
    
    def load_texmate_themes(self):
        '''
        Load textmate Bundles and Themes
        '''
        from prymatex.lib.textmate import load_textmate_themes
        from prymatex.lib.i18n import ugettext as _
        if not all(map(lambda x: hasattr(self.config, x), ('TEXTMATE_THEMES_PATHS',
                                                           'TEXTMATE_BUNDLES_PATHS' ))):
            QMessageBox.critical(self, _("Fatal Error"), 
                                 _("No bundle dirs have been found in config file."))
        
        self.splash.showMessage(_("Loading themes..."))
        themes = 0
        for dirname in self.config.TEXTMATE_THEMES_PATHS:
            if isdir(dirname):
                if not isabs(dirname):
                    dirname = join(getcwd(), dirname)
                themes += load_textmate_themes(dirname)
                
            else:
                self.logger.warning("The theme dir does not exist: %s", dirname)
            
        self.splash.showMessage(_("%d themes loaded", themes))
        QApplication.processEvents()
    
    # Decorador para imprimir cuanto tarda
    @logtime
    def load_texmate_bundles(self):
        from prymatex.lib.textmate import load_textmate_bundles
        from prymatex.lib.i18n import ugettext as _
        bundles = 0
        splash = self.splash
        def before_load_callback(counter, total, name):
            progress = (float(counter) / total) * 100
            splash.showMessage(_("Loading bundle %s\n%4d of %4d (%.d%%)", 
                                 name, counter, total, progress))
            QApplication.processEvents()
            
        for dirname in self.config.TEXTMATE_BUNDLES_PATHS:
            self.splash.showMessage(_("Loading bundles..."))
            if isdir(dirname):
                if not isabs(dirname):
                    dirname = join(getcwd(), dirname) 
                bundles += load_textmate_bundles(dirname, before_load_callback)
            else:
                self.logger.warning("The theme dir does not exist")
                
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
                res = w.customEvent(event);
                if res and event.isAccepted():
                    return res
                w = w.parent()
        return super(PMXApplication, self).notify(receiver, event)

import res_rc
