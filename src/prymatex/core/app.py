# -*- coding: utf-8 -*-
# encoding: utf-8
import os, sys
from os import getpid, unlink
from os.path import join, exists, dirname, abspath, expanduser
from datetime import datetime

from PyQt4.QtGui import QApplication, QMessageBox, QSplashScreen, QPixmap, QIcon
from PyQt4.QtCore import SIGNAL, QEvent

from prymatex.lib import deco
from prymatex.core.config import PMXSettings
#from prymatex.support import PMXSupportManager
from logging import getLogger
logger = getLogger(__name__)

# ipdb handling

sys_excepthook = sys.excepthook
class PMXApplication(QApplication):
    '''
    The application instance.
    There can't be two apps running simultaneously, since configuration issues
    may occur.
    The application loads the PMX Support.
    '''
    
    #===========================================================================
    # Settings 
    # Saved when the application is about to close
    #===========================================================================
    __settings = None
    __configdialog = None
    __options = None # Optparse options
    #===========================================================================
    # Logger, deprecated in favour of module level logger
    #===========================================================================
    __logger = None
    #===========================================================================
    # Command Line Arguments
    #===========================================================================
    __options = None 
    #===========================================================================
    # File manager
    #===========================================================================
    __file_manager = None
    #===========================================================================
    # Bundle Editor
    #===========================================================================
    __bundle_editor = None
    
    #@printtime
    @deco.logtime
    def __init__(self, open_args, options):
        '''
        Inicialización de la aplicación.
        '''
        self.options = options
        QApplication.__init__(self, [])
        # Logger setup
        self.setup_logging() 
        
        
        self.settings = PMXSettings.getSettingsForProfile(self.options.profile)
        self.settings.setValue('auto_save', True)
        self.settings.setValue('auto_save_interval', 30)
        # Some init's
        self.init_application_params()
        
        #self.res_mngr.loadStyleSheet()
        
        self.setup_splash()
        
        
        self.setWindowIcon(QIcon(":/resources/icons/Prymatex_Logo.png"))
        
        self.checkSingleInstance()
        
        # Bundles and Stuff
        self.load_stuff()
        
        self.connect(self, SIGNAL('aboutToQuit()'), self.cleanup)
        self.aboutToQuit.connect(self.settings.sync)
        
        self.setup_file_manager()
        # Config dialog
        self.setup_configdialog()
        # Creates the GUI
        self.createWindows(open_args[1:]) # Skip pmx.py
        
    
    @property
    def options(self):
        return self.__options
    
    @options.setter
    def options(self, options):
        if self.__options:
            raise ValueError("Options already defined")
        from optparse import Values
        if not isinstance(options, Values):
            raise ValueError("Options should be optparse.Values instances"
                             ", not %s" % options)
        self.__options = options
            
    def setup_configdialog(self):
        from prymatex.gui.config import  PMXSettingsDialog
        configdialog = PMXSettingsDialog()
        from prymatex.gui.config.widgets import PMXGeneralWidget,\
                                                PMXUpdatesWidget,\
                                                PMXSaveWidget,\
                                                PMXNetworkWidget,\
                                                PMXBundleWidget
        from prymatex.gui.config.envvars import PMXEnvVariablesWidgets
        from prymatex.gui.config.font_and_theme import PMXThemeConfigWidget
                                                
        configdialog.register(PMXGeneralWidget())
        configdialog.register(PMXThemeConfigWidget())
        configdialog.register(PMXUpdatesWidget())
        configdialog.register(PMXSaveWidget())
        configdialog.register(PMXBundleWidget())
        configdialog.register(PMXEnvVariablesWidgets())
        configdialog.register(PMXNetworkWidget())
        self.__configdialog = configdialog
    
    def show_bundle_editor(self):
        #TODO: terminar esto
        if self.__bundle_editor == None:
            from prymatex.gui.bundle_editor import PMXBundleEditor
            self.__bundle_editor = PMXBundleEditor()
        self.__bundle_editor.show()
    
    @property
    def configdialog(self):
        return self.__configdialog
    
    _bundleItemModel  = None
    @property
    def bundleItemModel(self):
        return self.manager.model
    
    #Deprecated
    @property
    def bundleManager(self):
        return self.__supportManager

    __supportManager = None
    @property
    def supportManager(self):
        return self.__supportManager
        
    def load_stuff(self):
        if not self.options.no_bundles:
            self.__supportManager = self.load_support()
        
    def setup_splash(self):
        self.splash = QSplashScreen(QPixmap(":/images/resources/prymatex/Prymatex_Splash.svg"))
        self.splash.show()
    
    def setup_file_manager(self):
        from prymatex.core.filemanager import PMXFileManager
        self.__file_manager = PMXFileManager(self)
    
    
    @property
    def file_manager(self):
        return self.__file_manager
    
    @file_manager.setter
    def file_manager(self, value):
        assert self.__file_manager is None
        from prymatex.core.filemanager import PMXFileManager
        assert isinstance(value, PMXFileManager)
        self.__file_manager = value
        
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
        '''
        @see PMXObject.debug, PMXObject.info, PMXObject.warn
        '''
        import logging
        
        logger = logging.getLogger("")
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        d = datetime.now().strftime('%d-%m-%G-%H-%M-%S')
        filename = self.getProfilePath('log', 'messages-%s.log' % d)
        try:
            fh = logging.FileHandler(filename)
        except IOError:
            fh =  logging.FileHandler()
        
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
        base_path = dirname(abspath(__file__))
        return join(base_path,  'LOCK')
    
    def cleanup(self):
        try:
            unlink(self.lock_filename)
        except:
            pass
    
    def commitData(self):
        print "Commit data"
        
    def saveState(self, session_manager):
        print "Save state", session_manager
        
    # Decorador para imprimir cuanto tarda
    @deco.logtime
    def load_support(self):
        # Lazy load
        from prymatex.gui.bundles.manager import PMXTableSupportManager

        sharePath = self.settings.value('PMX_SHARE_PATH')
        userPath = self.settings.value('PMX_USER_PATH')

        # esto hacerlo una propiedad del manager que corresponda
        disabled = self.settings.value("disabledBundles") if self.settings.value("disabledBundles") != None else []
        #manager = PMXSupportManager(disabledBundles = [], deletedBundles = [])
        manager = PMXTableSupportManager()
        manager.addNamespace('prymatex', sharePath)
        manager.updateEnvironment({ #TextMate Compatible :P
                'TM_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'TM_SUPPORT_PATH': manager.environment['PMX_SUPPORT_PATH'],
                'TM_BUNDLES_PATH': manager.environment['PMX_BUNDLES_PATH'],
                'TM_THEMES_PATH': manager.environment['PMX_THEMES_PATH'],
                #Prymatex 
                'PMX_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'PMX_PREFERENCES_PATH': self.settings.value('PMX_PREFERENCES_PATH')
        });

        manager.addNamespace('user', userPath)
        manager.updateEnvironment({ ##User
                'PMX_USER_PATH': userPath,
                'PMX_PROFILE_PATH': self.settings.value('PMX_PROFILE_PATH'),
                'PMX_TMP_PATH': self.settings.value('PMX_TMP_PATH'),
                'PMX_LOG_PATH': self.settings.value('PMX_LOG_PATH')
        });
        
        splash = self.splash
        
        def update_splash_popullate_model(counter, total, name, bundle, **kwargs):
            progress = (float(counter) / total) * 100
            splash.showMessage("Loading bundle %s\n%4d of %4d (%.d%%)", 
                                 name, counter, total, progress)
            # Loose coupling 
            #QApplication.processEvents()
            #bundleItemModel = QApplication.instance().bundleItemModel
            #bundleItemModel.appendRowFromBundle( bundle )
        
        self.splash.showMessage("Loading bundles...")
                        
        manager.loadSupport()
        return manager

    def checkSingleInstance(self):
        '''
        Checks if there's another instance using current profile
        '''
        from prymatex.lib import os
        
        lock_filename = self.getProfilePath('var', 'prymatex.pid')
        
        if exists(lock_filename):
            f = open(lock_filename)
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
            f = open(lock_filename, 'w')
            f.write('%s' % getpid())
            f.close()
    
    __profilePath = None
    @property
    def profilePath(self):
        if not self.__profilePath:
            self.__profilePath = join(expanduser('~'), '.prymatex')
        return self.__profilePath
    
    
    #@deco.printparams_and_output
    def getProfilePath(self, what, filename):
        '''
        Example
        
        self.getProfilePath('tmp', 'log.log')
        
        '''
        #from prymatex.core.config import get_prymatex_profile_path, get_prymatex_base_path
        path = join(self.profilePath, self.options.profile )
        final_path = abspath(join(path, what))
        if not exists(final_path):
            os.makedirs(final_path, 0700)
        return join(final_path, filename)
        
            
    def startDirectory(self):
        '''
        Returns the start dir
        '''
        if self.options.startdir and exists(self.options.startdir):
            return abspath(self.options.startdir)
        else:
            #from prymatex.lib.os import get_homedir
            #return get_homedir()
            return os.getcwd()

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
