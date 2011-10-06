#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4.QtGui import QMenu, QAction, QMessageBox, qApp
from PyQt4.QtGui import QApplication, QPixmap, QIcon
from PyQt4.QtCore import QMetaObject, Qt, pyqtSignature, SIGNAL, QDir, pyqtSignal

import os
from os.path import join, abspath, isfile, isdir, dirname
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

from prymatex.gui.dockers.fstree.bookmarks import PMXBookmarkModelFactory

class PMXFileSystemTreeView(QtGui.QTreeView, PMXObject):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        self.setAnimated(False)
        #self.setIndentation(20)

    def setModel(self, model):
        QtGui.QTreeView.setModel(self, model)
        self.setHeaderHidden(True)
        self.setUniformRowHeights(False)
        self.setSortingEnabled(True)

    def focusEditorPath(self, editor):
        path = editor.fileInfo.absoluteFilePath()
        index = self.model().index(path)
        self.setCurrentIndex(index)
    
    @property
    def current_selected_path(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
        else:
            index = self.rootIndex()
        return self.model().filePath(index)
        
class PMXBookmarksListView(QtGui.QListView):
    '''
    Bookmarks view
    '''
    pathChangeRequested = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        QtGui.QListView.__init__(self,parent)
        self.modelFactory = PMXBookmarkModelFactory(self)
        self.setModel(self.modelFactory.bookmarksModel)
        self.doubleClicked.connect(self.itemDoubleClicked)
    
    def itemDoubleClicked(self, index):
        path = self.model().index(index.row(), 1).data()
        self.pathChangeRequested.emit(path)
