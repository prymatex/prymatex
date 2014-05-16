#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, sys, shutil

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.menus import create_menu

from prymatex import resources

# FileSystem docker parents
from prymatex.core import PrymatexDock
from prymatex.gui.dockers.fstasks import FileSystemTasks
from prymatex.ui.dockers.filesystem import Ui_FileSystemDock

from prymatex import resources
from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import pmxConfigPorperty
from prymatex.models.filesystem import SortFilterFileSystemProxyModel

class FileSystemDock(PrymatexDock, FileSystemTasks, Ui_FileSystemDock, QtGui.QDockWidget):
    SEQUENCE = resources.get_sequence("Docks", "FileSystemDock", "Alt+Y")
    ICON = resources.get_icon("system-file-manager")
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    # ----------- Settings
    SETTINGS_GROUP = 'FileSystem'
    @pmxConfigPorperty(default = '')
    def customFilters(self, filters):
        self.fileSystemProxyModel.setFilterRegExp(filters)

    _pushButtonHistoryBack = []
    _pushButtonHistoryForward = []

    def __init__(self, **kwargs):
        super(FileSystemDock, self).__init__(**kwargs)
        self.setupUi(self)

        self.fileManager = self.application.fileManager

        #File System model
        self.fileSystemModel = QtGui.QFileSystemModel(self)
        self.fileSystemModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries) #http://doc.qt.nokia.com/latest/qdir.html#Filter-enum
        self.fileSystemModel.setRootPath(QtCore.QDir.rootPath())

        #Proxy para el file system tree view
        self.fileSystemProxyModel = SortFilterFileSystemProxyModel(self)
        self.fileSystemProxyModel.setSourceModel(self.fileSystemModel)

        self.setupComboBoxLocation()
        self.setupTreeViewFileSystem()

        self.treeViewFileSystem.installEventFilter(self)
        self.comboBoxLocation.installEventFilter(self)

        self.setupButtons()

    def initialize(self, **kwargs):
        super(FileSystemDock, self).initialize(**kwargs)
        self.templateDialog = self.mainWindow().findChild(QtGui.QDialog, "TemplateDialog")

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if obj == self.comboBoxLocation:
                if event.key() == QtCore.Qt.Key_Return:
                    text = self.comboBoxLocation.lineEdit().text()
                    self.on_comboBoxLocation_currentIndexChanged(text)
                    return True
            elif obj == self.treeViewFileSystem:
                if event.key() == QtCore.Qt.Key_Backspace:
                    self.pushButtonUp.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return:
                    path = self.currentPath()
                    if os.path.isdir(path):
                        self.setPathAsRoot(path)
                        return True
                    elif os.path.isfile(path):
                        self.application.openFile(path)
                        return True

                if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
                    # FIXME: Get Ctrl + F before editor's find, all the foucs is belong to us right now :P
                    self.pushButtonCustomFilters.click()
                    return True
        return QtGui.QDockWidget.eventFilter(self, obj, event)


    def setupComboBoxLocation(self):
        #Combo Dir Model
        self.comboDirModel = QtGui.QDirModel(self)
        self.comboTreeView = QtGui.QTreeView(self)
        self.comboTreeView.setModel(self.comboDirModel)
        self.comboBoxLocation.setView(self.comboTreeView)
        self.comboBoxLocation.setModel(self.comboDirModel)
        #self.comboBoxLocation.setModelColumn(1)
        pIndex = self.treeViewFileSystem.rootIndex()
        rootPath = self.fileSystemProxyModel.filePath(pIndex)
        comboIndex = self.comboBoxLocation.model().index(rootPath)
        #self.comboBoxLocation.setRootModelIndex(comboIndex)
        self.comboBoxLocation.setCurrentIndex(comboIndex.row())

    def setupButtons(self):
        self.pushButtonSync.setCheckable(True)
        self.pushButtonBack.setEnabled(False)
        self.pushButtonFoward.setEnabled(False)

    def setupTreeViewFileSystem(self):
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)

        #self.treeViewFileSystem.setHeaderHidden(True)
        #self.treeViewFileSystem.setUniformRowHeights(False)

        #Setup Context Menu
        contextMenu = {
            "text": "File System",
            "items": [
                {   "text": "New",
                    "items": [
                        self.actionNewFolder, self.actionNewFile, self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionOpen,
                {   "text": "Open With",
                    "items": [
                        self.actionOpenDefaultEditor, self.actionOpenSystemEditor
                    ]
                },
                self.actionSetInTerminal,
                "-",
                self.actionRename,
                self.actionCut,
                self.actionCopy,
                self.actionPaste,
                self.actionDelete,
            ]
        }
        self.fileSystemMenu = create_menu(self, contextMenu)

        #Setup Context Menu
        optionsMenu = {
            "text": "File System Options",
            "items": [
                {   "text": "Order",
                    "items": [
                        (self.actionOrderByName, self.actionOrderBySize, self.actionOrderByDate, self.actionOrderByType),
                        "-", self.actionOrderDescending, self.actionOrderFoldersFirst
                    ]
                }
            ]
        }

        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()

        self.fileSystemOptionsMenu = create_menu(self, optionsMenu)
        self.pushButtonOptions.setMenu(self.fileSystemOptionsMenu)

        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)

        # Drag and Drop (see the proxy model)
        self.treeViewFileSystem.setDragEnabled(True)
        self.treeViewFileSystem.setAcceptDrops(True)
        self.treeViewFileSystem.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewFileSystem.setDropIndicatorShown(True)

        self.treeViewFileSystem.setAlternatingRowColors(True)
        self.treeViewFileSystem.setAnimated(True)

    @QtCore.Slot(str)
    def on_comboBoxLocation_currentIndexChanged(self, text):
        path = self.fileManager.expandVars(text)
        #TODO: Mostrar un error cuando sea None
        if path is not None:
            path = self.fileManager.normpath(path)
            self.setPathAsRoot(path)

    @QtCore.Slot()
    def on_pushButtonUp_pressed(self):
        index = self.treeViewFileSystem.rootIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        dir = QtCore.QDir(self.fileSystemModel.filePath(sIndex))
        if dir.cdUp():
            self.setPathAsRoot(dir.path())
            self.comboBoxLocation.lineEdit().setText(dir.path())

    def addPathToFavourites(self, path):
        """
        Adds an entry to the File Manager
        @param path: Adds parameter to path
        """
        if os.path.isdir(str(path)):
            root, dirname_part = path.rsplit(os.sep, 1)
            self.comboFavourites.addItem(dirname_part, {
                                                    'path': path,
                                                    'icon': QtGui.QIcon()})
        else:
            self.logger.debug("Not a directory %s" % path)

    # -------------- Tree View File System
    def showTreeViewFileSystemContextMenu(self, point):
        self.fileSystemMenu.popup(self.treeViewFileSystem.mapToGlobal(point))

    def on_treeViewFileSystem_doubleClicked(self, index):
        path = self.currentPath()
        if os.path.isfile(path):
            self.application.openFile(path)
        elif os.path.isdir(path):
            self.setPathAsRoot(path)

    # --- Insted of using indexes, it's easier for history handling
    # to manage paths
    def currentPath(self):
        return self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())

    def currentDirectory(self):
        return self.application.fileManager.directory(self.currentPath())

    def currentRootPath(self):
        ''' Returns current root path '''
        proxyIndex = self.treeViewFileSystem.rootIndex()
        return self.fileSystemModel.filePath(self.fileSystemProxyModel.mapToSource(proxyIndex))

    def setPathAsRoot(self, path, trackHistory = True):
        assert os.path.isdir(path), _("{0} is not a valid directory!").format(path)

        #Set del treeViewFileSystem
        oldPath = self.currentRootPath()
        sourceIndex = self.fileSystemModel.index(path)
        proxyIndex = self.fileSystemProxyModel.mapFromSource(sourceIndex)
        self.treeViewFileSystem.setRootIndex(proxyIndex)

        #Set del comboBoxLocation
        comboIndex = self.comboBoxLocation.model().index(path)
        #self.comboBoxLocation.setRootModelIndex(comboIndex)
        self.comboBoxLocation.setCurrentIndex(comboIndex.row())
        self.comboBoxLocation.lineEdit().setText( self.fileManager.normpath(path) )

        #Store history
        if trackHistory and os.path.isdir(oldPath):
            self._pushButtonHistoryBack.append(oldPath)
            self.pushButtonBack.setEnabled(True)
            self._pushButtonHistoryForward = []
            self.pushButtonFoward.setEnabled(False)

    def on_pushButtonBack_pressed(self):
        if os.path.exists(self.currentPath()):
            self._pushButtonHistoryForward.append(self.currentPath())
            self.pushButtonFoward.setEnabled(True)
        destination = self._pushButtonHistoryBack.pop()
        self.pushButtonBack.setEnabled(bool(self._pushButtonHistoryBack))
        self.setPathAsRoot(destination, trackHistory = False)

    def on_pushButtonFoward_pressed(self):
        self._pushButtonHistoryBack.append(self.currentRootPath())
        self.pushButtonBack.setEnabled(True)
        destination = self._pushButtonHistoryForward.pop()
        self.setPathAsRoot(destination, trackHistory = False)
        if not len(self._pushButtonHistoryForward):
            self.pushButtonFoward.setEnabled(False)

    # ------------- Actions cut, copy, paste
    def on_actionCut_triggered(self):
        pass

    def on_actionCopy_triggered(self):
        mimeData = self.fileSystemProxyModel.mimeData( [ self.treeViewFileSystem.currentIndex() ] )
        self.application.clipboard().setMimeData(mimeData)

    def on_actionPaste_triggered(self):
        parentPath = self.currentPath()
        mimeData = self.application.clipboard().mimeData()
        if mimeData.hasUrls() and os.path.isdir(parentPath):
            for url in mimeData.urls():
                srcPath = url.toLocalFile()
                dstPath = os.path.join(parentPath, self.application.fileManager.basename(srcPath))
                if os.path.isdir(srcPath):
                    self.application.fileManager.copytree(srcPath, dstPath)
                else:
                    self.application.fileManager.copy(srcPath, dstPath)

    # ------ Actions Create and Delete objects
    @QtCore.Slot()
    def on_actionNewFolder_triggered(self):
        basePath = self.currentPath()
        self.createDirectory(basePath)

    @QtCore.Slot()
    def on_actionNewFile_triggered(self):
        basePath = self.currentPath()
        self.createFile(basePath)

    @QtCore.Slot()
    def on_actionNewFromTemplate_triggered(self):
        currentDirectory = self.currentDirectory()
        filePath = self.templateDialog.createFile(fileDirectory = self.currentDirectory())
        if filePath is not None:
            self.application.openFile(filePath)


    @QtCore.Slot()
    def on_actionDelete_triggered(self):
        basePath = self.currentPath()
        self.deletePath(basePath)

    @QtCore.Slot()
    def on_actionRename_triggered(self):
        basePath = self.currentPath()
        self.renamePath(basePath)

    # Tree View Context Menu Actions
    # Some of them are in fstask's PMXFileSystemTasks mixin
    def pathToClipboard(self, checked = False):
        basePath = self.currentPath()
        QtGui.QApplication.clipboard().setText(basePath)

    @QtCore.Slot()
    def on_actionOpen_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        if os.path.isfile(path):
            self.application.openFile(path)

    @QtCore.Slot()
    def on_actionOpenSystemEditor_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % path, QtCore.QUrl.TolerantMode))

    @QtCore.Slot()
    def on_actionOpenDefaultEditor_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        if os.path.isfile(path):
            self.application.openFile(path)

    # ------ Custom filters
    @QtCore.Slot()
    def on_pushButtonCustomFilters_pressed(self):
        filters, accepted = QtGui.QInputDialog.getText(self, _("Custom Filter"),
                                                        _("Enter the filters (separated by comma)\nOnly * and ? may be used for custom matching"),
                                                        text = self.customFilters)
        if accepted:
            #Save and set filters
            self.settings.setValue('customFilters', filters)
            self.fileSystemProxyModel.setFilterRegExp(filters)

    @QtCore.Slot()
    def on_pushButtonCollapseAll_pressed(self):
        self.treeViewFileSystem.collapseAll()

    @QtCore.Slot(bool)
    def on_pushButtonSync_toggled(self, checked):
        if checked:
            #Conectar señal
            self.mainWindow().currentEditorChanged.connect(self.on_mainWindow_currentEditorChanged)
            self.on_mainWindow_currentEditorChanged(self.mainWindow().currentEditor())
        else:
            #Desconectar señal
            self.mainWindow().currentEditorChanged.disconnect(self.on_mainWindow_currentEditorChanged)

    @QtCore.Slot()
    def on_actionSetInTerminal_triggered(self):
        path = self.currentPath()
        directory = self.application.fileManager.getDirectory(path)
        self.mainWindow().terminal.chdir(directory)

    # ----- Sort and order Actions
    @QtCore.Slot()
    def on_actionOrderByName_triggered(self):
        self.fileSystemProxyModel.sortBy("name", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionOrderBySize_triggered(self):
        self.fileSystemProxyModel.sortBy("size", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionOrderByDate_triggered(self):
        self.fileSystemProxyModel.sortBy("date", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionOrderByType_triggered(self):
        self.fileSystemProxyModel.sortBy("type", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionOrderDescending_triggered(self):
        self.fileSystemProxyModel.sortBy(self.fileSystemProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionOrderFoldersFirst_triggered(self):
        self.fileSystemProxyModel.sortBy(self.fileSystemProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    @QtCore.Slot()
    def on_actionConvertIntoProject_triggered(self):
        _base, name = os.path.split(self.currentPath())
        self.mainWindow().componentByName("projectdialog").createProject(directory = self.currentPath(), name = name)

    def on_mainWindow_currentEditorChanged(self, editor):
        if editor is not None and not editor.isNew():
            index = self.fileSystemModel.index(editor.filePath)
            proxyIndex = self.fileSystemProxyModel.mapFromSource(index)
            self.treeViewFileSystem.setCurrentIndex(proxyIndex)
