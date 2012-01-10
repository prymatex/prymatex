#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin.dock import PMXBaseDock

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.utils import createQMenu
from prymatex.ui.dockers.projects import Ui_ProjectsDock
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog
from prymatex.gui.dockers.fstasks import PMXFileSystemTasks
from prymatex.gui.project.base import PMXProject

class PMXProjectDock(QtGui.QDockWidget, Ui_ProjectsDock, PMXFileSystemTasks, PMXBaseDock):
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F8")

    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.projectTreeProxyModel = self.application.projectManager.projectTreeProxyModel
        self.treeViewProjects.setModel(self.projectTreeProxyModel)

        self.setupTreeViewProjects()

    def setMainWindow(self, mainWindow):
        PMXBaseDock.setMainWindow(self, mainWindow)
        mainWindow.projects = self
    
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
                self.actionOpenSystemEditor,
                "-",
                self.actionDelete,
                "-",
                self.actionRefresh,
                self.actionCloseProject,
                self.actionOpenProject,
                "-",
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
                "-",
                self.actionRefresh,
                "-",
                self.actionProperties
            ]
        }
        self.fileMenu = createQMenu(fileMenuSettings, self)
        
        directoryMenuSettings = { 
            "title": _("File"),
            "items": [
                {   "title": _("New"),
                    "items": [
                        self.actionNewProject, self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate
                    ]
                },
                "-",
                self.actionOpen,
                self.actionOpenSystemEditor,
                "-",
                self.actionDelete,
                "-",
                self.actionRefresh,
                "-",
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
        index = self.treeViewProjects.indexAt(point)
        if not index.isValid():
            index = self.treeViewProjects.currentIndex()
        if index.isValid():
            node = self.projectTreeProxyModel.node(index)
            if isinstance(node, PMXProject):
                self.projectsMenu.popup(self.treeViewProjects.mapToGlobal(point))
            elif node.isfile:
                self.fileMenu.popup(self.treeViewProjects.mapToGlobal(point))
            elif node.isdir:
                self.directoryMenu.popup(self.treeViewProjects.mapToGlobal(point))
                
    def on_treeViewProjects_doubleClicked(self, index):
        path = self.projectTreeProxyModel.filePath(index)
        if os.path.isfile(path):
            self.application.openFile(path)
    
    def currentPath(self):
        return self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())
    
    #======================================================
    # Tree View Context Menu Actions
    # Some of them are in fstask's PMXFileSystemTasks mixin
    #======================================================
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        path = self.currentPath()
        print(path)
    
    @QtCore.pyqtSlot()
    def on_actionCloseProject_triggered(self):
        path = self.currentPath()
        print(path)
    
    @QtCore.pyqtSlot()
    def on_actionOpenProject_triggered(self):
        print (self.currentPath())
    
    @QtCore.pyqtSlot()
    def on_actionProperties_triggered(self):
        path = self.currentPath()
    
    @QtCore.pyqtSlot()
    def on_actionRefresh_triggered(self):
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        print(self.currentPath())
        
    @QtCore.pyqtSlot()
    def on_actionOpenSystemEditor_triggered(self):
        path = self.currentPath()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % path, QtCore.QUrl.TolerantMode))
    
    @QtCore.pyqtSlot()
    def on_actionOpenDefaultEditor_triggered(self):
        print(self.currentPath())