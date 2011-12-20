#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.dockers.base import PMXBaseDock
from prymatex.ui.dockers.projects import Ui_ProjectsDock

class PMXProjectDock(QtGui.QDockWidget, Ui_ProjectsDock, PMXBaseDock, PMXObject):
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F8")
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.projectModel = self.application.projectManager.projectTreeProxyModel
        self.treeViewProjects.setModel(self.projectModel)

        self.setupTreeViewProjects()

    def setupTreeViewProjects(self):
        #Setup Context Menu
        self.projectsMenu = QtGui.QMenu(self)
        self.projectsMenu.setObjectName('projectsMenu')
        
        self.newMenu = QtGui.QMenu("New", self)
        self.newMenu.setObjectName('newMenu')
        self.newMenu.addAction(self.actionNewProject)
        self.newMenu.addAction(self.actionNewFolder)
        self.newMenu.addAction(self.actionNewFile)
        self.newMenu.addSeparator()
        self.newMenu.addAction(self.actionNewFromTemplate)
        
        self.projectsMenu.addMenu(self.newMenu)
        self.projectsMenu.addAction(self.actionDelete)
        
        self.projectsMenu.addSeparator()
        self.projectsMenu.addAction(self.actionCloseProject)
        self.projectsMenu.addAction(self.actionOpenProject)
        
        #Connect context menu
        self.treeViewProjects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewProjects.customContextMenuRequested.connect(self.showProjectTreeViewContextMenu)
    
        #self.actionNewFile
        #self.actionNewFolder
        #self.actionNewFromTemplate
        #self.actionDelete
        #self.actionNewProject
        #self.actionCloseProject
        #self.actionOpenProject
        #self.actionProperties
        #self.actionRefresh

    def showProjectTreeViewContextMenu(self, point):
        self.projectsMenu.popup(self.treeViewProjects.mapToGlobal(point))
    
    #Actions
    
    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
        
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionCloseProject_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionOpenProject_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionProperties_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path
    
    @QtCore.pyqtSlot()
    def on_actionRefresh_triggered(self):
        index = self.treeViewProjects.currentIndex()
        sIndex = self.projectModel.mapToSource(index)
        sourceModel = self.projectModel.sourceModel()
        path = sourceModel.filePath(sIndex)
        print path