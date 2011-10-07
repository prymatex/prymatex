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
    
    def __init__(self, parent = None):
        super(PMXFileSystemDock, self).__init__(parent = None)
        self.setupUi(self)
        
        #File System model
        self.fileSystemModel = QtGui.QFileSystemModel(self)
        self.fileSystemModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries) #http://doc.qt.nokia.com/latest/qdir.html#Filter-enum
        self.fileSystemModel.setRootPath(QtCore.QDir.rootPath())
        #Dir Model
        self.dirModel = QtGui.QDirModel(self)
        
        #Proxy para el file system tree view
        self.fileSystemProxyModel = PMXFileSystemProxyModel(self)
        self.fileSystemProxyModel.setSourceModel(self.fileSystemModel)
        
        self.setupComboBoxLocation()
        self.setupTreeViewFileSystem()
        
        self.configure()

    def setupComboBoxLocation(self):
        self.comboBoxLocation.setModel(self.dirModel)
        self.comboBoxLocation.installEventFilter(self)
        self.comboBoxLocation.lineEdit().setText(self.application.fileManager.getOpenDirectory())
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.comboBoxLocation and event.key() == QtCore.Qt.Key_Return:
            path = self.comboBoxLocation.lineEdit().text()
            dIndex = self.dirModel.index(path)
            if dIndex.isValid():
                self.on_comboBoxLocation_currentIndexChanged(path)
                return True
        else:
            return QtCore.QObject.eventFilter(self, obj, event)
    
    def setupTreeViewFileSystem(self):
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)
        index = self.fileSystemModel.index(self.application.fileManager.getOpenDirectory())
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
        
        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()
        
        self.orderMenu.addSeparator()
        self.orderMenu.addAction(self.actionOrderDescending)
        self.orderMenu.addAction(self.actionOrderFoldersFirst)
        
        self.fileSystemMenu.addSeparator()
        self.fileSystemMenu.addMenu(self.orderMenu)
        
        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)
    
    @QtCore.pyqtSlot(str)
    def on_comboBoxLocation_currentIndexChanged(self, path):
        sIndex = self.fileSystemModel.index(path)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(sIndex))
    
    @QtCore.pyqtSlot()
    def on_puchButtonSync_pressed(self):
        editor = self.mainWindow.currentEditor
        path = self.application.fileManager.getOpenDirectory(editor.fileInfo)
        sIndex = self.fileSystemModel.index(path)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(sIndex))
        self.comboBoxLocation.lineEdit().setText(dir.path())

    @QtCore.pyqtSlot()
    def on_pushButtonUp_pressed(self):
        index = self.treeViewFileSystem.rootIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        dir = QtCore.QDir(self.fileSystemModel.filePath(sIndex))
        if dir.cdUp():
            index = self.fileSystemModel.index(dir.path())
            self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))
            self.comboBoxLocation.lineEdit().setText(dir.path())

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
            self.comboBoxLocation.lineEdit().setText(path)
    
    def on_treeViewFileSystem_doubleClicked(self, index):
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        if os.path.isfile(path):
            self.mainWindow.openFile(QtCore.QFileInfo(path))
        if os.path.isdir(path):
            self.treeViewFileSystem.setRootIndex(index)
            self.comboBoxLocation.lineEdit().setText(path)

    #======================================================
    # Tree View Context Menu Actions
    #======================================================
    def pathToClipboard(self, checked = False):
        paths = map(self.model().filePath, self.selectedIndexes())
        if len(paths) == 1:
            QApplication.clipboard().setText(paths[0])
    
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        curpath = self.current_selected_path
        dir = self.application.fileManager.createDirectory(curpath)

    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        pass

    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        index = self.treeViewFileSystem.currentIndex()
        sIndex = self.fileSystemProxyModel.mapToSource(index)
        path = self.fileSystemModel.filePath(sIndex)
        ok = QtGui.QMessageBox.question(self, "Deletion Confirmation", "Are you sure you want to delete <b>%s</b>?" % path,
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if ok == QtGui.QMessageBox.Ok:
            self.application.fileManager.deletePath(path)
    
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