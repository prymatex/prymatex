#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Cosas interesantes
#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html
#http://www.qtcentre.org/wiki/index.php?title=Extended_Main_Window
import os, sys

from PyQt4 import QtGui, QtCore

import prymatex
from prymatex.core import exceptions
from prymatex import resources_rc

from prymatex.utils import coroutines
from prymatex.utils import decorator as deco
from prymatex.utils.i18n import ugettext as _

class PMXApplication(QtGui.QApplication):
    """
    The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the PMX Support.
    """
    
    def __init__(self, profile, args):
        """
        Inicialización de la aplicación.
        """
        QtGui.QApplication.__init__(self, args)
        
        # Some init's
        self.setApplicationName(prymatex.__name__)
        self.setApplicationVersion(prymatex.__version__)
        self.setOrganizationDomain(prymatex.__url__)
        self.setOrganizationName(prymatex.__author__)

        self.buildSettings(profile)
        
        self.setupLogging()

        #Connects
        self.aboutToQuit.connect(self.closePrymatex)
        
        self.initialArguments = args
    
    def exec_(self):
        splash = QtGui.QSplashScreen(QtGui.QPixmap(":/images/prymatex/Prymatex_Splash.svg"))
        splash.show()

        # Loads
        self.setupSupportManager(callbackSplashMessage = splash.showMessage)   #Support Manager
        self.setupFileManager()      #File Manager
        self.setupProjectManager()   #Project Manager
        self.setupKernelManager()    #Console kernel Manager
        self.setupCoroutines()
        self.setupZeroMQContext()

        # Setup Dialogs
        self.setupDialogs()         #Config Dialog
        
        # Creates the GUI
        self.createMainWindow()

        splash.finish(self.mainWindow)
        return super(PMXApplication, self).exec_()

    def resetSettings(self):
        self.settings.clear()
        
    def buildSettings(self, profile):
        from prymatex.core.settings import PMXSettings
        self.settings = PMXSettings(profile)

    def checkSingleInstance(self):
        """
        Checks if there's another instance using current profile
        """
        self.fileLock = os.path.join(self.settings.PMX_VAR_PATH, 'prymatex.pid')

        if os.path.exists(self.fileLock):
            #Mejorar esto
            pass
            #raise exceptions.AlreadyRunningError('%s seems to be runnig. Please close the instance or run other profile.' % (self.settings.PMX_PROFILE_NAME))
        else:
            f = open(self.fileLock, 'w')
            f.write('%s' % self.applicationPid())
            f.close()

    def setupLogging(self):
        """
        @see PMXObject.debug, PMXObject.info, PMXObject.warn
        """
        import logging
        from datetime import datetime
        
        # File name
        d = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        filename = os.path.join(self.settings.PMX_LOG_PATH, 'messages-%s.log' % d)
        logging.basicConfig(filename=filename, level=logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        logging.root.addHandler(ch)
        logging.root.info("Application startup")
        logging.root.debug("Application startup debug")
        
        self.logger = logging.root

    #========================================================
    # Managers
    #========================================================
    @deco.logtime
    def setupSupportManager(self, callbackSplashMessage = None):
        from prymatex.gui.support.manager import PMXSupportManager

        sharePath = self.settings.value('PMX_SHARE_PATH')
        homePath = self.settings.value('PMX_HOME_PATH')

        #Prepare prymatex namespace
        manager = PMXSupportManager(self)
        manager.addNamespace('prymatex', sharePath)
        manager.updateEnvironment({ #TextMate Compatible :P
                'TM_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'TM_SUPPORT_PATH': manager.environment['PMX_SUPPORT_PATH'],
                'TM_BUNDLES_PATH': manager.environment['PMX_BUNDLES_PATH'],
                'TM_THEMES_PATH': manager.environment['PMX_THEMES_PATH'],
                'TM_PID': os.getpid(),
                #Prymatex 
                'PMX_APP_NAME': self.applicationName().title(),
                'PMX_APP_PATH': self.settings.value('PMX_APP_PATH'),
                'PMX_PREFERENCES_PATH': self.settings.value('PMX_PREFERENCES_PATH'),
                'PMX_VERSION': self.applicationVersion(),
                'PMX_PID': self.applicationPid()
        })

        #Prepare user namespace
        manager.addNamespace('user', homePath)
        manager.updateEnvironment({
                'PMX_HOME_PATH': homePath,
                'PMX_PROFILE_PATH': self.settings.value('PMX_PROFILE_PATH'),
                'PMX_TMP_PATH': self.settings.value('PMX_TMP_PATH'),
                'PMX_LOG_PATH': self.settings.value('PMX_LOG_PATH')
        })
        manager.loadSupport(callbackSplashMessage)
        self.supportManager = manager

    def setupFileManager(self):
        from prymatex.core.filemanager import PMXFileManager
        self.fileManager = PMXFileManager(self)
    
    def setupProjectManager(self):
        from prymatex.gui.project.manager import PMXProjectManager
        self.projectManager = PMXProjectManager(self)
        self.projectManager.loadProject()
    
    def setupKernelManager(self):
        try:
            from IPython.frontend.qt.kernelmanager import QtKernelManager
            self.kernelManager = QtKernelManager()
            self.kernelManager.start_kernel()
            self.kernelManager.start_channels()
        except ImportError:
            self.kernelManager = None

    def setupCoroutines(self):
        self.scheduler = coroutines.Scheduler(self)

    def setupZeroMQContext(self):
        from prymatex.utils import zeromqt
        self.zmqContext = zeromqt.ZeroMQTContext(parent = self)

    #========================================================
    # Dialogs
    #========================================================
    def setupDialogs(self):
        #Settings
        from prymatex.gui.settings.dialog import PMXSettingsDialog
        from prymatex.gui.settings.widgets import PMXGeneralWidget, PMXNetworkWidget
        from prymatex.gui.settings.environment import PMXEnvVariablesWidgets
        from prymatex.gui.settings.themes import PMXThemeConfigWidget
        from prymatex.gui.settings.widgets import PMXFileManagerSettings
        self.configDialog = PMXSettingsDialog(self)
        self.configDialog.register(PMXGeneralWidget())
        self.configDialog.register(PMXFileManagerSettings())
        self.configDialog.register(PMXThemeConfigWidget())
        self.configDialog.register(PMXEnvVariablesWidgets())
        self.configDialog.register(PMXNetworkWidget())
        
        #Bundle Editor
        from prymatex.gui.support.bundleeditor import PMXBundleEditor
        self.bundleEditor = PMXBundleEditor(self)
        #self.bundleEditor.setModal(True)
        
        #Dialog System
        from prymatex.pmxdialog.base import PMXDialogSystem
        self.dialogSystem = PMXDialogSystem(self)
        
    def closePrymatex(self):
        self.logger.debug("Close")
        self.settings.setValue("mainWindowGeometry", self.mainWindow.saveGeometry())
        self.settings.setValue("mainWindowState", self.mainWindow.saveState())
        self.settings.sync()
        os.unlink(self.fileLock)
    
    def commitData(self):
        print "Commit data"
        
    def saveState(self, session_manager):
        self.logger.debug( "Save state %s" % session_manager)
    
    #---------------------------------------------------
    # Editors and mainWindow handle
    #---------------------------------------------------
    def createMainWindow(self):
        """
        Creates the windows
        """
        #Por ahora solo una mainWindow
        from prymatex.gui.mainwindow import PMXMainWindow
        geometry = self.settings.value("mainWindowGeometry")
        state = self.settings.value("mainWindowState")
        
        self.mainWindow = PMXMainWindow(self)
        if geometry:
            self.mainWindow.restoreGeometry(geometry)
        if state:
            self.mainWindow.restoreState(state)
        self.mainWindow.show()
        # Open files
        self.openFilePaths(self.initialArguments[1:])

    def findEditorForFile(self, filePath):
        #Para cada mainwindow buscar el editor
        return self.mainWindow, self.mainWindow.findEditorForFile(filePath)
            
    def getEditorInstance(self, filePath = None, parent = None):
        from prymatex.gui.codeeditor.editor import PMXCodeEditor
        return PMXCodeEditor.newInstance(self, filePath, parent)

    def openFile(self, filePath, cursorPosition = (0,0), focus = True):
        if self.fileManager.isOpen(filePath):
            mainWindow, editor = self.findEditorForFile(filePath)
            if editor is not None:
                mainWindow.setCurrentEditor(editor)
                editor.setCursorPosition(cursorPosition)
        else:
            self.mainWindow.tryCloseEmptyEditor()
            editor = self.getEditorInstance(filePath, self)
            def appendChunksTask(editor, filePath):
                content = self.fileManager.openFile(filePath)
                editor.setReadOnly(True)
                for line in content.splitlines():
                    editor.appendPlainText(line)
                    yield
                editor.setModified(False)
                editor.setReadOnly(False)
                yield coroutines.Return(editor, filePath)
            def on_editorReady(result):
                editor, filePath = result.value
                editor.setFilePath(filePath)
                self.mainWindow.addEditor(editor, focus)
            task = self.scheduler.newTask( appendChunksTask(editor, filePath) )
            task.done.connect( on_editorReady  )
    
    # FIXME: Refactor
    def openFilePaths(self, filePaths):
        if not isinstance(filePaths, (list, tuple)):
            filePaths = [filePaths, ]
        from prymatex.gui.mainwindow import PMXMainWindow
        mainwindows = filter(lambda w: isinstance(w, PMXMainWindow),  self.allWidgets())
        if not mainwindows:
            QtGui.QMessageBox.critical("No Main Window", "No window found while trying to open a file")
            return
        mw = mainwindows[0]
        for filePath in filter(lambda f: os.path.exists(f), filePaths):
            if os.path.isfile(filePath):
                mw.openLocalPath(filePath)
            else:
                self.openAllSupportedFilesInDirectory(filePath)
    
    def openAllSupportedFilesInDirectory(self, filePaths):
        raise NotImplementedError("Directory contents should be opened as files here")
        
    #---------------------------------------------------
    # Exceptions, Print exceptions in a window
    #---------------------------------------------------
    def replaceSysExceptHook(self):
        def displayExceptionDialog(exctype, value, traceback):
            ''' Display a nice dialog showing the python traceback'''
            from prymatex.gui.emergency.tracedialog import PMXTraceBackDialog
            sys.__excepthook__(exctype, value, traceback)
            PMXTraceBackDialog.fromSysExceptHook(exctype, value, traceback).exec_()

        sys.excepthook = displayExceptionDialog
