#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from functools import partial

import prymatex

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_shortcut
from prymatex.qt.quamash import QEventLoop

from prymatex.core import config
from prymatex.core.components import PrymatexComponent, PrymatexEditor
from prymatex.core import logger
from prymatex.core.settings import ConfigurableItem, ConfigurableHook

from prymatex.utils.i18n import ugettext as _
from prymatex.utils import six
from prymatex.utils.processes import get_process_map

from prymatex.models.shortcuts import ShortcutsTreeModel

class PrymatexApplication(PrymatexComponent, QtWidgets.QApplication):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the Support."""

    # ---------------------- Settings
    SETTINGS = "Global"
    RESOURCES = (config.USR_NS_NAME, config.PMX_NS_NAME)

    @ConfigurableItem()
    def qtStyle(self, styleName):
        if styleName:
            self.setStyle(styleName)

    @ConfigurableItem(default="default")
    def qtStyleSheet(self, styleSheetName):
        styleSheet = self.resources().get_stylesheets().get(styleSheetName)
        if styleSheet is not None:
            self.setStyleSheet(styleSheet.content)

    @ConfigurableItem(default=QtGui.QIcon.themeName())
    def iconTheme(self, iconThemeName):
        self.resources().set_theme(iconThemeName)

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

        #self._event_loop = QEventLoop(self)
        #asyncio.set_event_loop(self._event_loop)
        
        # Windows
        self._main_windows = []

        # Connects
        self.aboutToQuit.connect(self.closePrymatex)
        self.componentInstances = {}
        self.shortcutsTreeModel = ShortcutsTreeModel(self)
        self.replaceSysExceptHook()
    
    def eventLoop(self):
        return self._event_loop

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
        QtCore.qInstallMessageHandler(self.qtMessageHandler)

    def qtMessageHandler(self, *args, **kwargs):
        ''' Route Qt messaging system into Prymatex/Python one'''
        if args[0] == QtCore.QtDebugMsg:
            self.logger().debug(args[-1])
        elif args[0] == QtCore.QtWarningMsg:
            self.logger().warn(args[-1])
        elif args[0] == QtCore.QtCriticalMsg:
            self.logger().critical(args[-1])
        elif args[0] == QtCore.QtFatalMsg:
            self.logger().fatal(args[-1])
        elif args[0] == QtCore.QtSystemMsg:
            self.logger().debug("System: %s" % args[-1])

    # ------- prymatex's micro kernel
    def applyOptions(self, options):
        # The basic managers
        self.options = options
        self.resourceManager = self.profileManager = self.pluginManager = None        
        
        # Prepare resources
        from prymatex.managers.resources import ResourceManager
        self.resourceManager = self.createComponentInstance(ResourceManager, parent=self)
        self.resourceManager.install_icon_handler()
        for ns, path in config.NAMESPACES:
            self.resourceManager.add_source(ns, path, True)

        # Prepare profile
        from prymatex.managers.profile import ProfileManager
        self.profileManager = self.createComponentInstance(ProfileManager, parent=self)
        self.profileManager.install_current_profile(options.profile)

        # Prepare settings for application
        self.populateComponentClass(PrymatexApplication)
        self.profile().registerConfigurableInstance(self)

        if self.options.reset_settings:
            self.profile().clear()

        logger.config(self.options.verbose, self.profile().PMX_LOG_PATH,
                      self.options.log_pattern)

        return self.checkSingleInstance()

    def installTranslator(self):
        pass
        # slanguage = QtCore.QLocale.system().name()
        # print language
        # self.translator = QtCore.QTranslator()
        # print os.path.join(config.PMX_SHARE_PATH, "Languages")

        # self.translator.load(settings.LANGUAGE)
        # self.installTranslator(translator)

    # ---------------------- PrymatexComponent methods
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.general import GeneralSettingsWidget
        from prymatex.gui.settings.shortcuts import ShortcutsSettingsWidget

        return [GeneralSettingsWidget, ShortcutsSettingsWidget]

    def environmentVariables(self):
        env = {
            # TextMate Compatible
            'TM_APP_PATH': config.PMX_APP_PATH,
            'PMX_APP_PATH': config.PMX_APP_PATH,
            'TM_PID': self.applicationPid(),
            'PMX_PID': self.applicationPid(),
            'PMX_VERSION': self.applicationVersion(),
            'PMX_APP_NAME': self.applicationName().title(),
            'PMX_HOME_PATH': config.PMX_HOME_PATH,
            'PMX_PROFILE_NAME': self.profile().value('PMX_PROFILE_NAME'),
            'PMX_PROFILE_PATH': self.profile().value('PMX_PROFILE_PATH'),
            'PMX_TMP_PATH': self.profile().value('PMX_TMP_PATH'),
            'PMX_LOG_PATH': self.profile().value('PMX_LOG_PATH')
        }
        for manager in [self.resourceManager, self.profileManager,
            self.pluginManager, self.storageManager, self.supportManager,
            self.fileManager, self.projectManager, self.schedulerManager,
            self.serverManager]:
            env.update(manager.environmentVariables())
        return env

    def loadGraphicalUserInterface(self):
        self.showMessage = self.logger().info
        if not self.options.no_splash:
            from prymatex.widgets.splash import SplashScreen
            splash_image = self.resources().get_image('newsplash')
            splash = SplashScreen(splash_image)
            splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)

            splashFont = QtGui.QFont("Monospace", 11)
            splashFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

            splash.setFont(splashFont)
            splash.setMask(splash_image.mask())
            splash.show()
            self.showMessage = splash.showMessage
        try:
            # Build Managers WARN: Order is important
            self.pluginManager = self.buildPluginManager()      # Plugin manager
            self.storageManager = self.buildStorageManager()    # Persistence system Manager  # NOQA
            self.supportManager = self.buildSupportManager()    # Support Manager
            self.fileManager = self.buildFileManager()          # File Manager
            self.projectManager = self.buildProjectManager()    # Project Manager
            self.schedulerManager = self.buildSchedulerManager()
            self.serverManager = self.buildServerManager()
            
            # Load Bundles
            self.supportManager.loadSupport(self.showMessage)

            # Load Projects
            self.projectManager.loadProjects(self.showMessage)

            # Create Main Window
            main_window = self.buildMainWindow()

            # Change messages handler
            self.showMessage = main_window.showMessage

            # Load settings
            self.profileManager.loadSettings(self.showMessage)

            # Load standard shortcuts
            self.shortcutsTreeModel.loadStandardSequences(self.resources())

            if not self.options.no_splash:
                splash.finish(main_window)

            main_window.show()
            self.logger().info("Application startup")
        except KeyboardInterrupt:
            self.logger().critical("Quit signal catched during application startup. "
                                   "Quiting...")
            self.quit()

    def execute(self):
        return self.exec_()
        #self._event_loop.run_forever()

    def unloadGraphicalUserInterface(self):
        # TODO: ver como dejar todo lindo y ordenado para terminar correctamente
        # if self.zmqContext is not None:
        #     self.zmqContext.destroy()
        for main_window in self.mainWindows():
            main_window.close()
            main_window.deleteLater()

    def restart(self):
        self.exit(self.RESTART_CODE)

    def checkSingleInstance(self):
        """Checks if there's another instance using current profile"""
        self.fileLock = os.path.join(self.profile().PMX_PROFILE_PATH, 'prymatex.pid')
        remove_profile_lock = False
        if os.path.exists(self.fileLock):
            with open(self.fileLock) as fp:
                pid = fp.read()
            try:
                pid = int(pid)
            except ValueError:
                self.getLogger().debug("Prymatex might have not closed cleanly last "
                                       "session")
                remove_profile_lock = True
            else:
                if pid in get_process_map():
                    self.logger().critical("%s seems to be running. Please close the "
                                           "instance or run other profile." %
                                           (self.profile().PMX_PROFILE_NAME,))
                    remove_profile_lock = False
                else:
                    remove_profile_lock = True
        if remove_profile_lock:
            os.remove(self.fileLock)

        f = open(self.fileLock, 'w')
        f.write('%s' % self.applicationPid())
        f.close()
        return True

    # -------------------- Managers
    def buildPluginManager(self):
        from prymatex.managers.plugins import PluginManager
        manager = self.createComponentInstance(PluginManager, parent=self)
        
        for source in self.resources().sources():
            manager.addNamespace(source.name(), source.path())

        manager.loadPlugins()
        return manager

    def buildSupportManager(self):
        from prymatex.managers.support import SupportManager
        manager = self.createComponentInstance(SupportManager, parent=self)

        for source in reversed(self.resources().sources()):
            manager.addNamespace(source.name(), source.path())

        return manager

    def buildFileManager(self):
        from prymatex.managers.files import FileManager
        manager = self.createComponentInstance(FileManager, parent=self)

        manager.fileSytemChanged.connect(self.on_fileManager_fileSytemChanged)
        return manager

    def buildProjectManager(self):
        from prymatex.managers.projects import ProjectManager
        return self.createComponentInstance(ProjectManager, parent=self)

    def buildStorageManager(self):
        from prymatex.managers.storage import StorageManager
        return self.createComponentInstance(StorageManager, parent=self)

    def buildSchedulerManager(self):
        from prymatex.managers.coroutines import SchedulerManager
        return self.createComponentInstance(SchedulerManager, parent=self)

    def buildServerManager(self):
        from prymatex.managers.server import ServerManager
        return self.createComponentInstance(ServerManager, parent=self)

    # --------------------- Application events
    def closePrymatex(self):
        self.logger().debug("Close")

        self.storageManager.close()
        for main_window in self.mainWindows():
            self.profile().saveState(main_window)
        self.profile().sync()
        if os.path.exists(self.fileLock):
            os.unlink(self.fileLock)

    # --------------------- Populate components
    def populateComponentClass(self, componentClass):
        # ------- Application
        componentClass._application = self
        componentClass.application = classmethod(lambda cls: cls._application)

        # ------- Logger
        componentClass._logger = self.getLogger('.'.join([componentClass.__module__,
                                                componentClass.__name__]))
        componentClass.logger = classmethod(lambda cls: cls._logger)

        # ------- Resources
        componentClass._resources = self.resourceManager.providerForClass(componentClass) if self.resourceManager else None 
        componentClass.resources = classmethod(lambda cls: cls._resources)

        # ------- Profile
        componentClass._profile = self.profileManager.profileForClass(componentClass) if self.profileManager else None
        componentClass.profile = classmethod(lambda cls: cls._profile)

        # ------- Settings
        componentClass._settings = componentClass.profile().settingsForClass(componentClass) if componentClass.profile() else None
        componentClass.settings = classmethod(lambda cls: cls._settings)

        if issubclass(componentClass, PrymatexComponent):
            # Add settings widgets
            for settingClass in componentClass.contributeToSettings():
                self.populateComponentClass(settingClass)
                settingWidget = settingClass( settings=componentClass.settings(),
                    profile=componentClass.profile())
                componentClass.settings().addDialog(settingWidget)
                self.profileManager.registerSettingsWidget(settingWidget)
        componentClass._pmx_populated = True

    # ------------------- Create components
    def createComponentInstance(self, componentClass, **kwargs):
        if not getattr(componentClass, '_pmx_populated', False):
            self.populateComponentClass(componentClass)

        # ------------------- Build
        buildedInstances = []

        def buildComponentInstance(klass, **kwargs):
            component = klass(**kwargs)

            # Add components
            componentClasses = self.pluginManager is not None and \
                self.pluginManager.findComponentsForClass(klass) or []
            for componentClass in componentClasses:
                # Filter editors, editors create explicit
                if issubclass(componentClass, PrymatexEditor):
                    continue
                subComponent = buildComponentInstance(componentClass, parent=component)
                component.addComponent(subComponent)
            buildedInstances.append(component)
            return component

        component = buildComponentInstance(componentClass, **kwargs)

        # ------------------- Configure Bottom-up
        profile = componentClass.profile()
        if profile:
            for instance in buildedInstances[::-1]:
                profile.registerConfigurableInstance(instance)

        # ------------------- Initialize Top-down
        for instance in buildedInstances:
            instance.initialize()
            # Shortcuts
            for settings in instance.contributeToShortcuts():
                create_shortcut(component, settings,
                                sequence_handler=partial(self.registerShortcut,
                                                         instance.__class__))

        # -------------------- Store
        self.componentInstances.setdefault(componentClass, []).append(component)

        return component

    def deleteComponentInstance(self, component):
        self.profile().unregisterConfigurableInstance(component)
        component.deleteLater()

    # ------------ Find Component
    def componentHierarchyForClass(self, componentClass):
        return self.pluginManager.componentHierarchyForClass(componentClass)

    def findComponentsForClass(self, componentClass):
        return self.pluginManager.findComponentsForClass(componentClass)

    # ------------- Settings access
    def settingValue(self, settingPath):
        return self.profile().settingValue(settingPath)

    def registerSettingHook(self, settingPath, handler):
        self.profile().registerSettingHook(settingPath, handler)

    def unregisterSettingHook(self, settingPath, handler):
        self.profile().unregisterSettingHook(settingPath, handler)

    # ------------- Editors and windows handle
    def createEditorInstance(self, class_name = None, file_path=None,
                             cursor_position=None, parent=None):
        editorClass = None
        if class_name is not None:
            editorClass = self.pluginManager.findEditorClassByName(class_name)
        elif file_path is not None:
            editorClass = self.pluginManager.findEditorClassForFile(file_path)
        if editorClass is None:
            editorClass = self.pluginManager.defaultEditor()

        # Exists file ?
        if file_path and not self.fileManager.isfile(file_path):
            file_path = None
        editor = self.createComponentInstance(editorClass,
                                              parent=parent,
                                              file_path=file_path
                                              )
        if file_path:
            editor.open(file_path)
        if cursor_position:
            editor.setCursorPosition(cursor_position)
        return editor

    def deleteEditorInstance(self, editor):
        editor.close()
        self.deleteComponentInstance(editor)

    def findEditorForFile(self, filepath):
        for main_window in self.mainWindows():
            editor = main_window.findEditorForFile(filepath)
            if editor:
                return main_window, editor

    def mainWindows(self):
        return self._main_windows

    def buildMainWindow(self):
        """Creates the windows"""
        from prymatex.gui.main import PrymatexMainWindow

        main_window = self.createComponentInstance(PrymatexMainWindow)

        self.profile().restoreState(main_window)

        if not main_window.editors():
            main_window.addEmptyEditor()
        self._main_windows.append(main_window)
        return main_window

    def currentWindow(self):
        # TODO Aca retornar la window actual
        return self._main_windows[0]

    def canBeHandled(self, filepath):
        # from prymatex.utils.pyqtdebug import ipdb_set_trace
        # ipdb_set_trace()
        ext = os.path.splitext(filepath)[1].replace('.', '')
        for fileTypes in [syntax.item.fileTypes for syntax in
                          self.supportManager.getAllSyntaxes()
                          if hasattr(syntax.item, 'fileTypes') and
                          syntax.item.fileTypes]:

            if ext in fileTypes:
                return True
        return False

    # ---- Open (file, directory, url, canelones)
    def openFile(self, filepath, cursorPosition=None, focus=True, main_window=None):
        """Open a editor in current window"""
        file_path = self.fileManager.normcase(filepath)

        if self.fileManager.isOpen(file_path):
            main_window, editor = self.findEditorForFile(file_path)
            if editor is not None:
                main_window.setCurrentEditor(editor)
                if cursorPosition is not None:
                    editor.setCursorPosition(cursorPosition)
        elif self.fileManager.exists(file_path):
            main_window = main_window or self.currentWindow()
            editor = self.createEditorInstance(
                file_path=file_path,
                cursor_position=cursorPosition,
                parent=main_window,
                )
            # TODO el dialogo de no tengo editor para ese tipo de archivo
            if editor is not None:
                main_window.tryCloseEmptyEditor()
                main_window.addEditor(editor, focus)

    def openDirectory(self, directoryPath):
        raise NotImplementedError("Directory contents should be opened as files here")

    def openUrl(self, url):
        if isinstance(url, six.string_types):
            url = QtCore.QUrl(url)
        if url.scheme() == "txmt":
            query = QtCore.QUrlQuery(url.query())
            sourceFile = query.queryItemValue('url')
            position = (0, 0)
            line = query.queryItemValue('line')
            if line.isdigit():
                position = (int(line) - 1, position[1])
            column = query.queryItemValue('column')
            if column.isdigit():
                position = (position[0], int(column) - 1)
            if sourceFile:
                filePath = QtCore.QUrl(sourceFile, QtCore.QUrl.TolerantMode).toLocalFile()
                self.openFile(filePath, cursorPosition=position)
            else:
                self.currentWindow().currentEditor().setCursorPosition(position)
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

    # ------- Icons
    def registerIcon(self, componentClass, qobject, icon):
        if not isinstance(icon, QtGui.QIcon):
            icon = componentClass.resources().get_icon(icon)
        if not icon.isNull():
            qobject.setIcon(icon)

    # ------- Shortcuts
    def registerShortcut(self, componentClass, qobject, sequence):
        """Register QAction or QShortcut to Prymatex main application,
        with sequence
        """
        if not isinstance(sequence, (tuple, list)):
            sequence = ("Global", sequence)
        sequence = componentClass.resources().get_sequence(*sequence)
        if not sequence.isEmpty():
            self.shortcutsTreeModel.registerShortcut(qobject, sequence)

    def applyShortcuts(self):
        self.shortcutsTreeModel.applyShortcuts()

    def checkExternalAction(self, main_window, editor):
        if editor.isExternalChanged():
            message = ("The file '%s' has been changed on the file system, Do you want to "
            "replace the editor contents with these changes?")
            result = QtGui.QMessageBox.question(editor, _("File changed"),
                                                _(message) % editor.filePath,
                                                buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,  # NOQA
                                                defaultButton=QtGui.QMessageBox.Yes) if self.askAboutExternalChanges else QtGui.QMessageBox.Yes  # NOQA
            if result == QtGui.QMessageBox.Yes:
                editor.reload()
            elif result == QtGui.QMessageBox.No:
                pass
        elif editor.isExternalDeleted():
            message = ("The file '%s' has been deleted or is not accessible. Do you want "
                       "to save your changes or close the editor without saving?")
            result = QtGui.QMessageBox.question(
                editor, _("File deleted"),
                _(message) % editor.filePath,
                buttons=QtGui.QMessageBox.Save | QtGui.QMessageBox.Close,
                defaultButton=QtGui.QMessageBox.Close) if self.askAboutExternalDeletions else QtGui.QMessageBox.Close  # NOQA
            if result == QtGui.QMessageBox.Close:
                main_window.closeEditor(editor)
            elif result == QtGui.QMessageBox.Save:
                main_window.saveEditor(editor)

    def on_fileManager_fileSytemChanged(self, filePath, change):
        main_window, editor = self.findEditorForFile(filePath)
        editor.setExternalAction(change)
        if main_window.currentEditor() == editor:
            self.checkExternalAction(main_window, editor)

    def __str__(self):
        return '<PrymatexApplication at {} PID: {}>'.format(hash(self), os.getpid())

    __unicode__ = __repr__ = __str__
