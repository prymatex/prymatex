#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.compat import getSaveFileName
from prymatex.qt.helpers import (text_to_objectname, create_menu, extend_menu,
    add_actions, test_actions, center_widget, qbytearray_to_hex, hex_to_qbytearray)

from prymatex.core import exceptions
from prymatex.core.settings import (ConfigurableItem, ConfigurableHook)
from prymatex.core import (PrymatexComponentWidget, PrymatexComponent,
    PrymatexDock, PrymatexDialog, PrymatexStatusBar)

from prymatex.utils.i18n import ugettext as _
from prymatex.utils import html

from prymatex.widgets.docker import DockWidgetTitleBar
from prymatex.widgets.toolbar import DockWidgetToolBar
from prymatex.widgets.notification import OverlayNotifier
from prymatex.widgets.splitter import SplitterWidget

from prymatex.support.regexp import Snippet as Template

from .menubar import PrymatexMainMenuBar
from .statusbar import PrymatexMainStatusBar
from .processors import PrymatexMainCommandProcessor
from .actions import MainWindowActionsMixin, tabSelectableModelFactory

class PrymatexMainWindow(PrymatexComponentWidget, MainWindowActionsMixin, QtWidgets.QMainWindow):
    """Prymatex main window"""
    # --------------------- Signals
    editorCreated = QtCore.Signal(object)
    aboutToEditorDelete = QtCore.Signal(object)
    aboutToEditorChange = QtCore.Signal(object)
    editorChanged = QtCore.Signal(object)

    # --------------------- Settings
    @ConfigurableItem(default = "$TM_DISPLAYNAME - $PMX_APP_NAME ($PMX_VERSION)")
    def window_title_template(self, template):
        self.title_template = Template(template)
        self.updateWindowTitle()

    @ConfigurableItem(default = False)
    def show_tabs_if_more_than_one(self, value):
        self.centralWidget().setShowTabs(not value)

    @ConfigurableItem(default = True)
    def show_menu_bar(self, value):
        self.menuBar().setVisible(value)

    @ConfigurableHook("code_editor.default_theme")
    def defaultTheme(self, theme_uuid):
        theme = self.application().supportManager.getBundleItem(theme_uuid)
        if theme is not None:
            palette = self.application().supportManager.getThemePalette(theme.bundleItem())
            self.notifier.setPalette(palette)

    _editorHistory = []
    _editorHistoryIndex = 0

    # Constructor
    def __init__(self, **kwargs):
        """The main window
        @param parent: The QObject parent, in this case it should be the QApp
        @param files_to_open: The set of files to be opened when the window is shown in the screen.
        """
        super(PrymatexMainWindow, self).__init__(**kwargs)
        self.setupUi()
        
        self.tabSelectableModel = tabSelectableModelFactory(self)

        # Connect Signals
        self.application().supportManager.bundleItemTriggered.connect(self.on_bundleItemTriggered)

        center_widget(self, scale = (0.9, 0.8))
        self.dockWidgets = []
        self.dialogs = []

        self.setAcceptDrops(True)

        self.notifier = OverlayNotifier(self)
        self.notifier.setBackgroundRole(QtGui.QPalette.Window)
        self.notifier.setForegroundRole(QtGui.QPalette.WindowText)
        
        #Processor de comandos local a la main window
        self.commandProcessor = PrymatexMainCommandProcessor(parent = self)
        self.bundleItem_handler = self.insertBundleItem

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setWindowIcon(self.resources().get_icon("prymatex"))

        self.setupDockToolBars()
        
        self.setCentralWidget(SplitterWidget(parent = self))
        
        # Splitter signals
        self.centralWidget().widgetChanged.connect(self.on_splitter_widgetChanged)
        self.centralWidget().aboutToWidgetChange.connect(self.on_splitter_aboutToWidgetChange)
        self.centralWidget().layoutChanged.connect(self.on_splitter_layoutChanged)
        self.centralWidget().tabCloseRequest.connect(self.closeEditor)
        self.centralWidget().tabCreateRequest.connect(self.addEmptyEditor)

        # Status and menu bars
        self.setStatusBar(PrymatexMainStatusBar(parent = self))
        self.setMenuBar(PrymatexMainMenuBar(parent = self))
        
        self.resize(801, 600)
        
    # ---------- Implements PrymatexComponentWidget
    def addComponent(self, component):
        super(PrymatexMainWindow, self).addComponent(component)
        if isinstance(component, PrymatexDock):
            self.addDock(component, component.PREFERED_AREA)
        elif isinstance(component, PrymatexDialog):
            self.addDialog(component)
        elif isinstance(component, PrymatexStatusBar):
            self.addStatusBar(component)

    def initialize(self, **kwargs):
        super(PrymatexMainWindow, self).initialize(**kwargs)

        # Dialogs
        self.selectorDialog = self.findChild(QtWidgets.QDialog, "SelectorDialog")
        self.aboutDialog = self.findChild(QtWidgets.QDialog, "AboutDialog")
        self.settingsDialog = self.findChild(QtWidgets.QDialog, "SettingsDialog")
        self.bundleEditorDialog = self.findChild(QtWidgets.QDialog, "BundleEditorDialog")
        self.profileDialog = self.findChild(QtWidgets.QDialog, "ProfileDialog")
        self.templateDialog = self.findChild(QtWidgets.QDialog, "TemplateDialog")
        self.newProjectDialog = self.findChild(QtWidgets.QDialog, "NewProjectDialog")

        # Dockers
        self.browserDock = self.findChild(QtWidgets.QDockWidget, "BrowserDock")
        self.terminalDock = self.findChild(QtWidgets.QDockWidget, "TerminalDock")
        self.projectsDock = self.findChild(QtWidgets.QDockWidget, "ProjectsDock")

        # Build Main Menu
        self.menuBar().extend(self.__class__, self)
        
        # Load some menus as atters of the main window
        self.menuPanels = self.findChild(QtWidgets.QMenu, "menuPanels")
        self.menuRecentFiles = self.findChild(QtWidgets.QMenu, "menuRecentFiles")
        self.menuBundles = self.findChild(QtWidgets.QMenu, "menuBundles")
        self.menuFocusGroup = self.findChild(QtWidgets.QMenu, "menuFocusGroup")
        self.menuMoveEditorToGroup = self.findChild(QtWidgets.QMenu, "menuMoveEditorToGroup")
        
        # Metemos las acciones de las dockers al menu panels
        dockIndex = 1
        for dock in self.dockWidgets:
            toggleAction = dock.toggleViewAction()
            sequence = dock.SEQUENCE
            if sequence is None:
                sequence = ("Docks", dock.objectName(), "Alt+%d" % dockIndex)
                dockIndex += 1
            self.application().registerShortcut(dock.__class__, toggleAction, sequence)
            icon = dock.ICON
            if icon is None:
                icon = 'dock'
            self.application().registerIcon(dock.__class__, toggleAction, icon)
            self.menuPanels.addAction(toggleAction)
            self.addAction(toggleAction)

        # Metemos las acciones del support
        self.application().supportManager.appendMenuToBundleMenuGroup(self.menuBundles)
    
    def environmentVariables(self):
        env = self.application().environmentVariables()
        for component in self.components():
            env.update(component.environmentVariables())
        return env

    # OVERRIDE: PrymatexComponentWidget.contributeToMainMenu()
    @classmethod
    def contributeToMainMenu(cls):
        return MainWindowActionsMixin.contributeToMainMenu()

    # OVERRIDE: PrymatexComponentWidget.contributeToSettings()
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.mainwindow import MainWindowSettingsWidget

        return [ MainWindowSettingsWidget ]

    # --------------- Bundle Items
    def on_bundleItemTriggered(self, bundleItem):
        if self.bundleItem_handler is not None:
            self.bundleItem_handler(bundleItem)

    def insertBundleItem(self, bundleItem, **processorSettings):
        '''Insert selected bundle item in current editor if possible'''
        assert not bundleItem.isEditorNeeded(), "Bundle Item needs editor"

        self.commandProcessor.configure(processorSettings)
        bundleItem.execute(self.commandProcessor)

    # Browser error
    def showErrorInBrowser(self, title, summary, exitcode = -1, **settings):
        commandScript = '''
source "$TM_SUPPORT_PATH/lib/webpreview.sh"

html_header '%(name)s error'
echo -e '<pre>%(output)s</pre>'
echo -e '<p>Exit code was: %(exitcode)d</p>'
html_footer
        ''' % {
                'name': html.escape(title),
                'output': html.htmlize(summary),
                'exitcode': exitcode}
        bundle = self.application().supportManager.getBundle(self.application().supportManager.default_bundle_for_new_bundle_items)
        command = self.application().supportManager.buildAdHocCommand(commandScript,
            bundle,
            name = "%s error" % title,
            commandOutput = 'showAsHTML')
        self.bundleItem_handler(command, **settings)

    # -------------------- Setups
    def setupDockToolBars(self):
        self.dockToolBars = {
            QtCore.Qt.LeftDockWidgetArea: DockWidgetToolBar("Left Dockers", QtCore.Qt.LeftDockWidgetArea, self),
            QtCore.Qt.RightDockWidgetArea: DockWidgetToolBar("Right Dockers", QtCore.Qt.RightDockWidgetArea, self),
            QtCore.Qt.TopDockWidgetArea: DockWidgetToolBar("Top Dockers", QtCore.Qt.TopDockWidgetArea, self),
            QtCore.Qt.BottomDockWidgetArea: DockWidgetToolBar("Bottom Dockers", QtCore.Qt.BottomDockWidgetArea, self),
        }
        for dockArea, toolBar in self.dockToolBars.items():
            self.addToolBar(DockWidgetToolBar.DOCK_AREA_TO_TB[dockArea], toolBar)
            toolBar.hide()

    def toggleDockToolBarVisibility(self):
        for toolBar in list(self.dockToolBars.values()):
            if toolBar.isVisible():
                toolBar.hide()
            else:
                toolBar.show()

    # OVERRIDE QMainWindow.setFont(font):
    def setFont(self, font):
        super().setFont(font)
        font.setPointSize(font.pointSize() * 0.9)
        self.notifier.setFont(font)
        
    # ---------- Componer la mainWindow
    def addStatusBar(self, status_bar):
        self.statusBar().addStatusBar(status_bar)

    def addDock(self, dock, area):
        self.addDockWidget(area, dock)
        titleBar = DockWidgetTitleBar(dock)
        titleBar.collpaseAreaRequest.connect(self.on_dockWidgetTitleBar_collpaseAreaRequest)
        dock.setTitleBarWidget(titleBar)
        dock.hide()
        self.dockWidgets.append(dock)

    def addDialog(self, dialog):
        self.dialogs.append(dialog)

    def on_dockWidgetTitleBar_collpaseAreaRequest(self, dock):
        if not dock.isFloating():
            area = self.dockWidgetArea(dock)
            self.dockToolBars[area].show()

    def showDistractionFreeMode(self):
        self.showFullScreen()
        self.showMenuBar = False

    # -------------- Notifications
    def showMessage(self, *largs, **kwargs):
        message = self.notifier.create(*largs, **kwargs)
        message.show()
        return message
    
    # -------------------- Status
    def setStatus(self, key, value, timeout=None):
        return self.statusBar().setStatus(key, value, timeout)

    def status(self, key):
        """return String	Returns the previously assigned value associated with the key, if any."""
        return self.statusBar().status(key)

    def eraseStatus(self, key):
        """return None	Clears the named status."""
        return self.statusBar().eraseStatus(key)
    
    # ---------------- Create and manage groups
    def addEmptyGroup(self):
        pass
        
    def moveEditorToNewGroup(self):
        self.centralWidget().moveWidgetToNewGroup(self.currentEditor())
    
    def setCurrentGroup(self, group):
        self.centralWidget().setCurrentGroup(group)

    def moveEditorToGroup(self, group):
        self.centralWidget().moveWidgetToGroup(group, self.currentEditor())
        
    def closeGroup(self):
        pass
        
    def nextGroup(self):
        pass
        
    def previousGroup(self):
        pass
        
    def moveEditorToNextGroup(self):
        self.centralWidget().moveWidgetToNextGroup(self.currentEditor())
        
    def moveEditorToPreviousGroup(self):
        self.centralWidget().moveWidgetToPreviousGroup(self.currentEditor())

    # ---------------- Create and manage editors
    def createEditor(self, file_path=None, class_name=None):
        editorClass = None
        if class_name is not None:
            editorClass = self.application().findEditorClassByName(class_name)
        elif file_path is not None:
            editorClass = self.application().findEditorClassForFile(file_path)
        if editorClass is None:
            editorClass = self.application().defaultEditor()

        editor = self.application().createComponentInstance(editorClass,
                                              parent=self,
                                              file_path=file_path)
        # Exists file ?
        if file_path:
            if self.application().fileManager.isfile(file_path):
                editor.open(file_path)
            editor.setWindowFilePath(file_path)
        self.editorCreated.emit(editor)
        return editor

    def deleteEditor(self, editor):
        self.aboutToEditorDelete.emit(editor)
        editor.close()
        self.application().deleteComponentInstance(editor)

    def addEmptyEditor(self):
        editor = self.createEditor()
        self.addEditor(editor)

    def removeEditor(self, editor):
        #editor.newLocationMemento.disconnect(self.on_editor_newLocationMemento)
        self.centralWidget().removeTabWidget(editor)
        # TODO Clean history ?

    def addEditor(self, editor, focus=True):
        current = self.currentEditor()
        self.centralWidget().addTabWidget(editor)
        #editor.newLocationMemento.connect(self.on_editor_newLocationMemento)
        # If new editor has file, try to close current editor
        if current and editor.windowFilePath():
            self.tryCloseEmptyEditor(current)
        if focus:
            self.setCurrentEditor(editor)
        
    def findEditorForFile(self, filePath):
        # Find open editor for fileInfo
        for editor in self.centralWidget().tabWidgets():
            if editor.windowFilePath() == filePath:
                return editor

    def editors(self):
        return self.centralWidget().tabWidgets()

    def setCurrentEditor(self, editor):
        self.centralWidget().setCurrentWidget(editor)

    def currentEditor(self):
        return self.centralWidget().currentWidget()

    def on_splitter_aboutToWidgetChange(self, editor):
        if editor is not None:
            # Disconnect
            editor.deactivate()
            editor.windowTitleChanged.disconnect(self.updateWindowTitle)
            editor.modificationChanged.disconnect(self.updateWindowModified)
            self.aboutToEditorChange.emit(editor)
        
    def on_splitter_widgetChanged(self, editor):
        # ----- Not allow None
        if editor is None:
            return self.addEmptyEditor()
        
        editor.activate()
        # Avisar al manager de bundles del editor y preparar el handler de bundle items
        self.application().supportManager.setEditorAvailable(True)
        self.bundleItem_handler = editor.bundleItemHandler() or self.insertBundleItem

        self.addEditorToHistory(editor)
        editor.setFocus()
        self.application().checkExternalAction(self, editor)
        editor.windowTitleChanged.connect(self.updateWindowTitle)
        editor.modificationChanged.connect(self.updateWindowModified)
        self.updateWindowTitle()
        self.updateWindowModified(editor.isWindowModified())
        
        #Emitir señal de cambio
        self.editorChanged.emit(editor)

    def updateWindowModified(self, modified):
        self.setWindowModified(modified)

    def updateWindowTitle(self):
        widget = self.currentEditor() or self
        widget_variables = widget.environmentVariables()
        window_title = self.title_template.substitute(widget_variables)
        print(window_title)
        self.setWindowTitle(window_title)

    def saveEditor(self, editor=None, saveAs=False):
        editor = editor or self.currentEditor()
        has_file_path = editor.windowFilePath()
        file_manager = self.application().fileManager
        if editor.externalAction() == self.application().EXTERNAL_CHANGED:
            message = "The file '%s' has been changed on the file system, Do you want save the file with other name?"
            result = QtWidgets.QMessageBox.question(editor, "File changed",
                message % editor.windowFilePath(),
                buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                defaultButton = QtWidgets.QMessageBox.Yes)
            if result == QtWidgets.QMessageBox.Yes:
                saveAs = True
        if not has_file_path or saveAs:
            dirname = file_manager.directory(self.projectsDock.currentPath()) \
                if not has_file_path \
                else editor.windowFileDirectory()
            basename = editor.accessibleName()
            filters = editor.fileFilters()
            # TODO Armar el archivo destino y no solo el basedir
            file_path, _ = getSaveFileName(
                self,
                caption = "Save file as" if saveAs else "Save file",
                basedir = file_manager.join(dirname, basename),
                filters = filters
            )
        else:
            file_path = editor.windowFilePath()

        if file_path:
            editor.save(file_path)

    def closeEditor(self, editor=None, cancel=False):
        editor = editor or self.currentEditor()
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No
        if cancel:
            buttons |= QtWidgets.QMessageBox.Cancel
        if editor is None: return
        while editor and editor.isWindowModified():
            response = QtWidgets.QMessageBox.question(self, "Save",
                "Save %s" % editor.accessibleName(),
                buttons = buttons,
                defaultButton = QtWidgets.QMessageBox.Ok)
            if response == QtWidgets.QMessageBox.Ok:
                self.saveEditor(editor = editor)
            elif response == QtWidgets.QMessageBox.No:
                break
            elif response == QtWidgets.QMessageBox.Cancel:
                raise exceptions.UserCancelException()
        self.removeEditor(editor)
        self.deleteEditor(editor)

    def tryCloseEmptyEditor(self, editor):
        if not editor.windowFilePath() and editor.isEmpty():
            self.closeEditor(editor)

    # ---------------- Handle location history
    def on_editor_newLocationMemento(self, memento):
        self.addHistoryEntry({"editor": self.sender(), "memento": memento})

    def addEditorToHistory(self, editor):
        if self._editorHistory and self._editorHistory[self._editorHistoryIndex]["editor"] == editor:
            return
        self.addHistoryEntry({"editor": editor})

    def addHistoryEntry(self, entry):
        self._editorHistory = [entry] + self._editorHistory[self._editorHistoryIndex:]
        self._editorHistoryIndex = 0

    # ---------------- MainWindow Events
    def closeEvent(self, event):
        for editor in self.editors():
            while editor and editor.isWindowModified():
                response = QtWidgets.QMessageBox.question(self, "Save",
                    "Save %s" % editor.accessibleName(),
                    buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                    defaultButton = QtWidgets.QMessageBox.Ok)
                if response == QtWidgets.QMessageBox.Ok:
                    self.saveEditor(editor = editor)
                elif response == QtWidgets.QMessageBox.No:
                    break
                elif response == QtWidgets.QMessageBox.Cancel:
                    event.ignore()
                    return

    # ---------- MainWindow State
    def componentState(self):
        componentState = super(PrymatexMainWindow, self).componentState()

        componentState["editors"] = []
        for editor in self.editors():
            editorState = editor.componentState()
            editorState["name"] = editor.__class__.__name__
            editorState["modified"] = editor.isWindowModified()
            if editor.windowFilePath():
                editorState["file"] = editor.windowFilePath()
            componentState["editors"].append(editorState)

        # Store geometry
        componentState["geometry"] = qbytearray_to_hex(self.saveGeometry())

        # Store self
        componentState["self"] = qbytearray_to_hex(QtWidgets.QMainWindow.saveState(self))

        return componentState

    def setComponentState(self, componentState):
        super(PrymatexMainWindow, self).setComponentState(componentState)

        # Restore open documents
        for editorState in componentState.get("editors", []):
            editor = self.createEditor(
                class_name=editorState["name"],
                file_path=editorState.get("file", None))
            self.addEditor(editor)
            editor.setComponentState(editorState)
            editor.setWindowModified(editorState.get("modified", False))

        # Restore geometry
        if "geometry" in componentState:
            self.restoreGeometry(hex_to_qbytearray(componentState["geometry"]))

        # Restore self
        if "self" in componentState:
            QtWidgets.QMainWindow.restoreState(self, hex_to_qbytearray(componentState["self"]))

    # ------------ Drag and Drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        def collectFiles(paths):
            from glob import glob
            '''Recursively collect fileInfos'''
            for path in paths:
                if os.path.isfile(path):
                    yield path
                elif os.path.isdir(path):
                    dirSubEntries = glob(os.path.join(path, '*'))
                    for entry in collectFiles(dirSubEntries):
                        yield entry

        urls = [url.toLocalFile() for url in event.mimeData().urls()]

        for path in collectFiles(urls):
            # TODO: Take this code somewhere else, this should change as more editor are added
            if not self.canBeOpened(path):
                self.logger().debug("Skipping dropped element %s" % path)
                continue
            self.logger().debug("Opening dropped file %s" % path)
            #self.openFile(QtCore.QFileInfo(path), focus = False)
            self.application().openFile(path)

    FILE_SIZE_THERESHOLD = 1024 ** 2 # 1MB file is enough, ain't it?
    STARTSWITH_BLACKLIST = ['.', '#', ]
    ENDSWITH_BLACKLIST = ['~', 'pyc', 'bak', 'old', 'tmp', 'swp', '#', ]

    def canBeOpened(self, path):
        # Is there any support for it?
        if not self.application().supportManager.findSyntaxByFileType(path):
            return False
        for start in self.STARTSWITH_BLACKLIST:
            if path.startswith(start):
                return False
        for end in self.ENDSWITH_BLACKLIST:
            if path.endswith(end):
                return False
        if os.path.getsize(path) > self.FILE_SIZE_THERESHOLD:
            return False
        return True

