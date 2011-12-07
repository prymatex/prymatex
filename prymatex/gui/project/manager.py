#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.settings import USER_HOME_PATH
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.project.proxies import PMXProjectTreeProxyModel
from prymatex.gui.project.base import PMXProject

class PMXProjectManager(PMXObject):
    #Signals
    projectClosed = QtCore.pyqtSignal(object)
    projectOpened = QtCore.pyqtSignal(object)
    
    #Settings
    workspaceDirectory  = pmxConfigPorperty(default = os.path.join(USER_HOME_PATH, "workspace"))  #Eclipse muejejeje
    projects = pmxConfigPorperty(default = [])
    workingSets = pmxConfigPorperty(default = {})
    
    SETTINGS_GROUP = 'ProjectManager'
    
    def __init__(self, parent = None):
        PMXObject.__init__(self)
        self.projectTreeModel = PMXProjectTreeModel(self)
        self.projectTreeProxyModel = PMXProjectTreeProxyModel(self)
        self.projectTreeProxyModel.setSourceModel(self.projectTreeModel)
        
        self.configure()

    def loadProjects(self, filePath):
        project = PMXProject("diego", self.workspacePath)
        self.projectTreeModel.appendProject(project)    

    def addProject(self, project):
        self.projectTreeModel.appendProject(project)
        
    def openProject(self):
        pass

    def createProject(self, filePath):
        project = PMXProject("diego", self.workspacePath)
        self.projectTreeModel.appendProject(project)

    def deleteProject(self):
        pass

    def setWorkingSet(self, workingSet, project):
        projects = self.workingSets.setdefault(workingSet)
        projects.append(project.path)
        project.setWorkingSet(workingSet)
        
    def findProjectForFile(self, fileInfo):
        for project in self.projectTreeModel.getAllProjects():
            if os.path.commonprefix([project.directory, fileInfo.absolutePath()]) == project.directory:
                return project
