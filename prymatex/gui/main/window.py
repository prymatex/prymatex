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
    currentEditorChanged = QtCore.Signal(object)

    # --------------------- Settings
    SETTINGS = 'MainWindow'

    @ConfigurableItem(default = "$TM_FILENAME${TM_FILENAME/.+/ - /}$PMX_APP_NAME ($PMX_VERSION)")
    def windowTitleTemplate(self, titleTemplate):
        self.titleTemplate = Template(titleTemplate)
        self.updateWindowTitle()

    @ConfigurableItem(default = False)
    def showTabsIfMoreThanOne(self, value):
        self.centralWidget().setShowTabs(not value)

    @ConfigurableItem(default = True)
    def showMenuBar(self, value):
        self.menuBar().setVisible(value)

    @ConfigurableHook("CodeEditor.defaultTheme")
    def defaultTheme(self, themeUUID):
        print(themeUUID)
        theme = self.application().supportManager.getBundleItem(themeUUID)
        self.notifier.setPalette(theme.palette())

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
        font = self.font()
        font.setPointSize(font.pointSize() * 0.8)
        self.notifier.setFont(font)
        
        #Processor de comandos local a la main window
        self.commandProcessor = PrymatexMainCommandProcessor(parent = self)
        self.bundleItem_handler = self.insertBundleItem

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setWindowIcon(self.resources().get_icon(":/prymatex.png"))

        self.setupDockToolBars()
        
        self.setCentralWidget(SplitterWidget(parent = self))
        
        # Splitter signals
        self.centralWidget().currentWidgetChanged.connect(self.on_splitter_currentWidgetChanged)
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
        self.projectDialog = self.findChild(QtWidgets.QDialog, "ProjectDialog")

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

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.mainwindow import MainWindowSettingsWidget
        return [ MainWindowSettingsWidget ]

    # ---------- Override QMainWindow
    def show(self):
        QtWidgets.QMainWindow.show(self)
        self.menuBar().update(self.__class__, self)

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
        bundle = self.application().supportManager.getBundle(self.application().supportManager.defaultBundleForNewBundleItems)
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

    # ---------- Componer la mainWindow
    def addStatusBar(self, statusBar):
        self.statusBar().addPermanentWidget(statusBar)

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

    def updateMenuForEditor(self, editor):
        # Primero las del editor
        self.logger().debug("Update editor %s objects" % editor)
        self.menuBar().update(editor.__class__, editor)

        # Ahora sus children
        componentClass = self.application().findComponentsForClass(editor.__class__)
        for klass in componentClass:
            for componentInstance in editor.findChildren(klass):
                self.menuBar().update(klass, componentInstance)

    # -------------- Notifications
    def showMessage(self, *largs, **kwargs):
        if not hasattr(self, "_recyclable_message") and not kwargs:
            kwargs["recyclable"] = True
            self._recyclable_message = self.notifier.message(*largs, **kwargs)
            self._recyclable_message.show()
        else:
            self._recyclable_message.show(*largs)
        return self._recyclable_message

    def showTooltip(self, *largs, **kwargs):
        tooltip = self.notifier.tooltip(*largs, **kwargs)
        tooltip.show()
        return tooltip
        
    def showStatus(self, *largs, **kwargs):
        status = self.notifier.status(*largs, **kwargs)
        status.show()
        return status

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
    def addEmptyEditor(self):
        editor = self.application().createEditorInstance(parent = self)
        self.addEditor(editor)

    def removeEditor(self, editor):
        editor.newLocationMemento.disconnect(self.on_editor_newLocationMemento)
        self.centralWidget().removeTabWidget(editor)
        # TODO Clean history ?

    def addEditor(self, editor, focus = True):
        self.centralWidget().addTabWidget(editor)
        editor.newLocationMemento.connect(self.on_editor_newLocationMemento)
        if focus:
            self.setCurrentEditor(editor)

    def findEditorForFile(self, filePath):
        # Find open editor for fileInfo
        for editor in self.centralWidget().allWidgets():
            if editor.filePath() == filePath:
                return editor

    def editors(self):
        return self.centralWidget().allWidgets()

    def setCurrentEditor(self, editor):
        self.centralWidget().setCurrentWidget(editor)

    def currentEditor(self):
        return self.centralWidget().currentWidget()

    def on_splitter_currentWidgetChanged(self, editor):
        #Update Menu
        self.updateMenuForEditor(editor)

        #Avisar al manager si tenemos editor y preparar el handler
        self.application().supportManager.setEditorAvailable(editor is not None)
        self.bundleItem_handler = editor.bundleItemHandler() or self.insertBundleItem if editor is not None else self.insertBundleItem

        #Emitir señal de cambio
        self.currentEditorChanged.emit(editor)
        
        if editor is not None:
            self.addEditorToHistory(editor)
            editor.setFocus()
            self.application().checkExternalAction(self, editor)
        self.updateWindowTitle()
    
    def updateWindowTitle(self):
        self.setWindowTitle(self.titleTemplate.substitute(
            (self.currentEditor() or self).environmentVariables()))

    def saveEditor(self, editor = None, saveAs = False):
        editor = editor or self.currentEditor()
        if editor.isExternalChanged():
            message = "The file '%s' has been changed on the file system, Do you want save the file with other name?"
            result = QtWidgets.QMessageBox.question(editor, _("File changed"),
                _(message) % editor.filePath(),
                buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                defaultButton = QtWidgets.QMessageBox.Yes)
            if result == QtWidgets.QMessageBox.Yes:
                saveAs = True
        if not editor.hasFile() or saveAs:
            fileDirectory = self.application().fileManager.directory(self.projectsDock.currentPath()) if not editor.hasFile() else editor.fileDirectory()
            fileName = editor.title()
            fileFilters = editor.fileFilters()
            # TODO Armar el archivo destino y no solo el basedir
            file_path, _ = getSaveFileName(
                self,
                caption = "Save file as" if saveAs else "Save file",
                basedir = fileDirectory,
                filters = fileFilters
            )
        else:
            file_path = editor.filePath()

        if file_path:
            editor.save(file_path)

    def closeEditor(self, editor = None, cancel = False):
        editor = editor or self.currentEditor()
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No
        if cancel:
            buttons |= QtWidgets.QMessageBox.Cancel
        if editor is None: return
        while editor and editor.isModified():
            response = QtWidgets.QMessageBox.question(self, "Save",
                "Save %s" % editor.title(),
                buttons = buttons,
                defaultButton = QtWidgets.QMessageBox.Ok)
            if response == QtWidgets.QMessageBox.Ok:
                self.saveEditor(editor = editor)
            elif response == QtWidgets.QMessageBox.No:
                break
            elif response == QtWidgets.QMessageBox.Cancel:
                raise exceptions.UserCancelException()
        self.removeEditor(editor)
        self.application().deleteEditorInstance(editor)

    def tryCloseEmptyEditor(self, editor = None):
        editor = editor or self.currentEditor()
        if editor is not None and not editor.hasFile() and not editor.isModified():
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
            while editor and editor.isModified():
                response = QtWidgets.QMessageBox.question(self, "Save",
                    "Save %s" % editor.title(),
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
            editorState["modified"] = editor.isModified()
            if editor.hasFile():
                editorState["file"] = editor.filePath()
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
            editor = self.application().createEditorInstance(
                class_name = editorState["name"],
                file_path = editorState.get("file"),
                parent = self)
            editor.setComponentState(editorState)
            editor.setModified(editorState.get("modified", False))
            self.addEditor(editor)

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

