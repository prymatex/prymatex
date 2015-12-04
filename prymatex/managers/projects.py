#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import unicodedata
import fnmatch

from prymatex.qt import QtCore, QtGui

from prymatex.core import config
from prymatex.core import PrymatexComponent
from prymatex.core import exceptions
from prymatex.core.settings import ConfigurableItem
from prymatex.models.lists import CheckableListModel
from prymatex.models.projects import (ProjectTreeNode, ProjectTreeModel,
    ProjectTreeProxyModel, ProjectMenuProxyModel)

from prymatex.models.properties import PropertiesProxyModel, PropertiesTreeModel
from prymatex.core.exceptions import ProjectExistsException, FileException

from prymatex.projects import Project
from prymatex.utils.i18n import ugettext as _

class ProjectManager(PrymatexComponent, QtCore.QObject):
    #Signals
    projectAdded = QtCore.Signal(object)
    projectRemoved = QtCore.Signal(object)
    projectClose = QtCore.Signal(object)
    projectOpen = QtCore.Signal(object)

    # ------------- Settings
    default_directory  = ConfigurableItem(
        default=os.path.join(config.USER_HOME_PATH, "Projects")
    )

    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)

    def __init__(self, **kwargs):
        super(ProjectManager, self).__init__(**kwargs)
        self.fileManager = self.application().fileManager
        self.supportManager = self.application().supportManager

        self.projectTreeModel = ProjectTreeModel(self)
        self.keywordsListModel = CheckableListModel(self)
        self.propertiesTreeModel = PropertiesTreeModel(parent=self)

        self.projectTreeProxyModel = ProjectTreeProxyModel(self)
        self.projectTreeProxyModel.setSourceModel(self.projectTreeModel)

        self.projectMenuProxyModel = ProjectMenuProxyModel(self)
        self.projectMenuProxyModel.setSourceModel(self.application().supportManager.bundleProxyModel)

        self.propertiesProxyModel = PropertiesProxyModel(parent = self)
        self.propertiesProxyModel.setSourceModel(self.propertiesTreeModel)

        self.supportManager.bundleAdded.connect(self.on_supportManager_bundleAdded)
        self.supportManager.bundleRemoved.connect(self.on_supportManager_bundleRemoved)
        self.supportManager.bundleItemAdded.connect(self.on_supportManager_bundleItemAdded)
        self.supportManager.bundleItemRemoved.connect(self.on_supportManager_bundleItemRemoved)
        self.message_handler = None
    
    # ---------- OVERRIDE: PrymatexComponent.contributeToSettings()
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.projects import ProjectSettingsWidget
        from prymatex.gui.settings.addons import AddonsSettingsWidgetFactory
        return [ ProjectSettingsWidget, AddonsSettingsWidgetFactory("projects") ]

    # ---------- OVERRIDE: PrymatexComponent.componentState()
    def componentState(self):
        componentState = super(ProjectManager, self).componentState()

        componentState["projects"] = []
        for project in self.projectTreeModel.projects():
            componentState["projects"].append(project.path())

        return componentState

    # ---------- OVERRIDE: PrymatexComponent.setComponentState()
    def setComponentState(self, componentState):
        super(ProjectManager, self).setComponentState(componentState)
        
        # Restore projects
        for project_path in componentState.get("projects", []):
            try:
                self.openProject(project_path)
            except exceptions.FileIsNotProject as ex:
                pass
        
    def setupPropertiesWidgets(self):
        from prymatex.gui.properties.project import ProjectPropertiesWidget
        from prymatex.gui.properties.environment import EnvironmentPropertiesWidget
        from prymatex.gui.properties.resource import ResoucePropertiesWidget
        
        for property_class in [ProjectPropertiesWidget, EnvironmentPropertiesWidget, ResoucePropertiesWidget]:
            property_class.application = self.application
            self.registerPropertyWidget(property_class())

    def convertToValidPath(self, name):
        #TODO: este y el del manager de bundles pasarlos a utils
        validPath = []
        for char in unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore'):
            char = char if char in self.VALID_PATH_CARACTERS else '-'
            validPath.append(char)
        return ''.join(validPath)

    # -------------- Signals from suppor manager
    def on_supportManager_bundleAdded(self, bundle):
        for project in self.getAllProjects():
            if bundle.hasSource(project.namespaceName) and not project.hasBundleMenu(bundle):
                self.addProjectBundleMenu(project, bundle)

    def on_supportManager_bundleRemoved(self, bundle):
        for project in self.getAllProjects():
            if bundle.hasSource(project.namespaceName) and project.hasBundleMenu(bundle):
                self.removeProjectBundleMenu(project, bundle)

    def on_supportManager_bundleItemAdded(self, bundleItem):
        if bundleItem.type() == "syntax":
            self.keywordsListModel.addItems(bundleItem.bundleItem().scopeName.split('.'))


    def on_supportManager_bundleItemRemoved(self, bundleItem):
        if bundleItem.type() == "syntax":
            self.keywordsListModel.removeItems(bundleItem.bundleItem().scopeName.split('.'))

    # -------------------- Load projects
    def loadProjects(self, message_handler=None, *args, **kwargs):
        self.message_handler = message_handler
        self.setupPropertiesWidgets()
        self.message_handler = None

    def isOpen(self, project):
        return True

    # ------------------- Properties
    def registerPropertyWidget(self, propertyWidget):
        self.propertiesTreeModel.addConfigNode(propertyWidget)

    #---------------------------------------------------
    # Environment
    #---------------------------------------------------
    def environmentVariables(self):
        return {}

    #---------------------------------------------------
    # PROJECT CRUD
    #---------------------------------------------------
    def createProject(self, name, file_path, folders=(), overwrite=False):
        """Crea un proyecto nuevo y lo retorna"""
        if not overwrite and os.path.exists(file_path):
            raise exceptions.ProjectExistsException()

        project = ProjectTreeNode(name, file_path)
        project.load({
            "name": name,
            "source_folders": folders 
        })
        project.save()

        self.addProject(project)
        return project

    def updateProject(self, project, **attrs):
        """Actualiza un proyecto"""
        project.update(attrs)
        project.save()
        return project

    def openProject(self, file_path):
        try:
            project = ProjectTreeNode.loadProject(file_path, self)
        except exceptions.FileNotExistsException:
            raise exceptions.FileIsNotProject()

    def deleteProject(self, project, removeFiles = False):
        """Elimina un proyecto"""
        project.delete(removeFiles)
        self.removeProject(project)

    # ---------------- Project sources
    def addSourceFolder(self, project, path):
        project.addSourceFolder(path)
        project.save()
        
    def removeSourceFolder(self, project, path):
        project.removeSourceFolder(path)
        project.save()
        
    # ---------------- Project namespaces
    def addNamespaceFolder(self, project, path):
        namespace = self.application().createNamespace(project.nodeName(), path)
        self.application().addNamespace(namespace)
        project.addNamespace(namespace)
        project.save()
        
    def removeNamespace(self, project, namespace):
        project.removeNamespace(namespace)
        project.save()
        
    #---------------------------------------------------
    # PROJECT INTERFACE
    #---------------------------------------------------
    def addProject(self, project):
        project.setManager(self)
        # Agregar los namespace folders
        for folder in project.namespace_folders:
            self.addNamespaceFolder(project, folder)
        self.projectTreeModel.appendProject(project)
        self.projectAdded.emit(project)

    def modifyProject(self, project):
        pass

    def removeProject(self, project):
        self.projectTreeModel.removeProject(project)

    def getAllProjects(self):
        #TODO: devolver un copia o no hace falta?
        return self.projectTreeModel.rootNode.children()

    def closeProject(self, project):
        # Cuando cierro un proyecto quito su namespace al support
        print(project.path())

    def addProjectBundleMenu(self, project, bundle):
        project.addBundleMenu(bundle)
        project.save()

    def removeProjectBundleMenu(self, project, bundle):
        project.removeBundleMenu(bundle)
        project.save()

    def findProjectForPath(self, path):
        file_manager = self.application().fileManager
        for project in self.getAllProjects():
            if any(file_manager.issubpath(path, source) for source in project.source_folders):
                return project
