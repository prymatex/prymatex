#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.dockers.base import PMXBaseDock
from prymatex.gui.utils import createQMenu
from prymatex.ui.dockers.projects import Ui_ProjectsDock

class PMXProjectDock(QtGui.QDockWidget, Ui_ProjectsDock, PMXBaseDock, PMXObject):
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F8")
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.projectTreeProxyModel = self.application.projectManager.projectTreeProxyModel
        self.treeViewProjects.setModel(self.projectTreeProxyModel)

        self.setupTreeViewProjects()
        
    def setupTreeViewProjects(self):
        #Setup Context Menu
        projectMenuSettings = { 
            "title": "Project",
            "items": [
                {   "title": "New",
                    "items": [
                        self.actionNewProject, self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionOpen,
                "-",
                self.actionDelete,
                "-",
                self.actionCloseProject,
                self.actionOpenProject,
                self.actionProperties
            ]
        }
        self.projectsMenu = createQMenu(projectMenuSettings, self)
        
        fileMenuSettings = { 
            "title": "File",
            "items": [
                {   "title": "New",
                    "items": [
                        self.actionNewProject, self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionOpen,
                {   "title": "Open With",
                    "items": [
                        self.actionOpenDefaultEditor, self.actionOpenSystemEditor 
                    ]
                },
                "-",
                self.actionDelete,
                self.actionProperties
            ]
        }
        self.fileMenu = createQMenu(fileMenuSettings, self)
        
        directoryMenuSettings = { 
            "title": "File",
            "items": [
                {   "title": "New",
                    "items": [
                        self.actionNewProject, self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionDelete,
                self.actionProperties
            ]
        }
        self.directoryMenu = createQMenu(directoryMenuSettings, self)
        
        #Connect context menu
        self.treeViewProjects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewProjects.customContextMenuRequested.connect(self.showProjectTreeViewContextMenu)

    #================================================
    # Tree View Project
    #================================================
    def showProjectTreeViewContextMenu(self, point):
        self.projectsMenu.popup(self.treeViewProjects.mapToGlobal(point))
                
    def on_treeViewProjects_doubleClicked(self, index):
        path = self.projectTreeProxyModel.filePath(index)
        if os.path.isfile(path):
            self.application.openFile(path)
            
    #======================================================
    # Tree View Context Menu Actions
    #======================================================
    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
        
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionCloseProject_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionOpenProject_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionProperties_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print self.projectTreeProxyModel.sourceModel().fileWatcher.directories()
        print self.projectTreeProxyModel.sourceModel().fileWatcher.files()
    
    @QtCore.pyqtSlot()
    def on_actionRefresh_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path
    
    @QtCore.pyqtSlot()
    def on_actionOpenSystemEditor_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % path, QtCore.QUrl.TolerantMode))
    
    @QtCore.pyqtSlot()
    def on_actionOpenDefaultEditor_triggered(self):
        path = self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
        print path