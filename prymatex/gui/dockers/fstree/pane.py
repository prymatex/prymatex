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
        self.dirModel = QtGui.QDirModel(self)
        self.comboBoxLocation.setModel(self.dirModel)
        
        #http://doc.qt.nokia.com/latest/qdir.html#Filter-enum
        self.fileSystemModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)
        dir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DesktopLocation)
        self.fileSystemModel.setRootPath(dir)
        
        self.fileSystemProxyModel = PMXFileSystemProxyModel(self)
        self.fileSystemProxyModel.setSourceModel(self.fileSystemModel)
        
        self.setupTreeViewFileSystem()
        
        self.configure()

    def setupTreeViewFileSystem(self):
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)
        index = self.fileSystemModel.index(self.application.fileManager.currentDirectory)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))
        
        self.treeViewFileSystem.setHeaderHidden(True)
        self.treeViewFileSystem.setUniformRowHeights(False)
        
        #Setup Context Menu
        self.fileSystemMenu = QtGui.QMenu(self)
        self.fileSystemMenu.setObjectName('fileSystemMenu')
        
        self.newMenu = QtGui.QMenu("New", self)
        self.newMenu.setObjectName('newMenu')
        self.newMenu.addAction(self.actionNewFolder)
        self.newMenu.addAction(self.actionNewFile)
        self.newMenu.addSeparator()
        self.newMenu.addAction(self.actionNewFromTemplate)
        
        self.fileSystemMenu.addMenu(self.newMenu)
        self.fileSystemMenu.addAction(self.actionDelete)
        
        self.orderMenu = QtGui.QMenu("Order", self)
        self.orderMenu.setObjectName("orderMenu")
        self.orderGroup = QtGui.QActionGroup(self.orderMenu)
        self.orderGroup.setExclusive(True)
        orderActions = [self.actionOrderByName, self.actionOrderBySize, self.actionOrderByDate, self.actionOrderByType]
        map(self.orderMenu.addAction, orderActions)
        map(lambda action: action.setActionGroup(self.orderGroup), orderActions)
        
        self.actionOrderByName.trigger()
        
        self.orderMenu.addSeparator()
        self.orderMenu.addAction(self.actionOrderDescending)
        self.orderMenu.addAction(self.actionOrderFoldersFirst)
        
        self.fileSystemMenu.addSeparator()
        self.fileSystemMenu.addMenu(self.orderMenu)
        
        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)
    
    @QtCore.pyqtSignature('int')
    def on_comboBoxLocation_currentIndexChanged(self, index):
        pass
    
    @QtCore.pyqtSignature('bool')
    def on_puchButtonSync_toggled(self, sync):
        if sync:
            # Forzamos la sincronizacion
            editor = self.mainWindow.currentEditor
            self.treeViewFileSystem.focusWidgetPath(editor)

    @QtCore.pyqtSignature('')
    def on_pusButtonUp_pressed(self):
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
        self.fileSystemMenu.popup(self.treeViewFileSystem.mapToGlobal(point))
                
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

    def newDirectory(self, checked = False):
        curpath = self.current_selected_path
        dir = self.application.fileManager.createDirectory(curpath)
        print dir
    
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        pass

    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        pass

    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        pass
    
    @QtCore.pyqtSlot(str)
    def on_lineEditFilter_textChanged(self, text):
        self.fileSystemProxyModel.setFilterRegExp(text)
    
    @QtCore.pyqtSlot()
    def on_actionOrderByName_triggered(self):
        self.fileSystemProxyModel.sortBy("name", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderBySize_triggered(self):
        self.fileSystemProxyModel.sortBy("size", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderByDate_triggered(self):
        self.fileSystemProxyModel.sortBy("date", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderByType_triggered(self):
        self.fileSystemProxyModel.sortBy("type", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderDescending_triggered(self):
        self.fileSystemProxyModel.sortBy(self.fileSystemProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderFoldersFirst_triggered(self):
        self.fileSystemProxyModel.sortBy(self.fileSystemProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())