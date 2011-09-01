#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shutil
from os.path import *
from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
from prymatex.ui.panefilesystem import Ui_FSPane
from prymatex.ui.filesystemsettings import Ui_FSSettingsDialog
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty

class FSPaneWidget(PMXObject, Ui_FSPane):
    filters = pmxConfigPorperty(default = ['*~', '*.pyc'])
    
    def __init__(self, parent):
        PMXObject.__init__(self, parent)
        self.setObjectName('FSPaneWidget')
        self.dialogConfigFilters = PMXFSPaneConfigDialog(self)
        self.setupUi(self)

        self.tree.setRootIndex(self.tree.model().index(self.application.fileManager.currentDirectory))
        self.setupBookmarksCombo()
        self.tree.rootChanged.connect(self.treeRootPathChanged)
        
        self.bookmarksView.pathChangeRequested.connect(self.openBookmark)
        self.configure()
        
    class Meta:
        settings = "fspane"
    
    def treeRootPathChanged(self, path):
        #self.comboBookmarks.addItem(path)
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
            model = self.tree.model()
            icon = model.fileIcon(model.index(path))
            self.comboBookmarks.addItem(icon, name, path)
        self.comboBookmarks.setCurrentIndex(self.comboBookmarks.model().rowCount()-1)
        self.comboBookmarks.setEnabled(True)
        
        
        
    
    def openBookmark(self, path):
        self.tree.setRootIndex(self.tree.model().index(path))
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
            if self.tree.model().index(path) != self.tree.rootIndex():
                print "Should Change"
            #if os.path.exists(path):
            #    self.tree.setRootIndex(self.tree.model().index(path))
    
    @QtCore.pyqtSignature('bool')
    def on_buttonSyncTabFile_toggled(self, sync):
        if sync:
            # Forzamos la sincronizacion
            editor = self.mainWindow.currentEditorWidget
            self.tree.focusWidgetPath(editor)

    @QtCore.pyqtSignature('')
    def on_buttonUp_pressed(self):
        #QMessageBox.information(self, "UP", "Up")
        #self.get
        self.tree.goUp()
    
    @QtCore.pyqtSignature('')
    def on_buttonCollapseAll_pressed(self):
        self.tree.collapseAll()
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
    

class PMXFSPaneConfigDialog(Ui_FSSettingsDialog, QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

class PMXFSPaneDock(QtGui.QDockWidget):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))
