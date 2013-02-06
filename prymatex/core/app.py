#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import inspect
import logging
from datetime import datetime

import prymatex
from prymatex import resources

from prymatex.qt import QtGui, QtCore

from prymatex.core import config
from prymatex.core.components import PMXBaseComponent
from prymatex.core import exceptions
from prymatex.core.logger import NameFilter
from prymatex.core.profile import PMXProfile
from prymatex.core.settings import pmxConfigPorperty

from prymatex.utils.decorators import deprecated
from prymatex.utils import coroutines
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.decorators.helpers import printtime, logtime

# Global dialogs
from prymatex.gui.dialogs.profile import PMXProfileDialog
from prymatex.gui.dialogs.settings import PMXSettingsDialog
from prymatex.gui.dialogs.bundles.editor import BundleEditorDialog

# The basic managers
from prymatex.managers.profile import ProfileManager
from prymatex.managers.plugins import PluginManager

class PrymatexApplication(QtGui.QApplication, PMXBaseComponent):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the Support."""

    # ---------------------- Settings
    SETTINGS_GROUP = "Global"

    @pmxConfigPorperty(valueType=str)
    def qtStyle(self, styleName):
        self.setStyle(styleName)

    @pmxConfigPorperty(valueType=str)
    def qtStyleSheet(self, styleSheetName):
        self.setStyleSheet(resources.STYLESHEETS[styleSheetName])

    askAboutExternalDeletions = pmxConfigPorperty(default=False)
    askAboutExternalChanges = pmxConfigPorperty(default=False)

    RESTART_CODE = 1000

    def __init__(self):
        """Inicialización de la aplicación."""
        #TODO: Pasar los argumentos a la QApplication
        QtGui.QApplication.__init__(self, [])
        PMXBaseComponent.__init__(self)

        # Some init's
        self.setApplicationName(prymatex.__name__.title())
        self.setApplicationVersion(prymatex.__version__)
        self.setOrganizationDomain(prymatex.__url__)
        self.setOrganizationName(prymatex.__author__)
        self.platform = sys.platform

        resources.loadPrymatexResources(config.PMX_SHARE_PATH)

        #Connects
        self.aboutToQuit.connect(self.closePrymatex)
        self.componentInstances = {}
        
        # Exceptions, Print exceptions in a window
        self.replaceSysExceptHook()
        
        # Route Qt output
        QtCore.qInstallMsgHandler(self.qtMessageHandler)

    # ------ exception and logger handlers
    def replaceSysExceptHook(self):
        def displayExceptionDialog(exctype, value, traceback):
            ''' Display a nice dialog showing the python traceback'''
            from prymatex.gui.emergency.tracedialog import PMXTraceBackDialog
            sys.__excepthook__(exctype, value, traceback)
            PMXTraceBackDialog.fromSysExceptHook(exctype, value, traceback).exec_()

        sys.excepthook = displayExceptionDialog


    def qtMessageHandler(self, msgType, msgString):
        ''' Route Qt messaging system into Prymatex/Python one'''
        if msgType == QtCore.QtDebugMsg:
            self.logger.debug(msgString)
        elif msgType == QtCore.QtWarningMsg:
            self.logger.warn(msgString)
        elif msgType == QtCore.QtCriticalMsg:
            self.logger.critical(msgString)
        elif msgType == QtCore.QtFatalMsg:
            self.logger.fatal(msgString)
        elif msgType == QtCore.QtSystemMsg:
            self.logger.debug("System: %s" % msgString)


    # ------- prymatex's micro kernel
    def applyOptions(self, options):
        self.options = options

        # Prepare profile
        profileName = self.options.profile
        self.extendComponent(ProfileManager)
        self.profileManager = ProfileManager(self)
        
        if profileName is None or (profileName == "" and not self.profileManager.dontask):
            #Select profile
            profileName = PMXProfileDialog.selectProfile(self.profileManager.profilesFile)
        elif profileName == "":
            #Find default profile in config
            profileName = self.profileManager.default

        self.currentProfile = self.profileManager.createProfile(profileName)

        self.checkSingleInstance()
        
        if self.options.reset_settings:
            self.currentProfile.clear()

        # Create the settings dialog
        self.extendComponent(PMXSettingsDialog)
        self.settingsDialog = PMXSettingsDialog(self)

        # Prepare settings for application
        self.registerConfigurable(self.__class__)

        # Configure application
        self.configure(self.currentProfile)
        
        verbose = self.options.verbose
        namePattern = self.options.log_pattern
        
        # Prepara logging
        level = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][verbose % 5]

        # File name
        filename = os.path.join(self.currentProfile.PMX_LOG_PATH, '%s-%s.log' % (logging.getLevelName(level), datetime.now().strftime('%d-%m-%Y')))
        logging.basicConfig(filename=filename, level=level)

        # Console handler
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        ch.setLevel(level)

        if namePattern:
            #Solo al de consola
            ch.addFilter(NameFilter(namePattern))

        logging.root.addHandler(ch)
        logging.root.info("Application startup")
        logging.root.debug("Application startup debug")

        self.logger = logging.root

        # Prepare Plugins
        self.extendComponent(PluginManager)
        self.pluginManager = PluginManager(self)
        self.pluginManager.configure(self.currentProfile)
        self.pluginManager.initialize(self)

        self.pluginManager.addPluginDirectory(config.PMX_PLUGINS_PATH)

        self.pluginManager.loadPlugins()


    def installTranslator(self):
        pass
        #slanguage = QtCore.QLocale.system().name()
        #print language
        #self.translator = QtCore.QTranslator()
        #print os.path.join(config.PMX_SHARE_PATH, "Languages")

        #self.translator.load(settings.LANGUAGE)
        #self.installTranslator(translator)

    # ---------------------- PMXBaseComponent methods
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.general import GeneralSettingsWidget
        return [GeneralSettingsWidget]

    def loadGraphicalUserInterface(self):
        if not self.options.no_splash:
            from prymatex.widgets.splash import SplashScreen
            splash_image = resources.getImage('newsplash')
            splash = SplashScreen(splash_image)
            splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)

            splashFont = QtGui.QFont("Monospace", 11)
            splashFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

            splash.setFont(splashFont)
            splash.setMask(splash_image.mask())
            splash.show()
        try:
            self.cacheManager = self.setupCacheManager()  # Cache system Manager

            #TODO: Cambiar los setup por build, que retornen los manager
            # Loads
            self.supportManager = self.setupSupportManager()  # Support Manager
            self.fileManager = self.setupFileManager()  # File Manager
            self.projectManager = self.setupProjectManager()  # Project Manager
            self.setupCoroutines()
            self.server = self.buildPrymatexServer()

            #Connect all loads
            self.projectManager.loadProjects()
            
            showMessage = splash.showMessage if not self.options.no_splash else (lambda message: message)
            
            self.supportManager.loadSupport(showMessage)
            self.settingsDialog.loadSettings()

            # Creates the Main Window
            self.createMainWindow()

            if not self.options.no_splash:
                splash.finish(self.mainWindow)
            else:
                self.mainWindow.show()

        except KeyboardInterrupt:
            self.logger.critical("\nQuit signal catched during application startup. Quiting...")
            self.quit()

    def unloadGraphicalUserInterface(self):
        #TODO: ver como dejar todo lindo y ordenado para terminar correctamente
        #if self.zmqContext is not None:
        #    self.zmqContext.destroy()
        self.mainWindow.close()
        del self.mainWindow


    def switchProfile(self):
        profile = PMXProfileDialog.switchProfile(self.profileManager.profilesFile)
        if profile is not None and profile != self.currentProfile.PMX_PROFILE_NAME:
            self.restart()

    def restart(self):
        self.exit(self.RESTART_CODE)


    def checkSingleInstance(self):
        """
        Checks if there's another instance using current profile
        """
        self.fileLock = os.path.join(self.currentProfile.PMX_PROFILE_PATH, 'prymatex.pid')

        if os.path.exists(self.fileLock):
            #Mejorar esto
            pass
            #raise exceptions.AlreadyRunningError('%s seems to be runnig. Please close the instance or run other profile.' % (self.currentProfile.PMX_PROFILE_NAME))
        else:
            f = open(self.fileLock, 'w')
            f.write('%s' % self.applicationPid())
            f.close()

    # --------------------- Logging system and loggers
    def getLogger(self, name):
        """ return logger, for filter by name in future """
        return logging.getLogger(name)


    # -------------------- Managers
    def setupSupportManager(self):
        from prymatex.managers.support import SupportManager
        manager = self.createComponentInstance(SupportManager)

        #Prepare prymatex namespace
        manager.addNamespace('prymatex', config.PMX_SHARE_PATH)
        
        #Prepare user namespace
        manager.addNamespace('user', config.PMX_HOME_PATH)
        
        # Update environment
        manager.updateEnvironment({  
            # TextMate Compatible :P
            'TM_APP_PATH': self.currentProfile.value('PMX_APP_PATH'),
            'TM_SUPPORT_PATH': manager.environment['PMX_SUPPORT_PATH'],
            'TM_BUNDLES_PATH': manager.environment['PMX_BUNDLES_PATH'],
            'TM_THEMES_PATH': manager.environment['PMX_THEMES_PATH'],
            'TM_PID': self.applicationPid(),
            #Prymatex
            'PMX_APP_NAME': self.applicationName().title(),
            'PMX_APP_PATH': self.currentProfile.value('PMX_APP_PATH'),
            'PMX_PREFERENCES_PATH': self.currentProfile.value('PMX_PREFERENCES_PATH'),
            'PMX_VERSION': self.applicationVersion(),
            'PMX_PID': self.applicationPid(),
            #User
            'PMX_HOME_PATH': config.PMX_HOME_PATH,
            'PMX_PROFILE_NAME': self.currentProfile.value('PMX_PROFILE_NAME'),
            'PMX_PROFILE_PATH': self.currentProfile.value('PMX_PROFILE_PATH'),
            'PMX_TMP_PATH': self.currentProfile.value('PMX_TMP_PATH'),
            'PMX_LOG_PATH': self.currentProfile.value('PMX_LOG_PATH')
        })


        # Create bundle editor dialog
        self.extendComponent(BundleEditorDialog)
        self.bundleEditorDialog = BundleEditorDialog(self, manager)

        return manager

    def setupFileManager(self):
        from prymatex.managers.files import FileManager
        manager = self.createComponentInstance(FileManager)

        manager.fileSytemChanged.connect(self.on_fileManager_fileSytemChanged)
        return manager

    def setupProjectManager(self):
        from prymatex.managers.projects import ProjectManager
        manager = self.createComponentInstance(ProjectManager)
        return manager

    def setupCacheManager(self):
        from prymatex.managers.cache import CacheManager
        return self.createComponentInstance(CacheManager)


    def setupCoroutines(self):
        self.scheduler = coroutines.Scheduler(self)

    def buildPrymatexServer(self):
        from prymatex.core.server import PrymatexServer
        return self.createComponentInstance(PrymatexServer, self)

    # --------------------- Application events
    def closePrymatex(self):
        self.logger.debug("Close")

        self.currentProfile.saveState(self.mainWindow)
        if os.path.exists(self.fileLock):
            os.unlink(self.fileLock)

    def commitData(self, manager):
        print "Commit data"

    def saveState(self, manager):
        print "saveState"
        pass

    # --------------------- Exend and populate components
    def extendComponent(self, componentClass):
        componentClass.application = self
        componentClass.logger = self.getLogger('.'.join([componentClass.__module__, componentClass.__name__]))


    def registerConfigurable(self, componentClass):
        self.currentProfile.registerConfigurable(componentClass)
        for settingClass in componentClass.contributeToSettings():
            self.extendComponent(settingClass)
            settingWidget = settingClass(componentClass.settings, profile = self.currentProfile)
            componentClass.settings.addDialog(settingWidget)
            self.settingsDialog.register(settingWidget)


    def populateComponentClass(self, componentClass):
        self.extendComponent(componentClass)
        self.registerConfigurable(componentClass)


    # ------------------- Create components
    def createComponentInstance(self, componentClass, parent = None):
        parent = parent or self
        if not hasattr(componentClass, 'application') or componentClass.application != self:
            self.populateComponentClass(componentClass)

        instance = componentClass(parent)

        instance.populate(self.pluginManager)
        instance.configure(self.currentProfile)
        instance.initialize(parent)
        
        instances = self.componentInstances.setdefault(componentClass, [])
        instances.append(instance)

        return instance


    # ------------ Create Zmq Sockets
    def zmqSocket(self, socketType, name, addr='tcp://127.0.0.1'):
        # TODO ver la variable aca, creo que merjor seria que la app genere environ pregunatando a los components
        # que esta genera
        from prymatex.utils.zeromqt import ZmqSocket
        socket = ZmqSocket(socketType)
        port = socket.bind_to_random_port(addr)
        self.supportManager.addToEnvironment("PMX_" + name.upper() + "_PORT", port)
        return socket

    # ------------- Editors and mainWindow handle
    def createEditorInstance(self, filePath=None, parent=None):
        editorClass = filePath is not None and self.pluginManager.findEditorClassForFile(filePath) or self.pluginManager.defaultEditor()

        if editorClass is not None:
            return self.createComponentInstance(editorClass, parent)


    def createMainWindow(self):
        """Creates the windows"""
        from prymatex.gui.mainwindow import PMXMainWindow

        #TODO: Testeame con mas de una
        for _ in range(1):
            self.mainWindow = self.createComponentInstance(PMXMainWindow)

            self.mainWindow.show()
            self.currentProfile.restoreState(self.mainWindow)

            if not self.mainWindow.editors():
                self.mainWindow.addEmptyEditor()


    def showMessage(self, message):
        #Si tengo mainwindow vamos por este camino, sino hacerlo llegar de otra forma
        self.mainWindow.showMessage(message)

    def currentEditor(self):
        return self.mainWindow.currentEditor()

    def findEditorForFile(self, filePath):
        #Para cada mainwindow buscar el editor
        return self.mainWindow, self.mainWindow.findEditorForFile(filePath)

    def canBeHandled(self, filePath):
        #from prymatex.utils.pyqtdebug import ipdb_set_trace
        #ipdb_set_trace()
        ext = os.path.splitext(filePath)[1].replace('.', '')
        for fileTypes in [syntax.item.fileTypes for syntax in
                          self.supportManager.getAllSyntaxes()
                          if hasattr(syntax.item, 'fileTypes') and
                          syntax.item.fileTypes]:

            if ext in fileTypes:
                return True
        return False

    __options = None

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value
        # Send some singal? Don't think so yet, this is intended to be set at startup

    def openFile(self, filePath, cursorPosition=None, focus=True, mainWindow=None, useTasks=True):
        """Open a editor in current window"""
        filePath = self.fileManager.normcase(filePath)

        if self.fileManager.isOpen(filePath):
            mainWindow, editor = self.findEditorForFile(filePath)
            if editor is not None:
                mainWindow.setCurrentEditor(editor)
                if isinstance(cursorPosition, tuple):
                    editor.setCursorPosition(cursorPosition)
        elif self.fileManager.exists(filePath):
            mainWindow = mainWindow or self.mainWindow
            editor = self.createEditorInstance(filePath, mainWindow)

            def on_editorReady(mainWindow, editor, cursorPosition, focus):
                def editorReady(openResult):
                    if isinstance(cursorPosition, tuple):
                        editor.setCursorPosition(cursorPosition)
                    mainWindow.tryCloseEmptyEditor()
                    mainWindow.addEditor(editor, focus)
                return editorReady
            if useTasks and inspect.isgeneratorfunction(editor.open):
                task = self.scheduler.newTask(editor.open(filePath))
                task.done.connect(on_editorReady(mainWindow, editor, cursorPosition, focus))
            elif inspect.isgeneratorfunction(editor.open):
                on_editorReady(mainWindow, editor, cursorPosition, focus)(list(editor.open(filePath)))
            else:
                on_editorReady(mainWindow, editor, cursorPosition, focus)(editor.open(filePath))

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
                filePath = QtCore.QUrl(sourceFile, QtCore.QUrl.TolerantMode).toLocalFile()
                self.openFile(filePath, position)
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
                                                buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                defaultButton=QtGui.QMessageBox.Yes) if self.askAboutExternalChanges else QtGui.QMessageBox.Yes
            if result == QtGui.QMessageBox.Yes:
                if inspect.isgeneratorfunction(editor.reload):
                    task = self.scheduler.newTask(editor.reload())
                else:
                    editor.reload()
            elif result == QtGui.QMessageBox.No:
                pass
        elif editor.isExternalDeleted():
            message = "The file '%s' has been deleted or is not accessible. Do you want to save your changes or close the editor without saving?"
            result = QtGui.QMessageBox.question(editor, _("File deleted"),
                                                _(message) % editor.filePath,
                                                buttons=QtGui.QMessageBox.Save | QtGui.QMessageBox.Close,
                                                defaultButton=QtGui.QMessageBox.Close) if self.askAboutExternalDeletions else QtGui.QMessageBox.Close
            if result == QtGui.QMessageBox.Close:
                mainWindow.closeEditor(editor)
            elif result == QtGui.QMessageBox.Save:
                mainWindow.saveEditor(editor)

    def on_fileManager_fileSytemChanged(self, filePath, change):
        mainWindow, editor = self.findEditorForFile(filePath)
        editor.setExternalAction(change)
        if mainWindow.currentEditor() == editor:
            self.checkExternalAction(mainWindow, editor)

    
    def __str__(self):
        return '<PrymatexApplication at {} PID: {}>'.format(hash(self), os.getpid())

    __unicode__ = __repr__ = __str__
