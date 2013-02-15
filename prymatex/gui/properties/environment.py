#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.properties import PropertyTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget
from prymatex.models.environment import EnvironmentTableModel

class EnvironmentPropertiesWidget(MultiDictTableEditorWidget, PropertyTreeNode):
    """Environment variables"""
    NAMESPACE = ""
    TITLE = "Enviroment Variables"
    def __init__(self, parent = None):
        MultiDictTableEditorWidget.__init__(self, parent)
        PropertyTreeNode.__init__(self, "environment")
        self.project = None

    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isproject
    
    def edit(self, project):
        self.project = project
        self.clear()
        self.addDictionary('user', self.project.shellVariables, editable = True, selectable=True)
        self.addDictionary('project', self.project.environment())
        self.addDictionary('prymatex', self.application.supportManager.environmentVariables(), visible = False)

    def on_variablesModel_variablesChanged(self, group, variables):
        self.application.projectManager.updateProject(self.project, shellVariables = variables)

    def on_pushAdd_pressed(self):
        self.model.insertVariable()
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)