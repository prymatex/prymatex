#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import shutil
from os.path import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from prymatex.gui.panes import PaneDockBase
from prymatex.gui import PMXBaseGUIMixin
from prymatex.utils.translation import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
from prymatex.ui.panefilesystem import Ui_FSPane
from prymatex.ui.filesystemsettings import Ui_FSSettingsDialog
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty

class FSPaneWidget(QWidget, Ui_FSPane, PMXBaseGUIMixin, PMXObject):
    filters = pmxConfigPorperty(default = ['*~', '*.pyc'])
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setObjectName('FSPaneWidget')
        self.dialogConfigFilters = PMXFSPaneConfigDialog(self)
        self.setupUi(self)
        start_dir = qApp.instance().startDirectory()
        self.tree.setRootIndex(self.tree.model().index(start_dir))
        self.comboBookmarks.addItem(_("Bookmarks"), 1)
        #self.comboBookmarks.addItem(_("File System"), 2)
        #self.tree.model().rootPathChanged.connect(self.comboBookmarks.pathChanged)
        self.tree.model().rootPathChanged.connect(self.treeRootPathChanged)
        
        self.configure()
        
    class Meta:
        settings = "fspane"
    
    def treeRootPathChanged(self, path):
        self.comboBookmarks.addItem(path)
        #self.tree.model().rootPathChanged.connect(self.treeRootPathChanged)
    
    @pyqtSignature('int')
    def on_comboBookmarks_currentIndexChanged(self, index):
        data = self.comboBookmarks.itemData(index)
        print data.toPyObject()
    
    @pyqtSignature('bool')
    def on_buttonSyncTabFile_toggled(self, sync):
        if sync:
            # Forzamos la sincronizacion
            editor = self.mainWindow.currentEditorWidget
            self.tree.focusWidgetPath(editor)

    @pyqtSignature('')
    def on_buttonUp_pressed(self):
        #QMessageBox.information(self, "UP", "Up")
        #self.get
        self.tree.goUp()
    
    @pyqtSignature('')
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
    

class PMXFSPaneConfigDialog(Ui_FSSettingsDialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class PMXFSPaneDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))
