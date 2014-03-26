#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
import tempfile

import prymatex
from prymatex import resources

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import create_shortcut

from prymatex.core import config
from prymatex.core.components import PrymatexComponent, PMXBaseEditor
from prymatex.core import logger, exceptions
from prymatex.core.settings import ConfigurableItem

from prymatex.utils.i18n import ugettext as _
from prymatex.utils.zeromqt import ZmqSocket
from prymatex.utils import six

from prymatex.models.shortcuts import ShortcutsTreeModel

class PrymatexApplication(PrymatexComponent, QtGui.QApplication):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the Support."""

    # ---------------------- Settings
    SETTINGS_GROUP = "Global"

    @ConfigurableItem(valueType = str)
    def qtStyle(self, styleName):
        if styleName:
            self.setStyle(styleName)

    @ConfigurableItem(default = "default")
    def qtStyleSheet(self, styleSheetName):
        if styleSheetName in resources.STYLESHEETS:
            self.setStyleSheet(resources.STYLESHEETS[styleSheetName])

    askAboutExternalDeletions = ConfigurableItem(default=False)
    askAboutExternalChanges = ConfigurableItem(default=False)

    RESTART_CODE = 1000

    def __init__(self, **kwargs):
        """Inicialización de la aplicación."""
        super(PrymatexApplication, self).__init__(**kwargs)

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
        self.shortcutsTreeModel = ShortcutsTreeModel(self)

        self.replaceSysExceptHook()

    # ------ exception and logger handlers
    def getLogger(self, *largs, **kwargs):
        return logger.getLogger(*largs, **kwargs)

    def replaceSysExceptHook(self):
        # Exceptions, Print exceptions in a window
        def displayExceptionDialog(exctype, value, traceback):
            ''' Display a nice dialog showing the python traceback'''
            from prymatex.gui.emergency.tracedialog import PMXTraceBackDialog
            sys.__excepthook__(exctype, value, traceback)
            PMXTraceBackDialog.fromSysExceptHook(exctype, value, traceback).exec_()

        sys.excepthook = displayExceptionDialog

        # Route messages to application logger
        QtCore.qInstallMsgHandler(self.qtMessageHandler)

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
        # The basic managers
        self.options = options

        # Prepare profile
        from prymatex.managers.profile import ProfileManager
        self.extendComponent(ProfileManager)
        self.profileManager = ProfileManager(self)
        self.currentProfile = self.profileManager.currentProfile(self.options.profile)
        if self.currentProfile is None:
            return False

        if self.options.reset_settings:
            self.currentProfile.clear()

        # Prepare settings for application
        self.populateComponentClass(PrymatexApplication)
        self.currentProfile.configure(self)

        logger.config(self.options.verbose, self.currentProfile.PMX_LOG_PATH, self.options.log_pattern)

        self.checkSingleInstance()

        return True

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
        from prymatex.gui.settings.shortcuts import ShortcutsSettingsWidget

        return [ GeneralSettingsWidget, ShortcutsSettingsWidget ]

    def loadGraphicalUserInterface(self):
        self.showMessage = self.logger.info
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
            self.showMessage = splash.showMessage
        try:

            # Build Managers
            self.pluginManager = self.buildPluginManager()  # WARN: FIST Plugin Manager
            self.storageManager = self.buildStorageManager()  # Persistence system Manager
            self.supportManager = self.buildSupportManager()  # Support Manager
            self.fileManager = self.buildFileManager()  # File Manager
            self.projectManager = self.buildProjectManager()  # Project Manager
            self.schedulerManager =  self.buildSchedulerManager()
            self.serverManager = self.buildServerManager()

            # Load managers
            self.projectManager.loadProjects(self.showMessage)
            self.supportManager.loadSupport(self.showMessage)
            self.profileManager.loadSettings(self.showMessage)

            # Create the Main Window instance
            self.mainWindow = self.buildMainWindow()
            self.showMessage = self.mainWindow.showMessage

            if not self.options.no_splash:
                splash.finish(self.mainWindow)

            self.mainWindow.show()
            self.logger.info("Application startup")
        except KeyboardInterrupt:
            self.logger.critical("\nQuit signal catched during application startup. Quiting...")
            self.quit()

    def unloadGraphicalUserInterface(self):
        #TODO: ver como dejar todo lindo y ordenado para terminar correctamente
        #if self.zmqContext is not None:
        #    self.zmqContext.destroy()
        self.mainWindow.close()
        del self.mainWindow

    def restart(self):
        self.exit(self.RESTART_CODE)

    def checkSingleInstance(self):
        """Checks if there's another instance using current profile"""
        self.fileLock = os.path.join(self.currentProfile.PMX_PROFILE_PATH, 'prymatex.pid')

        if os.path.exists(self.fileLock):
            #Mejorar esto
            pass
            #raise exceptions.AlreadyRunningError('%s seems to be runnig. Please close the instance or run other profile.' % (self.currentProfile.PMX_PROFILE_NAME))
        else:
            f = open(self.fileLock, 'w')
            f.write('%s' % self.applicationPid())
            f.close()

    # -------------------- Managers
    def buildPluginManager(self):
        from prymatex.managers.plugins import PluginManager
        #manager = self.createComponentInstance(PluginManager, self)
        self.populateComponentClass(PluginManager)

        manager = PluginManager(self)

        self.currentProfile.configure(manager)

        manager.initialize(parent = self)

        manager.addPluginDirectory(config.PMX_PLUGINS_PATH)

        manager.loadPlugins()
        return manager

    def buildSupportManager(self):
        from prymatex.managers.support import SupportManager
        manager = self.createComponentInstance(SupportManager, self)

        #Prepare prymatex namespace
        manager.addNamespace('prymatex', config.PMX_SHARE_PATH)

        #Prepare user namespace
        manager.addNamespace('user', config.PMX_HOME_PATH)

        # Update environment
        manager.updateEnvironment({
            # TextMate Compatible :P
            'TM_APP_PATH': config.PMX_APP_PATH,
            'TM_SUPPORT_PATH': manager.environmentVariables()['PMX_SUPPORT_PATH'],
            'TM_BUNDLES_PATH': manager.environmentVariables()['PMX_BUNDLES_PATH'],
            'TM_THEMES_PATH': manager.environmentVariables()['PMX_THEMES_PATH'],
            'TM_PID': self.applicationPid(),
            #Prymatex
            'PMX_APP_NAME': self.applicationName().title(),
            'PMX_APP_PATH': config.PMX_APP_PATH,
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

        return manager

    def buildFileManager(self):
        from prymatex.managers.files import FileManager
        manager = self.createComponentInstance(FileManager, self)

        manager.fileSytemChanged.connect(self.on_fileManager_fileSytemChanged)
        return manager

    def buildProjectManager(self):
        from prymatex.managers.projects import ProjectManager
        return self.createComponentInstance(ProjectManager, self)

    def buildStorageManager(self):
        from prymatex.managers.storage import StorageManager
        return self.createComponentInstance(StorageManager, self)

    def buildSchedulerManager(self):
        from prymatex.utils import coroutines
        return coroutines.Scheduler(self)

    def buildServerManager(self):
        from prymatex.managers.server import ServerManager
        return self.createComponentInstance(ServerManager, self)

    # --------------------- Application events
    def closePrymatex(self):
        self.logger.debug("Close")

        self.storageManager.close()
        self.currentProfile.saveState(self.mainWindow)
        self.currentProfile.sync()
        if os.path.exists(self.fileLock):
            os.unlink(self.fileLock)

    # --------------------- Exend and populate components
    def extendComponent(self, componentClass):
        componentClass.application = self
        componentClass.logger = self.getLogger('.'.join([componentClass.__module__, componentClass.__name__]))

    def registerConfigurable(self, componentClass):
        self.currentProfile.registerConfigurable(componentClass)
        for settingClass in componentClass.contributeToSettings():
            self.extendComponent(settingClass)
            settingWidget = settingClass(componentClass._settings, profile = self.currentProfile)
            componentClass._settings.addDialog(settingWidget)
            self.profileManager.registerSettingsWidget(settingWidget)

    def populateComponentClass(self, componentClass):
        self.extendComponent(componentClass)
        self.registerConfigurable(componentClass)

    # ------------------- Create components
    def createComponentInstance(self, componentClass, componentParent = None):
        if not hasattr(componentClass, 'application') or componentClass.application != self:
            self.populateComponentClass(componentClass)

        buildedObjects = []
        def buildComponentInstance(klass, parent):
            instance = klass(parent = parent)

            # Configure
            self.currentProfile.configure(instance)

            # Add components
            componentClasses = self.pluginManager.findComponentsForClass(klass)
            for componentClass in componentClasses:
                # Filter editors, editors create explicit
                if issubclass(componentClass, PMXBaseEditor):
                    continue
                componentInstance = buildComponentInstance(componentClass, instance)
                instance.addComponent(componentInstance)
            buildedObjects.append((instance, parent))
            return instance

        instance = buildComponentInstance(componentClass, componentParent)

        # buildedObjects.reverse()
        # Initialize order is important, fist goes the internal components then the main component
        for ni, np in buildedObjects:
            ni.initialize(parent = np)
            # Shortcuts
            for settings in ni.contributeToShortcuts():
                create_shortcut(instance, settings, sequence_handler = self.registerShortcut)

        self.componentInstances.setdefault(componentClass, []).append(instance)

        return instance

    # ------------ Find Component
    def componentHierarchyForClass(self, componentClass):
        return self.pluginManager.componentHierarchyForClass(componentClass)

    def findComponentsForClass(self, componentClass):
        return self.pluginManager.findComponentsForClass(componentClass)

    # ------------ Create Zmq Sockets
    def zmqSocket(self, socketType, name, address='127.0.0.1', addressType='tcp', port = None):
        # TODO ver la variable aca, creo que merjor seria que la app genere environ pregunatando a los components
        # que esta genera
        socket = ZmqSocket(socketType)
        if addressType == "ipc":
            addr = "ipc://%s" % tempfile.mkstemp(prefix="pmx")[1]
            socket.bind(addr)
        elif addressType == "tcp":
            addr = "tcp://%s" % address
            if isinstance(port, int):
                addr += ":%d" % port
                socket.bind(addr)
            else:
                port = socket.bind_to_random_port(addr)
                addr += ":%d" % port
        self.supportManager.addToEnvironment("PMX_" + name.upper() + "_ADDRESS", addr)
        return socket

    # ------------- Settings access
    def settingValue(self, settingPath):
        groupName, settingName = settingPath.split(".")
        return self.currentProfile.groupByName(groupName).value(settingName)

    def registerSettingHook(self, settingPath, handler):
        groupName, settingName = settingPath.split(".")
        group = self.currentProfile.groupByName(groupName)
        group.addHook(settingName, handler)

    def unregisterSettingHook(self, settingPath, handler):
        groupName, settingName = settingPath.split(".")
        group = self.currentProfile.groupByName(groupName)
        group.removeHook(settingName, handler)

    # ------------- Editors and mainWindow handle
    def createEditorInstance(self, filePath=None, parent=None):
        editorClass = filePath and self.pluginManager.findEditorClassForFile(filePath) or self.pluginManager.defaultEditor()

        if editorClass:
            return self.createComponentInstance(editorClass, parent)

    def buildMainWindow(self):
        """Creates the windows"""
        from prymatex.gui.mainwindow import PrymatexMainWindow

        mainWindow = self.createComponentInstance(PrymatexMainWindow)

        self.currentProfile.restoreState(mainWindow)

        if not mainWindow.editors():
            mainWindow.addEmptyEditor()
        return mainWindow

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

    # ---- Open (file, directory, url, canelones)
    def openFile(self, filePath, cursorPosition=None, focus=True, mainWindow=None, useTasks=True):
        """Open a editor in current window"""
        filePath = self.fileManager.normcase(filePath)

        if self.fileManager.isOpen(filePath):
            mainWindow, editor = self.findEditorForFile(filePath)
            if editor is not None:
                mainWindow.setCurrentEditor(editor)
                if cursorPosition is not None:
                    editor.setCursorPosition(cursorPosition)
        elif self.fileManager.exists(filePath):
            mainWindow = mainWindow or self.mainWindow
            editor = self.createEditorInstance(filePath, mainWindow)

            def on_editorReady(mainWindow, editor, cursorPosition, focus):
                def editorReady(openResult):
                    if cursorPosition is not None:
                        editor.setCursorPosition(cursorPosition)
                    mainWindow.tryCloseEmptyEditor()
                    mainWindow.addEditor(editor, focus)
                return editorReady
            if useTasks and inspect.isgeneratorfunction(editor.open):
                task = self.schedulerManager.newTask(editor.open(filePath))
                task.done.connect(on_editorReady(mainWindow, editor, cursorPosition, focus))
            elif inspect.isgeneratorfunction(editor.open):
                on_editorReady(mainWindow, editor, cursorPosition, focus)(list(editor.open(filePath)))
            else:
                on_editorReady(mainWindow, editor, cursorPosition, focus)(editor.open(filePath))

    def openDirectory(self, directoryPath):
        raise NotImplementedError("Directory contents should be opened as files here")

    def openUrl(self, url):
        if isinstance(url, six.string_types):
            url = QtCore.QUrl(url)
        if url.scheme() == "txmt":
            sourceFile = url.queryItemValue('url')
            position = (0, 0)
            line = url.queryItemValue('line')
            if line.isdigit():
                position = (int(line) - 1, position[1])
            column = url.queryItemValue('column')
            if column.isdigit():
                position = (position[0], int(column) - 1)
            if sourceFile:
                filePath = QtCore.QUrl(sourceFile, QtCore.QUrl.TolerantMode).toLocalFile()
                self.openFile(filePath, cursorPosition = position)
            else:
                self.currentEditor().setCursorPosition(position)
        elif url.scheme() == "file":
            self.openFile(url.toLocalFile())
        else:
            QtGui.QDesktopServices.openUrl(url)

    def openPath(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                self.openFile(path)
            else:
                self.openDirectory(path)

    # ------- Shortcuts
    def registerShortcut(self, qobject, sequence):
        """Register QAction or QShortcut to Prymatex main application,
        with sequence
        """
        self.shortcutsTreeModel.registerShortcut(qobject, sequence)

    def applyShortcuts(self):
        self.shortcutsTreeModel.applyShortcuts()

    def checkExternalAction(self, mainWindow, editor):
        if editor.isExternalChanged():
            message = "The file '%s' has been changed on the file system, Do you want to replace the editor contents with these changes?"
            result = QtGui.QMessageBox.question(editor, _("File changed"),
                                                _(message) % editor.filePath,
                                                buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                defaultButton=QtGui.QMessageBox.Yes) if self.askAboutExternalChanges else QtGui.QMessageBox.Yes
            if result == QtGui.QMessageBox.Yes:
                if inspect.isgeneratorfunction(editor.reload):
                    task = self.schedulerManager.newTask(editor.reload())
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
