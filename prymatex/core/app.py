#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Cosas interesantes
#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html
#http://www.qtcentre.org/wiki/index.php?title=Extended_Main_Window
import os, sys

from PyQt4 import QtGui, QtCore

import prymatex
from prymatex import resources_rc
from prymatex.utils import decorator as deco
from prymatex.utils.i18n import ugettext as _

from prymatex.gui.emergency.tracedialog import PMXTraceBackDialog

# ipdb handling

sys_excepthook = sys.excepthook
class PMXApplication(QtGui.QApplication):
    '''
    The application instance.
    There can't be two apps running simultaneously, since configuration issues
    may occur.
    The application loads the PMX Support.
    '''
    
    #@printtime
    @deco.logtime
    def __init__(self, args, profile):
        '''
        Inicialización de la aplicación.
        '''
        super(PMXApplication, self).__init__(args)
        
        # Some init's
        self.setApplicationName(prymatex.__doc__)
        self.setApplicationVersion(prymatex.get_version())
        self.setOrganizationDomain("org")
        self.projectUrl = prymatex.__url__    

        self.checkSingleInstance()
        
        splash = QtGui.QSplashScreen(QtGui.QPixmap(":/images/prymatex/Prymatex_Splash.svg"))
        splash.show()
        
        # Setups
        self.setupSettings(profile) #Settings
        self.setupExecutor()        #Executor
        self.setupLogging()         #Logging
        self.setupFileManager()     #File Manager
        self.setupConfigDialog()    #Config Dialog
        self.setupBundleEditor()    #Bundle Editor
        
        # Loads
        self.loadSupportManager()   #Support Manager
        self.loadKernelManager()    #Console kernel Manager
        
        # Creates the GUI
        self.createWindows(args[1:]) # Skip pmx.py
        
        # Print exceptions in a window
        self.replaceSysExceptHook()
        
        self.createRPCThread()

        splash.finish()
        
        self.aboutToQuit.connect(self.cleanup)
        
    def setupConfigDialog(self):
        from prymatex.gui.config.configdialog import  PMXSettingsDialog
        configdialog = PMXSettingsDialog()
        from prymatex.gui.config.widgets import PMXGeneralWidget,\
                                                PMXUpdatesWidget,\
                                                PMXSaveWidget,\
                                                PMXNetworkWidget,\
                                                PMXBundleWidget
        from prymatex.gui.config.environment import PMXEnvVariablesWidgets
        from prymatex.gui.config.themes import PMXThemeConfigWidget
                                                
        configdialog.register(PMXGeneralWidget())
        configdialog.register(PMXThemeConfigWidget())
        configdialog.register(PMXUpdatesWidget())
        configdialog.register(PMXSaveWidget())
        configdialog.register(PMXBundleWidget())
        configdialog.register(PMXEnvVariablesWidgets())
        configdialog.register(PMXNetworkWidget())
        self.configDialog = configdialog
    
    def setupSettings(self, profile):
        from prymatex.core.settings import PMXSettings
        self.settings = PMXSettings.getSettingsForProfile(profile)
    
    def setupExecutor(self):
        from concurrent import futures
        self.executor = futures.ThreadPoolExecutor(max_workers=5)
    
    def setupBundleEditor(self):
        from prymatex.gui.support.bundleeditor import PMXBundleEditor
        self.bundleEditor = PMXBundleEditor()

    def setupFileManager(self):
        from prymatex.core.filemanager import PMXFileManager
        self.fileManager = PMXFileManager(self)

    def setupLogging(self):
        '''
        @see PMXObject.debug, PMXObject.info, PMXObject.warn
        '''
        import logging
        from datetime import datetime
        
        # File name
        d = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        filename = os.path.join(self.settings.PMX_LOG_PATH, 'messages-%s.log' % d)
        logging.basicConfig(filename=filename, level=logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        logging.root.addHandler(ch)
        logging.root.info("Application startup")
        
    def createWindows(self, files_to_open):
        '''
        Creates the windows
        '''
        from prymatex.gui.mainwindow import PMXMainWindow
        self.windows = []
        first_window = PMXMainWindow()
        first_window.show()
        self.windows.append(first_window)   # Could it be possible to hold it in
                                            # its childrens?
                                            
    def cleanup(self):
        self.settings.sync()
    
    def commitData(self):
        print "Commit data"
        
    def saveState(self, session_manager):
        print "Save state", session_manager
        
    def loadKernelManager(self):
        from IPython.frontend.qt.kernelmanager import QtKernelManager
        self.kernelManager = QtKernelManager()
        self.kernelManager.start_kernel()
        self.kernelManager.start_channels()
        
    # Decorador para imprimir cuanto tarda
    @deco.logtime
    def loadSupportManager(self):
        # Lazy load
        from prymatex.gui.support.manager import PMXSupportManager

        sharePath = self.settings.value('PMX_SHARE_PATH')
        homePath = self.settings.value('PMX_HOME_PATH')

        # esto hacerlo una propiedad del manager que corresponda
        disabled = self.settings.value("disabledBundles") if self.settings.value("disabledBundles") != None else []
        #manager = PMXSupportManager(disabledBundles = [], deletedBundles = [])
        manager = PMXSupportManager()
        manager.addNamespace('prymatex', sharePath)
        manager.updateEnvironment({ #TextMate Compatible :P
                'TM_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'TM_SUPPORT_PATH': manager.environment['PMX_SUPPORT_PATH'],
                'TM_BUNDLES_PATH': manager.environment['PMX_BUNDLES_PATH'],
                'TM_THEMES_PATH': manager.environment['PMX_THEMES_PATH'],
                'TM_PID': os.getpid(),
                #Prymatex 
                'PMX_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'PMX_PREFERENCES_PATH': self.settings.value('PMX_PREFERENCES_PATH'),
                'PMX_VERSION': prymatex.get_version(),
                'PMX_PID': os.getpid()
        });

        manager.addNamespace('user', homePath)
        manager.updateEnvironment({ ##User
                'PMX_HOME_PATH': homePath,
                'PMX_PROFILE_PATH': self.settings.value('PMX_PROFILE_PATH'),
                'PMX_TMP_PATH': self.settings.value('PMX_TMP_PATH'),
                'PMX_LOG_PATH': self.settings.value('PMX_LOG_PATH')
        });
        
        splash = self.splash
        
        self.splash.showMessage("Loading bundles...")
        manager.loadSupport()
        self.supportManager = manager

    def checkSingleInstance(self):
        '''
        Checks if there's another instance using current profile
        '''
        from prymatex.utils._os import pid_proc_dict
        
        lock_filename = os.path.join(self.settings.PMX_VAR_PATH, 'prymatex.pid')
        
        if os.path.exists(lock_filename):
            f = open(lock_filename)
            pid = int(f.read())
            f.close()
            self.logger.info("Checking for another instance: %s", pid in pid_proc_dict())
            if pid in pid_proc_dict():
                self.logger.warning("Another app running")
                QtGui.QMessageBox.critical(None, _('Application Already Running'),
                                     _('''%s seems to be runnig. Please
                                     close the other instance.''' % self.applicationName()),
                                     QtGui.QMessageBox.Ok)
                from prymatex.utils.exceptions import AlreadyRunningError
                raise AlreadyRunningError(pid)
            
        else:
            f = open(lock_filename, 'w')
            f.write('%s' % os.getpid())
            f.close()

            
    def createRPCThread(self):
        from prymatex.core.rpcserver import PMXXMLRPCServerThread
        self.RPCServerThread = PMXXMLRPCServerThread(self)
        self.RPCServerThread.start()

        
    def displayApplicationException(self, exctype, value, traceback):
        ''' Display a nice dialog showing the python traceback'''
        # run original trace
        sys.__excepthook__(exctype, value, traceback)
        print "displayApplicationException", exctype, value, traceback, type(traceback)
        dialog = PMXTraceBackDialog.fromSysExceptHook(exctype, value, traceback)
        dialog.exec_()
        

    def replaceSysExceptHook(self):
        sys.excepthook = self.displayApplicationException
