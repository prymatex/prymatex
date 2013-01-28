#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from string import Template

from prymatex.qt import QtCore, QtGui
from prymatex.qt.compat import getSaveFileName
from prymatex.qt.helpers import text2objectname
from prymatex.qt.helpers.widgets import center_widget
from prymatex.qt.helpers.menus import create_menu, extend_menu

from prymatex import resources

from prymatex.core import exceptions
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.components import PMXBaseComponent

from prymatex.utils.i18n import ugettext as _

from prymatex.gui.actions import MainWindowActions, tabSelectableModelFactory
from prymatex.gui.statusbar import PMXStatusBar
from prymatex.gui.processors import MainWindowCommandProcessor
from prymatex.gui.dialogs.selector import SelectorDialog

from prymatex.widgets.docker import DockWidgetTitleBar
from prymatex.widgets.toolbar import DockWidgetToolBar
from prymatex.widgets.message import PopupMessageWidget

from prymatex.ui.mainwindow import Ui_MainWindow

class PMXMainWindow(QtGui.QMainWindow, Ui_MainWindow, MainWindowActions, PMXBaseComponent):
    """Prymatex main window"""
    # --------------------- Signals
    currentEditorChanged = QtCore.pyqtSignal(object)

    # --------------------- Settings
    SETTINGS_GROUP = 'MainWindow'

    @pmxConfigPorperty(default = "$PMX_APP_NAME ($PMX_VERSION)")
    def windowTitleTemplate(self, titleTemplate):
         self.titleTemplate = Template(titleTemplate)

    @pmxConfigPorperty(default = True)
    def showMenuBar(self, value):
        self._showMenuBar = value
        self.menuBar().setShown(value)

    _editorHistory = []
    _editorHistoryIndex = 0
    
    # Constructor
    def __init__(self, application):
        """
        The main window
        @param parent: The QObject parent, in this case it should be the QApp
        @param files_to_open: The set of files to be opened when the window is shown in the screen.
        """
        QtGui.QMainWindow.__init__(self)
        PMXBaseComponent.__init__(self)

        self.application = application
        self.setupUi(self)
        
        self.setWindowIcon(resources.getIcon("prymatex"))
        
        # The selector dialog of this mainwindow
        self.selectorDialog = SelectorDialog(self)

        self.tabSelectableModel = tabSelectableModelFactory(self)
        
        self.setupDockToolBars()
        self.setupMenu()
        
        self.setStatusBar(PMXStatusBar(self))
        
        # Connect Signals
        self.splitTabWidget.currentWidgetChanged.connect(self.on_currentWidgetChanged)
        self.splitTabWidget.currentWidgetChanged.connect(self.setWindowTitleForEditor)
        self.splitTabWidget.tabCloseRequest.connect(self.closeEditor)
        self.splitTabWidget.tabCreateRequest.connect(self.addEmptyEditor)
        self.application.supportManager.bundleItemTriggered.connect(self.on_bundleItemTriggered)
        
        center_widget(self, scale = (0.9, 0.8))
        self.dockers = []
        self.customEditorActions = {}
        self.customDockActions = {}

        self.setAcceptDrops(True)
        
        #self.setMainWindowAsActionParent()
        self.setupHelpMenuMiscConnections()
        
        self.popupMessage = PopupMessageWidget(self)
        
        #Processor de comandos local a la main window
        self.commandProcessor = MainWindowCommandProcessor(self)
        self.bundleItem_handler = self.insertBundleItem

    #==========================================================================
    # Bundle Items
    #==========================================================================
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
        from prymatex.support.utils import makeHyperlinks
        from prymatex.utils import html
        commandScript = '''
            source "$TM_SUPPORT_PATH/lib/webpreview.sh" 
            
            html_header "An error has occurred while executing command %(name)s"
            echo -e "<pre>%(output)s</pre>"
            echo -e "<p>Exit code was: %(exitcode)d</p>"
            html_footer
        ''' % {
                'name': html.escape(title),
                'output': html.escape(summary),
                'exitcode': exitcode}
        bundle = self.application.supportManager.getBundle(self.application.supportManager.defaultBundleForNewBundleItems)
        command = self.application.supportManager.buildAdHocCommand(commandScript,
            bundle,
            name = "Error runing %s" % title,
            commandOutput = 'showAsHTML')
        self.bundleItem_handler(command, **settings)
        
    def environmentVariables(self):
        env = {}
        for docker in self.dockers:
            env.update(docker.environmentVariables())
        return env

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.mainwindow import MainWindowSettingsWidget
        return [ MainWindowSettingsWidget ]
        
    #============================================================
    # Setups
    #============================================================
    def setupDockToolBars(self):
        self.dockToolBars = {
            QtCore.Qt.LeftDockWidgetArea: DockWidgetToolBar("Left Dockers", QtCore.Qt.LeftDockWidgetArea, self),
            QtCore.Qt.RightDockWidgetArea: DockWidgetToolBar("Right Dockers", QtCore.Qt.RightDockWidgetArea, self),
            QtCore.Qt.TopDockWidgetArea: DockWidgetToolBar("Top Dockers", QtCore.Qt.TopDockWidgetArea, self),
            QtCore.Qt.BottomDockWidgetArea: DockWidgetToolBar("Bottom Dockers", QtCore.Qt.BottomDockWidgetArea, self),
        }
        for dockArea, toolBar in self.dockToolBars.iteritems():
            self.addToolBar(DockWidgetToolBar.DOCK_AREA_TO_TB[dockArea], toolBar)
            toolBar.hide()

    def toggleDockToolBarVisibility(self):
        for toolBar in self.dockToolBars.values():
            if toolBar.isVisible():
                toolBar.hide()
            else:
                toolBar.show()

    #============================================================
    # Componer la mainWindow
    #============================================================
    def addStatusBar(self, statusBar):
        self.statusBar().addPermanentWidget(statusBar)
    
    # Dockers    
    def addDock(self, dock, area):
        self.addDockWidget(area, dock)
        toggleAction = dock.toggleViewAction()
        self.menuPanels.addAction(toggleAction)
        self.addAction(toggleAction)
        titleBar = DockWidgetTitleBar(dock)
        titleBar.collpaseAreaRequest.connect(self.on_dockWidgetTitleBar_collpaseAreaRequest)
        dock.setTitleBarWidget(titleBar)
        dock.hide()
        self.dockers.append(dock)
    
    def on_dockWidgetTitleBar_collpaseAreaRequest(self, dock):
        if not dock.isFloating():
            area = self.dockWidgetArea(dock)
            self.dockToolBars[area].show()
        
    def contributeToMainMenu(self, name, settings):
        actions = []
        menuAttr = text2objectname(name, prefix = "menu")
        menu = getattr(self, menuAttr, None)
        if menu is None:
            if "text" not in settings:
                settings["text"] = name
            menu, actions = create_menu(self.menubar, settings)
            setattr(self, menuAttr, menu)
            actions.insert(0, self.menubar.insertMenu(self.menuNavigation.children()[0], menu))
        elif 'items' in settings:
            actions = extend_menu(menu, settings['items'])
        return actions

    def registerEditorClassActions(self, editorClass, actions):
        self.logger.debug("%s, actions: %d" % (str(editorClass), len(actions)))
        #Conect Actions
        for action in actions:
            if hasattr(action, 'callback'):
                receiver = lambda checked, action = action: self.currentEditorActionDispatcher(checked, action)
                self.connect(action, QtCore.SIGNAL('triggered(bool)'), receiver)
        self.customEditorActions[editorClass] = actions
    
    def registerDockClassActions(self, dockClass, actions):
        self.logger.debug("%s, actions: %d" % (str(dockClass), len(actions)))
        #Conect Actions
        for action in actions:
            if hasattr(action, 'callback'):
                receiver = lambda checked, action = action: self.dockActionDispatcher(checked, action)
                self.connect(action, QtCore.SIGNAL('triggered(bool)'), receiver)
        self.customDockActions[dockClass] = actions
        
    def registerStatusClassActions(self, statusClass, actions):
        self.statusBar().registerStatusClassActions(statusClass, actions)
    
    def dockActionDispatcher(self, checked, action):
        #Find class for action
        dockClasses = filter(lambda (cls, actions): action in actions, self.customDockActions.items())
        assert len(dockClasses) == 1, "More than one dock class for action %s" % action
        dockClass = dockClasses[0][0]
        #Find instance
        dockInstance = filter(lambda status: status.__class__ == dockClass, self.dockers)
        assert len(dockInstance) == 1, "More than one instance for class %s" % dockClass
        dockInstance = dockInstance[0]
        
        callbackArgs = [ dockInstance ]
        if action.isCheckable():
            callbackArgs.append(checked)
        action.callback(*callbackArgs)
        
    def currentEditorActionDispatcher(self, checked, action):
        callbackArgs = [self.currentEditor()]
        if action.isCheckable():
            callbackArgs.append(checked)
        action.callback(*callbackArgs)
    
    def updateMenuForEditor(self, editor):
        if editor is None:
            for editorClass, actions in self.customEditorActions.iteritems():
                map(lambda action: action.setVisible(False), actions)
        else:
            currentEditorClass = editor.__class__
            
            for editorClass, actions in self.customEditorActions.iteritems():
                for action in actions:
                    action.setVisible(editorClass == currentEditorClass)
                    if editorClass == currentEditorClass and action.isCheckable() and hasattr(action, 'testChecked'):
                        action.setChecked(action.testChecked(editor))

    def showMessage(self, *largs, **kwargs):
        self.popupMessage.showMessage(*largs, **kwargs)
        
    #============================================================
    # Create and manage editors
    #============================================================
    def addEmptyEditor(self):
        editor = self.application.createEditorInstance(parent = self)
        self.addEditor(editor)
        return editor

    def removeEditor(self, editor):
        self.disconnect(editor, QtCore.SIGNAL("newLocationMemento"), self.on_editor_newLocationMemento)
        self.splitTabWidget.removeTab(editor)
        # TODO Ver si el remove borra el editor y como acomoda el historial
        del editor

    def addEditor(self, editor, focus = True):
        self.splitTabWidget.addTab(editor)
        self.connect(editor, QtCore.SIGNAL("newLocationMemento"), self.on_editor_newLocationMemento)
        if focus:
            self.setCurrentEditor(editor)
    
    def findEditorForFile(self, filePath):
        # Find open editor for fileInfo
        for editor in self.splitTabWidget.allWidgets():
            if editor.filePath == filePath:
                return editor

    def editors(self):
        return self.splitTabWidget.allWidgets()
        
    def setCurrentEditor(self, editor):
        self.splitTabWidget.setCurrentWidget(editor)
    
    def currentEditor(self):
        return self.splitTabWidget.currentWidget()
    
    def on_currentWidgetChanged(self, editor):
        #Update Menu
        self.updateMenuForEditor(editor)        
        
        #Avisar al manager si tenemos editor y preparar el handler
        self.application.supportManager.setEditorAvailable(editor is not None)
        self.bundleItem_handler = editor.bundleItemHandler() or self.insertBundleItem if editor is not None else self.insertBundleItem    
        
        #Emitir señal de cambio
        self.currentEditorChanged.emit(editor)

        if editor is not None:
            self.addEditorToHistory(editor)
            editor.setFocus()
            self.application.checkExternalAction(self, editor)
            
    def setWindowTitleForEditor(self, editor):
        #Set Window Title for editor, editor can be None
        titleChunks = [ self.titleTemplate.safe_substitute(**self.application.supportManager.environmentVariables()) ]
        if editor is not None:
            titleChunks.insert(0, editor.tabTitle())
        self.setWindowTitle(" - ".join(titleChunks))
        
    def saveEditor(self, editor = None, saveAs = False):
        editor = editor or self.currentEditor()
        if editor.isExternalChanged():
            message = "The file '%s' has been changed on the file system, Do you want save the file with other name?"
            result = QtGui.QMessageBox.question(editor, _("File changed"),
                _(message) % editor.filePath,
                buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                defaultButton = QtGui.QMessageBox.Yes)
            if result == QtGui.QMessageBox.Yes:
                saveAs = True
        if editor.isNew() or saveAs:
            fileDirectory = self.application.fileManager.directory(self.projects.currentPath()) if editor.isNew() else editor.fileDirectory()
            fileName = editor.fileName()
            fileFilters = editor.fileFilters()
            # TODO Armar el archivo destino y no solo el basedir
            filePath, _ = getSaveFileName(
                self, 
                caption = "Save file as" if saveAs else "Save file", 
                basedir = fileDirectory, 
                filters = fileFilters
            )
        else:
            filePath = editor.filePath

        if filePath:
            editor.save(filePath)
    
    def closeEditor(self, editor = None, cancel = False):
        editor = editor or self.currentEditor()
        buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.No
        if cancel:
            buttons |= QtGui.QMessageBox.Cancel
        if editor is None: return
        while editor and editor.isModified():
            response = QtGui.QMessageBox.question(self, "Save", 
                "Save %s" % editor.tabTitle(), 
                buttons = buttons, 
                defaultButton = QtGui.QMessageBox.Ok)
            if response == QtGui.QMessageBox.Ok:
                self.saveEditor(editor = editor)
            elif response == QtGui.QMessageBox.No:
                break
            elif response == QtGui.QMessageBox.Cancel:
                raise exceptions.UserCancelException()
        editor.close()
        self.removeEditor(editor)
    
    def tryCloseEmptyEditor(self, editor = None):
        editor = editor or self.currentEditor()
        if editor is not None and editor.isNew() and not editor.isModified():
            self.closeEditor(editor)
    
    #=========================================================
    # Handle location history
    #=========================================================
    def on_editor_newLocationMemento(self, memento):
        self.addHistoryEntry({"editor": self.sender(), "memento": memento})
        
    def addEditorToHistory(self, editor):
        if self._editorHistory and self._editorHistory[self._editorHistoryIndex]["editor"] == editor:
            return
        self.addHistoryEntry({"editor": editor})
        
    def addHistoryEntry(self, entry):
        self._editorHistory = [entry] + self._editorHistory[self._editorHistoryIndex:]
        self._editorHistoryIndex = 0
        
    #===========================================================================
    # MainWindow Events
    #===========================================================================
    def closeEvent(self, event):
        for editor in self.editors():
            while editor and editor.isModified():
                response = QtGui.QMessageBox.question(self, "Save", 
                    "Save %s" % editor.tabTitle(), 
                    buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, 
                    defaultButton = QtGui.QMessageBox.Ok)
                if response == QtGui.QMessageBox.Ok:
                    self.saveEditor(editor = editor)
                elif response == QtGui.QMessageBox.No:
                    break
                elif response == QtGui.QMessageBox.Cancel:
                    event.ignore()
                    return
        
    #===========================================================================
    # MainWindow State
    #===========================================================================
    def saveState(self):
        #Documentos abiertos
        openDocumentsOnQuit = []
        for editor in self.editors():
            if not editor.isNew():
                openDocumentsOnQuit.append((editor.filePath, editor.cursorPosition()))
        state = {
            "self": QtGui.QMainWindow.saveState(self),
            "dockers": dict(map(lambda dock: (dock.objectName(), dock.saveState()), self.dockers)),
            "documents": openDocumentsOnQuit,
            "geometry": self.saveGeometry(),
        }
        return state

    def restoreState(self, state):
        # Restore dockers
        for dock in self.dockers:
            dockName = dock.objectName()
            if dockName in state["dockers"]:
                dock.restoreState(state["dockers"][dockName])
        
        # Restore Main window
        self.restoreGeometry(state["geometry"])
        for doc in state["documents"]:
            self.application.openFile(*doc, mainWindow = self)
        QtGui.QMainWindow.restoreState(self, state["self"])

    #===========================================================================
    # Drag and Drop
    #===========================================================================
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
                        
        urls = map(lambda url: url.toLocalFile(), event.mimeData().urls())
        
        for path in collectFiles(urls):
            # TODO: Take this code somewhere else, this should change as more editor are added
            if not self.canBeOpened(path):
                self.logger.debug("Skipping dropped element %s" % path)
                continue
            self.logger.debug("Opening dropped file %s" % path)
            #self.openFile(QtCore.QFileInfo(path), focus = False)
            self.application.openFile(path)

    FILE_SIZE_THERESHOLD = 1024 ** 2 # 1MB file is enough, ain't it?
    STARTSWITH_BLACKLIST = ['.', '#', ]
    ENDSWITH_BLACKLIST = ['~', 'pyc', 'bak', 'old', 'tmp', 'swp', '#', ]
    
    def canBeOpened(self, path):
        # Is there any support for it?
        if not self.application.supportManager.findSyntaxByFileType(path):
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
        