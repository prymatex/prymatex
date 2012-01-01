#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import shutil

from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.dockers.proxies import PMXFileSystemProxyModel
from prymatex.gui.dockers.base import PMXBaseDock
from prymatex.gui.utils import createQMenu
from prymatex.ui.dockers.filesystem import Ui_FileSystemDock
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog
from prymatex.gui.dockers.fstasks import PMXFileSystemTasks
from prymatex.gui.dialogs.newproject import PMXNewProjectDialog

class PMXFileSystemDock(QtGui.QDockWidget, Ui_FileSystemDock, PMXObject, PMXFileSystemTasks):
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'FileSystem'
    filters = pmxConfigPorperty(default = ['*~', '*.pyc'])
    
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("Shift+F8")
    def __init__(self, parent = None):
        QtGui.QDockWidget.__init__(self, parent)
        self.setupUi(self)
        PMXBaseDock.__init__(self)        
        
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
        
        self.installEventFilter(self)
        
        self.setupButtons()
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            #print "Key press", obj #
            if obj in (self, self.treeViewFileSystem) and event.key() == QtCore.Qt.Key_Backspace:
                self.pushButtonUp.click()
                return True
            if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
                # FIXME: Get Ctrl + F before editor's find, all the foucs is belong to us right now :P
                self.lineEditFilter.setFocus()
                return True
        return QtGui.QDockWidget.eventFilter(self, obj, event)

    def setupComboBoxLocation(self):
        self.comboBoxLocation.setModel(self.dirModel)
        self.comboBoxLocation.lineEdit().setText(self.application.fileManager.getDirectory())
        self.comboBoxLocation.lineEdit().returnPressed.connect(self.on_lineEdit_returnPressed)
    
    def on_lineEdit_returnPressed(self):
        path = self.comboBoxLocation.lineEdit().text()
        print(path)
        dIndex = self.dirModel.index(path)
        if dIndex.isValid():
            self.on_comboBoxLocation_currentIndexChanged(path)
    
    def setupButtons(self):
        self.pushButtonSync.setCheckable(True)
        
    
    def setupTreeViewFileSystem(self):
        self.treeViewFileSystem.setModel(self.fileSystemProxyModel)
        index = self.fileSystemModel.index(self.application.fileManager.getDirectory())
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(index))
        
        self.treeViewFileSystem.setHeaderHidden(True)
        self.treeViewFileSystem.setUniformRowHeights(False)
        
        #Setup Context Menu
        menuSettings = { 
            "title": "File System",
            "items": [
                {   "title": "New",
                    "items": [
                        self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionOpen,
                {   "title": "Open With",
                    "items": [
                        self.actionOpenDefaultEditor, self.actionOpenSystemEditor 
                    ]
                },
                self.actionRename,
                self.actionConvert_Into_Project,
                "-",
                self.actionDelete,
                {   "title": "Order",
                    "items": [
                        (self.actionOrderByName, self.actionOrderBySize, self.actionOrderByDate, self.actionOrderByType),
                        "-", self.actionOrderDescending, self.actionOrderFoldersFirst
                    ]
                }
            ]
        }
        self.fileSystemMenu = createQMenu(menuSettings, self)

        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()
        
        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)
    
    @QtCore.pyqtSlot(str)
    def on_comboBoxLocation_currentIndexChanged(self, path):
        sIndex = self.fileSystemModel.index(path)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(sIndex))
    
    @QtCore.pyqtSlot()
    def on_pushButtonSync_pressed(self):
        editor = self.application.currentEditor()
        path = self.application.fileManager.getDirectory(editor.filePath)
        sIndex = self.fileSystemModel.index(path)
        self.treeViewFileSystem.setRootIndex(self.fileSystemProxyModel.mapFromSource(sIndex))
        self.comboBoxLocation.lineEdit().setText(path)

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
        """
        Adds an entry to the File Manager 
        @param path: Adds parameter to path
        """
        if os.path.isdir(unicode(path)):
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
                
    def on_treeViewFileSystem_doubleClicked(self, index):
        path = self.fileSystemProxyModel.filePath(index)
        if os.path.isfile(path):
            self.application.openFile(path)
        if os.path.isdir(path):
            self.treeViewFileSystem.setRootIndex(index)
            self.comboBoxLocation.lineEdit().setText(path)

    def currentPath(self):
        return self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())

    #======================================================
    # Tree View Context Menu Actions
    # Some of them are in fstask's PMXFileSystemTasks mixin
    #======================================================
    def pathToClipboard(self, checked = False):
        path = self.currentPath()
        QtGui.QApplication.clipboard().setText(path)
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        if os.path.isfile(path):
            self.application.openFile(path)
    
    @QtCore.pyqtSlot()
    def on_actionOpenSystemEditor_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % path, QtCore.QUrl.TolerantMode))
    
    @QtCore.pyqtSlot()
    def on_actionOpenDefaultEditor_triggered(self):
        path = self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())
        if os.path.isfile(path):
            self.application.openFile(path)
    
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
        
        
    @QtCore.pyqtSlot()
    def on_actionConvert_Into_Project_triggered(self):
        _base, name = os.path.split(self.currentPath())
        PMXNewProjectDialog.getNewProject(self, self.currentPath(), name)
        
    def on_currentEditorChanged(self, editor):
        available = editor is not None
        self.pushButtonSync.setEnabled(available)
        if available:
            filePath = editor.filePath
            index = self.fileSystemModel.index(filePath)
            proxyIndex = self.fileSystemProxyModel.mapFromSource(index)
            print("Setting path to ", filePath)
            self.treeViewFileSystem.setCurrentIndex(proxyIndex)
        