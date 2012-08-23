#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, string, unicodedata
import fnmatch

from PyQt4 import QtCore, QtGui

from prymatex.core import exceptions
from prymatex.core.settings import USER_HOME_PATH, pmxConfigPorperty
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.project.proxies import PMXProjectTreeProxyModel, ProjectMenuProxyModel
from prymatex.gui.project.base import PMXProject
from prymatex.core.exceptions import ProjectExistsException, FileException
from prymatex.utils.i18n import ugettext as _

class PMXProjectManager(QtCore.QObject):
    #Signals
    projectAdded = QtCore.pyqtSignal(object)
    projectRemoved = QtCore.pyqtSignal(object)
    projectClose = QtCore.pyqtSignal(object)
    projectOpen = QtCore.pyqtSignal(object)
    
    #Settings
    SETTINGS_GROUP = 'ProjectManager'
    
    workspaceDirectory  = pmxConfigPorperty(default = os.path.join(USER_HOME_PATH, "workspace"))  #Eclipse muejejeje
    knownProjects = pmxConfigPorperty(default = [])
    workingSets = pmxConfigPorperty(default = {})
    
    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.fileManager = application.fileManager
        self.projectTreeModel = PMXProjectTreeModel(self)
        
        self.projectTreeProxyModel = PMXProjectTreeProxyModel(self)
        self.projectTreeProxyModel.setSourceModel(self.projectTreeModel)
        
        self.projectMenuProxyModel = ProjectMenuProxyModel(self)
        self.projectMenuProxyModel.setSourceModel(self.application.supportManager.bundleProxyModel)
    
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

    def loadProjects(self):
        for path in self.knownProjects[:]:
            try:
                PMXProject.loadProject(path, self)
            except exceptions.FileNotExistsException as e:
                print e
                self.knownProjects.remove(path)
                self.settings.setValue('knownProjects', self.knownProjects)

    def isOpen(self, project):
        return True

    def appendToKnowProjects(self, project):
        self.knownProjects.append(project.path)
        self.settings.setValue('knownProjects', self.knownProjects)

    def removeFromKnowProjects(self, project):
        self.knownProjects.remove(project.path)
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
        try:
            project.save()
        except ProjectExistsException:
            rslt = QtGui.QMessageBox.information(None, _("Project already created on %s") % name,
                                          _("Directory %s already contains .pmxproject directory structure. "
                                            "Unless you know what you are doing, Cancel and import project,"
                                            " if it still fails, choose overwirte. Overwrite?") % directory,
                                          QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel) 
            if rslt == QtGui.QMessageBox.Cancel:
                return
            try:
                project.save(overwirte = True)
            except FileException as excp:
                QtGui.QMessageBox.critical(None, _("Project creation failed"), 
                                           _("<p>Project %s could not be created<p><pre>%s</pre>") % (name, excp))
        self.addProject(project)
        self.appendToKnowProjects(project)
        return project
    
    def updateProject(self, project, **attrs):
        """Actualiza un proyecto"""
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == item.name:
            #Updates que no son updates
            return item

        project.update(attrs)
        project.save()
        return project

    def importProject(self, directory):
        try:
            project = PMXProject.loadProject(directory, self)
        except exceptions.FileNotExistsException:
            raise exceptions.LocationIsNotProject()
        self.appendToKnowProjects(project)

    def deleteProject(self, project, removeFiles = False):
        """
        Elimina un proyecto
        """
        project.delete(removeFiles)
        self.removeProject(project)

    #---------------------------------------------------
    # PROJECT INTERFACE
    #---------------------------------------------------
    def addProject(self, project):
        project.setManager(self)
        if project.hasBundles() or project.hasThemes():
            self.application.supportManager.addProjectNamespace(project)
        self.projectTreeModel.appendProject(project)
        self.projectAdded.emit(project)

    def modifyProject(self, project):
        pass

    def removeProject(self, project):
        self.removeFromKnowProjects(project)
        self.projectTreeModel.removeProject(project)
    
    def getAllProjects(self):
        #TODO: devolver un copia o no hace falta?
        return self.projectTreeModel.rootNode.childrenNodes
        
    def openProject(self, project):
        # Cuando abro un proyecto agrego su namespace al support para aportar bundles y themes
        print project.directory
    
    def closeProject(self, project):
        # Cuando cierro un proyecto quito su namespace al support
        print project.directory

    def setWorkingSet(self, project, workingSet):
        projects = self.workingSets.setdefault(workingSet)
        projects.append(project.filePath)
        project.setWorkingSet(workingSet)
        self.projectTreeModel.dataChanged.emit()
        
    def addProjectBundleMenu(self, project, bundle):
        project.addBundleMenu(bundle)
        project.save()
        
    def removeProjectBundleMenu(self, project, bundle):
        project.removeBundleMenu(bundle)
        project.save()
        
    def findProjectForPath(self, path):
        for project in self.getAllProjects():
            if self.application.fileManager.issubpath(path, project.path):
                return project
