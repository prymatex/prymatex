#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from functools import partial
from collections import OrderedDict

import prymatex

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_shortcut
from prymatex.qt.extensions import ContextKeySequence

from prymatex.utils.i18n import ugettext as _
from prymatex.utils import six
from prymatex.utils import text as textutils
from prymatex.utils.processes import get_process_map

from prymatex.gui.main import PrymatexMainWindow
from prymatex.widgets.texteditor import TextEditWidget

from . import config
from . import exceptions
from . import logger
from . import notifier
from .components import PrymatexComponent, PrymatexEditor
from .settings import ConfigurableItem, ConfigurableHook
from .namespace import Namespace

class PrymatexApplication(PrymatexComponent, QtWidgets.QApplication):
    """The application instance.
    There can't be two apps running simultaneously, since configuration issues may occur.
    The application loads the Support."""
    # --------------------- Signals
    windowCreated = QtCore.Signal(object)
    aboutToWindowDelete = QtCore.Signal(object)
    aboutToWindowChange = QtCore.Signal(object)
    windowChanged = QtCore.Signal(object)

    # ---------------------- Settings
    SETTINGS = "global"

    @ConfigurableItem()
    def qt_style(self, styleName):
        if styleName:
            self.setStyle(styleName)

    @ConfigurableItem(default="default")
    def qt_style_sheet(self, styleSheetName):
        styleSheet = self.resources().get_stylesheets().get(styleSheetName)
        if styleSheet is not None:
            self.setStyleSheet(styleSheet.content)

    @ConfigurableItem(default=QtGui.QIcon.themeName())
    def icon_theme(self, iconThemeName):
        self.resources().set_theme(iconThemeName)

    askAboutExternalDeletions = ConfigurableItem(default=False)
    askAboutExternalChanges = ConfigurableItem(default=False)
    shortcuts = ConfigurableItem(default={})

    RESTART_CODE = 1000

    def __init__(self, options, *args, **kwargs):
        """Inicialización de la aplicación."""
        super(PrymatexApplication, self).__init__(**kwargs)

        # Some init's
        self.setApplicationName(prymatex.__name__.title())
        self.setObjectName(prymatex.__name__.title())
        self.setApplicationVersion(prymatex.__version__)
        self.setOrganizationDomain(prymatex.__url__)
        self.setOrganizationName(prymatex.__author__)
        self.platform = sys.platform
        self.options = options

        self._namespaces = OrderedDict()
        self.component_classes = {}
        self.component_instances = {}
        self.default_component = type("DefaultComponent", (PrymatexEditor, TextEditWidget), {})

        # Base Managers
        self.resourceManager = self.profileManager = self.packageManager = self.settingsManager = None
        # Windows
        self._main_windows = []

        # Connects
        self.aboutToQuit.connect(self.closePrymatex)
        self.lastWindowClosed.connect(self.quit)
        
        # Exceptions
        self.replaceSysExceptHook()
        
        # File Notifier
        #notifier.start_notifier()
    
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

    def initialize(self):
        # Connect signals
        self.fileManager.openFileChanged.connect(self.on_fileManager_openFileChanged)
        self.applyOptions()

    def finalize(self):
        pass

    # ------- Prymatex's micro kernel
    @staticmethod
    def instance(*args, **kwargs):
        # Bootstrap
        from prymatex.managers.resources import ResourceManager
        from prymatex.managers.profiles import ProfileManager
        from prymatex.managers.settings import SettingsManager
        from prymatex.managers.packages import PackageManager
        from prymatex.managers.storage import StorageManager
        from prymatex.managers.support import SupportManager
        from prymatex.managers.files import FileManager
        from prymatex.managers.projects import ProjectManager
        from prymatex.managers.server import ServerManager
        
        # Build Application
        app = PrymatexApplication(*args, **kwargs)

        # Build Managers resources, profile and settings are the backbone of prymatex
        app.profileManager = app.createComponentInstance(ProfileManager, parent=app)
        app.settingsManager = app.createComponentInstance(SettingsManager, parent=app)
        app.resourceManager = app.createComponentInstance(ResourceManager, parent=app)
        
        # Populate application's class
        app.populateComponentClass(PrymatexApplication)
        app.populateComponentClass(PrymatexMainWindow)

        # Build more Managers
        app.packageManager = app.createComponentInstance(PackageManager, parent=app)        
        app.storageManager = app.createComponentInstance(StorageManager, parent=app)
        app.supportManager = app.createComponentInstance(SupportManager, parent=app)
        app.fileManager = app.createComponentInstance(FileManager, parent=app)
        app.projectManager = app.createComponentInstance(ProjectManager, parent=app)
        app.serverManager = app.createComponentInstance(ServerManager, parent=app)

        # Add builtin Namespaces
        for name, path in config.BUILTINS:
            namespace = app.createNamespace(name, path, builtin=True)
            app.addNamespace(namespace)
        
        # Configure Application instance
        app.settingsManager.registerConfigurableInstance(app)
        app.initialize()

        return app

    def applyOptions(self):
        # Logger
        logger.config(self.options.verbose, self.profile().PMX_LOG_PATH,
            self.options.log_pattern)
        # Reset
        if self.options.reset_settings:
            self.profile().clear()

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
        
        return [ GeneralSettingsWidget ]

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
            'PMX_PROFILE_NAME': self.profile().get('PMX_PROFILE_NAME'),
            'PMX_PROFILE_PATH': self.profile().get('PMX_PROFILE_PATH'),
            'PMX_TMP_PATH': self.profile().get('PMX_TMP_PATH'),
            'PMX_LOG_PATH': self.profile().get('PMX_LOG_PATH')
        }
        for manager in [self.resourceManager, self.profileManager,
            self.packageManager, self.storageManager, self.supportManager,
            self.fileManager, self.projectManager,
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
            # Load Packages
            self.packageManager.loadPackages(self.showMessage)            
            # Load Resources
            self.resourceManager.loadResources(self.showMessage)
            # Load Bundles
            self.supportManager.loadSupport(self.showMessage)
            # Load Projects
            self.projectManager.loadProjects(self.showMessage)
            # Load Settings
            self.settingsManager.loadSettings(self.showMessage)

            # Restore State
            self.settingsManager.restoreApplicationState()
            window = self.currentWindow()
            if not window:
                window = self.createMainWindow(editor=True)
            
            # Change messages handler
            def show_message(app):
                def _show_message(*args, **kwargs):
                    app.currentWindow().showMessage(*args, **kwargs)
                return _show_message
            self.showMessage = show_message(self)

            if not self.options.no_splash:
                splash.finish(window)

            window.show()
            
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
        if os.path.exists(self.fileLock):
            with open(self.fileLock) as fp:
                pid = fp.read()
            try:
                pid = int(pid)
            except ValueError:
                self.logger().debug("Prymatex might have not closed cleanly last "
                    "session")
            else:
                if pid in get_process_map():
                    raise exceptions.AlreadyRunningError("The '%s' profile seems to be running. Please close the "
                                "instance or run other profile." %
                                (self.profile().PMX_PROFILE_NAME,))
            os.remove(self.fileLock)

        f = open(self.fileLock, 'w')
        f.write('%s' % self.applicationPid())
        f.close()
    
    def setTimeout(self, delay, callback):
        return QtCore.QTimer.singleShot(delay, callback)
    
    # ----------- Namespaces
    def createNamespace(self, name, path, builtin=False):
        # Build one unique name
        counter = 1
        name = textutils.slugify(name)
        while name in self._namespaces:
            name = textutils.slugify("%s %d" % (name, counter))
            counter += 1
        return Namespace(name, path, builtin)
        
    def addNamespace(self, namespace):
        assert not [ ns for ns in self._namespaces.values() if ns.path == namespace.path ], "Namespace is allready registered"
        self._namespaces[namespace.name] = namespace
        self.resourceManager.addNamespace(namespace)
        self.packageManager.addNamespace(namespace)
        self.supportManager.addNamespace(namespace)

    def namespace(self, name):
        return self._namespaces.get(name)

    def namespaces(self):
        return list(self._namespaces.values())

    def builtins(self):
        return [ ns for ns in self.namespaces() if ns.builtin ]
        
    def protectedNamespace(self):
        return self.namespaces()[0]
        
    # ---------- OVERRIDE: PrymatexComponent.componentState()
    def componentState(self):
        componentState = super(PrymatexApplication, self).componentState()

        componentState["windows"] = []
        for window in self.mainWindows():
            componentState["windows"].append(window.componentState())
        
        componentState["project_manager"] = self.projectManager.componentState()
        componentState["file_manager"] = self.fileManager.componentState()

        return componentState

    # ---------- OVERRIDE: PrymatexComponent.setComponentState()
    def setComponentState(self, componentState):
        super(PrymatexApplication, self).setComponentState(componentState)

        if "project_manager" in componentState:
            self.projectManager.setComponentState(componentState["project_manager"])

        if "file_manager" in componentState:
            self.fileManager.setComponentState(componentState["file_manager"])

        # Restore open documents
        for windowState in componentState.get("windows", []):
            window = self.createMainWindow()
            window.setComponentState(windowState)

    # --------------------- Application events
    def closePrymatex(self):
        self.logger().debug("Close")

        self.storageManager.close()
        if os.path.exists(self.fileLock):
            os.unlink(self.fileLock)

    # --------------------- Populate components
    def populateComponentClass(self, component_class):
        if component_class._populated:
            return

        # ------- Application
        component_class.__application = self
        component_class.application = classmethod(lambda cls: cls.__application)

        # ------- Logger
        component_class.__logger = self.getLogger('.'.join([component_class.__module__, component_class.__name__]))
        component_class.logger = classmethod(lambda cls: cls.__logger)

        # ------- Resources
        component_class.__resources = None
        def get_resources(app):
            def _get_resources(cls):
                if cls.__resources is None and app.resourceManager is not None:
                    cls.__resources = app.resourceManager.providerForClass(cls)
                return cls.__resources
            return _get_resources
        component_class.resources = classmethod(get_resources(self))

        # ------- Profile
        component_class.__profile = None
        def get_profile(app):
            def _get_profile(cls):
                if cls.__profile is None and app.profileManager is not None:
                    cls.__profile = app.profileManager.profileForClass(cls)
                return cls.__profile
            return _get_profile
        component_class.profile = classmethod(get_profile(self))

        # ------- Settings
        component_class.__settings = None
        def get_settings(app):
            def _get_settings(cls):
                if cls.__settings is None and app.settingsManager is not None:
                    cls.__settings = app.settingsManager.settingsForClass(cls)
                return cls.__settings
            return _get_settings
        component_class.settings = classmethod(get_settings(self))
        if self.settingsManager is not None:
            self.settingsManager.populateConfigurableClass(component_class)
        component_class._populated = True

    # ------------------- Create components
    def createComponentInstance(self, componentClass, *args, **kwargs):

        # ------------------- Build
        def buildComponentInstance(klass, *args, **kwargs):
            self.populateComponentClass(klass)

            component = klass(*args, **kwargs)

            # Add components
            for componentClass in self.findComponentsForClass(klass):
                # Filter editors, editors create explicit
                if issubclass(componentClass, PrymatexEditor):
                    continue
                subComponent = buildComponentInstance(componentClass, parent=component)
                component.addComponent(subComponent)
            return component

        component = buildComponentInstance(componentClass, *args, **kwargs)

        # ------------------- Setup components Bottom-up
        components = [ component ] + list(component.components())
        for instance in components[::-1]:
            # Settings
            if self.settingsManager is not None:
                self.settingsManager.registerConfigurableInstance(instance)
            # Initialize
            instance.initialize()
            # Shortcuts
            for settings in instance.contributeToShortcuts():
                create_shortcut(component, settings,
                            sequence_handler=partial(self.registerShortcut,
                                                     instance.__class__))

        # -------------------- Store
        self.component_instances.setdefault(componentClass, []).append(component)

        return component

    def deleteComponentInstance(self, component):
        # ------------------- Remove
        self.component_instances[component.__class__].remove(component)

        # ------------------- Unsetup components Bottom-up
        components = [ component ] + list(component.components())
        for instance in components[::-1]:
            if self.settingsManager is not None:
                self.settingsManager.unregisterConfigurableInstance(instance)
            instance.finalize()

        # ------------------- Delete
        component.deleteLater()

    # ------------ Handle component classes
    def registerComponent(self, klass, base, default):
        self.populateComponentClass(klass)
        self.component_classes.setdefault(base, []).append(klass)
        if default:
            self.default_component = klass

    def componentHierarchyForClass(self, klass):
        hierarchy = []
        while klass != PrymatexMainWindow:
            hierarchy.append(klass)
            for parent, childs in self.component_classes.items():
                if klass in childs:
                    klass = parent
                    break
        return hierarchy[::-1]

    def findComponentsForClass(self, klass):
        return self.component_classes.get(klass, [])

    # ------------ Handle editor classes
    def findEditorClassByName(self, name):
        editors = (cmp for cmp in self.component_classes.get(PrymatexMainWindow, []) if issubclass(cmp, PrymatexEditor))
        for klass in editors:
            if name == klass.__name__:
                return klass

    def findEditorClassForFile(self, filepath):
        mimetype = self.fileManager.mimeType(filepath)
        editors = (cmp for cmp in self.component_classes.get(PrymatexMainWindow, []) if issubclass(cmp, PrymatexEditor))
        for klass in editors:
            if klass.acceptFile(filepath, mimetype):
                return klass
    
    def defaultEditor(self):
        return self.default_component

    # ------------- Settings access
    def on_settings_changed(self, path):
        print("Cambiaron los settings", path)
        
    def settingValue(self, settingPath):
        return self.settingsManager.settingValue(settingPath)

    def registerSettingCallback(self, settingPath, handler):
        self.settingsManager.registerSettingCallback(settingPath, handler)

    def unregisterSettingCallback(self, settingPath, handler):
        self.settingsManager.unregisterSettingCallback(settingPath, handler)

    # ------------- Main windows handlers
    def findEditorForFile(self, filepath):
        for window in self.mainWindows():
            editor = window.findEditorForFile(filepath)
            if editor:
                return editor

    def mainWindows(self):
        return self._main_windows

    def createMainWindow(self, editor=False):
        """Creates the windows"""
        window = self.createComponentInstance(PrymatexMainWindow)
        self.windowCreated.emit(window)
        if editor:
            window.addEmptyEditor()
        self._main_windows.append(window)    
        return window

    def currentWindow(self):
        windows = self.mainWindows()
        if windows:
            return windows[0]

    def closeAllWindows(self):
        for window in self._main_windows:
            window.close()

    # ---- Open (file)
    def openFile(self, path, position=None, editor_name=None, focus=True, window=None):
        """Open a editor in current window"""
        path = self.fileManager.normcase(path)

        editor = self.findEditorForFile(path)
        if editor is None:
            window = window or self.currentWindow()
            editor = window.createEditor(
                file_path=path,
                class_name=editor_name)
            window.addEditor(editor, focus)
        elif focus:
            window = editor.window()
            window.setCurrentEditor(editor)
        if position is not None:
            editor.setCursorPosition(position)
        return editor

    def openDirectory(self, directoryPath):
        raise NotImplementedError("Directory contents should be opened as files here")

    def openUrl(self, url):
        if not isinstance(url, QtCore.QUrl):
            url = QtCore.QUrl(url)
        if url.scheme() == "txmt":
            query = QtCore.QUrlQuery(url.query())
            source_file = query.queryItemValue('url')
            position = (0, 0)
            line = query.queryItemValue('line')
            if line.isdigit():
                position = (int(line) - 1, position[1])
            column = query.queryItemValue('column')
            if column.isdigit():
                position = (position[0], int(column) - 1)
            if source_file:
                self.openFile(source_file, cursorPosition=position)
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
        sequence = ContextKeySequence(*sequence)
        # TODO: Algo interesante si no hago esto podria registrar para todo lo que tenga keysequence
        if sequence:    
            shortcut = self.resourceManager.registerShortcut(qobject, sequence)
            if shortcut.identifier() in self.shortcuts:
                shortcut.setKeySequence(self.shortcuts[shortcut.identifier()])

    EXTERNAL_DELETED = 1 << 0
    EXTERNAL_CHANGED = 1 << 1
    def checkExternalAction(self, window, editor):
        action = editor.externalAction()
        if action == self.EXTERNAL_CHANGED:
            message = ("The file '%s' has been changed on the file system, Do you want to "
            "replace the editor contents with these changes?")
            result = QtWidgets.QMessageBox.question(editor, _("File changed"),
                                                _(message) % editor.windowFilePath(),
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,  # NOQA
                                                defaultButton=QtWidgets.QMessageBox.Yes) if self.askAboutExternalChanges else QtWidgets.QMessageBox.Yes  # NOQA
            if result == QtWidgets.QMessageBox.Yes:
                editor.reload()
            elif result == QtWidgets.QMessageBox.No:
                pass
        elif action == self.EXTERNAL_DELETED:
            message = ("The file '%s' has been deleted or is not accessible. Do you want "
                       "to save your changes or close the editor without saving?")
            result = QtWidgets.QMessageBox.question(
                editor, _("File deleted"),
                _(message) % editor.windowFilePath(),
                buttons=QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Close,
                defaultButton=QtWidgets.QMessageBox.Close) if self.askAboutExternalDeletions else QtWidgets.QMessageBox.Close  # NOQA
            if result == QtWidgets.QMessageBox.Close:
                window.closeEditor(editor)
            elif result == QtWidgets.QMessageBox.Save:
                window.saveEditor(editor)

    def on_fileManager_openFileChanged(self, file_path):
        editor = self.findEditorForFile(file_path)
        window = editor.window()
        action = self.fileManager.exists(file_path) and self.EXTERNAL_CHANGED or self.EXTERNAL_DELETED
        editor.setExternalAction(action)
        if window.currentEditor() == editor:
            self.checkExternalAction(window, editor)

    def __str__(self):
        return '<PrymatexApplication at {} PID: {}>'.format(hash(self), os.getpid())

    __unicode__ = __repr__ = __str__
