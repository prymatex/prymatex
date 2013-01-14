#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import inspect
import logging

import prymatex
from prymatex import resources

from prymatex.qt import QtGui, QtCore, Qt

from prymatex.core import exceptions
from prymatex.core.logger import NameFilter
from prymatex.core.profile import PMXProfile
from prymatex.core.settings import pmxConfigPorperty

from prymatex.utils.decorators import deprecated
from prymatex.utils import coroutines
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.decorators.helpers import printtime, logtime

class PrymatexApplication(QtGui.QApplication):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the PMX Support."""

    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = "Global"

    @pmxConfigPorperty(default=resources.APPLICATION_STYLE)
    def styleSheet(self, style):
        self.setStyleSheet(style)

    askAboutExternalActions = pmxConfigPorperty(default=False)

    RESTART_CODE = 1000

    def __init__(self):
        """Inicialización de la aplicación."""
        #TODO: Pasar los argumentos a la QApplication
        QtGui.QApplication.__init__(self, [])

        # Some init's
        self.setApplicationName(prymatex.__name__.title())
        self.setApplicationVersion(prymatex.__version__)
        self.setOrganizationDomain(prymatex.__url__)
        self.setOrganizationName(prymatex.__author__)
        self.platform = sys.platform

        resources.loadPrymatexResources(PMXProfile.PMX_SHARE_PATH)

        #Connects
        self.aboutToQuit.connect(self.closePrymatex)

    def installTranslator(self):
        pass
        #slanguage = QtCore.QLocale.system().name()
        #print language
        #self.translator = QtCore.QTranslator()
        #print os.path.join(PMXProfile.PMX_SHARE_PATH, "Languages")

        #self.translator.load(settings.LANGUAGE)
        #self.installTranslator(translator)


    def buildSplashScreen(self):
        from prymatex.widgets.splash import SplashScreen
        splash_image = resources.getImage('newsplash')
        splash = SplashScreen(splash_image)
        splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)

        splashFont = QtGui.QFont("Monospace", 11)
        splashFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

        splash.setFont(splashFont)
        splash.setMask(splash_image.mask())

        return splash

    def loadGraphicalUserInterface(self):
        splash = self.buildSplashScreen()
        if not self.options.no_splash:
            splash.show()
        try:
            self.cacheManager = self.setupCacheManager()        #Cache system Manager
            self.pluginManager = self.setupPluginManager()      #Prepare plugin manager

            #TODO: Cambiar los setup por build, que retornen los manager
            # Loads
            self.supportManager = self.setupSupportManager()    #Support Manager
            self.fileManager = self.setupFileManager()          #File Manager
            self.projectManager = self.setupProjectManager()    #Project Manager
            self.setupCoroutines()
            self.setupMainWindow()
            self.setupServer()

            # Setup Dialogs
            self.setupDialogs()

            #Connect all loads
            self.projectManager.loadProjects()

            self.supportManager.loadSupport(splash.showMessage)
            self.settingsDialog.loadSettings()

            # Creates the Main Window
            self.createMainWindow()

            splash.finish(self.mainWindow)

        except KeyboardInterrupt:
            self.logger.critical("\nQuit signal catched during application startup. Quiting...")
            self.quit()

    def unloadGraphicalUserInterface(self):
        #TODO: ver como dejar todo lindo y ordenado para terminar correctamente
        #if self.zmqContext is not None:
        #    self.zmqContext.destroy()
        self.mainWindow.close()
        del self.mainWindow

    def resetSettings(self):
        self.profile.clear()

    def switchProfile(self):
        from prymatex.gui.dialogs.profile import PMXProfileDialog
        profile = PMXProfileDialog.switchProfile(PMXProfile.PMX_PROFILES_FILE)
        if profile is not None and profile != self.profile.PMX_PROFILE_NAME:
            self.restart()

    def restart(self):
        self.exit(self.RESTART_CODE)

    def buildSettings(self, profile):
        # TODO Cambiar este metodo a buildProfile
        if profile is None or (profile == "" and not PMXProfile.PMX_PROFILES_DONTASK):
            #Select profile
            from prymatex.gui.dialogs.profile import PMXProfileDialog
            profile = PMXProfileDialog.selectProfile(PMXProfile.PMX_PROFILES_FILE)
        elif profile == "":
            #Find default profile in config
            profile = PMXProfile.PMX_PROFILE_DEFAULT

        #Settings
        from prymatex.gui.dialogs.settings import PMXSettingsDialog
        if not profile:
            raise ValueError("Invalid Profile")
        self.profile = PMXProfile(profile)

        # Configure application
        self.profile.registerConfigurable(self.__class__)
        self.profile.configure(self)

        # TODO Este dialogo no va mas aca
        self.settingsDialog = PMXSettingsDialog(self)

    def checkSingleInstance(self):
        """
        Checks if there's another instance using current profile
        """
        self.fileLock = os.path.join(self.profile.PMX_PROFILE_PATH, 'prymatex.pid')

        if os.path.exists(self.fileLock):
            #Mejorar esto
            pass
            #raise exceptions.AlreadyRunningError('%s seems to be runnig. Please close the instance or run other profile.' % (self.profile.PMX_PROFILE_NAME))
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

    def setupLogging(self, verbose, namePattern):
        from datetime import datetime

        level = [ logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG ][verbose % 5]

        # File name
        filename = os.path.join(self.profile.PMX_LOG_PATH, '%s-%s.log' % (logging.getLevelName(level), datetime.now().strftime('%d-%m-%Y')))
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

        # Route Qt output
        Qt.qInstallMsgHandler(self.qtMessageHandler)

    def qtMessageHandler(self, msgType, msgString):
        ''' Route Qt messaging system into Prymatex/Python one'''
        if msgType == Qt.QtDebugMsg:
            self.logger.debug(msgString)
        elif msgType == Qt.QtWarningMsg:
            self.logger.warn(msgString)
        elif msgType == Qt.QtCriticalMsg:
            self.logger.critical(msgString)
        elif msgType == Qt.QtFatalMsg:
            self.logger.fatal(msgString)
        elif msgType == Qt.QtSystemMsg:
            self.logger.debug("System: %s" % msgString)

    #========================================================
    # Managers
    #========================================================
    @logtime
    def setupSupportManager(self):
        from prymatex.managers.support import SupportManager

        self.populateComponent(SupportManager)

        manager = SupportManager(self)
        self.profile.configure(manager)

        #Prepare prymatex namespace
        sharePath = self.profile.value('PMX_SHARE_PATH')
        manager.addNamespace('prymatex', sharePath)
        manager.updateEnvironment({ #TextMate Compatible :P
                'TM_APP_PATH': self.profile.value('PMX_APP_PATH'),
                'TM_SUPPORT_PATH': manager.environment['PMX_SUPPORT_PATH'],
                'TM_BUNDLES_PATH': manager.environment['PMX_BUNDLES_PATH'],
                'TM_THEMES_PATH': manager.environment['PMX_THEMES_PATH'],
                'TM_PID': self.applicationPid(),
                #Prymatex
                'PMX_APP_NAME': self.applicationName().title(),
                'PMX_APP_PATH': self.profile.value('PMX_APP_PATH'),
                'PMX_PREFERENCES_PATH': self.profile.value('PMX_PREFERENCES_PATH'),
                'PMX_VERSION': self.applicationVersion(),
                'PMX_PID': self.applicationPid()
        })

        #Prepare user namespace
        homePath = self.profile.value('PMX_HOME_PATH')
        manager.addNamespace('user', homePath)
        manager.updateEnvironment({
                'PMX_HOME_PATH': homePath,
                'PMX_PROFILE_PATH': self.profile.value('PMX_PROFILE_PATH'),
                'PMX_TMP_PATH': self.profile.value('PMX_TMP_PATH'),
                'PMX_LOG_PATH': self.profile.value('PMX_LOG_PATH')
        })
        return manager

    def setupFileManager(self):
        from prymatex.managers.files import FileManager

        self.populateComponent(FileManager)

        manager = FileManager(self)
        self.profile.configure(manager)

        manager.fileSytemChanged.connect(self.on_fileManager_fileSytemChanged)
        return manager

    def setupProjectManager(self):
        from prymatex.managers.projects import ProjectManager

        self.populateComponent(ProjectManager)

        manager = ProjectManager(self)
        self.profile.configure(manager)
        return manager

    def setupCacheManager(self):
        from prymatex.managers.cache import CacheManager
        return CacheManager()

    def setupPluginManager(self):
        from prymatex.managers.plugins import PluginManager

        self.populateComponent(PluginManager)

        pluginManager = PluginManager(self)
        self.profile.configure(pluginManager)

        # TODO: Ruta de los plugins ver de aprovechar settings quiza esta sea una ruta base solamente
        pluginManager.addPluginDirectory(self.profile.value('PMX_PLUGINS_PATH'))

        pluginManager.loadPlugins()
        return pluginManager

    def setupCoroutines(self):
        self.scheduler = coroutines.Scheduler(self)

    def setupMainWindow(self):
        from prymatex.gui.mainwindow import PMXMainWindow
        self.populateComponent(PMXMainWindow)

    def setupServer(self):
        from prymatex.core.server import PrymatexServer
        self.populateComponent(PrymatexServer)
        self.server = PrymatexServer(self)

    #========================================================
    # Dialogs
    #========================================================
    def setupDialogs(self):
        # TODO: Creo que esto del bundle editor global asi no va a caminar muy bien
        #Bundle Editor
        from prymatex.gui.support.bundleeditor import PMXBundleEditor
        self.populateComponent(PMXBundleEditor)

        self.bundleEditor = PMXBundleEditor(self)
        #self.bundleEditor.setModal(True)

    def closePrymatex(self):
        self.logger.debug("Close")

        self.profile.saveState(self.mainWindow)
        os.unlink(self.fileLock)

    def commitData(self, manager):
        print "Commit data"

    def saveState(self, manager):
        print "saveState"
        pass

    #========================================================
    # Components
    #========================================================
    def extendComponent(self, componentClass):
        componentClass.application = self
        componentClass.logger = self.getLogger('.'.join([componentClass.__module__, componentClass.__name__]))

    def populateComponent(self, componentClass):
        self.extendComponent(componentClass)
        self.profile.registerConfigurable(componentClass)
        for settingClass in componentClass.contributeToSettings():
            try:
                self.extendComponent(settingClass)
                self.settingsDialog.register(settingClass(componentClass.settings))
            except (RuntimeError, ImportError):
                # TODO: Inform user but dont' prevent pmx from starting
                pass

    def createWidgetInstance(self, widgetClass, parent):
        # TODO Que parent sea opcional y pueda ser la mainWindow si no viene seteado
        return self.pluginManager.createWidgetInstance(widgetClass, parent)

    #========================================================
    # Create Zmq Sockets
    #========================================================
    def zmqSocket(self, socketType, name, addr='tcp://127.0.0.1'):
        # TODO ver la variable aca, creo que merjor seria que la app genere environ pregunatando a los components
        # que esta genera
        from prymatex.utils.zeromqt import ZmqSocket
        socket = ZmqSocket(socketType)
        port = socket.bind_to_random_port(addr)
        self.supportManager.addToEnvironment("PMX_" + name.upper() + "_PORT", port)
        return socket

    #========================================================
    # Editors and mainWindow handle
    #========================================================
    def createEditorInstance(self, filePath=None, parent=None):
        editorClass = filePath is not None and self.pluginManager.findEditorClassForFile(filePath) or self.pluginManager.defaultEditor()

        if editorClass is not None:
            return self.createWidgetInstance(editorClass, parent)

    def createMainWindow(self):
        """Creates the windows"""
        from prymatex.gui.mainwindow import PMXMainWindow

        #TODO: Testeame con mas de una
        for _ in range(1):
            self.mainWindow = PMXMainWindow(self)

            #Configure and add dockers
            self.pluginManager.populateMainWindow(self.mainWindow)
            self.profile.configure(self.mainWindow)
            self.mainWindow.show()
            self.profile.restoreState(self.mainWindow)

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
        for fileTypes in  [ syntax.item.fileTypes for syntax in
                            self.supportManager.getAllSyntaxes()
                            if hasattr(syntax.item, 'fileTypes') and
                            syntax.item.fileTypes ]:

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
                defaultButton=QtGui.QMessageBox.Yes) if self.askAboutExternalActions else QtGui.QMessageBox.Yes
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
                defaultButton=QtGui.QMessageBox.Close) if self.askAboutExternalActions else QtGui.QMessageBox.Close
            if result == QtGui.QMessageBox.Close:
                mainWindow.closeEditor(editor)
            elif result == QtGui.QMessageBox.Save:
                mainWindow.saveEditor(editor)

    def on_fileManager_fileSytemChanged(self, filePath, change):
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

    def execWithArgs(self, files):
        '''Finishes setup of QApplication and run'''
        self.replaceSysExceptHook()
        self.checkSingleInstance()
        if self.options.reset_settings:
            self.resetSettings()
        self.loadGraphicalUserInterface()
        self.openArgumentFiles(files)
        return self.exec_()

    def __str__(self):
        return '<PrymatexApplication at {} PID: {}>'.format(hash(self), os.getpid())

    __unicode__ = __repr__ = __str__
