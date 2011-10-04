#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4.QtGui import QMenu, QAction, QMessageBox, qApp
from PyQt4.QtGui import QApplication, QPixmap, QIcon
from PyQt4.QtCore import QMetaObject, Qt, pyqtSignature, SIGNAL, QDir, pyqtSignal

import os
import shutil
from os.path import join, abspath, isfile, isdir, dirname
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

class FSTree(QtGui.QTreeView, PMXObject):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        self.setupMenus()
        
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)

    #======================================================
    # Menus
    #======================================================
    def setupMenus(self):
        from prymatex.utils.i18n import ugettext as _
        # File Menu
        self.menuFile = QMenu(self)
        self.menuFile.setObjectName('menuFile')
        
        # Directory Menu
        self.menuDirectory = QMenu(self)
        self.menuDirectory.setObjectName('menuDirectory')
        
        # Default menu 
        self.defaultMenu = QMenu(self)
        self.defaultMenu.setObjectName("defaultMenu")
        
        # Actions for those menus
        #Copy to ClipBoard
        actionCopyPathToClipBoard = QtGui.QAction(_("Copy Path To &Clipboard"), self)
        actionCopyPathToClipBoard.setObjectName("actionCopyPathToClipBoard")
        actionCopyPathToClipBoard.triggered.connect(self.pathToClipboard)
        self.menuFile.addAction(actionCopyPathToClipBoard)
        self.menuDirectory.addAction(actionCopyPathToClipBoard)
        
        #Rename
        actionRename = QAction(_("&Rename"), self)
        actionRename.setObjectName("actionRename")
        actionRename.setIcon(QIcon(":/icons/actions/edit-rename.png"))
        actionRename.triggered.connect(self.pathRename)
        self.menuFile.addAction(actionRename)
        self.menuDirectory.addAction(actionRename)
        
        #Delete
        actionDelete = QAction(_("&Delete"), self)
        actionDelete.setObjectName("actionDelete")
        actionDelete.triggered.connect(self.pathDelete)
        self.menuFile.addAction(actionDelete)
        self.menuDirectory.addAction(actionDelete)
        
        #Open
        actionOpen = QAction(_("&Open"), self)
        actionOpen.setObjectName("actionFileOpen")
        actionOpen.setIcon(QIcon(":/icons/actions/document-open.png"))
        actionOpen.triggered.connect(self.pathOpen)
        self.menuFile.addAction(actionOpen)
        
        #Refresh
        actionRefresh = QAction(_("&Refresh"), self)
        actionRefresh.setObjectName("actionRefresh")
        actionRefresh.setIcon(QIcon(":/icons/actions/view-refresh.png"))
        actionRefresh.triggered.connect(self.pathRefresh)
        self.menuFile.addAction(actionRefresh)
        self.menuDirectory.addAction(actionRefresh)
        self.defaultMenu.addAction(actionRefresh)
        
        #Properties
        actionProperties = QAction(_("&Properties"), self)
        actionProperties.setObjectName("actionProperties")
        actionProperties.setIcon(QIcon(":/icons/actions/document-properties.png"))
        actionProperties.triggered.connect(self.pathProperties)
        self.menuFile.addAction(actionProperties)
        self.menuDirectory.addAction(actionProperties)

        # Set As Root
        actionSetAsRoot = QAction(_("&Set as root"), self)
        actionSetAsRoot.setObjectName("actionSetAsRoot")
        actionSetAsRoot.triggered.connect(self.pathSetAsRoot)
        self.menuDirectory.addAction(actionSetAsRoot)
        
        # New Menu
        self.menuNewFileSystemElement = QMenu(_("&New.."), self)
        self.menuNewFileSystemElement.setObjectName('menuNewFileSystemElement')
        self.menuNewFileSystemElement.setIcon(QIcon(":/icons/actions/document-new.png"))
        self.menuDirectory.addMenu(self.menuNewFileSystemElement)
        self.defaultMenu.addMenu(self.menuNewFileSystemElement)
        
        # New File
        actionFileNew = QAction(_("&File"), self)
        actionFileNew.setObjectName("actionFileNew")
        actionFileNew.triggered.connect(self.newFile)
        self.menuNewFileSystemElement.addAction(actionFileNew)
        
        # New Directory
        actionDirNew = QAction(_("&Directory"), self)
        actionDirNew.setObjectName("actionDirNew")
        actionDirNew.triggered.connect(self.newDirectory)
        self.menuNewFileSystemElement.addAction(actionDirNew)
        
    #======================================================
    # Menu Actions
    #======================================================
    def pathToClipboard(self):
        paths = map(self.model().filePath, self.selectedIndexes())
        if len(paths) == 1:
            QApplication.clipboard().setText(paths[0])
    
    def pathRename(self):
        pass
    
    def pathDelete(self):
        curpath = self.current_selected_path
        self.application.fileManager.deletePath(curpath)

    def pathOpen(self):
        pass
        
    def pathRefresh(self):
        self.model().refresh()
        
    def pathProperties(self):
        pass
    
    def pathSetAsRoot(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
            self.setRootIndex(index)

    def newFile(self):
        pass
    
    def newDirectory(self):
        curpath = self.current_selected_path
        dir = self.application.fileManager.createDirectory(curpath)
        print dir
        
    #======================================================
    # Mouse events
    #======================================================
    # Trigger correct menu for path
    def mouseReleaseEvent(self, event):
        QtGui.QTreeView.mouseReleaseEvent(self, event)
        if event.button() == Qt.RightButton:
            index = self.indexAt(event.pos())
            data = self.model().filePath(index)
            if os.path.isfile(data):
                self.menuFile.popup(event.globalPos())
            elif os.path.isdir(data):
                self.menuDirectory.popup(event.globalPos())
            else:
                self.defaultMenu.popup(event.globalPos())

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        QtGui.QTreeView.mouseDoubleClickEvent(self, event)
        
        index = self.indexAt(event.pos())
        path = self.model().filePath(index)
        if os.path.isfile(path):
            self.mainWindow.openFile(QtCore.QFileInfo(path))
        if os.path.isdir(path):
            if self.model().hasChildren(index):
                self.setRootIndex(index)

    def focusEditorPath(self, editor):
        path = editor.fileInfo.absoluteFilePath()
        index = self.model().index(path)
        self.setCurrentIndex(index)
    
    def goUp(self):
        current_top = self.model().filePath(self.rootIndex())
        #self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        upper = abspath(join(current_top, '..'))
        
        if upper != current_top:
            self.setRootIndex(self.model().index(upper))
    
    @property
    def current_selected_path(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
        else:
            index = self.rootIndex()
        return self.model().filePath(index)
