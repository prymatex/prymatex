#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys
import shutil
from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.dockers.proxies import PMXFileSystemProxyModel
from prymatex.gui.utils import createQMenu
from prymatex.ui.dockers.filesystem import Ui_FileSystemDock
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog
from prymatex.gui.dockers.fstasks import PMXFileSystemTasks
from prymatex.gui.dialogs.newproject import PMXNewProjectDialog


class PMXSafeFilesytemLineEdit(QtGui.QLineEdit):
    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        
    def event(self, event):
        if isinstance(event, QtGui.QKeyEvent):
            key = event.key()
            if not self.isValidPlatformPathKey(key):
                return False
            elif key == QtCore.Qt.Key_Return:
                if not self.currentTextIsValidPath():
                    return False
        return super(PMXSafeFilesytemLineEdit, self).event(event)
    
    
    def isValidPlatformPathKey(self, key):
        k = QtCore.Qt
        if key in [k.Key_Asterisk,
                   k.Key_Backslash,
                   k.Key_Less,
                   k.Key_Greater,
                   k.Key_Question,
                   k.Key_Colon,
                   ]:
            return False
        return True

    DOS_NAMES = 'CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9'.split()
    
    def currentTextIsValidPath(self):
        ''' Check if name is valid '''
        text = self.text()
        if not text:
            return False
        if sys.platform.count('win'):
            if text.upper() in self.DOS_NAMES:
                return False
        
        return False

    
class PMXFileSystemItemDelegate(QtGui.QItemDelegate):
    ''' '''
    def createEditor(self, parent, option, index):
        ''' Create a new editor ''' 
        
        editor = PMXSafeFilesytemLineEdit(parent)
        editor.setText(index.data())
        return editor
    
    def setEditorData(self, editor, index):
        return QtGui.QItemDelegate.setEditorData(self, editor, index)
    
    def setModelData(self, editor, model, index):
        return QtGui.QItemDelegate.setModelData(self, editor, model, index)
        
class PMXFileSystemDock(QtGui.QDockWidget, Ui_FileSystemDock, PMXFileSystemTasks):
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("Shift+F8")
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'FileSystem'
    filters = pmxConfigPorperty(default = ['*~', '*.pyc'])
    
    _pushButtonHistoryBack = []
    _pushButtonHistoryForward = []
    
    def __init__(self, parent = None):
        QtGui.QDockWidget.__init__(self, parent)
        PMXFileSystemTasks.__init__(self)     
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
        
        self.installEventFilter(self)
        
        self.setupButtons()
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            #print "Key press", obj #
            if obj in (self, self.treeViewFileSystem):
                if  event.key() == QtCore.Qt.Key_Backspace:
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
                self.lineEditFilter.setFocus()
                return True
        return QtGui.QDockWidget.eventFilter(self, obj, event)
    
    
    def setupComboBoxLocation(self):
        self.comboBoxLocation.setModel(self.dirModel)
        self.comboBoxLocation.lineEdit().setText(self.application.fileManager.getDirectory())
        self.comboBoxLocation.lineEdit().returnPressed.connect(self.on_lineEdit_returnPressed)
    
    def on_lineEdit_returnPressed(self):
        path = self.comboBoxLocation.lineEdit().text()
        dIndex = self.dirModel.index(path)
        if dIndex.isValid():
            self.on_comboBoxLocation_currentIndexChanged(path)
    
    def setupButtons(self):
        self.pushButtonSync.setCheckable(True)
        self.pushButtonBack.setEnabled(False)
        self.pushButtonFoward.setEnabled(False)
    
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
        self.fileSystemMenu, self.fileSystemMenuActions = createQMenu(menuSettings, self)

        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()
        
        #Connect context menu
        self.treeViewFileSystem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewFileSystem.customContextMenuRequested.connect(self.showTreeViewFileSystemContextMenu)
    
        #=======================================================================
        # Drag and Drop (see the proxy model)
        #=======================================================================
        self.treeViewFileSystem.setDragEnabled(True)
        self.treeViewFileSystem.setAcceptDrops(True)
        self.fileSystemModel.setReadOnly(False)
        self.treeViewFileSystem.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewFileSystem.setDropIndicatorShown(True)

        # Allow Rename
        self.treeViewFileSystem.setEditTriggers( QtGui.QAbstractItemView.EditKeyPressed )
        self.treeViewFileSystem.setItemDelegateForColumn(0, PMXFileSystemItemDelegate(self))
        self.treeViewFileSystem.setAlternatingRowColors(True)
        self.treeViewFileSystem.setAnimated(True)

    @QtCore.pyqtSlot(str)
    def on_comboBoxLocation_currentIndexChanged(self, path):
        self.setPathAsRoot(path)

    @QtCore.pyqtSlot()
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
        if os.path.isdir(unicode(path)):
            root, dirname_part = path.rsplit(os.sep, 1)
            self.comboFavourites.addItem(dirname_part, {
                                                    'path': path,
                                                    'icon': QtGui.QIcon()})
        else:
            self.logger.debug("Not a directory %s" % path)

    #================================================
    # Tree View File System
    #================================================
    def showTreeViewFileSystemContextMenu(self, point):
        self.fileSystemMenu.popup(self.treeViewFileSystem.mapToGlobal(point))
                
    def on_treeViewFileSystem_doubleClicked(self, index):
        # History
        
        path = self.currentPath()
        if os.path.isfile(path):
            self.application.openFile(path)
            
        elif os.path.isdir(path):
            self.setPathAsRoot(path)
            self.comboBoxLocation.lineEdit().setText(path)
    
    
    #===========================================================================
    # Insted of using indexes, it's easier for history handling
    # to manage paths 
    #===========================================================================
    def currentPath(self):
        return self.fileSystemProxyModel.filePath(self.treeViewFileSystem.currentIndex())

    def currentRootPath(self):
        ''' Returns current root path '''
        proxyIndex = self.treeViewFileSystem.rootIndex()
        return self.fileSystemModel.filePath(self.fileSystemProxyModel.mapToSource(proxyIndex))
    
    def setPathAsRoot(self, path, trackHistory = True):
        assert os.path.isdir(path), _("{0} is not a valid directory!").format(path)
        oldPath = self.currentRootPath()
        sourceIndex = self.fileSystemModel.index(path)
        proxyIndex = self.fileSystemProxyModel.mapFromSource(sourceIndex)
        self.treeViewFileSystem.setRootIndex(proxyIndex)
        self.comboBoxLocation.lineEdit().setText( path )
        if trackHistory and os.path.isdir(oldPath):
            self._pushButtonHistoryBack.append(oldPath)
            self.pushButtonBack.setEnabled(True)
            self._pushButtonHistoryForward = []
            self.pushButtonFoward.setEnabled(False)
        print ("Back history: %s" % self._pushButtonHistoryBack)
        print ("Fwd  history: %s" % self._pushButtonHistoryForward)
    
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
            self.treeViewFileSystem.setCurrentIndex(proxyIndex)
        