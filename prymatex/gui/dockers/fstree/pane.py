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
        
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)
        index = self.fileSystemModel.index(self.application.fileManager.currentDirectory)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))
        self.setupBookmarksCombo()
        
        self.fileSystemModel.rootPathChanged.connect(self.treeRootPathChanged)
        self.bookmarksView.pathChangeRequested.connect(self.openBookmark)
        
        self.configure()

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
                                                    'icon': QIcon()})
        else:
            self.debug("Not a directory %s" % path)
