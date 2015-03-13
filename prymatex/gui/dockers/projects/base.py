#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu

from prymatex.core import PrymatexDock
from prymatex.core.settings import ConfigurableItem, ConfigurableHook

from prymatex.utils.i18n import ugettext as _

from prymatex.models.trees import TreeNodeBase
from prymatex.models.projects.lists import SelectableProjectFileProxyModel

from prymatex.ui.dockers.projects import Ui_ProjectsDock

from .actions import ProjectsDockActionsMixin

class ProjectsDock(PrymatexDock, Ui_ProjectsDock, ProjectsDockActionsMixin, QtWidgets.QDockWidget):
    SEQUENCE = ("Docks", "ProjectsDock", "Alt+X")
    ICON = "dock-projects"
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    # -------------- Settings
    @ConfigurableHook("code_editor.default_theme")
    def default_theme(self, theme_uuid):
        theme = self.application().supportManager.getBundleItem(theme_uuid)
        self.treeViewProjects.setPalette(theme.palette())
        self.treeViewProjects.viewport().setPalette(theme.palette())
    
    def __init__(self, **kwargs):
        super(ProjectsDock, self).__init__(**kwargs)
        self.setupUi(self)
        self.projectManager = self.application().projectManager
        self.fileManager = self.application().fileManager
        self.projectTreeProxyModel = self.projectManager.projectTreeProxyModel
    
        self.setupTreeViewProjects()
        
        # Model for selector dialog
        self.selectableProjectFileModel = SelectableProjectFileProxyModel(self.projectManager, self.fileManager, parent = self)
       
    def initialize(self, **kwargs):
        super(ProjectsDock, self).initialize(**kwargs)
        self.newProjectDialog = self.window().findChild(QtWidgets.QDialog, "NewProjectDialog")
        self.templateDialog = self.window().findChild(QtWidgets.QDialog, "TemplateDialog")
        self.bundleEditorDialog = self.window().findChild(QtWidgets.QDialog, "BundleEditorDialog")
        self.propertiesDialog = self.window().findChild(QtWidgets.QDialog, "PropertiesDialog")
        self.bundleFilterDialog = self.window().findChild(QtWidgets.QDialog, "BundleFilterDialog")
        self.bundleFilterDialog.setWindowTitle("Select Related Bundles")
        self.bundleFilterDialog.setModel(self.projectManager.projectMenuProxyModel)
        self.bundleFilterDialog.setHelpVisible(False)

    @classmethod
    def contributeToSettings(cls):
        return [ ]
    
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        navigation = [
                {'text': 'Go to project file',
                 'triggered': cls.on_actionGoToProjectFile_triggered,
                 'sequence': ("Projects", "GoToProjectFiles", 'Meta+Ctrl+Shift+F'),
                 },
                {'text': 'Go to project symbol',
                 'triggered': cls.on_actionGoToProjectFile_triggered,
                 'sequence': ("Projects", "GoToProjectFiles", 'Meta+Ctrl+Shift+F'),
                 }
            ]
        return { "navigation": navigation}
    
    # ------------------ Menu Actions
    def on_actionGoToProjectFile_triggered(self):
        filePath = self.window().selectorDialog.select(self.selectableProjectFileModel, title=_("Select Project File"))
        if filePath is not None:
            index = self.projectTreeProxyModel.indexForPath(filePath)
            self.treeViewProjects.setCurrentIndex(index)
            self.application().openFile(filePath)

    def addFileSystemNodeFormater(self, formater):
        self.projectTreeProxyModel.addNodeFormater(formater)
    
    def componentState(self):
        expandedIndexes = [index for index in self.projectTreeProxyModel.persistentIndexList() if self.treeViewProjects.isExpanded(index)]
        expandedPaths = [self.projectTreeProxyModel.node(index).path() for index in expandedIndexes]
        return { "expanded": expandedPaths }

    def setComponentState(self, state):
        #Expanded Nodes
        list(map(lambda index: index.isValid() and self.treeViewProjects.setExpanded(index, True), 
            [self.projectTreeProxyModel.indexForPath(path) for path in state["expanded"]]))

    def environmentVariables(self):
        environment = PrymatexDock.environmentVariables(self)
        indexes = self.treeViewProjects.selectedIndexes()
        if indexes:
            node = self.currentNode()
            paths = [self.application().fileManager.normcase(node.path()) for node in [ self.projectTreeProxyModel.node(index) for index in indexes ]]
            environment.update({
                'TM_SELECTED_FILE': node.path(), 
                'TM_SELECTED_FILES': " ".join(["'%s'" % path for path in paths ])
            })
        return environment

    def setupTreeViewProjects(self):
        self.treeViewProjects.setModel(self.projectTreeProxyModel)
        
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setUniformRowHeights(False)
        
        self.setupMenues()

        # Drag and Drop (see the proxy model)
        self.treeViewProjects.setDragEnabled(True)
        self.treeViewProjects.setAcceptDrops(True)
        self.treeViewProjects.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewProjects.setDropIndicatorShown(True)

        self.treeViewProjects.setAlternatingRowColors(True)
        self.treeViewProjects.setAnimated(True)
        
        # Selection Mode
        self.treeViewProjects.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    # ---------- OVERRIDE: QWidget.setWindowTitle
    def setWindowTitle(self, node_or_str):
        if isinstance(node_or_str, TreeNodeBase):
            if node_or_str.isRootNode():
                node_or_str = "Projects"
            else:
                node_or_str = "%s (%s)" % (
                    node_or_str.nodeName(), 
                    node_or_str.project().nodeName()
                )
        super(ProjectsDock, self).setWindowTitle(node_or_str)
        
    def on_treeViewProjects_doubleClicked(self, index):
        node = self.projectTreeProxyModel.node(index)
        if node.isFile():
            self.application().openFile(node.path())

    def currentPath(self):
        return self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())

    def currentNode(self):
        return self.projectTreeProxyModel.node(self.treeViewProjects.currentIndex())
        
    def currentDirectory(self):
        return self.application().fileManager.directory(self.currentPath())

    @QtCore.Slot()
    def on_actionRemove_triggered(self):
        node = self.currentNode()
        if node.isproject:
            ret = QtWidgets.QMessageBox.question(self,
                "Remove project",
                "Are you sure you want to remove project '%s' from the workspace?" % node.name,
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Ok
            )
            if ret == QtWidgets.QMessageBox.Ok:
                self.application().projectManager.removeProject(node)
    
    @QtCore.Slot()
    def on_actionProperties_triggered(self):
        self.propertiesDialog.setModel(self.application().projectManager.propertiesProxyModel)
        self.propertiesDialog.exec_(self.currentNode())

    def on_window_editorChanged(self, editor):
        if editor.hasFile():
            index = self.projectTreeProxyModel.indexForPath(editor.filePath())
            self.treeViewProjects.setCurrentIndex(index)
 
    # ---------- SIGNAL: pushButtonGoUp.pressed
    @QtCore.Slot()
    def on_pushButtonGoUp_pressed(self):
        index = self.projectTreeProxyModel.parent(self.treeViewProjects.rootIndex())
        self.treeViewProjects.setRootIndex(index)
        node = self.projectTreeProxyModel.node(index)
        self.setWindowTitle(node)
