#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Cosas interesantes
#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html
import os
import sys
import logging
import inspect

from PyQt4 import QtGui, QtCore

import prymatex
from prymatex import resources
from prymatex.core import exceptions

from prymatex.utils.decorator import deprecated
from prymatex.utils import coroutines
from prymatex.utils import decorator as deco
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.style import PrymatexStyle

class PMXApplication(QtGui.QApplication):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the PMX Support."""
    
    def __init__(self, profile):
        """Inicializaci�n de la aplicaci�n."""
        #TODO: Pasar los argumentos a la QApplication
        QtGui.QApplication.__init__(self, [])
        self.setStyleSheet(resources.APPLICATION_STYLE)
        
        # Some init's
        self.setApplicationName(prymatex.__name__)
        self.setApplicationVersion(prymatex.__version__)
        self.setOrganizationDomain(prymatex.__url__)
        self.setOrganizationName(prymatex.__author__)

        self.buildSettings(profile)
        
        #Connects
        self.aboutToQuit.connect(self.closePrymatex)

    def loadGraphicalUserInterface(self):
        splash = QtGui.QSplashScreen(QtGui.QPixmap(":/images/prymatex/Prymatex_Splash.svg"))
        splash.show()
        try:
            
            self.setupPluginManager()     #Prepare plugin manager

            #TODO: Cambiar los setup por build, que retornen los manager
            # Loads
            self.supportManager = self.setupSupportManager()    #Support Manager
            self.fileManager = self.setupFileManager()          #File Manager
            self.projectManager = self.setupProjectManager()                                              #Project Manager
            self.setupKernelManager()                           #Console kernel Manager
            self.setupCoroutines()
            self.setupZeroMQContext()
            self.setupMainWindow()
            
            # Setup Dialogs
            self.setupDialogs()
            
            #Connect all loads
            self.projectManager.loadProject()
            self.supportManager.loadSupport(splash.showMessage)
            self.settingsDialog.loadSettings()
            
            # Creates the Main Window
            self.createMainWindow()
            
            splash.finish(self.mainWindow)

        except KeyboardInterrupt:
            self.logger.critical("\nQuit signal catched during application startup. Quiting...")
            self.quit()
            
    def resetSettings(self):
        self.settings.clear()
        
    def buildSettings(self, profile):
        from prymatex.gui.dialogs.settings import PMXSettingsDialog
        from prymatex.core.settings import PMXSettings
        self.settings = PMXSettings(profile)
        self.settingsDialog = PMXSettingsDialog(self)

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

    #========================================================
    # Logging system and loggers
    #========================================================
    def getLogger(self, name):
        """ return logger, for filter by name in future """
        return logging.getLogger(name)
        
    def setupLogging(self, verbose):
        from datetime import datetime
        
        level = [ logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG ][verbose % 5]
        
        # File name
        d = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        filename = os.path.join(self.settings.PMX_LOG_PATH, 'messages-%s.log' % d)
        logging.basicConfig(filename = filename, level=level)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        logging.root.addHandler(ch)
        logging.root.info("Application startup")
        logging.root.debug("Application startup debug")

        self.logger = logging.root

    #========================================================
    # Managers
    #========================================================
    @deco.logtime
    def setupSupportManager(self):
        from prymatex.gui.support.manager import PMXSupportManager
        
        self.pluginManager.prepareWidgetPlugin(PMXSupportManager)

        manager = PMXSupportManager(self)
        self.settings.configure(manager)
        
        #Prepare prymatex namespace
        sharePath = self.settings.value('PMX_SHARE_PATH')
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
        homePath = self.settings.value('PMX_HOME_PATH')
        manager.addNamespace('user', homePath)
        manager.updateEnvironment({
                'PMX_HOME_PATH': homePath,
                'PMX_PROFILE_PATH': self.settings.value('PMX_PROFILE_PATH'),
                'PMX_TMP_PATH': self.settings.value('PMX_TMP_PATH'),
                'PMX_LOG_PATH': self.settings.value('PMX_LOG_PATH')
        })
        return manager

    def setupFileManager(self):
        from prymatex.core.filemanager import PMXFileManager
        
        self.pluginManager.prepareWidgetPlugin(PMXFileManager)

        manager = PMXFileManager(self)
        self.settings.configure(manager)
        
        manager.filesytemChange.connect(self.on_filesytemChange)
        return manager
    
    def setupProjectManager(self):
        from prymatex.gui.project.manager import PMXProjectManager
        
        self.pluginManager.prepareWidgetPlugin(PMXProjectManager)

        manager = PMXProjectManager(self)
        self.settings.configure(manager)
        return manager
    
    def setupKernelManager(self):
        try:
            from IPython.frontend.qt.kernelmanager import QtKernelManager
            self.kernelManager = QtKernelManager()
            self.kernelManager.start_kernel()
            self.kernelManager.start_channels()
            if hasattr(self.kernelManager, "connection_file"):
                ipconnection = self.kernelManager.connection_file
            else:
                shell_port = self.kernelManager.shell_address[1]
                iopub_port = self.kernelManager.sub_address[1]
                stdin_port = self.kernelManager.stdin_address[1]
                hb_port = self.kernelManager.hb_address[1]
                ipconnection = "--shell={0} --iopub={1} --stdin={2} --hb={3}".format(shell_port, iopub_port, stdin_port, hb_port)
            self.supportManager.updateEnvironment({ 
                    "PMX_IPYTHON_CONNECTION": ipconnection
            })
        except ImportError as e:
            self.logger.warn("Warning: %s" % e)
            self.kernelManager = None

    def setupPluginManager(self):
        from prymatex.core.plugin.manager import PMXPluginManager
        self.pluginManager = PMXPluginManager(self)
        defaultDirectory = self.settings.value('PMX_PLUGINS_PATH')
        self.pluginManager.addPluginDirectory(defaultDirectory)
        self.pluginManager.loadPlugins()

    def setupCoroutines(self):
        self.scheduler = coroutines.Scheduler(self)

    def setupZeroMQContext(self):
        try:
            from prymatex.utils import zeromqt
            self.zmqContext = zeromqt.ZeroMQTContext(parent = self)
        except ImportError as e:
            self.logger.warn("Warning: %s" % e)
            self.zmqContext = None

    def setupMainWindow(self):
        from prymatex.gui.mainwindow import PMXMainWindow
        self.pluginManager.prepareWidgetPlugin(PMXMainWindow)
        
    #========================================================
    # Dialogs
    #========================================================
    def setupDialogs(self):
        #Bundle Editor
        from prymatex.gui.support.bundleeditor import PMXBundleEditor
        self.bundleEditor = PMXBundleEditor(self)
        #self.bundleEditor.setModal(True)
        
        #Dialog System
        if self.zmqContext:
            from prymatex.gui.dialogs.pmxdialog import PMXDialogSystem
            self.dialogSystem = PMXDialogSystem(self)
    
    def closePrymatex(self):
        self.logger.debug("Close")
        self.settings.setValue("mainWindowGeometry", self.mainWindow.saveGeometry())
        self.settings.setValue("mainWindowState", self.mainWindow.saveState())
        self.settings.sync()
        os.unlink(self.fileLock)
    
    def commitData(self):
        self.logger.debug("Commit data")
        
    def saveState(self, session_manager):
        self.logger.debug( "Save state %s" % session_manager)
    
    #---------------------------------------------------
    # Editors and mainWindow handle
    #---------------------------------------------------
    def createMainWindow(self):
        """
        Creates the windows
        """
        from prymatex.gui.mainwindow import PMXMainWindow

        print PMXMainWindow.application
        
        #TODO: Testeame con mas de una
        for _ in range(1):
            self.mainWindow = PMXMainWindow(self)

            #Configure and add dockers
            self.pluginManager.populateMainWindow(self.mainWindow)
            self.settings.configure(self.mainWindow)

            geometry = self.settings.value("mainWindowGeometry")
            state = self.settings.value("mainWindowState")
            if geometry:
                self.mainWindow.restoreGeometry(geometry)
            if state:
                self.mainWindow.restoreState(state)
                
            self.mainWindow.addEmptyEditor()
            self.mainWindow.show()

    def currentEditor(self):
        return self.mainWindow.currentEditor()

    def findEditorForFile(self, filePath):
        #Para cada mainwindow buscar el editor
        return self.mainWindow, self.mainWindow.findEditorForFile(filePath)
            
    def getEditorInstance(self, filePath = None, parent = None):
        return self.pluginManager.createEditor(filePath, parent)

    def openFile(self, filePath, cursorPosition = (0,0), focus = True):
        """
        Opens a editor in current window
        """
        if self.fileManager.isOpen(filePath):
            mainWindow, editor = self.findEditorForFile(filePath)
            if editor is not None:
                mainWindow.setCurrentEditor(editor)
                editor.setCursorPosition(cursorPosition)
        else:
            editor = self.getEditorInstance(filePath, self.mainWindow)
            project = self.projectManager.findProjectForPath(filePath)
            if project != None:
                editor.setProject(project)
            def on_editorReady(editor, cursorPosition, focus):
                def editorReady(openResult):
                    editor.setCursorPosition(cursorPosition)
                    self.mainWindow.tryCloseEmptyEditor()
                    self.mainWindow.addEditor(editor, focus)
                return editorReady
            if inspect.isgeneratorfunction(editor.open):
                task = self.scheduler.newTask( editor.open(filePath) )
                task.done.connect( on_editorReady(editor, cursorPosition, focus) )
            else:
                on_editorReady(editor, cursorPosition, focus)(editor.open(filePath))

    @deprecated
    def _populate_editor(self, editor, content, readyCallback = None):
        useCoroutines = False
        if useCoroutines:
            def appendChunksTask(editor, content, chunksize = 1024):
                editor.textCursor().beginEditBlock()
                currentIndex = 0
                contentLength = len(content)
                while currentIndex <= contentLength:
                    editor.insertPlainText(content[currentIndex:currentIndex + chunksize])
                    currentIndex += chunksize
                    yield
                editor.textCursor().endEditBlock()
                yield coroutines.Return(editor)
            task = self.scheduler.newTask( appendChunksTask(editor, content) )
            if readyCallback != None:
                task.done.connect( readyCallback )
        else:
            editor.setPlainText(content)
            if readyCallback != None:
                readyCallback(coroutines.Return(editor))

    def openDirectory(self, directoryPath):
        raise NotImplementedError("Directory contents should be opened as files here")        
    
    def handleUrlCommand(self, url):
        if isinstance(url, basestring):
            url = QtCore.QUrl(url)
        if url.scheme() == "txmt":
            #TODO: Controlar que sea un open
            sourceFile = url.queryItemValue('url')
            position = (0, 0)
            line = url.queryItemValue('line')
            if line:
                position = (int(line) - 1, position[1])
            column = url.queryItemValue('column')
            if column:
                position = (position[0], int(column) - 1)
            if sourceFile:
                self.openFile(sourceFile, position)
            else:
                self.currentEditor().setCursorPosition(position)

    def openArgumentFiles(self, args):
        for filePath in filter(lambda f: os.path.exists(f), args):
            if os.path.isfile(filePath):
                self.openFile(filePath)
            else:
                self.openDirectory(filePath)

    def checkExternalAction(self, mainWindow, editor):
        if editor.isExternalChanged():
            message = "The file '%s' has been changed on the file system, Do you want to replace the editor contents with these changes?"
            result = QtGui.QMessageBox.question(editor, _("File changed"),
                _(message) % editor.filePath,
                buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                defaultButton = QtGui.QMessageBox.Yes)
            if result == QtGui.QMessageBox.Yes:
                cursorPosition = editor.cursorPosition()
                def on_editorReady(editor, cursorPosition):
                    def editorReady(openResult):
                        editor.setCursorPosition(cursorPosition)
                    return editorReady
                if inspect.isgeneratorfunction(editor.reload):
                    task = self.scheduler.newTask( editor.reload() )
                    task.done.connect( on_editorReady(editor, cursorPosition) )
                else:
                    on_editorReady(editor, cursorPosition)(editor.reload())
            elif result == QtGui.QMessageBox.No:
                pass
        elif editor.isExternalDeleted():
            message = "The file '%s' has been deleted or is not accessible. Do you want to save your changes or close the editor without saving?"
            result = QtGui.QMessageBox.question(editor, _("File deleted"),
                _(message) % editor.filePath,
                buttons = QtGui.QMessageBox.Save | QtGui.QMessageBox.Close,
                defaultButton = QtGui.QMessageBox.Close)
            if result == QtGui.QMessageBox.Close:
                mainWindow.closeEditor(editor)
            elif result == QtGui.QMessageBox.Save:
                mainWindow.saveEditor(editor)
                
    def on_filesytemChange(self, filePath, change):
        mainWindow, editor = self.findEditorForFile(filePath)
        editor.setExternalAction(change)
        if mainWindow.currentEditor() == editor:
            self.checkExternalAction(mainWindow, editor)
    
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
    
    def __str__(self):
        return '<PMXApplication at {} PID: {}>'.format(hash(self), os.getpid())
    
    __unicode__ = __repr__ = __str__