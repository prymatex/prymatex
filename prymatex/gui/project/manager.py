#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, string, unicodedata
import fnmatch

from PyQt4 import QtCore, QtGui

from prymatex.core.settings import USER_HOME_PATH
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.project.proxies import PMXProjectTreeProxyModel
from prymatex.gui.project.base import PMXProject

class PMXProjectManager(QtCore.QObject):
    #Signals
    projectClosed = QtCore.pyqtSignal(object)
    projectOpened = QtCore.pyqtSignal(object)
    
    #Settings
    SETTINGS_GROUP = 'ProjectManager'
    
    workspaceDirectory  = pmxConfigPorperty(default = os.path.join(USER_HOME_PATH, "workspace"))  #Eclipse muejejeje
    knownProjects = pmxConfigPorperty(default = [])
    workingSets = pmxConfigPorperty(default = {})
    
    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.projectTreeModel = PMXProjectTreeModel(self)
        
        self.projectTreeProxyModel = PMXProjectTreeProxyModel(self)
        self.projectTreeProxyModel.setSourceModel(self.projectTreeModel)
    
    @classmethod
    def contributeToSettings(cls):
        return []

    def convertToValidPath(self, name):
        #TODO: este y el del manager de bundles pasarlos a utils
        validPath = []
        for char in unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'):
            char = char if char in self.VALID_PATH_CARACTERS else '-'
            validPath.append(char)
        return ''.join(validPath)

    def loadProject(self):
        for path in self.knownProjects[:]:
            project = PMXProject.loadProject(path, self)

    def isOpen(self, project):
        return True

    def removeFromKnowProjects(self, path):
        self.knownProjects.remove(path)
        self.settings.setValue('knownProjects', self.knownProjects)
        
    #---------------------------------------------------
    # PROJECT CRUD
    #---------------------------------------------------
    def createProject(self, name, directory, reuseDirectory = True):
        """
        Crea un proyecto nuevo lo agrega en los existentes y lo retorna,
        """
        #TODO: dejar este trabajo al file manager
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not reuseDirectory:
            raise Exception()
        project = PMXProject(directory, { "name": name })
        project.save()
        self.addProject(project)
        self.knownProjects.append(project.path)
        self.settings.setValue('knownProjects', self.knownProjects)
        return project

    def deleteProject(self, project, removeFiles = False):
        """
        Elimina un proyecto
        """
        project.delete(removeFiles)
        self.removeProject(project)

    def addProject(self, project):
        project.setManager(self)
        self.projectTreeModel.appendProject(project)

    def removeProject(self, project):
        self.projectTreeModel.removeProject(project)
        
    def openProject(self):
        pass

    def deleteProject(self):
        pass

    def setWorkingSet(self, project, workingSet):
        projects = self.workingSets.setdefault(workingSet)
        projects.append(project.filePath)
        project.setWorkingSet(workingSet)
        #TODO: avisar que se movio el projecto al proxy
        
    def findProjectForPath(self, path):
        return self.projectTreeModel.projectForPath(path)
