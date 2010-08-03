# -*- coding: utf-8 -*-
# encoding: utf-8
from PyQt4.QtGui import QApplication, QMessageBox, QSplashScreen, QPixmap, QIcon
from PyQt4.QtCore import SIGNAL

from os.path import join, exists, isdir, isabs

from os import getpid, unlink, getcwd
from os.path import dirname, abspath
from prymatex.lib.deco import printtime

from prymatex.lib.exceptions import AlreadyRunningError
from prymatex.lib.textmate import load_textmate_bundles, load_textmate_themes
        
import prymatex

BASE_PATH = dirname(__file__)

import logging
logger = logging.getLogger(__name__)

class PMXApplication(QApplication):
    
    __config = None
    __res_mngr = None
    
    @printtime
    def __init__(self, arguments):
        '''
        Inicialización de la aplicación.
        '''
        QApplication.__init__(self, arguments)
        
        from prymatex.optargs import parser
        self.options, args = parser.parse_args(arguments) # Options are readonly
        files_to_open = args[1:]
        
        self.init_application_params()
        self.init_config()
        self.init_resources()
        self.res_mngr.loadStyleSheet()
        
        self.splash = QSplashScreen(QPixmap(":/resources/Prymatex_Splash.png"))
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
    
    def _get_current_editor(self):
        '''
        Shortcut al editor actual
        '''
        return self.main_window.tabWidgetEditors.currentWidget()
        
    
    current_editor = property(_get_current_editor)
    
    def init_application_params(self):
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
        logger.info("Save config")
        self.config.save()
        logger.info("Config saved")
    
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
                logger.warning("The theme dir does not exist: %s", dirname)
            
        self.splash.showMessage(_("%d themes loaded", themes))
        QApplication.processEvents()
    
    # Decorador para imprimir cuanto tarda
    @printtime
    def load_texmate_bundles(self):
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
                logger.warning("The theme dir does not exist")
                
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
            logger.info("Checking for another instance: %s", 
                        pid in os.pid_proc_dict()
                        )
            if pid in os.pid_proc_dict():
                from prymatex.lib.i18n import ugettext as _
                logger.warning("Another app running")
                QMessageBox.critical(None, _('Application Already Running'),
                                     _('''%s seems to be runnig. Please
                                     close the other instance.''', self.applicationName()),
                                     QMessageBox.Ok)
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

            
import res_rc