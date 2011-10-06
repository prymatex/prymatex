#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shutil
from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.panefilesystem import Ui_FileSystemDock
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.dockers.fstree.proxies import PMXFileSystemProxyModel

class PMXFileSystemDock(QtGui.QDockWidget, Ui_FileSystemDock, PMXObject):
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'FileSystem'
    filters = pmxConfigPorperty(default = ['*~', '*.pyc'])
    
    def __init__(self, parent):
        super(PMXFileSystemDock, self).__init__(parent)
        self.setupUi(self)
        
        self.fileSystemModel = QtGui.QFileSystemModel(self)
        #http://doc.qt.nokia.com/latest/qdir.html#Filter-enum
        self.fileSystemModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)
        dir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DesktopLocation)
        self.fileSystemModel.setRootPath(dir)
        
        self.fileSystemProxyModel = PMXFileSystemProxyModel(self)
        self.fileSystemProxyModel.setSourceModel(self.fileSystemModel)
        
        self.setupTreeViewFileSystem()
        self.setupBookmarksCombo()
        
        #self.fileSystemModel.rootPathChanged.connect(self.treeRootPathChanged)
        self.bookmarksView.pathChangeRequested.connect(self.openBookmark)
        
        self.configure()

    def setupTreeViewFileSystem(self):
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)
        index = self.fileSystemModel.index(self.application.fileManager.currentDirectory)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))
        
        #Setup Context Menu
        # File Menu
        self.menuFile = QtGui.QMenu(self)
        self.menuFile.setObjectName('menuFile')
        
        # Directory Menu
        self.menuDirectory = QtGui.QMenu(self)
        self.menuDirectory.setObjectName('menuDirectory')
        
        # Default menu 
        self.defaultMenu = QtGui.QMenu(self)
        self.defaultMenu.setObjectName("defaultMenu")
        
        # Actions for those menus
        #Copy to ClipBoard
        actionCopyPathToClipBoard = QtGui.QAction(_("Copy Path To &Clipboard"), self)
        actionCopyPathToClipBoard.setObjectName("actionCopyPathToClipBoard")
        actionCopyPathToClipBoard.triggered.connect(self.pathToClipboard)
        self.menuFile.addAction(actionCopyPathToClipBoard)
        self.menuDirectory.addAction(actionCopyPathToClipBoard)
        
        #Rename
        actionRename = QtGui.QAction(_("&Rename"), self)
        actionRename.setObjectName("actionRename")
        actionRename.setIcon(QtGui.QIcon(":/icons/actions/edit-rename.png"))
        actionRename.triggered.connect(self.pathRename)
        self.menuFile.addAction(actionRename)
        self.menuDirectory.addAction(actionRename)
        
        #Delete
        actionDelete = QtGui.QAction(_("&Delete"), self)
        actionDelete.setObjectName("actionDelete")
        actionDelete.triggered.connect(self.pathDelete)
        self.menuFile.addAction(actionDelete)
        self.menuDirectory.addAction(actionDelete)
        
        #Open
        actionOpen = QtGui.QAction(_("&Open"), self)
        actionOpen.setObjectName("actionFileOpen")
        actionOpen.setIcon(QtGui.QIcon(":/icons/actions/document-open.png"))
        actionOpen.triggered.connect(self.pathOpen)
        self.menuFile.addAction(actionOpen)
        
        #Refresh
        actionRefresh = QtGui.QAction(_("&Refresh"), self)
        actionRefresh.setObjectName("actionRefresh")
        actionRefresh.setIcon(QtGui.QIcon(":/icons/actions/view-refresh.png"))
        actionRefresh.triggered.connect(self.pathRefresh)
        self.menuFile.addAction(actionRefresh)
        self.menuDirectory.addAction(actionRefresh)
        self.defaultMenu.addAction(actionRefresh)
        
        #Properties
        actionProperties = QtGui.QAction(_("&Properties"), self)
        actionProperties.setObjectName("actionProperties")
        actionProperties.setIcon(QtGui.QIcon(":/icons/actions/document-properties.png"))
        actionProperties.triggered.connect(self.pathProperties)
        self.menuFile.addAction(actionProperties)
        self.menuDirectory.addAction(actionProperties)

        # Set As Root
        actionSetAsRoot = QtGui.QAction(_("&Set as root"), self)
        actionSetAsRoot.setObjectName("actionSetAsRoot")
        actionSetAsRoot.triggered.connect(self.pathSetAsRoot)
        self.menuDirectory.addAction(actionSetAsRoot)
        
        # New Menu
        self.menuNewFileSystemElement = QtGui.QMenu(_("&New.."), self)
        self.menuNewFileSystemElement.setObjectName('menuNewFileSystemElement')
        self.menuNewFileSystemElement.setIcon(QtGui.QIcon(":/icons/actions/document-new.png"))
        self.menuDirectory.addMenu(self.menuNewFileSystemElement)
        self.defaultMenu.addMenu(self.menuNewFileSystemElement)
        
        # New File
        actionFileNew = QtGui.QAction(_("&File"), self)
        actionFileNew.setObjectName("actionFileNew")
        actionFileNew.triggered.connect(self.newFile)
        self.menuNewFileSystemElement.addAction(actionFileNew)
        
        # New Directory
        actionDirNew = QtGui.QAction(_("&Directory"), self)
        actionDirNew.setObjectName("actionDirNew")
        actionDirNew.triggered.connect(self.newDirectory)
        self.menuNewFileSystemElement.addAction(actionDirNew)
        
        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)
        
    def treeRootPathChanged(self, path):
        newPathParts = unicode(path).split(os.sep)
        rows = self.comboBookmarks.model().rowCount()
        self.comboBookmarks.setEnabled(False)
        self.comboBookmarks.model().removeRows(2, rows -2)
        self.comboBookmarks.insertSeparator(2)
        for i in range(len(newPathParts)):
            
            name = newPathParts[i]
            if not name:
                continue
            path = os.sep.join(newPathParts[:i+1])
            model = self.treeViewFileSystem.model()
            icon = model.fileIcon(model.index(path))
            self.comboBookmarks.addItem(icon, name, path)
        self.comboBookmarks.setCurrentIndex(self.comboBookmarks.model().rowCount()-1)
        self.comboBookmarks.setEnabled(True)

    def openBookmark(self, path):
        self.treeViewFileSystem.setRootIndex(self.treeViewFileSystem.model().index(path))
        self.comboBookmarks.setCurrentIndex(1)
    
    def setupBookmarksCombo(self):
        self.comboBookmarks.insertSeparator(self.comboBookmarks.model().rowCount())
        #self.comboBookmarks.addItem("Cosas")
    
    @QtCore.pyqtSignature('int')
    def on_comboBookmarks_currentIndexChanged(self, index):
        if index == 0:
            self.stackedWidget.setCurrentIndex(1)
        elif index == 1:
            self.stackedWidget.setCurrentIndex(0)
        
        else:
            path = self.comboBookmarks.itemData(index)
            if self.treeViewFileSystem.model().index(path) != self.treeViewFileSystem.rootIndex():
                print "Should Change"
            #if os.path.exists(path):
            #    self.treeViewFileSystem.setRootIndex(self.treeViewFileSystem.model().index(path))
    
    @QtCore.pyqtSignature('bool')
    def on_buttonSyncTabFile_toggled(self, sync):
        if sync:
            # Forzamos la sincronizacion
            editor = self.mainWindow.currentEditor
            self.treeViewFileSystem.focusWidgetPath(editor)

    @QtCore.pyqtSignature('')
    def on_buttonUp_pressed(self):
        index = self.treeViewFileSystem.rootIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        currentPath = self.fileSystemModel.filePath(sIndex)
        newPath = os.path.abspath(os.path.join(currentPath, '..'))
        
        if newPath != self.fileSystemModel.rootPath():
            index = self.fileSystemModel.index(newPath)
            self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))

    @QtCore.pyqtSignature('')
    def on_buttonCollapseAll_pressed(self):
        self.treeViewFileSystem.collapseAll()
        #self.buttonSyncTabFile.setEnabled(False)
    
    def on_buttonFilter_pressed(self):
        self.dialogConfigFilters.exec_()
    
    def changeToFavourite(self, index):
        print "-"*40
        #print index, self.comboFavourites.
        print "-"*40
    
    def addPathToFavourites(self, path):
        '''
        Adds an entry to the File Manager 
        @param path: Adds parameter to path
        '''
        if isdir(unicode(path)):
            root, dirname_part = path.rsplit(os.sep, 1)
            self.comboFavourites.addItem(dirname_part, {
                                                    'path': path,
                                                    'icon': QtGui.QIcon()})
        else:
            self.debug("Not a directory %s" % path)

    #================================================
    # Tree View File System
    #================================================
    def showTreeViewFileSystemContextMenu(self, point):
        index = self.treeViewFileSystem.indexAt(point)
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        if os.path.isfile(path):
            self.menuFile.popup(self.treeViewFileSystem.mapToGlobal(point))
        elif os.path.isdir(path):
            self.menuDirectory.popup(self.treeViewFileSystem.mapToGlobal(point))
        else:
            self.defaultMenu.popup(self.treeViewFileSystem.mapToGlobal(point))
                
    def on_treeViewFileSystem_activated(self, index):
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        if os.path.isfile(path):
            self.mainWindow.openFile(QtCore.QFileInfo(path))
        if os.path.isdir(path):
            self.treeViewFileSystem.setRootIndex(index)
    
    def on_treeViewFileSystem_doubleClicked(self, index):
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        if os.path.isfile(path):
            self.mainWindow.openFile(QtCore.QFileInfo(path))
        if os.path.isdir(path):
            self.treeViewFileSystem.setRootIndex(index)

    #======================================================
    # Tree View Context Menu Actions
    #======================================================
    def pathToClipboard(self, checked = False):
        paths = map(self.model().filePath, self.selectedIndexes())
        if len(paths) == 1:
            QApplication.clipboard().setText(paths[0])
    
    def pathRename(self, checked = False):
        pass
    
    def pathDelete(self, checked = False):
        index = self.treeViewFileSystem.currentIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        ok = QtGui.QMessageBox.question(self, "Deletion Confirmation", "Are you sure you want to delete <b>%s</b>?" % path,
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if ok == QtGui.QMessageBox.Ok:
            self.application.fileManager.deletePath(path)

    def pathOpen(self, checked = False):
        index = self.treeViewFileSystem.currentIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        if os.path.isfile(path):
            self.mainWindow.openFile(QtCore.QFileInfo(path))
        if os.path.isdir(path):
            self.treeViewFileSystem.setRootIndex(index)
        
    def pathRefresh(self, checked = False):
        self.model().refresh()
        
    def pathProperties(self, checked = False):
        pass
    
    def pathSetAsRoot(self, checked = False):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
            self.setRootIndex(index)

    def newFile(self, checked = False):
        pass
    
    def newDirectory(self, checked = False):
        curpath = self.current_selected_path
        dir = self.application.fileManager.createDirectory(curpath)
        print dir