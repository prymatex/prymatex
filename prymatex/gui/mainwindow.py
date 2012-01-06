#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from string import Template

from PyQt4 import QtCore, QtGui

from prymatex.ui.mainwindow import Ui_MainWindow
from prymatex.gui.actions import MainWindowActions
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.base import PMXObject
from prymatex.core import exceptions
from prymatex.utils.i18n import ugettext as _
from prymatex.gui import utils
from prymatex.gui import dialogs
from prymatex.utils import coroutines

class PMXMainWindow(QtGui.QMainWindow, Ui_MainWindow, MainWindowActions, PMXObject):
    """ 
    Prymatex main window
    """
    #=========================================================
    # Signals
    #=========================================================
    newFileCreated = QtCore.pyqtSignal(str)
    
    #=========================================================
    # Settings
    #=========================================================
    SETTINGS_GROUP = 'MainWindow'

    windowTitleTemplate = pmxConfigPorperty(default = "$PMX_APP_NAME")
    
    @pmxConfigPorperty(default = True)
    def showMenuBar(self, value):
        self._showMenuBar = value
        self.menuBar().setShown(value)
    
    # Constructor
    def __init__(self, parent = None):
        """
        The main window
        @param parent: The QObject parent, in this case it should be the QApp
        @param files_to_open: The set of files to be opened when the window
                              is shown in the screen.
        """
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.setupDockers()
        self.setupDialogs()
        self.setupMenu()
        self.setupStatusBar()
        
        # Connect Signals
        self.splitTabWidget.currentWidgetChanged.connect(self.on_currentWidgetChanged)
        self.splitTabWidget.currentWidgetChanged.connect(self.paneFileSystem.on_currentEditorChanged)
        self.splitTabWidget.tabCloseRequest.connect(self.closeEditor)
        self.splitTabWidget.tabCreateRequest.connect(self.addEmptyEditor)
        self.application.supportManager.bundleItemTriggered.connect(lambda item: self.currentEditor().insertBundleItem(item))
        
        utils.centerWidget(self, scale = (0.9, 0.8))
        self.configure()
        
        self.setAcceptDrops(True)
        
        self.addEmptyEditor()

    #============================================================
    # Setups
    #============================================================
    def setupStatusBar(self):
        #TODO: este estado pertenece a un tipo de editor, ver como establecer la relacion
        from prymatex.gui.statusbar import PMXStatusBar
        from prymatex.gui.codeeditor.status import PMXCodeEditorStatus
        status = PMXStatusBar(self)
        status.addPermanentWidget(PMXCodeEditorStatus(self))
        self.setStatusBar(status)
        
    def setupDockers(self):
        """
        Basic panels, dock objects. More docks should be available via plugins
        """
        from prymatex.gui.dockers.filesystem import PMXFileSystemDock
        from prymatex.gui.dockers.browser import PMXBrowserDock
        from prymatex.gui.dockers.console import PMXConsoleDock
        from prymatex.gui.dockers.logger import QtLogHandler, PMXLoggerDock
        from prymatex.gui.dockers.projects import PMXProjectDock
        from prymatex.gui.codeeditor.dockers import PMXCodeSymbolsDock, PMXCodeBookmarksDock
        #from prymatex.gui.dockers.terminal import PMXTerminalWidget
        
        self.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        self.paneFileSystem = PMXFileSystemDock(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.paneFileSystem)
        self.menuPanels.addAction(self.paneFileSystem.toggleViewAction())
        self.paneFileSystem.hide()
        
        self.paneProject = PMXProjectDock(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.paneProject)
        self.menuPanels.addAction(self.paneProject.toggleViewAction())
        self.paneProject.hide()
        
        self.paneBrowser = PMXBrowserDock(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.paneBrowser)
        self.menuPanels.addAction(self.paneBrowser.toggleViewAction())
        self.paneBrowser.hide()
        
        self.paneConsole = PMXConsoleDock(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.paneConsole)
        self.menuPanels.addAction(self.paneConsole.toggleViewAction())
        self.paneConsole.hide()
        
        self.paneLogging = PMXLoggerDock(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.paneLogging)
        self.menuPanels.addAction(self.paneLogging.toggleViewAction())
        self.paneLogging.hide()

        codeBookmarks = PMXCodeBookmarksDock(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, codeBookmarks)
        self.menuPanels.addAction(codeBookmarks.toggleViewAction())
        codeBookmarks.hide()        

        codeSymbols = PMXCodeSymbolsDock(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, codeSymbols)
        self.menuPanels.addAction(codeSymbols.toggleViewAction())
        codeSymbols.hide()
        
        #self.paneTerminal = PMXTerminalWidget(self)
        #self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.paneTerminal)
        #self.menuPanels.addAction(self.paneTerminal.toggleViewAction())
        #self.paneTerminal.hide()
        
        self.tabifyDockWidget(codeSymbols, codeBookmarks)
        
        self.dockers = [codeSymbols, codeBookmarks]
    
    def setupDialogs(self):
        from prymatex.gui.dialogs.selector import PMXSelectorDialog
                
        # Create dialogs
        self.bundleSelectorDialog = PMXSelectorDialog(self, title = _("Select Bundle Item"))
        # TODO: Connect these selectors 
        self.tabSelectorDialog = PMXSelectorDialog(self, title = _("Select tab"))
        self.symbolSelectorDialog = PMXSelectorDialog(self, title = _("Select Symbol"))
        self.bookmarkSelectorDialog = PMXSelectorDialog(self, title = _("Select Bookmark"))

    #============================================================
    # Create and manage editors
    #============================================================
    def addEmptyEditor(self):
        editor = self.application.getEditorInstance()
        self.addEditor(editor)
        
    def addEditor(self, editor, focus = True):
        self.statusBar().addEditor(editor)
        self.splitTabWidget.addTab(editor)
        if focus:
            self.setCurrentEditor(editor)

    def removeEditor(self, editor):
        self.statusBar().removeEditor(editor)
        self.splitTabWidget.removeTab(editor)
        del editor

    def findEditorForFile(self, filePath):
        # Find open editor for fileInfo
        for editor in self.splitTabWidget.getAllWidgets():
            if editor.filePath == filePath:
                return editor

    def setCurrentEditor(self, editor):
        self.splitTabWidget.setCurrentWidget(editor)
    
    def currentEditor(self):
        return self.splitTabWidget.currentWidget()
    
    def on_currentWidgetChanged(self, editor):
        #Set editor to statusbar
        self.statusBar().setCurrentEditor(editor)
        
        #Set editor to Dockers
        for docker in self.dockers:
            docker.setCurrentEditor(editor)

        #Update Menu
        self.updateMenuForEditor(editor)        

        template = Template(self.windowTitleTemplate)
        title = [ editor.tabTitle() ] if editor is not None else []
        title.append(template.safe_substitute(**self.application.supportManager.buildEnvironment()))
        self.setWindowTitle(" - ".join(title))
        if editor is not None:
            editor.setFocus()
        
    def saveEditor(self, editor = None, saveAs = False):
        editor = editor or self.currentEditor()
        if editor.isNew() or saveAs:
            fileDirectory = editor.fileDirectory()
            fileName = editor.fileName()
            fileFilters = editor.fileFilters()
            filePath = dialogs.getSaveFile( fileDirectory, title = "Save file as" if saveAs else "Save file", 
                                            filters = fileFilters, 
                                            name = fileName)
        else:
            filePath = editor.filePath

        if filePath is not None:
            self.application.fileManager.saveFile(filePath, editor.toPlainText())
            editor.saved(filePath)
    
    def closeEditor(self, editor = None):
        editor = editor or self.currentEditor()
        if editor is None: return
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
                raise exceptions.UserCancelException()
        editor.closed()
        self.removeEditor(editor)
    
    def tryCloseEmptyEditor(self, editor = None):
        editor = editor or self.currentEditor()
        if editor is not None and editor.isNew() and not editor.isModified():
            self.closeEditor(editor)
    
    def closeEvent(self, event):
        try:
            for editor in self.splitTabWidget.getAllWidgets():
                self.closeEditor(editor)
        except exceptions.UserCancelException:
            event.ignore()

    #===========================================================================
    # Drag and Drop
    #===========================================================================
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        def collectFiles(paths):
            from glob import glob
            ''' Recursively collect fileInfos '''
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
                self.debug("Skipping dropped element %s" % path)
                continue
            self.debug("Opening dropped file %s" % path)
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
        